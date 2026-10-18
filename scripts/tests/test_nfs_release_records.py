"""Real parsers/files with synthetic bytes. No Actions, signing or qualification."""
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
from release_support import candidate, identity as i, payload, qualification


class ReleaseRecordsTest(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='nfs-release-fixture-')
        self.f=Fixture(Path(self.temp.name))
        self.addCleanup(self.temp.cleanup); self.addCleanup(self.f.close)

    def test_complete_candidate_qualification_payload(self):
        self.assertEqual(candidate.verify(self.f.c),self.f.record)
        layout=Path(self.temp.name)/'layout'
        self.assertEqual(candidate.materialize_oci(self.f.c/'engine.oci.tar',layout),self.f.image)
        with tarfile.open(self.f.c/'engine.oci.tar') as tar:
            for member in tar:
                if member.isreg():self.assertEqual((layout/member.name).read_bytes(),tar.extractfile(member).read())
        self.assertEqual(qualification.validate(self.f.c),self.f.q)
        self.f.final_payload()
        result=payload.verify(self.f.p,self.f.c)
        self.assertEqual(result['candidateRecordSha256'],self.f.q['candidate']['recordSha256'])
        checksums=(self.f.p/'assets/SHA256SUMS-nfs').read_text()
        self.assertIn('autobyteus-nfs-install.sh',checksums)
        self.assertIn('autobyteus-nfs-manifest.json',checksums)
        self.assertIn('release-provenance.json',checksums)

    def test_strict_version_paths_json_and_sizes(self):
        for bad in ('v01.2.3','v1.2.3-beta.1','v1.2.3+build','1.2.3','v1.2','v1.2.3\n'):
            with self.subTest(value=bad),self.assertRaises(ValueError):i.version(bad)
        for bad in ('../x','/x','a//b','a/./b','a/../b','a\\b','a\nx'):
            with self.subTest(value=bad),self.assertRaises(ValueError):i.safe_name(bad)
        for bad in (True,0,-1,1.2,'1'):
            with self.subTest(value=bad),self.assertRaises(ValueError):i.positive(bad)
        for bad in (b'{"x":1,"x":2}',b'{"x":NaN}',b'{} trailing'):
            with self.subTest(value=bad),self.assertRaises(ValueError):i.decode(bad)
        link=self.f.repo/'evidence/link';link.symlink_to(self.f.repo/'evidence/user')
        with self.assertRaises(ValueError):qualification.evidence({'path':'evidence/link','sha256':i.sha(link)})

    def test_new_executables_invalidate_production_hash_not_qualification(self):
        before=i.source_hash(self.f.lock['engine'])
        for name in ('packaging/release_support/identity.py','packaging/release_support/candidate.py',
                     'packaging/release_support/qualification.py','packaging/release_support/payload.py',
                     'packaging/release_support/publication.py','packaging/sign-macos.sh',i.WORKFLOW):
            path=self.f.repo/name;old=path.read_bytes();path.write_bytes(old+b'\n# mutation\n')
            self.assertNotEqual(before,i.source_hash(self.f.lock['engine']),name)
            with self.assertRaises(ValueError):candidate.verify(self.f.c)
            path.write_bytes(old)
        self.f.lock['qualifiedSourceHash']='x';self.f.save_q()
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

    def test_qualification_missing_failed_duplicate_inapplicable_and_consent(self):
        original=copy.deepcopy(self.f.q)
        mutations=[lambda q:q['rows'].pop(),lambda q:q['rows'].__setitem__(1,q['rows'][0]),
                   lambda q:q['rows'][0]['cases'].__setitem__('create-connect','fail'),
                   lambda q:q['rows'][0].__setitem__('osVersion','15.0'),
                   lambda q:q['rows'][0]['topology'].__setitem__('clientKernel','server-boot'),
                   lambda q:q['rows'][0].__setitem__('engineImage','registry.invalid/a@sha256:'+'0'*64),
                   lambda q:q['userVerification'].__setitem__('kind','publication-consent'),
                   lambda q:q['userVerification'].__setitem__('candidateRecordSha256','0'*64),
                   lambda q:q.__setitem__('sourceHash','0'*64),
                   lambda q:q['candidate']['envelope'].__setitem__('runAttempt',2),
                   lambda q:q['rows'][0]['evidence'].__setitem__('sha256','0'*64)]
        for mutate in mutations:
            self.f.q=copy.deepcopy(original);mutate(self.f.q);self.f.save_q()
            with self.assertRaises(ValueError):qualification.validate(self.f.c)
        self.f.q=copy.deepcopy(original)
        for row in self.f.q['rows']:row['topology']['kind']='virtual'
        self.f.save_q()
        with self.assertRaisesRegex(ValueError,'physical'):qualification.validate(self.f.c)

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

    def test_executed_workflow_and_qualified_metadata_cannot_drift(self):
        with patch.object(i,'command',return_value=b'other workflow'),self.assertRaisesRegex(ValueError,'Executed workflow'):
            candidate.verify(self.f.c)
        import importlib.util
        from types import SimpleNamespace
        spec=importlib.util.spec_from_file_location('release_facade_test',i.ROOT/'packaging/release.py')
        facade=importlib.util.module_from_spec(spec);spec.loader.exec_module(facade)
        args=SimpleNamespace(engine_manifest=self.f.c/'engine/engine-manifest.json',source_hash=False,check_publish=False,
             tag='v9.9.9',qualified=True,candidate=self.f.c,engine_image=self.f.metadata['engineImage'],target=None,
             output=Path(self.temp.name)/'bad-metadata.json')
        with self.assertRaisesRegex(ValueError,'Qualified metadata inputs differ'):facade.metadata(args)
        self.assertFalse(args.output.exists())
        args.qualified=False;args.tag=TAG;args.engine_image='registry.test:5443/owned@'+self.f.image['index']
        facade.metadata(args)
        alias=json.loads(args.output.read_text())
        self.assertEqual(alias['qualifiedTargets'],[])
        self.assertEqual(alias['sourceHash'],self.f.record['sourceHash'])
        self.assertEqual(alias['engineImage'],args.engine_image)
        args.qualified=True
        with self.assertRaises(ValueError):facade.metadata(args)

    def test_actions_zip_paths_and_duplicate_files(self):
        for names in (['a','a'],['../outside'],['/outside'],['a//b']):
            path=Path(self.temp.name)/'wrapper.zip'
            with zipfile.ZipFile(path,'w') as archive:
                for name in names:archive.writestr(name,'bad')
            dest=Path(self.temp.name)/'extract';dest.mkdir(exist_ok=True)
            with self.assertRaises(ValueError):candidate.extract_wrapper(path,dest)
            self.assertEqual(list(dest.iterdir()),[])

    def test_payload_refuses_missing_checksums_signature_and_member(self):
        self.f.final_payload()
        path=self.f.p/'assets/SHA256SUMS-nfs';path.write_text('wrong')
        with self.assertRaises(ValueError):payload.verify(self.f.p,self.f.c)
        proof={'status':'Rejected','submissionId':'12345678-1234-1234-1234-123456789abc','teamId':'ABCDEFG123','binarySha256':'0'*64}
        with self.assertRaisesRegex(ValueError,'Accepted'):
            payload.signing_proof(proof,self.f.p/'assets'/i.archive_name(TAG,'darwin-arm64'))

if __name__=='__main__':unittest.main()
