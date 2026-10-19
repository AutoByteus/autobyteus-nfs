"""IMP-08-03 scope audit; command: PYTHONDONTWRITEBYTECODE=1 python3 this-file.
Input a7eb8a819c604358a5b01bd66b1fe1ffda313b19; Darwin arm64; 2026-10-19.
"""
import ast
import json
from pathlib import Path
import subprocess

R=Path(__file__).resolve().parents[4]
T=R/'tickets/done/nfs-first-release'
base='a7eb8a819c604358a5b01bd66b1fe1ffda313b19'
main='238bdc183e8affac99ffdee9be9cb333b0eb126f'
def git(*args):return subprocess.check_output(['git',*args],cwd=R,text=True).strip()
changed=git('diff','--name-only',base).splitlines()
assert changed==['tickets/done/nfs-first-release/implementation-handoff.md',
                 'tickets/done/nfs-first-release/implementation-revision-record.md']
record=T/'implementation-revision-record.md'
prior=subprocess.check_output(['git','show',base+':'+str(record.relative_to(R))],cwd=R)
assert record.read_bytes().startswith(prior)
assert git('merge-base',base,main)==main
probe=T/'evidence/IMP-08-01-recovery-probe.py'
tree=ast.parse(probe.read_text())
loads={n.id for n in ast.walk(tree) if isinstance(n,ast.Name) and isinstance(n.ctx,ast.Load)}
unused=[a.asname or a.name.split('.')[0] for n in ast.walk(tree) if isinstance(n,(ast.Import,ast.ImportFrom)) for a in n.names if (a.asname or a.name.split('.')[0]) not in loads]
assert not unused
result=json.loads((T/'evidence/IMP-08-01-recovery-probe.json').read_text())
assert result['allExpectedObservationsConfirmed'] and result['ownedScratchRemoved']
(T/'evidence/IMP-08-03-audit.json').write_text(json.dumps({'check':'IMP-08-03','command':'PYTHONDONTWRITEBYTECODE=1 python3 tickets/done/nfs-first-release/evidence/IMP-08-03-audit.py','commit':base,'environment':'Darwin arm64 read-only source audit','date':'2026-10-19','productionUnchanged':True,'changedTrackedPaths':changed,'priorHistoryPrefixPreserved':True,'finalizedMainAncestor':True,'unusedProbeImports':unused,'ownedScratchRemoved':True,'remoteOrSigningActions':False},indent=2)+'\n')
print('IMP-08-03: production unchanged; history/main preserved; probe imports/cleanup checked')
