"""Real isolated P/H/E Git histories and endpoint doubles, never release authority."""
import copy
import os
import subprocess
import tempfile
import unittest
from contextlib import ExitStack
from pathlib import Path
from unittest.mock import patch

from nfs_release_fixture import Fixture, TAG
from test_nfs_release_publication import Remote
from release_support import candidate, identity as i, payload, publication as p, recovery, source_context as sc


class RecoveryTest(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='nfs-recovery-fixture-')
        self.f=Fixture(Path(self.temp.name));self.f.final_payload()
        self.addCleanup(self.temp.cleanup);self.addCleanup(self.f.close)
        self.remote=Remote(self.f)
        repair=self.f.repo/'packaging/release_support/publication.py'
        repair.write_text(repair.read_text()+'\n# synthetic reviewed executor repair\n')
        self.h=self.f.commit_all()
        self.auth_path=self.f.repo/'packaging/recovery'/TAG/'authorization.json'
        evidence={}
        for name in ('architectureReview','sourceReview','validation','retainedSigning','deliveryAuthorization'):
            path=self.auth_path.parent/(name+'.md');path.parent.mkdir(parents=True,exist_ok=True)
            path.write_text('SYNTHETIC FIXTURE ONLY; NOT RELEASE AUTHORITY: '+name+'\n')
            evidence[name]={'path':path.relative_to(self.f.repo).as_posix(),'sha256':i.sha(path)}
        self.auth={'schema':1,'kind':'same-payload-executor-repair','repository':i.REPOSITORY,'version':TAG,
                   'payloadSourceCommit':self.f.source,'tagObject':self.remote.tag['object'],'binding':self.f.binding,
                   'payloadJobId':1000,'expectedReleaseId':417014769,
                   'executor':{'reviewedCommit':self.h,'sourceHash':i.source_hash()},'evidence':evidence}
        self.save_authority()

    def save_authority(self):
        i.write_json(self.auth_path,self.auth)
        self.e=self.f.commit_all();self.remote.main=self.e

    def admit(self):
        with sc.frozen(sc.current(),self.f.source) as source:
            return recovery.admit(sc.current(),source,self.remote.tag)

    def test_distinct_git_context_full_chain_and_fresh_refusal(self):
        self.assertEqual(len({self.f.c_commit,self.f.source,self.h,self.e}),4)
        with sc.frozen(sc.current(),self.f.source) as source:
            frozen_root=source.root
            self.assertEqual(candidate.verify(self.f.c,source),self.f.record)
            self.assertEqual(payload.verify(self.f.p,self.f.c,source)['sourceCommit'],self.f.source)
            record,ref=recovery.admit(sc.current(),source,self.remote.tag)
            self.assertEqual(record,self.auth);self.assertEqual(ref['sha256'],i.sha(self.auth_path))
            self.assertNotEqual(source.source_hash(),sc.current().source_hash())
        self.assertFalse(frozen_root.exists())
        with self.assertRaisesRegex(ValueError,'source/engine differs'):candidate.verify(self.f.c)
        with self.assertRaises(ValueError):payload.verify(self.f.p,self.f.c)

    def test_corrected_full_path_reuses_original_bytes_and_known_id(self):
        before=i.inventory(self.f.p)
        with ExitStack() as stack:
            self.remote.install(stack)
            report=p.prepare(TAG,self.e,42,Path(self.temp.name)/'prepare')
            self.assertEqual(report['mode'],'recover');self.assertEqual(report['payloadSourceCommit'],self.f.source)
            result=p.publish(self.f.p,self.f.c,self.f.binding,Path(self.temp.name)/'receipt.json')
        self.assertEqual(result['result'],'published');self.assertEqual(result['reviewedCommit'],self.h)
        self.assertEqual(result['executor']['commit'],self.e);self.assertEqual(result['payloadSourceCommit'],self.f.source)
        self.assertEqual(result['releaseId'],417014769);self.assertEqual(i.inventory(self.f.p),before)
        self.assertFalse(any(method=='POST' for _,method,_ in self.remote.calls))
        self.assertTrue(any(method=='PATCH' for _,method,_ in self.remote.calls))

    def test_missing_authorization_blocks_effects_but_inspection_is_read_only(self):
        self.auth_path.unlink();self.f.git('add','--',str(self.auth_path));self.e=self.f.commit_all();self.remote.main=self.e
        with ExitStack() as stack:
            self.remote.install(stack)
            with self.assertRaisesRegex(ValueError,'authorization required'):p.publish(self.f.p,self.f.c,self.f.binding)
            report=p.inspect_bound(TAG,Path(self.temp.name)/'inspection')
        self.assertEqual(report['executorPublicationAdmission'],'not performed')
        self.assertEqual(report['verifiedPayloadJobId'],1000)
        self.assertIsNone(report['authorization']);self.assertTrue(all(method=='GET' for _,method,_ in self.remote.calls))

    def test_exact_authority_schema_binding_and_evidence(self):
        original=copy.deepcopy(self.auth)
        mutations=[lambda a:a.__setitem__('schema',True),lambda a:a.__setitem__('skipChecks',True),
                   lambda a:a.__setitem__('version','v0.2.0'),lambda a:a.__setitem__('kind','qualified'),
                   lambda a:a.__setitem__('payloadSourceCommit',self.h),lambda a:a.__setitem__('tagObject','0'*40),
                   lambda a:a['binding'].__setitem__('payloadSha256','0'*64),lambda a:a.__setitem__('payloadJobId',False),
                   lambda a:a.__setitem__('expectedReleaseId',0),lambda a:a['executor'].__setitem__('sourceHash','0'*64),
                   lambda a:a['executor'].__setitem__('reviewedCommit',self.f.c_commit),
                   lambda a:a['evidence'].pop('sourceReview'),
                   lambda a:a['evidence']['sourceReview'].__setitem__('path','tickets/done/nfs-first-release/x'),
                   lambda a:a['evidence']['sourceReview'].__setitem__('sha256','0'*64)]
        for index,mutate in enumerate(mutations):
            with self.subTest(index=index):
                self.auth=copy.deepcopy(original);mutate(self.auth);self.save_authority()
                with self.assertRaises((ValueError,subprocess.CalledProcessError)):self.admit()
        self.auth=original;self.save_authority();self.admit()
        evidence=self.f.repo/self.auth['evidence']['sourceReview']['path'];evidence.write_text('changed')
        with self.assertRaises(ValueError):self.admit()

    def test_full_tree_scope_and_original_lock_readiness_immutable(self):
        for name in ('internal/cli/release.go','packaging/sign-macos.sh','packaging/engine/source.py',
                     'cmd/autobyteus-nfs/release.json','internal/backend/engine-assets/generated.deb',
                     'packaging/release-lock.json','packaging/releases/v0.1.0/notes',
                     'packaging/release_support/unapproved.py','another-workflow.yml'):
            with self.subTest(path=name):
                path=self.f.repo/name;exists=path.exists();old=path.read_bytes() if exists else None
                path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes((old or b'')+b'\nmutation\n')
                new=self.f.commit_all()
                for repair in (True,False):
                    with self.assertRaisesRegex(ValueError,'Unreviewed recovery change'):
                        recovery.scope(self.f.repo,self.f.source,new,TAG,repair)
                if exists:path.write_bytes(old)
                else:path.unlink();self.f.git('add','--',name)
                self.f.commit_all()
        path=self.f.repo/'packaging/release_support/publication.py';path.write_text(path.read_text()+'\n# drift after review\n')
        self.f.commit_all()
        with self.assertRaisesRegex(ValueError,'Unreviewed recovery change'):self.admit()

    def test_scope_allows_only_named_repair_and_later_docs(self):
        self.assertIn('packaging/release_support/publication.py',recovery.scope(self.f.repo,self.f.source,self.h,TAG,True))
        (self.f.repo/'RELEASE.md').write_text('synthetic docs only\n');self.e=self.f.commit_all()
        self.admit()
        self.assertNotIn('packaging/engine/source.py',recovery.REPAIR_PATHS)
        self.assertEqual(len(recovery.REPAIR_PATHS),9)

    def test_source_projection_bounds_links_missing_tamper_and_cleanup(self):
        with self.assertRaises(ValueError):
            with patch.object(sc,'MAX_FILES',1),sc.frozen(sc.current(),self.f.source):pass
        with self.assertRaises(ValueError):
            with patch.object(sc,'MAX_TOTAL',1),sc.frozen(sc.current(),self.f.source):pass
        with self.assertRaises(ValueError):
            with patch.object(sc,'MAX_FILE',1),sc.frozen(sc.current(),self.f.source):pass
        with sc.frozen(sc.current(),self.f.source) as source:
            entries=sc.tree(source.repository,source.commit,sc.SELECTED)
            path=source.root/'LICENSE';path.chmod(0o600);path.write_text('tampered')
            with self.assertRaisesRegex(ValueError,'differs from Git'):source.assert_files(entries)
            scratch=source.root
        self.assertFalse(scratch.exists())
        name='packaging/release_support/symlink.py';path=self.f.repo/name;path.symlink_to('/private/outside')
        bad=self.f.commit_all()
        with self.assertRaisesRegex(ValueError,'Non-regular'):
            with sc.frozen(sc.current(),bad):pass
        self.f.git('rm','--',name);self.f.commit_all()
        self.f.git('rm','--','LICENSE');bad=self.f.commit_all()
        with self.assertRaisesRegex(ValueError,'Missing Git source'):
            with sc.frozen(sc.current(),bad):pass

    def test_missing_known_draft_wrong_job_and_main_dispatch_refuse(self):
        for kind in ('missing','wrong-id','job','event','branch','sha'):
            with self.subTest(kind=kind),ExitStack() as stack:
                r=Remote(self.f);r.main=self.e
                if kind=='missing':r.releases=[]
                if kind=='wrong-id':r.releases=[r.record(9)]
                r.install(stack)
                if kind=='job':
                    jobs=r.jobs('');jobs['jobs'][0]['id']=500
                    stack.enter_context(patch.object(candidate,'api',return_value=jobs))
                if kind in ('event','branch','sha'):
                    key={'event':'GITHUB_EVENT_NAME','branch':'GITHUB_REF','sha':'GITHUB_SHA'}[kind]
                    stack.enter_context(patch.dict(os.environ,{key:'wrong'}))
                with self.assertRaises(ValueError):p.publish(self.f.p,self.f.c,self.f.binding)
                self.assertTrue(all(method=='GET' for _,method,_ in r.calls))

    def test_transport_cannot_supply_changed_binding_or_payload(self):
        for kind in ('binding','payload','candidate'):
            with self.subTest(kind=kind),ExitStack() as stack:
                self.remote.install(stack)
                binding=copy.deepcopy(self.f.binding)
                if kind=='binding':binding['sourceCommit']=self.e
                if kind=='payload':
                    path=self.f.p/'assets/release-notes.md';old=path.read_bytes();path.write_text('changed')
                if kind=='candidate':
                    path=self.f.c/'candidate.json';old=path.read_bytes();path.write_bytes(b'{}')
                with self.assertRaises((ValueError,KeyError)):p.publish(self.f.p,self.f.c,binding)
                if kind!='binding':path.write_bytes(old)
        self.assertTrue(all(method=='GET' for _,method,_ in self.remote.calls))

if __name__=='__main__':unittest.main()
