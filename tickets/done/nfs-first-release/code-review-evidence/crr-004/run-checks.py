"""Independent local reviewer checks; no hosted/publication or live NFS effects."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import time
import urllib.request

E = Path(__file__).resolve().parent
ROOT = E.parents[4]
A = json.loads((E / 'input-audit.json').read_text())
S = Path(tempfile.mkdtemp(prefix='nfs-release-crr004-', dir='/Users/normy'))
(E / 'scratch-path.txt').write_text(str(S) + '\n')
rows = []
try:
    for name in ('source', 'home', 'tmp', 'cache', 'modules', 'out'):
        (S / name).mkdir()
    for name, digest in A['source_inputs'].items():
        data = (ROOT / name).read_bytes()
        assert hashlib.sha256(data).hexdigest() == digest, name
        target = S / 'source' / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / name, target)
    with urllib.request.urlopen('https://go.dev/dl/?mode=json&include=all', timeout=90) as response:
        releases = json.load(response)
    release = next(r for r in releases if r['version'] == 'go1.27.2')
    package = next(f for f in release['files'] if f['os'] == 'darwin' and f['arch'] == 'arm64' and f['kind'] == 'archive')
    archive = S / package['filename']
    urllib.request.urlretrieve('https://go.dev/dl/' + package['filename'], archive)
    assert hashlib.sha256(archive.read_bytes()).hexdigest() == package['sha256']
    (E / 'toolchain.json').write_text(json.dumps(package, indent=2) + '\n')
    subprocess.run(['tar', '-xzf', str(archive), '-C', str(S)], check=True)
    env = {'HOME': str(S / 'home'), 'TMPDIR': str(S / 'tmp'),
           'PATH': str(S / 'go/bin') + ':/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin',
           'GOCACHE': str(S / 'cache'), 'GOMODCACHE': str(S / 'modules'), 'GOTOOLCHAIN': 'local',
           'PYTHONDONTWRITEBYTECODE': '1', 'LANG': 'en_US.UTF-8'}
    def run(name, argv, expected=0):
        started = time.monotonic()
        with (E / (name + '.log')).open('w') as log:
            result = subprocess.run(argv, cwd=S / 'source', env=env, stdout=log, stderr=subprocess.STDOUT, timeout=1200)
        row = {'name': name, 'argv': argv, 'exit': result.returncode, 'expected': expected,
               'seconds': round(time.monotonic() - started, 3)}
        rows.append(row)
        (E / 'checks-result.json').write_text(json.dumps(rows, indent=2) + '\n')
        print(json.dumps(row), flush=True)
        assert result.returncode == expected, name
    run('go-version', ['go', 'version'])
    run('shell-version', ['/bin/bash', '--version'])
    run('python-version', ['/usr/bin/python3', '--version'])
    run('python-all', ['/usr/bin/python3', '-m', 'unittest', 'discover', '-s', 'scripts/tests', '-p', 'test_nfs_*.py', '-v'])
    run('go-race', ['go', 'test', '-race', '-v', './...'])
    run('go-vet', ['go', 'vet', './...'])
    run('native-build', ['go', 'build', '-o', str(S / 'out/autobyteus-nfs'), './cmd/autobyteus-nfs'])
    run('native-version', [str(S / 'out/autobyteus-nfs'), 'version'])
    run('actionlint', ['/opt/homebrew/bin/actionlint', '.github/workflows/ci.yml', '.github/workflows/release-nfs.yml'])
    run('shell-syntax', ['/bin/bash', '-n', 'packaging/sign-macos.sh', 'scripts/public/nfs/install.sh'])
    run('shellcheck', ['/opt/homebrew/bin/shellcheck', 'packaging/sign-macos.sh', 'scripts/public/nfs/install.sh'])
    run('source-hash', ['/usr/bin/python3', 'packaging/release.py', '--source-hash'])
    run('readiness-refusal', ['/usr/bin/python3', 'packaging/release.py', '--check-publish'], 1)
    for name, digest in A['source_inputs'].items():
        assert hashlib.sha256((S / 'source' / name).read_bytes()).hexdigest() == digest, name
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest, name
    (E / 'source-integrity.json').write_text(json.dumps({'all_match': True, 'source_count': len(A['source_inputs'])}, indent=2) + '\n')
finally:
    shutil.rmtree(S)
    (E / 'cleanup.json').write_text(json.dumps({'scratch': str(S), 'removed': not S.exists(), 'subprocesses_synchronous': True,
        'no_vm_container_mount_provider_signing_remote_actions': True}, indent=2) + '\n')
