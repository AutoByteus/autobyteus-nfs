"""Nonpublishing service-only refusal fixtures; no real install or mounts."""
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

class NfsPackagingTest(unittest.TestCase):
    def test_unpublished_installer_fails_before_download(self):
        result = subprocess.run(['/bin/bash', str(ROOT / 'scripts/public/nfs/install.sh')],
                                capture_output=True, text=True, env={'PATH':'/usr/bin:/bin'})
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('No qualified versioned release', result.stderr)

    def test_unqualified_release_cannot_publish(self):
        result = subprocess.run(['python3', str(ROOT / 'packaging/release.py'), '--check-publish'],
                                capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('No qualified release targets', result.stderr)

    def test_nfs_workflow_build_only_never_pushes_or_publishes(self):
        content=(ROOT/'.github/workflows/release-nfs.yml').read_text()
        self.assertIn('default: false',content)
        self.assertIn("push: ${{ needs.prepare.outputs.publish == 'true' }}",content)
        self.assertIn("if: needs.prepare.outputs.publish == 'true'",content)
        self.assertIn('--check-publish',content)
        self.assertNotIn('gh release create',content)


if __name__ == "__main__":
    unittest.main()
