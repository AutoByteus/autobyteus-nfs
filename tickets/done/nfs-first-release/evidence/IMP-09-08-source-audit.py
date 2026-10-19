"""IMP-09-08; 2026-10-19; read-only source, ownership and cleanup audit.
Command: PYTHONDONTWRITEBYTECODE=1 python3 tickets/done/nfs-first-release/evidence/IMP-09-08-source-audit.py
Source commit recorded in result; no remote or candidate/payload mutation.
"""
import ast
import datetime
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys

N=Path(__file__).resolve().parents[4];E=Path(__file__).resolve().parent
sys.path.insert(0,str(N/'packaging'))
from release_support import identity as i, recovery

BASE='630cc997eddbd936002d14123a3702973112fc38'
P='238bdc183e8affac99ffdee9be9cb333b0eb126f'
SOURCE='4c665e0eb23adf1f9bb45363a496b7786e76b138'
T='tickets/done/nfs-first-release/'
def git(*args):return subprocess.check_output(['git',*args],cwd=N)
def blob(commit,name):return git('show',commit+':'+name)
changed=git('diff','--name-only',BASE,SOURCE).decode().splitlines()
assert all(n in recovery.REPAIR_PATHS|recovery.GUIDES|recovery.TESTS for n in changed)
allowed=recovery.scope(N,P,SOURCE,'v0.1.0',True)
assert all(n in allowed for n in changed)
assert not (N/'packaging/recovery').exists(), 'Implementation must not create actual authorization'
assert not git('diff',P,SOURCE,'--','internal','cmd','go.mod','scripts/public','packaging/engine',
               'packaging/sign-macos.sh','packaging/release-lock.json','packaging/releases','LICENSE','CLA.md','THIRD_PARTY_NOTICES')
old_identity=ast.parse(blob(P,'packaging/release_support/identity.py'))
new_identity=ast.parse((N/'packaging/release_support/identity.py').read_text())
def selected(tree):
    return [ast.dump(n,include_attributes=False) for n in tree.body if
            isinstance(n,ast.FunctionDef) and n.name=='source_hash' or
            isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SOURCES' for t in n.targets)]
assert selected(old_identity)==selected(new_identity)
unused=[];sizes={}
for name in changed:
    if not name.endswith('.py'):continue
    text=(N/name).read_text();tree=ast.parse(text)
    loads={n.id for n in ast.walk(tree) if isinstance(n,ast.Name) and isinstance(n.ctx,ast.Load)}
    for node in ast.walk(tree):
        if isinstance(node,(ast.Import,ast.ImportFrom)):
            for alias in node.names:
                local=alias.asname or (alias.name.split('.')[0] if isinstance(node,ast.Import) else alias.name)
                if local not in loads:unused.append({'path':name,'line':node.lineno,'binding':local})
    if name.startswith('packaging/'):
        sizes[name]=sum(bool(line.strip()) for line in text.splitlines())
assert not unused,unused
assert max(sizes.values())<=500
for name in ('implementation-revision-record.md',):
    assert (N/T/name).read_bytes().startswith(blob(BASE,T+name))
for name in ('requirements-doc.md','approval-record-sr004.md','design-spec.md','investigation-notes.md',
             'solution-design-handoff.md','solution-revision-record.md','design-review-report.md',
             'architecture-review-revision-record.md','code-review-report.md','code-review-revision-record.md',
             'api-e2e-execution-coverage-report.md','api-e2e-revision-record.md',
             'handoff-summary.md','docs-sync-report.md','release-deployment-report.md','delivery-revision-record.md','release-notes.md'):
    assert (N/T/name).read_bytes()==blob(BASE,T+name),name
result={'check':'IMP-09-08','command':__doc__.splitlines()[1],
        'date':datetime.datetime.now(datetime.timezone.utc).isoformat(),'commit':SOURCE,'environment':platform.platform(),
        'result':'pass','classification':'Large/High confirmed; SR005/ARCH003 boundary preserved',
        'changedNonTicketPaths':changed,'unusedLocalImports':unused,'sourceNonemptyLines':sizes,
        'sizePressure':'publication.py delta306 additions/135 deletions (>220) assessed: source projection and admission split into designed owners; draft/effect sequencing remains one publication owner below500. No further framework/split warranted.',
        'unchanged':'runtime, installed metadata schema, installer, engine recipe/pins, signer, original lock/releases, licenses; source_hash algorithm/SOURCES AST identical',
        'otherOwnerAuthoritiesUnchanged':True,'priorIR001to008PrefixPreserved':True,'realRecoveryAuthorizationAbsent':True,
        'sourceHash':i.source_hash(),
        'priorRevisionSha256':hashlib.sha256(blob(BASE,T+'implementation-revision-record.md')).hexdigest(),
        'remoteFreshness':'Not queried this round; DR013 remains last actual remote observation',
        'limits':'Static local audit, not fresh API/hosted/publication or user verification.'}
(E/'IMP-09-08-source-audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
