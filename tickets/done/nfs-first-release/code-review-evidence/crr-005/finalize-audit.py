"""Verify review-only changes, history/preservation, raw-log exceptions and cleanup."""
import hashlib
import json
from pathlib import Path
import subprocess

E = Path(__file__).resolve().parent
R = E.parents[4]
T = E.parent.parent
A = json.loads((E / 'input-audit.json').read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(name, value):
    (E / name).write_text(json.dumps(value, indent=2) + '\n')


updates = {(T / n).relative_to(R).as_posix() for n in ('code-review-report.md', 'code-review-revision-record.md')}
for name, digest in A['source_inputs'].items():
    assert sha(R / name) == digest, name
protected = {p: h for p, h in A['protected_ticket_inputs'].items() if p not in updates}
for name, digest in protected.items():
    assert sha(R / name) == digest, name
for name, digest in A['delivery_untracked'].items():
    assert sha(R / name) == digest, name
tracked = set(subprocess.check_output(['git', 'ls-files'], cwd=R).decode().splitlines())
assert not tracked.intersection(A['delivery_untracked'])
history = (T / 'code-review-revision-record.md').read_bytes()
assert hashlib.sha256(history[:A['history_bytes']]).hexdigest() == A['history_sha256']
report = (T / 'code-review-report.md').read_text()
structural = report.split('## Structural / Design Checks\n')[1].split('\n## ')[0]
score = report.split('## Review Scorecard\n')[1].split('\n## ')[0]
assert sum(line.startswith('| ') for line in structural.splitlines()) - 2 == 24
assert sum(line.startswith('| ') for line in score.splitlines()) - 2 == 10
assert '| Fail |' not in structural
assert sum('| 10.0 |' in line for line in score.splitlines()) == 10
cleanup = json.loads((E / 'cleanup.json').read_text())
assert cleanup['removed'] and not Path(cleanup['scratch']).exists()
checks = json.loads((E / 'checks-result.json').read_text())['commands']
assert len(checks) == 6 and all(c['exit_code'] == c['expected_exit'] for c in checks)
whitespace = []
for path in sorted(E.iterdir()) + [T / 'code-review-report.md', T / 'code-review-revision-record.md']:
    if not path.is_file():
        continue
    text = path.read_text()
    lines = [i for i, line in enumerate(text.splitlines(), 1) if line.rstrip() != line]
    eof = text.endswith('\n\n')
    if lines or eof:
        assert path.suffix in ('.log', '.diff'), str(path)
        whitespace.append({'path': path.relative_to(R).as_posix(), 'sha256': sha(path),
                           'trailing_whitespace_lines': lines, 'blank_line_at_eof': eof,
                           'disposition': 'Preserve exact raw output/diff context, not source formatting.'})
write('artifact-whitespace.json', {'exceptions': whitespace, 'nonraw_violations': []})
write('final-checks.json', {
    'review': 'CRR-005', 'entry': 'Implementation Review / Targeted Delta Review',
    'result': 'Pass', 'source_score': 100, 'open_findings': [],
    'resolved_findings': ['CR-002'], 'prior_resolved_retained': ['CR-001'],
    'basis': 'R3/SR004 Approved / SR004 Ready / ARCH002',
    'source_commit': A['source_commit'], 'source_inputs_unchanged': len(A['source_inputs']),
    'protected_prior_ticket_unchanged': len(protected),
    'delivery_untracked_unchanged_unstaged': len(A['delivery_untracked']),
    'prior_history_prefix_unchanged_bytes': A['history_bytes'],
    'intentional_canonical_updates': sorted(updates),
    'review_document_hashes': {n: sha(T / n) for n in ('code-review-report.md', 'code-review-revision-record.md')},
    'structural_checks': 24, 'score_categories': 10, 'scope': 'Standalone NFS only',
    'current_commands': len(checks), 'python_collected': 45, 'python_executed': 44, 'python_skips': 1,
    'current_source_hash': (E / 'source-hash.log').read_text().strip(),
    'current_recipe_hash': (E / 'recipe-hash.log').read_text().strip(),
    'scratch_removed': True, 'source_test_edits_by_reviewer': False,
    'remote_live_signing_release_actions': False,
    'new_current_hosted_candidate_required': True,
    'field_and_user_tests': 'Deferred, not a publication/closure prerequisite',
})
print(json.dumps({'result': 'Pass100', 'source': 120, 'protected_ticket': len(protected),
                  'delivery': 16, 'prior_history_bytes': A['history_bytes'],
                  'raw_whitespace_exceptions': len(whitespace)}))
