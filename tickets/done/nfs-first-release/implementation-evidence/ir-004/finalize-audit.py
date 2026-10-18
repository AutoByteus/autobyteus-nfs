"""Verify bounded source delta, checks and protected-owner preservation before handoff."""
import ast
import hashlib
import json
import subprocess
from pathlib import Path

E = Path(__file__).resolve().parent
R = E.parents[4]
T = E.parent.parent

def git(*args):
    return subprocess.check_output(['git', *args], cwd=R)

def sha(data):
    return hashlib.sha256(data).hexdigest()

a = json.loads((E/'input-audit.json').read_text())
source_commit = (E/'source-commit.txt').read_text().strip()
expected = {'packaging/engine/manifest.py': 'LOCK',
            'scripts/tests/nfs_release_fixture.py': 'readiness'}
inventory = json.loads((E/'source-inputs.json').read_text())
assert len(inventory) == 120
assert all(sha((R/p).read_bytes()) == h for p,h in inventory.items())
delta = {p for p,h in inventory.items() if h != a['sourceInputs'][p]}
assert delta == set(expected)
committed_delta = set(git('diff', '--name-only', a['head'], source_commit).decode().splitlines())
assert committed_delta == set(expected)
for p,binding in expected.items():
    before = ast.parse(git('show', a['head']+':'+p))
    for node in ast.walk(before):
        if isinstance(node, ast.ImportFrom):
            node.names = [name for name in node.names if (name.asname or name.name) != binding]
    assert ast.dump(before) == ast.dump(ast.parse((R/p).read_bytes()))
assert all(sha((R/p).read_bytes()) == h for p,h in a['protectedUntracked'].items())
assert len(a['protectedUntracked']) == 16
tracked = set(git('ls-files').decode().splitlines())
assert not (set(a['protectedUntracked']) & tracked)
history_path = str((T/'implementation-revision-record.md').relative_to(R))
history_before = git('show', a['head']+':'+history_path)
assert sha(history_before) == a['priorHistorySha256']
assert (R/history_path).read_bytes().startswith(history_before)
assert (E/'prior-implementation-handoff-ir003.md').read_bytes() == git('show', a['head']+':'+str((T/'implementation-handoff.md').relative_to(R)))
allowed = set(expected) | {history_path, str((T/'implementation-handoff.md').relative_to(R))}
for p in git('diff', '--name-only', a['head']).decode().splitlines():
    assert p in allowed or p.startswith(str(E.relative_to(R))+'/'), p
checks = json.loads((E/'checks-result.json').read_text())
assert all(check['passed'] for check in checks)
cleanup = json.loads((E/'cleanup.json').read_text())
assert cleanup['absent'] and not Path(cleanup['ownedScratch']).exists()
assert json.loads((E/'unused-imports.json').read_text())['after'] == []
log = (E/'python-all.log').read_text()
assert 'Ran 45 tests' in log and 'OK (skipped=1)' in log
subprocess.run(['git','diff','--check'], cwd=R, check=True)
manifest_lines = sum(bool(line.strip()) for line in (R/'packaging/engine/manifest.py').read_text().splitlines())
assert manifest_lines < 500
result = {
    'result': 'Pass — bounded implementation self-check, not independent review/API',
    'inputHead': a['head'], 'sourceCommit': source_commit,
    'currentSourceInputs': len(inventory), 'exactChangedSourceInputs': sorted(delta),
    'other118InputsUnchanged': True, 'otherASTIdentical': True,
    'protectedDeliveryUntrackedFiles': 16, 'protectedHashesUnchangedAndNotTracked': True,
    'priorImplementationHistoryBytePrefixPreserved': True,
    'priorHandoffSnapshotExact': True, 'unexpectedTrackedDelta': [],
    'localChecksPassed': True, 'pythonCollected': 45, 'pythonExecuted': 44,
    'pythonSkipped': 1, 'skip': 'standalone Go-child fixture; no new Go parent run',
    'manifestEffectiveNonEmptyLines': manifest_lines,
    'hashTransition': json.loads((E/'hash-transition.json').read_text()),
    'ownedScratchAbsent': True, 'noRemoteOrLiveActions': True,
    'classification': {'task_size': 'Large', 'architectural_risk': 'High'},
    'remaining': 'Targeted source review; new complete current-source hosted candidate and affected API; actual signed release/public receipts remain outstanding.'
}
(E/'final-checks.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
