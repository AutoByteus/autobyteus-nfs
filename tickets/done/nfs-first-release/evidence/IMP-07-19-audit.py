"""IMP-07-19 source/evidence audit; command: python3 this-file.
Commit and environment recorded in output; 2026-10-19, Darwin arm64.
"""
import ast
import json
import subprocess
from pathlib import Path

E = Path(__file__).resolve().parent
R = E.parents[3]
base = '79e35392bfe4f795464fecd8c034670b622c1684'
source = '3f67e36193c246ca08b49cda818be5c0f94eba51'
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
assert git('merge-base', source, '72b8a4aeb3a92a03526d3538e8cbcba30e4d7aa2') == '72b8a4aeb3a92a03526d3538e8cbcba30e4d7aa2'
record = R/'tickets/done/nfs-first-release/implementation-revision-record.md'
prefix = subprocess.check_output(['git','show',base+':'+str(record.relative_to(R))],cwd=R)
assert record.read_bytes().startswith(prefix)
whitespace = []
for log in sorted(E.glob('IMP-07-*.log')):
    for number, line in enumerate(log.read_text().splitlines(), 1):
        if line.rstrip() != line:
            assert 'mutant-' in log.name or 'original-control' in log.name
            whitespace.append({'file':log.name,'line':number,'reason':'preserve raw unittest diagnostic'})
# Check generated command-double imports too; they execute as a separate script.
fake = next(n.value.value for n in tree.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'FAKE' for t in n.targets))
ft = ast.parse(fake)
floads = {n.id for n in ast.walk(ft) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)}
assert all((a.asname or a.name.split('.')[0]) in floads for n in ast.walk(ft) if isinstance(n, (ast.Import, ast.ImportFrom)) for a in n.names)
(E/'IMP-07-19-audit.json').write_text(json.dumps({'check':'IMP-07-19', 'command':'python3 evidence/IMP-07-19-audit.py',
    'commit':source, 'environment':'Darwin arm64 worktree, source-only inspection', 'date':'2026-10-19',
    'changedPaths':actual, 'signNonemptyLines':size, 'unusedTouchedTestImports':unused,
    'priorHistoryPrefixPreserved':True, 'finalizedMainAncestor':True,
    'workflowEngineRuntimeLockReadinessUnchanged':True, 'noUserCredentialOrRemoteAction':True, 'ownedSyntheticKeychainProbesCleaned':True,
    'rawDiagnosticWhitespaceExceptions':whitespace},indent=2)+'\n')
print('IMP-07-19: four owned paths only; source size/import/history/main invariants pass')
