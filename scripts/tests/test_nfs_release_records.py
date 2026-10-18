"""Real parsers/files with synthetic bytes. No Actions, signing or readiness."""
import copy
import io
import json
import tarfile
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from nfs_release_fixture import Fixture, TAG, SHA, make_oci
from release_support import candidate, identity as i, payload, readiness


class ReleaseRecordsTest(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='nfs-release-fixture-')
        self.f=Fixture(Path(self.temp.name))
        self.addCleanup(self.temp.cleanup); self.addCleanup(self.f.close)

    def test_complete_candidate_readiness_payload(self):
        self.assertEqual(candidate.verify(self.f.c),self.f.record)
        layout=Path(self.temp.name)/'layout'
        self.assertEqual(candidate.materialize_oci(self.f.c/'engine.oci.tar',layout),self.f.image)
        with tarfile.open(self.f.c/'engine.oci.tar') as tar:
            for member in tar:
                if member.isreg():self.assertEqual((layout/member.name).read_bytes(),tar.extractfile(member).read())
        self.assertEqual(readiness.validate(self.f.c),self.f.q)
        self.f.final_payload()
        result=payload.verify(self.f.p,self.f.c)
        self.assertEqual(result['candidateRecordSha256'],self.f.q['candidate']['recordSha256'])
        checksums=(self.f.p/'assets/SHA256SUMS-nfs').read_text()
        self.assertIn('autobyteus-nfs-install.sh',checksums)
        self.assertIn('autobyteus-nfs-manifest.json',checksums)
        self.assertIn('release-provenance.json',checksums)
        provenance=i.read_json(self.f.p/'assets/release-provenance.json')
        self.assertEqual(provenance['schema'],2)
        self.assertEqual(provenance['fieldValidation'],i.DEFERRED_FIELD_VALIDATION)
        self.assertIn(readiness.DISCLOSURE,(self.f.p/'assets/release-notes.md').read_text())
        self.assertEqual(self.f.metadata['schema'],2)
        self.assertEqual(self.f.metadata['releaseTargets'],[])

    def test_strict_version_paths_json_and_sizes(self):
        for bad in ('v01.2.3','v1.2.3-beta.1','v1.2.3+build','1.2.3','v1.2','v1.2.3\n'):
            with self.subTest(value=bad),self.assertRaises(ValueError):i.version(bad)
        for bad in ('../x','/x','a//b','a/./b','a/../b','a\\b','a\nx'):
            with self.subTest(value=bad),self.assertRaises(ValueError):i.safe_name(bad)
        for bad in (True,0,-1,1.2,'1'):
            with self.subTest(value=bad),self.assertRaises(ValueError):i.positive(bad)
        for bad in (b'{"x":1,"x":2}',b'{"x":NaN}',b'{} trailing'):
            with self.subTest(value=bad),self.assertRaises(ValueError):i.decode(bad)
        link=self.f.repo/'evidence/link';link.symlink_to(self.f.repo/'evidence/authorization')
        with self.assertRaises(ValueError):readiness.evidence({'path':'evidence/link','sha256':i.sha(link)})

    def test_new_executables_invalidate_production_hash_not_readiness(self):
        before=i.source_hash(self.f.lock['engine'])
        for name in ('packaging/release_support/identity.py','packaging/release_support/candidate.py',
                     'packaging/release_support/readiness.py','packaging/release_support/payload.py',
                     'packaging/release_support/publication.py','packaging/sign-macos.sh',i.WORKFLOW):
            path=self.f.repo/name;old=path.read_bytes();path.write_bytes(old+b'\n# mutation\n')
            self.assertNotEqual(before,i.source_hash(self.f.lock['engine']),name)
            with self.assertRaises(ValueError):candidate.verify(self.f.c)
            path.write_bytes(old)
        self.f.lock['note']='changed note';self.f.save_q()
        self.assertEqual(before,i.source_hash(self.f.lock['engine']))

    def test_candidate_mutations_refused(self):
        path=self.f.c/'candidate.json'
        original=path.read_bytes()
        changes={'repository':'other/repo','workflow':'wrong.yml','runAttempt':True,'sourceCommit':'bad',
                 'sourceHash':'0'*64,'engineManifestSha256':'0'*64,'version':'v0.1.0-beta',
                 'oci':{'index':'sha256:'+'0'*64,'children':{}},'buildInputs':{'go':'0'}}
        for key,value in changes.items():
            with self.subTest(key=key):
                changed=copy.deepcopy(self.f.record);changed[key]=value;i.write_json(path,changed)
                with self.assertRaises(ValueError):candidate.verify(self.f.c)
                path.write_bytes(original)
        native=self.f.c/'native'/i.archive_name(TAG,'linux-arm64');old=native.read_bytes();native.write_bytes(old+b'x')
        with self.assertRaises(ValueError):candidate.verify(self.f.c)
        native.write_bytes(old)
        (self.f.c/'extra').write_text('unexpected')
        with self.assertRaises(ValueError):candidate.verify(self.f.c)

    def test_readiness_missing_failed_stale_false_claims_and_authority(self):
        original=copy.deepcopy(self.f.q)
        mutations=[lambda q:q.pop('postpublicationPlan'), lambda q:q.__setitem__('schema',True),
                   lambda q:q.__setitem__('kind','qualified'), lambda q:q.__setitem__('version','v9.9.9'),
                   lambda q:q['targets'].pop(), lambda q:q['targets'].reverse(),
                   lambda q:q['targets'].__setitem__(1,q['targets'][0]),
                   lambda q:q['checks'].pop('native'), lambda q:q['checks']['native'].__setitem__('status','skipped'),
                   lambda q:q['checks']['releaseControls'].__setitem__('status','failed'),
                   lambda q:q['authorization'].__setitem__('requirementsRevision','R2/SR002'),
                   lambda q:q['authorization'].__setitem__('kind','executed-user-check'),
                   lambda q:q['authorization'].__setitem__('version','v9.9.9'),
                   lambda q:q['authorization']['evidence'].__setitem__('sha256','0'*64),
                   lambda q:q['fieldValidation'].__setitem__('user','passed'),
                   lambda q:q['fieldValidation'].__setitem__('filesystem','passed'),
                   lambda q:q['fieldValidation'].__setitem__('unknown','deferred'),
                   lambda q:q.__setitem__('sourceHash','0'*64),
                   lambda q:q.__setitem__('engineManifestSha256','0'*64),
                   lambda q:q['oci'].__setitem__('index','sha256:'+'0'*64),
                   lambda q:q['candidate'].__setitem__('recordSha256','0'*64),
                   lambda q:q['candidate']['envelope'].__setitem__('runAttempt',2),
                   lambda q:q['review'].__setitem__('candidateCommit','0'*40),
                   lambda q:q.__setitem__('userVerified',True)]
        for number,mutate in enumerate(mutations):
            with self.subTest(mutation=number):
                self.f.q=copy.deepcopy(original);mutate(self.f.q);self.f.save_q()
                with self.assertRaises(ValueError):readiness.validate(self.f.c)
        self.f.q=original;self.f.save_q()
        self.assertEqual(readiness.validate(self.f.c)['fieldValidation'], i.DEFERRED_FIELD_VALIDATION)

    def test_readiness_references_are_hashed_regular_stable_and_nonempty(self):
        original=copy.deepcopy(self.f.q)
        for name in ('postpublicationPlan','releaseNotes'):
            self.f.q=copy.deepcopy(original);self.f.q[name]['sha256']='0'*64;self.f.save_q()
            with self.assertRaises(ValueError):readiness.validate(self.f.c)
        for name in ('tickets/in-progress/task/evidence.json','../escape'):
            with self.assertRaises(ValueError):readiness.evidence({'path':name,'sha256':'0'*64})
        empty=self.f.repo/'evidence/empty';empty.write_bytes(b'')
        with self.assertRaises(ValueError):readiness.evidence({'path':'evidence/empty','sha256':i.sha(empty)})
        self.f.q=original;self.f.save_q()
        self.f.lock['qualifiedTargets']=list(i.TARGETS);self.f.save_q()
        with self.assertRaises(ValueError):readiness.load()

    def test_oci_graph_not_just_declared_digest(self):
        path=Path(self.temp.name)/'bad-oci.tar';files=make_oci(path)
        for variant in ('missing','corrupt','duplicate','traversal','symlink','unexpected-platform'):
            content=copy.deepcopy(files)
            blob=next(k for k in content if k.startswith('blobs/'))
            if variant=='missing':del content[blob]
            if variant=='corrupt':
                layer=next(k for k,v in content.items() if k.startswith('blobs/') and not v.startswith(b'{'));content[layer]=b'x'*len(content[layer])
            if variant=='unexpected-platform':
                index=json.loads(content['index.json']);index['manifests'].append(index['manifests'][0]);content['index.json']=json.dumps(index).encode()
            with tarfile.open(path,'w') as tar:
                for name,data in content.items():
                    info=tarfile.TarInfo(name);info.size=len(data);tar.addfile(info,io.BytesIO(data))
                if variant in ('duplicate','traversal','symlink'):
                    info=tarfile.TarInfo('index.json' if variant=='duplicate' else '../escape' if variant=='traversal' else 'link')
                    if variant=='symlink':info.type=tarfile.SYMTYPE;info.linkname='/tmp'
                    else:info.size=1
                    tar.addfile(info,None if variant=='symlink' else io.BytesIO(b'x'))
            with self.subTest(variant=variant),self.assertRaises(ValueError):candidate.oci(path)

    def test_actions_envelope_checks_real_attempt_source_conclusion_and_expiry(self):
        e=self.f.envelope
        run={'id':42,'run_attempt':1,'repository':{'full_name':i.REPOSITORY},'head_repository':{'full_name':i.REPOSITORY},
             'path':i.WORKFLOW,'event':'workflow_dispatch','head_sha':SHA,'status':'completed','conclusion':'success',
             'run_started_at':'2026-10-01T00:00:00Z'}
        artifact={'id':43,'name':candidate.CANDIDATE,'workflow_run':{'id':42,'head_sha':SHA},'expired':False,
                  'created_at':'2026-10-01T01:00:00Z','expires_at':e['expiresAt'],'digest':e['digest'],'size_in_bytes':100}
        def check(r,a):
            with patch.object(candidate,'api',side_effect=[r,a]):
                return candidate.envelope(43,42,1,SHA,candidate.CANDIDATE)
        self.assertEqual(check(run,artifact),e)
        for key,value in [('event','push'),('run_attempt',2),('head_sha','0'*40),('conclusion','failure'),('status','in_progress')]:
            with self.subTest(key=key),self.assertRaises(ValueError):check(run|{key:value},artifact)
        for key,value in [('expired',True),('name','different'),('expires_at','2000-01-01T00:00:00Z'),
                          ('created_at','2000-01-01T00:00:00Z'),('digest','bad'),('id',44)]:
            with self.subTest(key=key),self.assertRaises(ValueError):check(run,artifact|{key:value})

    def test_executed_workflow_and_release_metadata_cannot_drift(self):
        with patch.object(i,'command',return_value=b'other workflow'),self.assertRaisesRegex(ValueError,'Executed workflow'):
            candidate.verify(self.f.c)
        import importlib.util
        from types import SimpleNamespace
        spec=importlib.util.spec_from_file_location('release_facade_test',i.ROOT/'packaging/release.py')
        facade=importlib.util.module_from_spec(spec);spec.loader.exec_module(facade)
        args=SimpleNamespace(engine_manifest=self.f.c/'engine/engine-manifest.json',source_hash=False,check_publish=False,
             tag='v9.9.9',release=True,candidate=self.f.c,engine_image=self.f.metadata['engineImage'],target=None,
             output=Path(self.temp.name)/'bad-metadata.json')
        with self.assertRaisesRegex(ValueError,'Release metadata inputs differ'):facade.metadata(args)
        self.assertFalse(args.output.exists())
        args.tag=TAG
        facade.metadata(args)
        final=json.loads(args.output.read_text())
        self.assertEqual(final['schema'],2)
        self.assertEqual(final['releaseTargets'],list(i.TARGETS))
        self.assertEqual(final['fieldValidation'],i.DEFERRED_FIELD_VALIDATION)
        args.check_publish=True;facade.metadata(args);args.check_publish=False
        args.release=False;args.tag=TAG;args.engine_image='registry.test:5443/owned@'+self.f.image['index']
        facade.metadata(args)
        alias=json.loads(args.output.read_text())
        self.assertEqual(alias['releaseTargets'],[])
        self.assertEqual(alias['sourceHash'],self.f.record['sourceHash'])
        self.assertEqual(alias['engineImage'],args.engine_image)
        args.release=True
        with self.assertRaises(ValueError):facade.metadata(args)

    def test_actions_zip_paths_and_duplicate_files(self):
        for names in (['a','a'],['../outside'],['/outside'],['a//b']):
            path=Path(self.temp.name)/'wrapper.zip'
            with zipfile.ZipFile(path,'w') as archive:
                for name in names:archive.writestr(name,'bad')
            dest=Path(self.temp.name)/'extract';dest.mkdir(exist_ok=True)
            with self.assertRaises(ValueError):candidate.extract_wrapper(path,dest)
            self.assertEqual(list(dest.iterdir()),[])

    def test_payload_semantic_disclosure_and_provenance_cannot_be_rehashed_away(self):
        self.f.final_payload()
        assets=self.f.p/'assets'
        original={p.name:p.read_bytes() for p in assets.iterdir()}
        receipt=(self.f.p/'publication.json').read_bytes()
        for kind in ('notes','status','schema','reference'):
            with self.subTest(kind=kind):
                for name,data in original.items():(assets/name).write_bytes(data)
                (self.f.p/'publication.json').write_bytes(receipt)
                provenance=i.read_json(assets/'release-provenance.json')
                if kind=='notes':(assets/'release-notes.md').write_bytes(readiness.evidence(self.f.q['releaseNotes']).read_bytes())
                if kind=='status':provenance['fieldValidation']['user']='passed'
                if kind=='schema':provenance['schema']=1
                if kind=='reference':provenance['releaseReadiness']['sha256']='0'*64
                provenance['members']=i.inventory(assets,('release-provenance.json','SHA256SUMS-nfs'))
                i.write_json(assets/'release-provenance.json',provenance)
                (assets/'SHA256SUMS-nfs').write_text(''.join(v['sha256']+'  '+n+'\n' for n,v in i.inventory(assets,('SHA256SUMS-nfs',)).items()))
                publication=i.decode(receipt);publication['members']=i.inventory(self.f.p,('publication.json',))
                i.write_json(self.f.p/'publication.json',publication)
                with self.assertRaisesRegex(ValueError,'Provenance differs|Unreviewed release notes'):payload.verify(self.f.p,self.f.c)

    def test_payload_refuses_missing_checksums_signature_and_member(self):
        self.f.final_payload()
        path=self.f.p/'assets/SHA256SUMS-nfs';path.write_text('wrong')
        with self.assertRaises(ValueError):payload.verify(self.f.p,self.f.c)
        proof={'status':'Rejected','submissionId':'12345678-1234-1234-1234-123456789abc','teamId':'ABCDEFG123','binarySha256':'0'*64}
        with self.assertRaisesRegex(ValueError,'Accepted'):
            payload.signing_proof(proof,self.f.p/'assets'/i.archive_name(TAG,'darwin-arm64'))

if __name__=='__main__':unittest.main()
