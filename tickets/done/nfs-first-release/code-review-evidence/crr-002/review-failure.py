"""Focused R03-F001 review. Executes exact shell lines with an inert command only."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import tempfile

E = Path(__file__).resolve().parent
T = E.parent.parent
N = T.parent.parent.parent
A = T / 'evidence/api-e2e/api-rev-001'

def digest(data):
    return hashlib.sha256(data).hexdigest()

def git(*args):
    return subprocess.check_output(['git', *args], cwd=N, text=True).strip()

workflow = N / '.github/workflows/release-nfs.yml'
text = workflow.read_text()
start = text.index('          args=()\n', text.index('name: Native checks and exact engine metadata'))
end = text.index('\n          go test -race', start)
body = '\n'.join(line[10:] for line in text[start:end].splitlines()) + '\n'
api_probe = json.loads((A / 'mac-array-reproduction.json').read_text())
assert body == api_probe['exactExtractedLines']
assert digest(workflow.read_bytes()) == api_probe['workflowSha256']
input_head = git('rev-parse', 'HEAD')
source = '886b55e1cf88f3f696334bd5e7b8c374946a594d'
hosted_source = '518f4b51e251edaa6b5664f71c7171bde57bafc9'
assert git('diff', '--name-only', source, '--', '.', ':!tickets') == ''
assert git('diff', '--name-only', source, hosted_source, '--', '.', ':!tickets') == ''
history = (T / 'code-review-revision-record.md').read_bytes()
paths = [N / 'TESTING.md', N / '.github/workflows/release-nfs.yml', N / 'scripts/tests/test_nfs_release_workflow.py']
paths += [T / name for name in ['requirements-doc.md', 'design-spec.md', 'implementation-handoff.md', 'code-review-report.md', 'code-review-revision-record.md', 'api-e2e-coverage-investigation.md', 'api-e2e-execution-coverage-report.md', 'api-e2e-test-case-ledger.md', 'api-e2e-revision-record.md']]
paths += [A / name for name in ['failure-summary.json', 'hosted-final.json', 'hosted-job-117628928559.log', 'hosted-job-117628928627.log', 'mac-array-reproduction.json', 'post-run-remote.json']]
untracked = git('ls-files', '--others', '--exclude-standard').splitlines()
delivery = [p for p in untracked if p.startswith('tickets/in-progress/nfs-first-release/') and ('/delivery-evidence/' in p or Path(p).name in ['delivery-revision-record.md', 'docs-sync-report.md', 'handoff-summary.md', 'release-deployment-report.md'])]
inputs = {
    'head': input_head, 'source': source, 'hosted_source': hosted_source,
    'branch': git('branch', '--show-current'),
    'source_same_since_review': True,
    'scoped_files': {str(p.relative_to(N)): digest(p.read_bytes()) for p in paths},
    'delivery_owned_untracked': {p: digest((N / p).read_bytes()) for p in delivery},
    'history_bytes': len(history), 'history_sha256': digest(history),
    'prior_report_commit': 'c1f1330b8310bfadf772cebb09d085821be8da92',
    'source_line_start': text[:start].count('\n') + 1,
    'workflow_sha256': digest(workflow.read_bytes()),
}
(E / 'input-audit.json').write_text(json.dumps(inputs, indent=2) + '\n')
prior = json.loads((T / 'code-review-evidence/crr-001/input-audit.json').read_text())
assert all(digest((N / name).read_bytes()) == sha for name, sha in prior['inputs'].items())
run = json.loads((A / 'hosted-final.json').read_text())
r = run['run']
assert r['id'] == 39111348848 and r['head_sha'] == hosted_source and r['run_attempt'] == 1 and r['conclusion'] == 'failure'
jobs = [{k: j[k] for k in ['id', 'name', 'status', 'conclusion']} for j in run['jobs']['jobs']]
excerpts = {}
for job in [117628928559, 117628928627]:
    lines = (A / f'hosted-job-{job}.log').read_text().splitlines()
    excerpts[str(job)] = [{'line': idx + 1, 'text': line} for idx, line in enumerate(lines) if any(s in line for s in ['shell: /bin/bash', 'MODE: candidate', 'TARGET: darwin', 'unbound variable', 'Process completed with exit code'])]
    assert any('args[@]: unbound variable' in item['text'] for item in excerpts[str(job)])
(E / 'hosted-evidence-review.json').write_text(json.dumps({'run': {k: r[k] for k in ['id', 'head_sha', 'event', 'status', 'conclusion', 'run_attempt', 'html_url']}, 'jobs': jobs, 'mac_excerpts': excerpts, 'hosted_bash_version': 'Not printed; do not infer it from local version'}, indent=2) + '\n')
probe = 'set -euo pipefail\npython3() { printf "COMMAND_ENTERED\\n"; printf "<%s>\\n" "$@"; }\n' + body
(E / 'exact-snippet.sh').write_text(probe)
scratch = Path(tempfile.mkdtemp(prefix='nfs-release-crr002-'))
rows = []
try:
    version = subprocess.check_output(['/bin/bash', '--version'], text=True).splitlines()[0]
    for target in ['darwin-arm64', 'darwin-amd64']:
        for mode in ['candidate', 'fresh']:
            home = scratch / (target + '-' + mode)
            home.mkdir(mode=0o700)
            env = {'PATH': '/usr/bin:/bin', 'HOME': str(home), 'TMPDIR': str(home), 'MODE': mode, 'TARGET': target, 'TAG': 'v0.1.0', 'image': 'inert-metadata-control'}
            argv = ['/bin/bash', '-e', str(E / 'exact-snippet.sh')]
            p = subprocess.run(argv, env=env, cwd=home, capture_output=True, text=True, timeout=20)
            entered = p.stdout.startswith('COMMAND_ENTERED\n')
            expected = p.returncode == (1 if mode == 'candidate' else 0) and entered == (mode == 'fresh')
            if mode == 'candidate': expected = expected and 'args[@]: unbound variable' in p.stderr
            else: expected = expected and '<--qualified>\n<--candidate>\n<work/candidate>\n' in p.stdout
            row = {'argv': argv, 'shell_version': version, 'target_env': target, 'mode': mode, 'exit': p.returncode, 'command_entered': entered, 'stdout': p.stdout, 'stderr': p.stderr, 'expected_observation': expected}
            rows.append(row)
            assert expected
finally:
    shutil.rmtree(scratch)
    (E / 'reproduction.json').write_text(json.dumps({'workflow_sha256': inputs['workflow_sha256'], 'exact_source_lines': body, 'rows': rows, 'scratch': str(scratch), 'scratch_absent': not scratch.exists(), 'scope': 'Local system shell; TARGET is only an environment value. No amd64 execution or hosted rerun. Inert python boundary; no metadata, engine, signing or NFS execution.'}, indent=2) + '\n')
assert all(digest(p.read_bytes()) == inputs['scoped_files'][str(p.relative_to(N))] for p in paths)
assert all(digest((N / p).read_bytes()) == sha for p, sha in inputs['delivery_owned_untracked'].items())
(E / 'checks-and-cleanup.json').write_text(json.dumps({'result': 'Confirmed implementation failure', 'source_inputs_unchanged': len(prior['inputs']), 'scoped_files_unchanged': len(paths), 'delivery_owned_files_unchanged': len(delivery), 'probe_observations': len(rows), 'scratch_absent': not scratch.exists(), 'durable_or_production_edits': False, 'hosted_dispatch_or_remote_mutations': False, 'resource_effects': 'Own temporary directories only; no network, secrets, mounts, VM, container or user data'}, indent=2) + '\n')
print(json.dumps({'source_line_start': inputs['source_line_start'], 'shell_version': version, 'observations': [(x['target_env'], x['mode'], x['exit'], x['command_entered']) for x in rows], 'cleanup': not scratch.exists(), 'delivery_files_preserved': len(delivery)}, indent=2))
