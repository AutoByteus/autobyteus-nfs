"""Endpoint-faithful GitHub doubles; no credentials, registry or remote effects."""
import copy
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from contextlib import ExitStack
from pathlib import Path
from unittest.mock import patch, Mock

from nfs_release_fixture import Fixture, TAG
from release_support import candidate, identity as i, publication as p, source_context as sc


class Remote:
    def __init__(self, fixture, tagged=True, draft=True):
        self.f = fixture
        self.tag = {'object': 'b'*40, 'binding': fixture.binding} if tagged else None
        self.releases = [self.record(417014769, draft)] if tagged else []
        self.assets = {}
        self.calls = []
        self.main = fixture.source
        self.image = None
        self.after_upload = None

    def record(self, ident, draft=True):
        return {'id': ident, 'url': f'https://api.github.com/{p.RELEASES}/{ident}',
                'tag_name': TAG, 'draft': draft, 'prerelease': False,
                'body': p.body_for(self.f.p, self.f.binding),
                'upload_url': f'https://uploads.github.com/{p.RELEASES}/{ident}/assets{{?name,label}}',
                'html_url': f'https://github.com/{i.REPOSITORY}/releases/tag/{TAG}', 'assets': []}

    def api(self, endpoint, method='GET', body=None, missing=False):
        self.calls.append((endpoint, method, body))
        if endpoint.endswith('/git/ref/heads/main'):
            return {'object': {'type': 'commit', 'sha': self.main}}
        if endpoint.endswith('/git/ref/tags/'+TAG):
            return {'object': {'type': 'tag', 'sha': self.tag['object']}} if self.tag else None
        if '/git/tags/' in endpoint:
            return {'sha': self.tag['object'], 'tag': TAG, 'object': {'type': 'commit', 'sha': self.f.source},
                    'message': p.TAG_PREFIX + json.dumps(self.tag['binding'])}
        if endpoint.endswith('/git/tags') and method=='POST':
            self.new_tag = {'object':'b'*40,'binding':i.decode(body['message'][len(p.TAG_PREFIX):])}
            return {'sha':'b'*40}
        if endpoint.endswith('/git/refs') and method=='POST':
            self.tag=self.new_tag; return {}
        if endpoint.startswith(p.RELEASES+'?'):
            page=int(endpoint.rsplit('=',1)[1]);return copy.deepcopy(self.releases[(page-1)*100:page*100])
        if endpoint==p.RELEASES and method=='POST':
            record=self.record(417014769);self.releases.append(record);return copy.deepcopy(record)
        if '/releases/tags/' in endpoint:
            return next((copy.deepcopy(x) for x in self.releases if not x['draft']),None)
        if endpoint.startswith(p.RELEASES+'/'):
            rest=endpoint[len(p.RELEASES)+1:]
            if '/assets?' in rest:
                return [v|{'id':ident,'state':'uploaded'} for ident,v in self.assets.items()]
            record=next(x for x in self.releases if x['id']==int(rest))
            if method=='PATCH':record['draft']=body['draft']
            return copy.deepcopy(record)
        raise AssertionError((endpoint,method,body))

    def jobs(self, endpoint):
        jobs=[{'id':1000,'name':'payload'}]
        for index,(runner,os_name,arch) in enumerate((('macos-15','darwin','arm64'),('macos-15-intel','darwin','amd64'),
                       ('ubuntu-24.04','linux','amd64'),('ubuntu-24.04-arm','linux','arm64'))):
            jobs.append({'id':1001+index,'name':f'binaries ({runner}, {os_name}, {arch})',
                'steps':[{'name':'Developer ID and Accepted notarization before public effects',
                          'status':'completed','conclusion':'success'}] if os_name=='darwin' else []})
        return {'total_count':len(jobs),'jobs':[j|{'run_id':99,'run_attempt':1,'head_sha':self.f.source,
                'status':'completed','conclusion':'success'} for j in jobs]}

    def download(self, envelope, name, dest, successful=True):
        if name==candidate.CANDIDATE:
            assert envelope==self.f.envelope and successful
            shutil.copytree(self.f.c,dest)
        else:
            assert envelope==self.f.binding['envelope'] and not successful
            shutil.copytree(self.f.p,dest)

    def upload(self, existing, path):
        assert existing['id']==417014769 and path.name not in {x['name'] for x in self.assets.values()}
        self.assets[len(self.assets)+1]={'name':path.name,'size':path.stat().st_size}
        if self.after_upload:self.after_upload()

    def command(self,*args,**kwargs):
        if args[:2]==('gh','api'):
            ident=int(args[4].rsplit('/',1)[1]);kwargs['stdout'].write((self.f.p/'assets'/self.assets[ident]['name']).read_bytes())
            return Mock(returncode=0)
        return subprocess.CompletedProcess(args,0)

    def install(self, stack):
        stack.enter_context(patch.object(p,'api',side_effect=self.api))
        stack.enter_context(patch.object(candidate,'api',side_effect=self.jobs))
        stack.enter_context(patch.object(candidate,'download',side_effect=self.download))
        stack.enter_context(patch.object(p,'package_version',side_effect=lambda _:self.image))
        stack.enter_context(patch.object(p,'upload',side_effect=self.upload))
        # Mock only gh asset transport, allowing real Git subprocesses to run.
        real_run=subprocess.run
        stack.enter_context(patch.object(subprocess,'run',side_effect=lambda args,**kw:
            self.command(*args,**kw) if args[:2]==['gh','api'] else real_run(args,**kw)))
        stack.enter_context(patch.object(p,'promote',return_value={'digest':self.f.image['index']}))
        stack.enter_context(patch.object(p,'public_downloads'))
        stack.enter_context(patch.dict(os.environ,{'GITHUB_REPOSITORY':i.REPOSITORY,'GITHUB_REF':'refs/heads/main',
            'GITHUB_EVENT_NAME':'workflow_dispatch','GITHUB_SHA':self.main,'GITHUB_RUN_ID':'200','GITHUB_RUN_ATTEMPT':'1'}))


class PublicationTest(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='nfs-publish-fixture-')
        self.f=Fixture(Path(self.temp.name));self.f.final_payload()
        self.addCleanup(self.temp.cleanup);self.addCleanup(self.f.close)
        self.remote=Remote(self.f)

    def test_published_only_404_does_not_hide_draft(self):
        r=self.remote
        with patch.object(p,'api',side_effect=r.api):
            self.assertIsNone(p.api(p.RELEASES+'/tags/'+TAG,missing=True))
            result=p.discover(self.f.p,self.f.binding,417014769)
        self.assertEqual(result['id'],417014769)
        self.assertTrue(result['draft'])
        self.assertEqual([c[1] for c in r.calls],['GET']*3)
        self.assertIn(p.RELEASES+'/417014769',[x[0] for x in r.calls])

    def test_api_404_only_explicit_read_missing_is_absence(self):
        error=subprocess.CalledProcessError(1,['gh'],stderr=b'Not Found (HTTP 404)')
        with patch.object(i,'command',side_effect=error):
            self.assertIsNone(p.api(p.RELEASES+'/tags/'+TAG,missing=True))
            for method in ('POST','GET'):
                with self.assertRaises(subprocess.CalledProcessError):p.api(p.RELEASES,method)

    def test_unique_paginated_inventory_known_missing_and_direct_correlation(self):
        r=self.remote;owned=r.releases[0]
        r.releases=[r.record(n)|{'tag_name':'v9.0.0'} for n in range(1,101)]+[owned]
        with patch.object(p,'api',side_effect=r.api):
            self.assertEqual(p.discover(self.f.p,self.f.binding,417014769),owned)
        for entries in ([],[owned,owned|{'id':99}],[owned,owned]):
            r.releases=entries
            with patch.object(p,'api',side_effect=r.api),self.assertRaises(ValueError):
                p.reconcile_release(self.f.p,self.f.binding,417014769,lambda:None)
        for changed in (owned|{'body':'wrong'},owned|{'prerelease':True},owned|{'id':1},owned|{'url':'https://evil.invalid/'}):
            r.releases=[owned]
            def api(path,*a,**kw):return changed if path==p.RELEASES+'/417014769' else r.api(path,*a,**kw)
            with patch.object(p,'api',side_effect=api),self.assertRaises(ValueError):p.discover(self.f.p,self.f.binding)
        with patch.object(p,'api',return_value={}),self.assertRaises(ValueError):p.inventory(p.RELEASES)
        with patch.object(p,'api',side_effect=lambda url:[{'id':int(url.rsplit('=',1)[1])*100+x+1} for x in range(100)]),self.assertRaisesRegex(ValueError,'bounded'):
            p.inventory(p.RELEASES)

    def test_draft_create_response_and_ambiguous_effects_never_retry(self):
        r=self.remote;r.releases=[];guard=Mock()
        with patch.object(p,'api',side_effect=r.api):result=p.reconcile_release(self.f.p,self.f.binding,None,guard)
        self.assertEqual(result['id'],417014769);guard.assert_called_once()
        posts=[c for c in r.calls if c[1]=='POST'];self.assertEqual(len(posts),1)
        self.assertEqual(posts[0][2],{'tag_name':TAG,'draft':True,'prerelease':False,'name':'AutoByteus NFS '+TAG,
                                     'body':p.body_for(self.f.p,self.f.binding)})
        for response in (None,{}, {'id':True}):
            r.releases=[];r.calls=[]
            def api(url,method='GET',body=None,missing=False):
                value=r.api(url,method,body,missing);return response if method=='POST' else value
            with patch.object(p,'api',side_effect=api),self.assertRaises((ValueError,TypeError,KeyError)):
                p.reconcile_release(self.f.p,self.f.binding,None,guard)
            self.assertEqual(sum(c[1]=='POST' for c in r.calls),1)

    def test_post_create_direct_404_and_upload_ambiguity_stop_without_more_effects(self):
        r=self.remote;r.releases=[]
        def api(url,method='GET',body=None,missing=False):
            if url==p.RELEASES+'/417014769':
                raise subprocess.CalledProcessError(1,['gh'],stderr=b'(HTTP 404)')
            return r.api(url,method,body,missing)
        with patch.object(p,'api',side_effect=api),self.assertRaises(subprocess.CalledProcessError):
            p.reconcile_release(self.f.p,self.f.binding,None,Mock())
        self.assertEqual(sum(method=='POST' for _,method,_ in r.calls),1)
        r=Remote(self.f)
        journal=Path(self.temp.name)/'ambiguous.json'
        with ExitStack() as stack:
            r.install(stack)
            stack.enter_context(patch.object(p,'upload',side_effect=ValueError('ambiguous upload')))
            with self.assertRaisesRegex(ValueError,'ambiguous upload'):p.publish(self.f.p,self.f.c,self.f.binding,journal)
        self.assertFalse(any(method=='PATCH' for _,method,_ in r.calls))
        self.assertEqual(i.read_json(journal)['stages'][-1],'draft-confirmed; asset-reconciliation-attempted')

    def test_assets_use_id_list_state_and_content_never_embedded_array(self):
        owned=self.remote.releases[0];name=next(iter(i.inventory(self.f.p/'assets')))
        for assets in ([{'id':1,'name':name,'state':'starter','size':1}],
                       [{'id':1,'name':'unexpected','state':'uploaded','size':1}],
                       [{'id':1,'name':name,'state':'uploaded','size':1}]):
            with patch.object(p,'api',return_value=assets),patch.object(p,'upload') as upload,self.assertRaises(ValueError):
                p.verify_assets(owned,self.f.p,True,Mock())
            upload.assert_not_called()
        with patch.object(p,'api',return_value=[]),self.assertRaisesRegex(ValueError,'incomplete'):
            p.verify_assets(owned,self.f.p,False,Mock())
        with ExitStack() as stack:
            self.remote.install(stack)
            p.verify_assets(owned,self.f.p,True,Mock())
        self.assertEqual({x['name'] for x in self.remote.assets.values()},set(i.inventory(self.f.p/'assets')))
        self.assertTrue(all('/417014769/assets?' in url for url,_,_ in self.remote.calls))

    def test_raw_upload_validates_exact_origin_id_encodes_name_and_never_redirects(self):
        path=Path(self.temp.name)/'asset+name.tar.gz';path.write_bytes(b'synthetic')
        existing=self.remote.releases[0]
        conn=Mock();response=Mock(status=201);response.read.return_value=json.dumps({'id':7,'name':path.name,'state':'uploaded','size':9}).encode();conn.getresponse.return_value=response
        with patch.dict(os.environ,{'GH_TOKEN':'fixture-token'}),patch.object(p.http.client,'HTTPSConnection',return_value=conn) as factory:
            p.upload(existing,path)
        factory.assert_called_once_with('uploads.github.com',timeout=600)
        self.assertEqual(conn.request.call_args.args[:2],('POST',f'/{p.RELEASES}/417014769/assets?name=asset%2Bname.tar.gz'))
        self.assertNotIsInstance(conn.request.call_args.kwargs['body'],bytes)
        conn.close.assert_called_once()
        for url in ('https://evil.invalid/x',existing['upload_url'].replace('/417014769/','/9/'),existing['upload_url']+'&x=1'):
            with patch.object(p.http.client,'HTTPSConnection') as factory,self.assertRaises(ValueError):p.upload(existing|{'upload_url':url},path)
            factory.assert_not_called()
        for status in (302,422,502):
            response.status=status;conn.reset_mock()
            with patch.dict(os.environ,{'GH_TOKEN':'fixture-token'}),patch.object(p.http.client,'HTTPSConnection',return_value=conn),self.assertRaisesRegex(ValueError,'ambiguous'):
                p.upload(existing,path)
            self.assertEqual(conn.request.call_count,1);conn.close.assert_called_once()

    def test_fresh_resume_completed_and_stage_drift(self):
        for tagged in (False,True):
            self.remote=Remote(self.f,tagged=tagged)
            with ExitStack() as stack:
                self.remote.install(stack)
                result=p.publish(self.f.p,self.f.c,self.f.binding)
            self.assertEqual(result['result'],'published');self.assertEqual(result['payload'],self.f.binding)
            self.assertEqual(sum(c[1]=='POST' and c[0]==p.RELEASES for c in self.remote.calls),0 if tagged else 1)
            self.remote.calls=[]
            with ExitStack() as stack:
                self.remote.install(stack)
                p.publish(self.f.p,self.f.c,self.f.binding)
            self.assertTrue(all(c[1]=='GET' for c in self.remote.calls))
        for kind in ('main','tag','body','state'):
            self.remote=Remote(self.f)
            def drift():
                if kind=='main':self.remote.main='0'*40
                if kind=='tag':self.remote.tag=self.remote.tag|{'object':'c'*40}
                if kind=='body':self.remote.releases[0]['body']='foreign'
                if kind=='state':self.remote.releases[0]['draft']=False
            self.remote.after_upload=drift
            with ExitStack() as stack:
                self.remote.install(stack)
                with self.assertRaises(ValueError):p.publish(self.f.p,self.f.c,self.f.binding)
            self.assertEqual(len(self.remote.assets),1)
            self.assertFalse(any(c[1]=='PATCH' for c in self.remote.calls))

    def test_resume_prepare_inspect_and_lost_payload(self):
        with ExitStack() as stack:
            self.remote.install(stack)
            report=p.prepare(TAG,self.f.source,42,Path(self.temp.name)/'prepare')
            self.assertEqual(report['mode'],'resume');self.assertIn('non-authoritative',report['draftInventory'])
            report=p.inspect_bound(TAG,Path(self.temp.name)/'inspect')
            self.assertEqual(report['executorPublicationAdmission'],'not performed')
            with patch.object(candidate,'download',side_effect=ValueError('expired')),self.assertRaisesRegex(ValueError,'expired'):
                p.prepare(TAG,self.f.source,42,Path(self.temp.name)/'lost')
        self.assertTrue(all(c[1]=='GET' for c in self.remote.calls))

    def test_payload_jobs_duplicate_failure_wrong_attempt_and_signing(self):
        original=self.remote.jobs('')
        variants=[]
        for key,value in [('status','in_progress'),('conclusion','cancelled'),('run_attempt',2),('head_sha','0'*40)]:
            changed=copy.deepcopy(original);changed['jobs'][0][key]=value;variants.append(changed)
        changed=copy.deepcopy(original);changed['jobs'].append(changed['jobs'][0]|{'id':9});changed['total_count']+=1;variants.append(changed)
        changed=copy.deepcopy(original);changed['jobs'][1]['steps'][0]['conclusion']='failure';variants.append(changed)
        variants.append({'total_count':0,'jobs':[]})
        for data in variants:
            with patch.object(candidate,'api',return_value=data),self.assertRaises(ValueError):p.payload_jobs(self.f.binding,1000)
        with patch.object(candidate,'api',return_value=original):
            self.assertEqual(p.payload_jobs(self.f.binding,1000),1000)
            with self.assertRaisesRegex(ValueError,'ID differs'):p.payload_jobs(self.f.binding,99)

    def test_exact_oci_copy_and_anonymous_all_children(self):
        version={'name':self.f.image['index'],'id':90};calls=[]
        def command(*args,**kwargs):
            calls.append(args)
            if str(args[-1]).startswith('oci-archive:'):shutil.copyfile(self.f.c/'engine.oci.tar',str(args[-1]).split(':',1)[1])
            return b''
        with patch.object(p,'package_version',side_effect=[None,version]),patch.object(i,'command',side_effect=command):
            result=p.promote(self.f.c,TAG,True,sc.current(),Mock())
        self.assertEqual(len(calls),2)
        for args in calls:self.assertIn('--all',args);self.assertIn('--preserve-digests',args)
        self.assertIn('--src-authfile',calls[1]);self.assertEqual(result['anonymousPlatforms'],['linux-amd64','linux-arm64'])
        with patch.object(p,'package_version',return_value={'name':'sha256:'+'0'*64}),patch.object(i,'command') as commands,self.assertRaisesRegex(ValueError,'conflict'):
            p.promote(self.f.c,TAG,True,sc.current(),Mock())
        commands.assert_not_called()

if __name__=='__main__':unittest.main()
