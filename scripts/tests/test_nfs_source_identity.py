"""Local owned-input digest controls; no app checkout or publication.
Run: python3 -m unittest scripts/tests/test_nfs_source_identity.py -v
"""
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('standalone_release', ROOT/'packaging/release.py')
facade = importlib.util.module_from_spec(spec)
spec.loader.exec_module(facade)
release = facade.i


class SourceIdentityTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='nfs-source-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in release.SOURCES + ('packaging/release-lock.json',):
            src, dst = ROOT/name, self.root/name
            dst.parent.mkdir(parents=True, exist_ok=True)
            if src.is_dir():
                shutil.copytree(src, dst)
            else:
                shutil.copyfile(src, dst)
        self.root_patch = patch.object(release, 'ROOT', self.root)
        self.root_patch.start()
        self.addCleanup(self.root_patch.stop)
        self.lock_path=self.root/'packaging/release-lock.json'
        lock=json.loads(self.lock_path.read_text())
        lock.update(engine=None,releaseReadiness=None)
        self.lock_path.write_text(json.dumps(lock))
        def git(*args):
            return subprocess.run(['git', *args], cwd=self.root, check=True, capture_output=True).stdout
        git('init', '-q')
        git('config', 'user.name', 'Synthetic Source Fixture')
        git('config', 'user.email', 'fixture@example.invalid')
        files = [str(p.relative_to(self.root)) for p in self.root.rglob('*')
                 if p.is_file() and '.git' not in p.relative_to(self.root).parts and '__pycache__' not in p.parts]
        git('add', '--', *files)
        git('commit', '-qm', 'synthetic source fixture')

    def test_declared_owned_boundary_and_default_readiness(self):
        self.assertEqual(set(release.SOURCES), {
            'internal', 'cmd/autobyteus-nfs/main.go', 'go.mod', 'scripts/public/nfs',
            'packaging/Dockerfile', 'packaging/engine', 'packaging/release.py',
            '.github/workflows/release-nfs.yml', 'testdata/connection.json',
            'docs/filesystem-usage.md', 'LICENSE', 'THIRD_PARTY_NOTICES',
            'packaging/release_support', 'packaging/sign-macos.sh'})
        lock = json.loads(self.lock_path.read_text())
        self.assertEqual(set(lock), {'ubuntuBaseImage','ubuntuPackages','engine','releaseReadiness','note'})
        self.assertIsNone(lock['releaseReadiness'])
        self.assertIsNone(lock['engine'])
        self.assertEqual(release.source_hash(), release.source_hash())
        # Neither undeclared app bytes nor readiness/generated outputs attest source.
        (self.root/'app-source').write_text('not service-owned')
        before = release.source_hash()
        lock.update(releaseReadiness={'path':'receipt','sha256':'0'*64})
        self.lock_path.write_text(json.dumps(lock))
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

    def test_owned_input_changes_invalidate_readiness(self):
        before = release.source_hash()
        lock = json.loads(self.lock_path.read_text())
        lock.update(releaseReadiness=None)
        self.lock_path.write_text(json.dumps(lock))
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
                        with self.assertRaisesRegex(ValueError, 'Current engine and structured release readiness'):
                            facade.main()
                    out = self.root/'generated.json'
                    with patch.object(sys, 'argv', ['release.py', '--tag', 'v0.0.0', '--output', str(out)]):
                        facade.main()
                    self.assertEqual(json.loads(out.read_text())['releaseTargets'], [])
                finally:
                    p.write_bytes(original)
        self.assertEqual(before, release.source_hash())


if __name__ == '__main__':
    unittest.main()
