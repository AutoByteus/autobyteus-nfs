"""Nonpublishing service-only refusal fixtures; no real install or mounts."""
import subprocess
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

class NfsPackagingTest(unittest.TestCase):
    def test_unpublished_installer_fails_before_download(self):
        result = subprocess.run(['/bin/bash', str(ROOT / 'scripts/public/nfs/install.sh')],
                                capture_output=True, text=True, env={'PATH':'/usr/bin:/bin'})
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('No versioned release', result.stderr)

    def test_missing_readiness_cannot_publish(self):
        sys.path.insert(0,str(ROOT/'packaging'))
        from release_support import readiness
        with tempfile.TemporaryDirectory() as scratch:
            root=Path(scratch);(root/'packaging').mkdir()
            lock=json.loads((ROOT/'packaging/release-lock.json').read_text())
            lock.update(engine=None,releaseReadiness=None)
            (root/'packaging/release-lock.json').write_text(json.dumps(lock))
            with self.assertRaisesRegex(ValueError,'Current engine and structured release readiness'):readiness.load(root)

    def test_removed_qualified_flag_is_not_an_alias(self):
        result=subprocess.run([sys.executable,str(ROOT/'packaging/release.py'),'--qualified','--tag','v0.1.0'],
                              capture_output=True,text=True)
        self.assertEqual(result.returncode,2)
        self.assertIn('unrecognized arguments: --qualified',result.stderr)

    def test_nfs_workflow_build_only_never_pushes_or_publishes(self):
        content=(ROOT/'.github/workflows/release-nfs.yml').read_text()
        self.assertIn('default: false',content)
        self.assertIn('push: false',content)
        self.assertIn("needs.prepare.outputs.mode == 'fresh'",content)
        self.assertIn('--operation prepare',content)
        self.assertNotIn('gh release create',content)


if __name__ == "__main__":
    unittest.main()
