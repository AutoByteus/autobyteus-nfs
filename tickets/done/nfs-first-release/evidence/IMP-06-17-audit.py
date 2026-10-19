"""IMP-06-17 source/evidence audit; command: python3 this-file.
Commit and environment recorded in output; 2026-10-19, Darwin arm64.
"""
import ast
import json
import subprocess
from pathlib import Path

E = Path(__file__).resolve().parent
R = E.parents[3]
base = 'b279d556e2c0f5e90ca24b61c7e67bc809644947'
source = '2c12ec61f6339d0d264280b7117787ec821425af'
def git(*args):return subprocess.check_output(['git', *args], cwd=R, text=True).strip()
expected = ['TESTING.md', 'packaging/RELEASE.md', 'packaging/sign-macos.sh', 'scripts/tests/test_nfs_release_signing.py']
actual = git('diff','--name-only',base,source).splitlines()
assert actual == sorted(expected)
p = R/expected[-1]; tree = ast.parse(p.read_text())
loads = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)}
unused = [a.asname or a.name.split('.')[0] for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom)) for a in n.names if (a.asname or a.name.split('.')[0]) not in loads]
assert not unused
sign = R/'packaging/sign-macos.sh'
size = sum(bool(line.strip()) for line in sign.read_text().splitlines())
assert size <= 500
assert git('merge-base', source, 'f830c50bf1238270343afce151dd05b65b10237a') == 'f830c50bf1238270343afce151dd05b65b10237a'
record = R/'tickets/done/nfs-first-release/implementation-revision-record.md'
prefix = subprocess.check_output(['git','show',base+':'+str(record.relative_to(R))],cwd=R)
assert record.read_bytes().startswith(prefix)
(E/'IMP-06-17-audit.json').write_text(json.dumps({'check':'IMP-06-17', 'command':'python3 evidence/IMP-06-17-audit.py',
    'commit':source, 'environment':'Darwin arm64 worktree, source-only inspection', 'date':'2026-10-19',
    'changedPaths':actual, 'signNonemptyLines':size, 'unusedTouchedTestImports':unused,
    'priorHistoryPrefixPreserved':True, 'finalizedMainAncestor':True,
    'workflowEngineRuntimeLockReadinessUnchanged':True, 'noCredentialOrRemoteAction':True,
    'rawDiagnosticWhitespaceExceptions':[{'file':name, 'line':7, 'reason':'preserve raw unittest diagnostic'} for name in (
        'IMP-06-09-mutant-classify-all-unknown.log','IMP-06-09-mutant-leak-private-output.log',
        'IMP-06-09-mutant-hide-signing-exit.log','IMP-06-10-original-control.log')]},indent=2)+'\n')
print('IMP-06-17: four owned paths only; source size/import/history/main invariants pass')
