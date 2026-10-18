from pathlib import Path
import hashlib, json, subprocess

E = Path(__file__).resolve().parent
T = E.parent.parent
N = T.parent.parent.parent
S = Path('/Users/normy/autobyteus_org/autobyteus-worktrees/extract-autobyteus-nfs')
sha = lambda b: hashlib.sha256(b).hexdigest()
def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args])
def paths(repo):
    return git(repo, 'ls-tree', '-r', '--name-only', '-z', 'HEAD').decode().split('\0')[:-1]
def aggregate(repo, names):
    return sha(''.join(p + '\0' + sha((repo / p).read_bytes()) + '\n' for p in sorted(names)).encode())

prior = '5559abbf017566f0030d95b023614f7418d3f212'
head = '60b67dabecaf5569a8e26128dbdb26117c988811'
p = 'autobyteus-server-ts/tests/unit/agent-execution/backends/claude/backend/claude-session-bootstrapper.test.ts'
line = b'import { Skill } from "../../../../../../src/skills/domain/models.js";\n'
assert git(S, 'rev-parse', 'HEAD').decode().strip() == head
assert not git(S, 'status', '--porcelain')
assert git(S, 'diff', '--name-only', prior, head).decode().splitlines() == [p]
before = git(S, 'show', prior + ':' + p)
after = (S / p).read_bytes()
assert before.count(line) == 1 and after == before.replace(line, b'', 1)
assert after == git(S, 'show', head + ':' + p)
assert git(S, 'diff', '--numstat', prior, head).decode().strip() == '0\t1\t' + p
subprocess.run(['git', '-C', str(S), 'diff', '--check', prior, head], check=True)
domain = 'autobyteus-server-ts/src/skills/domain/models.ts'
assert (S / domain).read_bytes() == git(S, 'show', prior + ':' + domain)
unused = json.loads((E / 'unused-locals.json').read_text())
assert unused['diagnostics'] == [] and len(unused['production']) == 25 and len(unused['tests']) == 4
assert all((S / n).read_bytes() == git(S, 'show', prior + ':' + n) for n in unused['production'])
old = json.loads((E.parent / 'crr-004/source-audit.json').read_text())
identities = {}
for key, repo in [('N', N), ('S', S)]:
    names = [n for n in paths(repo) if not n.startswith('tickets/')]
    identities[key] = {'count': len(names), 'sha256': aggregate(repo, names)}
assert identities['N']['count'] == old['input_identity']['N']['paths'] == 108
assert identities['N']['sha256'] == old['input_identity']['N']['sha256']
authority = json.loads((E.parent / 'crr-002/input-audit.json').read_text())['authority_files_unchanged']
assert all(sha((T / name).read_bytes()) == h for name, h in authority.items())
ir = T / 'implementation-evidence/ir-004'
checks = json.loads((ir / 'checks-result.json').read_text())
assert len(checks) == 3 and all(c['exit'] == 0 for c in checks)
cleanup = json.loads((ir / 'cleanup.json').read_text())
assert cleanup['scratch_removed'] and not Path(cleanup['scratch']).exists()
protected = [n for n in paths(N) if n.startswith(str(T.relative_to(N)) + '/') and Path(n).name not in ['code-review-report.md', 'code-review-revision-record.md']]
result = {
    'review': 'CRR-005', 'scope': 'Targeted Delta Review',
    'N_head': git(N, 'rev-parse', 'HEAD').decode().strip(),
    'N_service': '83726b27400b405a7a6a79bd962d8e2419daa561', 'S_head': head, 'S_prior': prior,
    'changed': [p], 'exact_delta': '0 additions / 1 deletion',
    'whole_file_equals_prior_minus_import': True,
    'all_assertions_fixtures_and_domain_class_preserved': True,
    'all_25_production_owners_unchanged': True,
    'unused_diagnostics': [], 'input_identity': identities,
    'unchanged_authority_documents': len(authority),
    'IR004_checks_inspected_not_reexecuted': checks,
    'IR004_scratch_absent': True,
    'protected_ticket_inputs': {'count': len(protected), 'sha256': aggregate(N, protected)},
    'prior_history_sha256': sha((T / 'code-review-revision-record.md').read_bytes()),
    'no_source_or_test_edits_by_reviewer': True,
    'no_runtime_suite_rerun': True,
}
(E / 'delta-audit.json').write_text(json.dumps(result, indent=2) + '\n')
(E / 'source.diff').write_bytes(git(S, 'diff', prior, head, '--', p))
print(json.dumps(result, indent=2))
