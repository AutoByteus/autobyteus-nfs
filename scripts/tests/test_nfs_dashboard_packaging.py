"""Embedded local dashboard source contract; no browser, installer or host effects."""
import importlib.util
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location('dashboard_source_identity', ROOT / 'packaging/release_support/identity.py')
IDENTITY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(IDENTITY)


class DashboardPackagingTests(unittest.TestCase):
    def test_embedded_static_allowlist_is_self_contained(self):
        owner = (ROOT / 'internal/dashboard/assets.go').read_text()
        self.assertIn('//go:embed web/*', owner)
        for name in ('index.html', 'styles.css', 'app.js', 'api.js', 'forms.js'):
            self.assertIn('"' + name + '"', owner)
            self.assertTrue((ROOT / 'internal/dashboard/web' / name).is_file())
        html = (ROOT / 'internal/dashboard/web/index.html').read_text()
        self.assertIn('src="/app.js"', html)
        self.assertIn('href="/styles.css"', html)
        self.assertNotIn('https://', html)
        self.assertNotIn('http://', html)

    def test_js_and_css_change_existing_source_identity(self):
        with tempfile.TemporaryDirectory(prefix='nfs-dashboard-hash-') as temporary:
            root = Path(temporary)
            for name in (*IDENTITY.SOURCES, 'packaging/release-lock.json'):
                source, target = ROOT / name, root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                if source.is_dir():
                    shutil.copytree(source, target, dirs_exist_ok=True)
                else:
                    shutil.copyfile(source, target)
            baseline = IDENTITY.source_hash(root=root)
            for name in ('app.js', 'styles.css'):
                path = root / 'internal/dashboard/web' / name
                original = path.read_bytes()
                path.write_bytes(original + b'\n/* owned mutation */\n')
                self.assertNotEqual(baseline, IDENTITY.source_hash(root=root), name)
                path.write_bytes(original)
                self.assertEqual(baseline, IDENTITY.source_hash(root=root))


if __name__ == '__main__':
    unittest.main()
