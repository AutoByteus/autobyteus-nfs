"""Synthetic records/bytes only. Never readiness or a native engine build."""
import io
import json
import hashlib
import shutil
import sys
import subprocess
import tarfile
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'packaging'))
from release_support import candidate, identity as i, payload
from source import source_identity, VERSION, NAMES

TAG = 'v0.1.0'


def make_oci(path):
    files = {'oci-layout': json.dumps({'imageLayoutVersion': '1.0.0'}).encode()}
    def blob(value, media, platform=None):
        data = json.dumps(value).encode() if isinstance(value, dict) else value
        digest = hashlib.sha256(data).hexdigest()
        files['blobs/sha256/' + digest] = data
        record = {'mediaType': media, 'digest': 'sha256:' + digest, 'size': len(data)}
        if platform: record['platform'] = platform
        return record
    children = []
    for arch in ('amd64', 'arm64'):
        buffer=io.BytesIO()
        with tarfile.open(fileobj=buffer,mode='w') as layer_tar:
            content=b'fixture-layer-'+arch.encode();info=tarfile.TarInfo('fixture-'+arch);info.size=len(content)
            layer_tar.addfile(info,io.BytesIO(content))
        layer_bytes=buffer.getvalue()
        config = blob({'os': 'linux', 'architecture': arch, 'config': {},
                       'rootfs': {'type': 'layers', 'diff_ids': ['sha256:'+hashlib.sha256(layer_bytes).hexdigest()]}},
                      'application/vnd.oci.image.config.v1+json')
        layer = blob(layer_bytes, 'application/vnd.oci.image.layer.v1.tar')
        child = blob({'schemaVersion': 2, 'config': config, 'layers': [layer]},
                     'application/vnd.oci.image.manifest.v1+json', {'os': 'linux', 'architecture': arch})
        children.append(child)
    root = blob({'schemaVersion': 2, 'manifests': children}, 'application/vnd.oci.image.index.v1+json')
    files['index.json'] = json.dumps({'schemaVersion': 2, 'manifests': [root]}).encode()
    with tarfile.open(path, 'w') as tar:
        for name, data in files.items():
            info = tarfile.TarInfo(name); info.size = len(data); tar.addfile(info, io.BytesIO(data))
    return files


def make_native(path, metadata):
    with tarfile.open(path, 'w:gz') as tar:
        files = {'LICENSE': (i.ROOT/'LICENSE').read_bytes(), 'THIRD_PARTY_NOTICES': (i.ROOT/'THIRD_PARTY_NOTICES').read_bytes(),
                 'autobyteus-nfs': b'fixture-not-executable', 'release.json': json.dumps(metadata).encode()}
        for name, data in files.items():
            info = tarfile.TarInfo(name); info.size = len(data); tar.addfile(info, io.BytesIO(data))


class Fixture:
    def __init__(self, root):
        self.root = root
        self.repo = root / 'repo'; self.repo.mkdir()
        for name in i.SOURCES + ('packaging/release-lock.json',):
            src, dst = ROOT / name, self.repo / name
            dst.parent.mkdir(parents=True, exist_ok=True)
            if src.is_dir(): shutil.copytree(src, dst, ignore=shutil.ignore_patterns('__pycache__','*.deb'))
            else: shutil.copyfile(src,dst)
        self.root_patch = patch.object(i, 'ROOT', self.repo); self.root_patch.start()
        self.git('init', '-q')
        self.git('config', 'user.name', 'Synthetic Fixture')
        self.git('config', 'user.email', 'fixture@example.invalid')
        self.c = root/'candidate'; (self.c/'engine').mkdir(parents=True); (self.c/'native').mkdir()
        lock = i.read_json(self.repo/'packaging/release-lock.json')
        measured = {'source': source_identity(lock['ubuntuBaseImage']), 'architectures': {}}
        for arch in ('amd64','arm64'):
            folder = self.c/'engine'/arch; folder.mkdir()
            records = []
            for name in NAMES:
                path=folder/f'{name}_{VERSION}_{arch}.deb'; path.write_bytes((name+arch).encode())
                records.append({'file':path.name,**i.file_record(path),'name':name,'version':VERSION,'architecture':arch})
            source=folder/f'source-{arch}.tar.gz'; source.write_bytes(b'source-fixture')
            build=folder/f'build-{arch}.txt'; build.write_bytes(b'build-fixture')
            (folder/'COPYRIGHT').write_bytes(b'engine copyright fixture')
            (folder/'SHA256SUMS').write_bytes(b'fixture checksum inventory')
            measured['architectures'][arch]={'packages':records,'correspondingSource':{'file':source.name,**i.file_record(source)},
                                           'buildInventory':{'file':build.name,**i.file_record(build)}}
        i.write_json(self.c/'engine/engine-manifest.json',measured)
        i.write_json(self.repo/'packaging/release-lock.json',lock|{'engine':measured, 'releaseReadiness':None})
        self.c_commit = self.commit_all()
        make_oci(self.c/'engine.oci.tar')
        self.image=candidate.oci(self.c/'engine.oci.tar')
        self.metadata=candidate.runtime_metadata(TAG,i.IMAGE+'@'+self.image['index'],measured)
        for target in i.TARGETS: make_native(self.c/'native'/i.archive_name(TAG,target),self.metadata)
        self.record=candidate.assemble(self.c,TAG,self.c_commit,self.c_commit,42,1)
        self.envelope={'artifactId':43,'runId':42,'runAttempt':1,'workflowCommit':self.c_commit,
                       'digest':'sha256:'+'b'*64,'expiresAt':'2099-01-01T00:00:00Z'}
        self.q={'schema':1,'kind':'release-first','version':TAG,'targets':list(i.TARGETS),
                'candidate':{'recordSha256':i.sha(self.c/'candidate.json'),'envelope':self.envelope},
                'sourceHash':self.record['sourceHash'],'engineManifestSha256':self.record['engineManifestSha256'],
                'oci':self.image,'fieldValidation':dict(i.DEFERRED_FIELD_VALIDATION),
                'authorization':{'kind':'publish-before-field-testing','requirementsRevision':'R3/SR004',
                                 'version':TAG,'evidence':self.evidence('authorization')},
                'checks':{name:{'status':'passed','evidence':self.evidence(name)} for name in ('native','releaseControls')},
                'postpublicationPlan':self.evidence('plan'),
                'review':{'candidateCommit':self.c_commit,'sourceHash':self.record['sourceHash'],'evidence':self.evidence('review')},
                'releaseNotes':self.evidence('notes')}
        self.lock=lock|{'engine':measured}
        self.save_q()
        self.source = self.commit_all()

    def evidence(self,name):
        path=self.repo/'packaging/releases'/TAG/name; path.parent.mkdir(parents=True,exist_ok=True); path.write_text('synthetic '+name+'\n')
        return {'path':path.relative_to(self.repo).as_posix(),'sha256':i.sha(path)}

    def save_q(self):
        path=self.repo/'packaging/releases'/TAG/'readiness.json'; i.write_json(path,self.q)
        self.lock['releaseReadiness']={'path':'packaging/releases/'+TAG+'/readiness.json','sha256':i.sha(path)}
        i.write_json(self.repo/'packaging/release-lock.json',self.lock)

    def final_payload(self):
        native=self.root/'native';native.mkdir()
        metadata=candidate.runtime_metadata(TAG,self.metadata['engineImage'],self.lock['engine'],True)
        for target in i.TARGETS:
            archive=native/i.archive_name(TAG,target);make_native(archive,metadata)
            if target.startswith('darwin'):
                i.write_json(native/(target+'-notary.json'),{'status':'Accepted','submissionId':'12345678-1234-1234-1234-123456789abc',
                             'teamId':'ABCDEFG123','binarySha256':payload.binary_hash(archive)})
        self.p=self.root/'payload';payload.assemble(self.p,self.c,native,self.source,99,1)
        self.binding={'repository':i.REPOSITORY,'version':TAG,'sourceCommit':self.source,'payloadSha256':i.sha(self.p/'publication.json'),
                      'envelope':self.envelope|{'artifactId':100,'runId':99,'workflowCommit':self.source}}
        return self.p

    def git(self, *args):
        return subprocess.run(['git', *args], cwd=self.repo, capture_output=True, check=True).stdout

    def commit_all(self):
        paths = self.git('ls-files', '--modified', '--others', '--exclude-standard', '-z').split(b'\0')
        paths = [p.decode() for p in paths if p]
        if paths:
            self.git('add', '--', *paths)
        self.git('commit', '-qm', 'synthetic fixture', '--allow-empty')
        return self.git('rev-parse', 'HEAD').decode().strip()

    def close(self):
        self.root_patch.stop()
