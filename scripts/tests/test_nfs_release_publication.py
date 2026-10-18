"""Same-payload stage/retry fixtures. All remote effects are explicit doubles."""
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, Mock

from nfs_release_fixture import Fixture, TAG, SHA
from release_support import candidate, identity as i, publication


class PublicationTest(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='nfs-publish-fixture-')
        self.f=Fixture(Path(self.temp.name));self.f.final_payload()
        self.addCleanup(self.temp.cleanup);self.addCleanup(self.f.close)

    def test_annotated_tag_exact_sha_and_retained_identity(self):
        ref={'object':{'type':'tag','sha':'b'*40}}
        tag={'tag':TAG,'object':{'type':'commit','sha':SHA},
             'message':publication.TAG_PREFIX+json.dumps(self.f.binding)}
        with patch.object(publication,'api',side_effect=[ref,tag]):
            self.assertEqual(publication.tag_binding(TAG,SHA),self.f.binding)
        for changed in (tag|{'object':{'type':'commit','sha':'c'*40}},tag|{'message':'unowned'},tag|{'tag':'v9.9.9'}):
            with patch.object(publication,'api',side_effect=[ref,changed]),self.assertRaises(ValueError):
                publication.tag_binding(TAG,SHA)
        with patch.object(publication,'api',return_value={'object':{'type':'commit','sha':SHA}}),self.assertRaises(ValueError):
            publication.tag_binding(TAG,SHA)

    def test_fresh_main_no_stale_write_permission(self):
        with patch.object(publication,'api',return_value={'object':{'type':'commit','sha':'0'*40}}),self.assertRaisesRegex(ValueError,'advanced'):
            publication.fresh_main(SHA)

    def test_resume_downloads_original_payload_before_build_and_refuses_lost_input(self):
        env={'GITHUB_REPOSITORY':i.REPOSITORY,'GITHUB_REF':'refs/heads/main','GITHUB_SHA':SHA}
        work=Path(self.temp.name)/'work'
        def fetch(record,dest):shutil.copytree(self.f.c,dest);return self.f.record
        def download(e,name,dest,successful=True):
            self.assertEqual(e,self.f.binding['envelope']);self.assertEqual(name,candidate.PAYLOAD)
            self.assertFalse(successful);shutil.copytree(self.f.p,dest)
        with patch.dict(os.environ,env),patch.object(candidate,'fetch',side_effect=fetch),\
             patch.object(candidate,'download',side_effect=download) as downloaded,\
             patch.object(publication,'tag_binding',return_value=self.f.binding),\
             patch.object(publication,'release',return_value=None),patch.object(publication,'package_version',return_value=None),\
             patch.object(candidate,'api',return_value={'total_count':1,'jobs':[{'name':'payload','conclusion':'success'}]}):
            self.assertEqual(publication.prepare(TAG,SHA,42,work),'resume')
            downloaded.assert_called_once()
            self.assertEqual((work/'payload/publication.json').read_bytes(),(self.f.p/'publication.json').read_bytes())
        with patch.dict(os.environ,env),patch.object(candidate,'fetch',side_effect=fetch),\
             patch.object(candidate,'download',side_effect=ValueError('expired')),\
             patch.object(publication,'tag_binding',return_value=self.f.binding),\
             patch.object(publication,'release',return_value=None),self.assertRaisesRegex(ValueError,'expired'):
            publication.prepare(TAG,SHA,42,Path(self.temp.name)/'lost')

    def test_native_asset_conflicts_never_upload_or_clobber(self):
        assets=i.inventory(self.f.p/'assets');name=next(iter(assets))
        existing={'tag_name':TAG,'assets':[{'name':name,'size':assets[name]['size'],'id':10}]}
        def download(*args,**kwargs):kwargs['stdout'].write(b'wrong')
        with patch.object(subprocess,'run',side_effect=download),patch.object(i,'command') as commands,self.assertRaisesRegex(ValueError,'bytes conflict'):
            publication.verify_assets(existing,self.f.p,True)
        commands.assert_not_called()
        with self.assertRaisesRegex(ValueError,'incomplete'):publication.verify_assets({'tag_name':TAG,'assets':[]},self.f.p,False)

    def test_draft_identity_and_nonclobber_creation(self):
        existing={'tag_name':TAG,'prerelease':False,'body':publication.body_for(self.f.p,self.f.binding),'assets':[]}
        with patch.object(publication,'release',return_value=existing),patch.object(i,'command') as commands:
            self.assertEqual(publication.reconcile_release(None,self.f.p,self.f.binding),existing)
            args=commands.call_args.args
            self.assertIn('--verify-tag',args);self.assertIn('--draft',args);self.assertIn('--prerelease=false',args)
            self.assertNotIn('--clobber',args)
        with self.assertRaises(ValueError):publication.reconcile_release(existing|{'body':'unrelated'},self.f.p,self.f.binding)

    def test_exact_oci_copy_and_anonymous_all_children(self):
        version={'name':self.f.image['index'],'id':90}
        calls=[]
        def command(*args,**kwargs):
            if args[:2]==('git','show'):return (i.ROOT/i.WORKFLOW).read_bytes()
            calls.append(args)
            if str(args[-1]).startswith('oci-archive:'):
                shutil.copyfile(self.f.c/'engine.oci.tar',str(args[-1]).split(':',1)[1])
            return b''
        with patch.object(publication,'package_version',side_effect=[None,version]),patch.object(i,'command',side_effect=command):
            result=publication.promote(self.f.c,TAG,True)
        self.assertEqual(len(calls),2)
        for args in calls:self.assertIn('--all',args);self.assertIn('--preserve-digests',args)
        self.assertIn('--src-authfile',calls[1]);self.assertEqual(result['anonymousPlatforms'],['linux-amd64','linux-arm64'])
        with patch.object(publication,'package_version',return_value={'name':'sha256:'+'0'*64}),patch.object(i,'command',side_effect=lambda *args,**kwargs:(i.ROOT/i.WORKFLOW).read_bytes()) as commands,self.assertRaisesRegex(ValueError,'conflict'):
            publication.promote(self.f.c,TAG,True)
        self.assertTrue(all(c.args[:2]==('git','show') for c in commands.call_args_list))

    def test_publisher_stage_order_failed_promotion_and_same_payload_retry(self):
        events=[];state={'tag':None,'release':None};journal=Path(self.temp.name)/'journal.json'
        def envelope(artifact,run,attempt,commit,name,successful=True):
            return self.f.envelope if name==candidate.CANDIDATE else self.f.binding['envelope']
        def download(e,name,dest,successful=True):shutil.copytree(self.f.p,dest)
        def tag(*args):return state['tag']
        def api(path,method='GET',body=None,missing=False):
            if path.endswith('/git/tags'):events.append('tag-object');return {'sha':'b'*40}
            if path.endswith('/git/refs'):events.append('tag-ref');state['tag']=self.f.binding
            if '/releases/' in path and method=='PATCH':events.append('publish');state['release']['draft']=False
        def reconcile(existing,*args):
            events.append('draft')
            state['release']={'id':30,'tag_name':TAG,'draft':True,'prerelease':False,'body':publication.body_for(self.f.p,self.f.binding),
                              'html_url':'https://github.com/AutoByteus/autobyteus-nfs/releases/tag/'+TAG,'assets':[]}
            return state['release']
        def curl(*args,**kwargs):
            if args[:2]==('git','show'):return (i.ROOT/i.WORKFLOW).read_bytes()
            if args[0]=='curl':
                dest=Path(args[-1]);shutil.copyfile(self.f.p/'assets'/dest.name,dest)
            return b''
        with patch.object(candidate,'envelope',side_effect=envelope),patch.object(candidate,'download',side_effect=download),\
             patch.object(publication,'tag_binding',side_effect=tag),patch.object(publication,'release',side_effect=lambda _:state['release']),\
             patch.object(publication,'api',side_effect=api),patch.object(publication,'package_version',return_value=None),\
             patch.object(publication,'fresh_main',side_effect=lambda _:events.append('fresh-main')),\
             patch.object(publication,'reconcile_release',side_effect=reconcile),\
             patch.object(publication,'verify_assets',side_effect=lambda *args:events.append('assets')),\
             patch.object(publication,'promote',side_effect=ValueError('package private')):
            with self.assertRaisesRegex(ValueError,'private'):publication.publish(self.f.p,self.f.c,self.f.binding,journal)
        self.assertEqual(events,['fresh-main','tag-object','tag-ref','draft','assets'])
        self.assertEqual(state['tag'],self.f.binding);self.assertTrue(state['release']['draft'])
        self.assertIn('image-promotion',json.loads(journal.read_text())['stages'][-1])
        events.clear()
        with patch.object(candidate,'envelope',side_effect=envelope),patch.object(candidate,'download',side_effect=download),\
             patch.object(publication,'tag_binding',side_effect=tag),patch.object(publication,'release',side_effect=lambda _:state['release']),\
             patch.object(publication,'api',side_effect=api),patch.object(publication,'package_version',return_value=None),\
             patch.object(publication,'fresh_main',side_effect=lambda _:events.append('fresh-main')),\
             patch.object(publication,'reconcile_release',side_effect=lambda existing,*_:existing),\
             patch.object(publication,'verify_assets',side_effect=lambda *args:events.append('assets')),\
             patch.object(publication,'promote',side_effect=lambda *args:events.append('image-public') or {}),\
             patch.object(i,'command',side_effect=curl),patch.object(subprocess,'run',return_value=Mock(stdout=TAG)):
            result=publication.publish(self.f.p,self.f.c,self.f.binding,journal)
        self.assertEqual(events,['fresh-main','assets','image-public','publish','assets'])
        self.assertEqual(result['payload'],self.f.binding)
        self.assertFalse(state['release']['draft'])

if __name__=='__main__':unittest.main()
