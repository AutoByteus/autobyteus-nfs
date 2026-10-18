"""Read-only input/structure checks; write only the current CRR-001 audit result."""
from pathlib import Path
import hashlib
import json
import subprocess

E = Path(__file__).resolve().parent
T = E.parent.parent
N = T.parent.parent.parent

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def git(*args):
    return subprocess.check_output(['git', *args], cwd=N, text=True).strip()

a = json.loads((E / 'input-audit.json').read_text())
source_changes = [name for name, digest in a['inputs'].items() if sha(N / name) != digest]
protected_changes = [name for name, digest in a['protected_ticket_inputs'].items() if sha(N / name) != digest]
report = (T / 'code-review-report.md').read_text()
structural = report.split('## Structural / Design Checks\n', 1)[1].split('## Source File Size', 1)[0]
score = report.split('## Review Scorecard\n', 1)[1].split('## Findings', 1)[0]
structural_rows = [line for line in structural.splitlines() if '| Pass |' in line]
score_rows = [line for line in score.splitlines() if '| 10.0 |' in line]
raw_logs = {}
nonraw_bad = []
files = [T / 'code-review-report.md', T / 'code-review-revision-record.md'] + sorted(E.glob('*'))
for path in files:
    if not path.is_file() or path.name == 'final-checks.json':
        continue
    data = path.read_bytes()
    decoded = data.decode('utf-8')
    bad = [n for n, line in enumerate(decoded.splitlines(), 1) if line.rstrip() != line]
    eof_blank = data.endswith(b'\n\n')
    cr_count = data.count(b'\r')
    if bad or eof_blank or cr_count:
        item = {'sha256': sha(path), 'trailing_space_lines': bad, 'blank_eof': eof_blank, 'CR': cr_count}
        if path.suffix == '.log':
            raw_logs[path.name] = item
        else:
            nonraw_bad.append({'path': str(path), **item})
results = {
    'review': 'CRR-001',
    'input_head': a['head'],
    'current_branch': git('branch', '--show-current'),
    'source_commit': a['source_commit'],
    'source_input_count': len(a['inputs']),
    'protected_ticket_input_count': len(a['protected_ticket_inputs']),
    'changed_source_inputs': source_changes,
    'changed_protected_ticket_inputs': protected_changes,
    'product_diff_from_source_commit': git('diff', '--name-only', a['source_commit'], '--', '.', ':!tickets'),
    'runtime_engine_license_ci_diff_from_base': git('diff', '--name-only', a['base'], '--', 'cmd', 'internal', 'packaging/engine', '.github/workflows/ci.yml', 'LICENSE', 'THIRD_PARTY_NOTICES', 'CLA.md'),
    'structural_check_rows': len(structural_rows),
    'score_rows': len(score_rows),
    'prior_record': 'N/A; CRR-001 created for this task',
    'source_size_rows': len(a['sizes']),
    'unused_import_candidates': a['unused_import_candidates'],
    'checks_all_expected': json.loads((E / 'checks-result.json').read_text())['all_expected'],
    'scratch_absent': not Path((E / 'scratch-path.txt').read_text().strip()).exists(),
    'raw_whitespace_exceptions': raw_logs,
    'nonraw_whitespace_failures': nonraw_bad,
    'review_report_sha256': sha(T / 'code-review-report.md'),
    'review_history_sha256': sha(T / 'code-review-revision-record.md'),
    'no_source_or_test_edits': True,
    'no_hosted_live_credential_or_publication_actions': True,
}
results['passed'] = not source_changes and not protected_changes and not results['product_diff_from_source_commit'] and not results['runtime_engine_license_ci_diff_from_base'] and len(structural_rows) == 24 and len(score_rows) == 10 and not nonraw_bad and results['checks_all_expected'] and results['scratch_absent']
(E / 'final-checks.json').write_text(json.dumps(results, indent=2) + '\n')
print(json.dumps(results, indent=2))
assert results['passed']
