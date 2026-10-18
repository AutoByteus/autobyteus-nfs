"""Bounded reviewer checks; all execution and baseline substitution use an owned copy."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import tempfile
import textwrap
import time

E = Path(__file__).resolve().parent
T = E.parent.parent
N = T.parent.parent.parent

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def git(*args):
    return subprocess.check_output(['git', *args], cwd=N, text=True).strip()

head = git('rev-parse', 'HEAD')
source = '8436d0cf6048cd3b4cadbf28815e3d9f82ba6b34'
prior_source = '886b55e1cf88f3f696334bd5e7b8c374946a594d'
assert not git('diff', '--name-only', source, '--', '.', ':!tickets')
inputs = {p: sha(N / p) for p in git('ls-files').splitlines() if not p.startswith('tickets/')}
assert len(inputs) == 119
delta = git('diff', '--name-only', prior_source, source, '--', '.', ':!tickets').splitlines()
assert delta == ['.github/workflows/release-nfs.yml', 'TESTING.md', 'scripts/tests/test_nfs_release_workflow.py']
delivery = json.loads((T / 'implementation-evidence/ir-002/final-checks.json').read_text())['preservedDeliveryUntracked']
assert all(sha(N / p) == x['sha256'] for p, x in delivery.items())
scoped = ['requirements-doc.md', 'design-spec.md', 'implementation-handoff.md', 'implementation-revision-record.md', 'api-e2e-execution-coverage-report.md', 'api-e2e-revision-record.md', 'api-e2e-test-case-ledger.md', 'api-e2e-coverage-investigation.md', 'code-review-report.md', 'code-review-revision-record.md']
history = (T / 'code-review-revision-record.md').read_bytes()
audit = {'head': head, 'source': source, 'prior_source': prior_source, 'branch': git('branch', '--show-current'), 'source_inputs': inputs, 'changed_inputs': delta, 'unaffected_inputs': 116, 'scoped_inputs': {p: sha(T / p) for p in scoped}, 'delivery_owned_inputs': delivery, 'history_bytes': len(history), 'history_sha256': hashlib.sha256(history).hexdigest()}
(E / 'input-audit.json').write_text(json.dumps(audit, indent=2) + '\n')
scratch = Path(tempfile.mkdtemp(prefix='nfs-release-crr003-', dir='/Users/normy'))
copy = scratch / 'source'
copy.mkdir(mode=0o700)
for name in inputs:
    dst = copy / name
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(N / name, dst)
for name in ['home', 'tmp']:
    (scratch / name).mkdir(mode=0o700)
env = {'PATH': '/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin', 'HOME': str(scratch / 'home'), 'TMPDIR': str(scratch / 'tmp'), 'PYTHONDONTWRITEBYTECODE': '1', 'LANG': 'en_US.UTF-8'}
rows = []
def run(name, argv, expected=0):
    start = time.monotonic()
    p = subprocess.run(argv, cwd=copy, env=env, text=True, capture_output=True, timeout=180)
    (E / (name + '.log')).write_text(p.stdout + p.stderr)
    rows.append({'name': name, 'argv': argv, 'exit': p.returncode, 'expected': expected, 'seconds': round(time.monotonic()-start, 3)})
    print(name, p.returncode, flush=True)
    assert p.returncode == expected
    return p.stdout + p.stderr

try:
    run('python-version', ['/usr/bin/python3', '--version'])
    run('shell-version', ['/bin/bash', '--version'])
    focused = ['/usr/bin/python3', '-m', 'unittest', 'discover', '-s', 'scripts/tests', '-p', 'test_nfs_release_workflow.py', '-v']
    current = run('current-workflow', focused)
    assert 'Ran 7 tests' in current and '\nOK\n' in current
    wf = copy / '.github/workflows/release-nfs.yml'
    current_bytes = wf.read_bytes()
    try:
        wf.write_bytes(subprocess.check_output(['git', 'show', prior_source + ':.github/workflows/release-nfs.yml'], cwd=N))
        baseline = run('original-workflow-control', focused, 1)
        assert 'FAILED (failures=5)' in baseline and 'args[@]: unbound variable' in baseline
    finally:
        wf.write_bytes(current_bytes)
    full = run('python-all', ['/usr/bin/python3', '-m', 'unittest', 'discover', '-s', 'scripts/tests', '-p', 'test_nfs_*.py', '-v'])
    assert 'Ran 41 tests' in full and 'OK (skipped=1)' in full
    run('actionlint', ['/opt/homebrew/bin/actionlint', '.github/workflows/ci.yml', '.github/workflows/release-nfs.yml'])
    block = wf.read_text().split('      - name: Native checks and exact engine metadata (not physical qualification)\n', 1)[1].split('        run: |\n', 1)[1].split('          go test -race ./...\n', 1)[0]
    prefix = scratch / 'native-prefix.sh'
    prefix.write_text(textwrap.dedent(block))
    run('prefix-syntax', ['/bin/bash', '-n', str(prefix)])
    run('prefix-shellcheck', ['/opt/homebrew/bin/shellcheck', '-s', 'bash', str(prefix)])
    source_hash = run('source-hash', ['/usr/bin/python3', 'packaging/release.py', '--source-hash'])
    assert source_hash.strip() == '26af7e5bcab00ae22d4bdebe1820c6d38b0dc51a44f1b834036334ea79528298'
    refusal = run('publish-refusal', ['/usr/bin/python3', 'packaging/release.py', '--check-publish'], 1)
    assert 'No qualified release targets: exactly all four required' in refusal
    assert all(sha(copy / p) == value and sha(N / p) == value for p, value in inputs.items())
    assert all(sha(T / p) == value for p, value in audit['scoped_inputs'].items())
    assert all(sha(N / p) == x['sha256'] for p, x in delivery.items())
finally:
    shutil.rmtree(scratch)
    (E / 'checks-result.json').write_text(json.dumps({'review': 'CRR-003', 'rows': rows, 'current_unique_tests': 41, 'executed': 40, 'standalone_go_child_skips': 1, 'focused7_overlap_full41': True, 'baseline_is_expected_failure_not_new_product_pass': True, 'all_expected': len(rows) == 10 and all(x['exit'] == x['expected'] for x in rows), 'limits': 'Local Mac arm64 Bash3.2 invocation and Python/static checks, not hosted/four CPU/metadata/NFS/signing qualification. No Go rerun or mutation rerun; IR002 mutations attributed.'}, indent=2) + '\n')
    (E / 'cleanup.json').write_text(json.dumps({'scratch': str(scratch), 'scratch_absent': not scratch.exists(), 'resources': 'Only own copy/HOME/tmp and synchronous subprocesses; no live/hosted/remote action', 'source_inputs': len(inputs), 'delivery_owned_inputs': len(delivery)}, indent=2) + '\n')
print('complete', flush=True)
