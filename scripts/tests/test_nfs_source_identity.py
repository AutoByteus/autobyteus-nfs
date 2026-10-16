"""Local owned-input digest controls; no app checkout or publication.
Run: python3 -m unittest scripts/tests/test_nfs_source_identity.py -v
"""
import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('standalone_release', ROOT/'packaging/release.py')
release = importlib.util.module_from_spec(spec)
spec.loader.exec_module(release)


class SourceIdentityTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='nfs-source-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in release.SOURCES + ['packaging/release-lock.json']:
            src, dst = ROOT/name, self.root/name
            dst.parent.mkdir(parents=True, exist_ok=True)
            if src.is_dir():
                shutil.copytree(src, dst)
            else:
                shutil.copyfile(src, dst)
        self.root_patch = patch.object(release, 'ROOT', self.root)
        self.lock_patch = patch.object(release, 'LOCK', self.root/'packaging/release-lock.json')
        self.root_patch.start(); self.lock_patch.start()
        self.addCleanup(self.root_patch.stop); self.addCleanup(self.lock_patch.stop)

    def test_declared_owned_boundary_and_default_qualification(self):
        self.assertEqual(set(release.SOURCES), {
            'internal', 'cmd/autobyteus-nfs/main.go', 'go.mod', 'scripts/public/nfs',
            'packaging/Dockerfile', 'packaging/engine', 'packaging/release.py',
            '.github/workflows/release-nfs.yml', 'testdata/attachment.json',
            'docs/integration-contract.md', 'LICENSE', 'THIRD_PARTY_NOTICES'})
        lock = json.loads(release.LOCK.read_text())
        self.assertEqual([lock[k] for k in ['qualifiedTargets', 'qualifiedSourceHash',
                         'physicalEvidence', 'userVerified', 'engine']], [[], '', [], False, None])
        self.assertEqual(release.source_hash(), release.source_hash())
        # Neither undeclared app bytes nor qualification/generated outputs attest source.
        (self.root/'app-source').write_text('not service-owned')
        before = release.source_hash()
        lock.update(qualifiedSourceHash='receipt', userVerified=True, physicalEvidence=['receipt'])
        release.LOCK.write_text(json.dumps(lock))
        (self.root/'cmd/autobyteus-nfs/release.json').write_text('generated')
        (self.root/'out').mkdir(); (self.root/'out/binary').write_bytes(b'generated')
        self.assertEqual(before, release.source_hash())

    def test_every_declared_input_is_required(self):
        for name in release.SOURCES:
            with self.subTest(input=name):
                p = self.root/name; hidden = p.with_name(p.name+'.absent')
                p.rename(hidden)
                try:
                    with self.assertRaises(FileNotFoundError): release.source_hash()
                finally:
                    hidden.rename(p)

    def test_owned_input_changes_invalidate_qualification(self):
        before = release.source_hash()
        lock = json.loads(release.LOCK.read_text())
        lock.update(qualifiedTargets=['linux-arm64'], qualifiedSourceHash=before,
                    userVerified=True, physicalEvidence=['one', 'two', 'three'])
        release.LOCK.write_text(json.dumps(lock))
        for name in release.SOURCES:
            p = self.root/name
            if p.is_dir():
                p = next(x for x in sorted(p.rglob('*')) if x.is_file()
                         and not x.name.endswith('_test.go') and '__pycache__' not in x.parts)
            with self.subTest(input=name):
                original = p.read_bytes(); p.write_bytes(original+b'\nchanged input\n')
                try:
                    self.assertNotEqual(before, release.source_hash())
                    with patch.object(sys, 'argv', ['release.py', '--check-publish']):
                        with self.assertRaisesRegex(SystemExit, 'Current-source'):
                            release.main()
                    out = self.root/'generated.json'
                    with patch.object(sys, 'argv', ['release.py', '--tag', 'v0.0.0-test', '--output', str(out)]):
                        release.main()
                    self.assertEqual(json.loads(out.read_text())['qualifiedTargets'], [])
                finally:
                    p.write_bytes(original)
        self.assertEqual(before, release.source_hash())


if __name__ == '__main__':
    unittest.main()
