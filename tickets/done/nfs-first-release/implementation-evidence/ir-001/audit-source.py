"""Read-only scope/source audit for this implementation, not product qualification."""
import ast
import hashlib
import json
from pathlib import Path
import subprocess

E=Path(__file__).resolve().parent
ROOT=E.parents[4]
BASE='2051fd9559f4f4fa7beae68723429f8199b50004'
def git(*args):
 return subprocess.check_output(['git',*args],cwd=ROOT)
def digest(data):return hashlib.sha256(data).hexdigest()
def write(name,value):(E/name).write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')
names=git('ls-files','--cached','--others','--exclude-standard').decode().splitlines()
current={name:digest((ROOT/name).read_bytes()) for name in names if not name.startswith('tickets/') and (ROOT/name).is_file()}
checked=json.loads((E/'source-inputs.json').read_text())
assert current==checked,'Current source differs from final independent native copy'
base_names=git('ls-tree','-r','--name-only',BASE).decode().splitlines()
preserved={}
for name in base_names:
 if name.startswith(('cmd/','internal/','packaging/engine/')) or name in ('LICENSE','CLA.md','LICENSING.md','THIRD_PARTY_NOTICES','go.mod','.github/workflows/ci.yml'):
  assert (ROOT/name).read_bytes()==git('show',BASE+':'+name),name
  preserved[name]=current[name]
lock=json.loads((ROOT/'packaging/release-lock.json').read_text())
old=json.loads(git('show',BASE+':packaging/release-lock.json'))
assert all(lock[k]==old[k] for k in ('ubuntuBaseImage','ubuntuPackages','engine'))
assert lock['engine'] is None and lock['qualification'] is None and lock['qualifiedTargets']==[] and lock['physicalEvidence']==[] and lock['qualifiedSourceHash']=='' and lock['userVerified'] is False
changed=[]
for name in current:
 if name not in base_names or digest(git('show',BASE+':'+name))!=current[name]:changed.append(name)
source_size={};unused=[]
for name in changed:
 p=ROOT/name
 if p.suffix=='.py':
  tree=ast.parse(p.read_text());refs={n.id for n in ast.walk(tree) if isinstance(n,ast.Name) and isinstance(n.ctx,ast.Load)}
  for node in ast.walk(tree):
   if isinstance(node,(ast.Import,ast.ImportFrom)):
    for value in node.names:
     binding=value.asname or value.name.split('.')[0]
     if binding not in refs:unused.append({'path':name,'line':node.lineno,'binding':binding})
 if not name.startswith('scripts/tests/') and p.suffix in ('.py','.sh','.yml'):
  effective=sum(bool(line.strip()) for line in p.read_text().splitlines())
  assert effective<=500,name
  source_size[name]={'nonemptyLines':effective,'newFile':name not in base_names}
assert not unused,unused
write('source-audit.json',{'base':BASE,'changed':sorted(changed),'currentInputs':len(current),'currentCopyEqual':True,'preservedInputs':preserved,'releasePinsUnchanged':True,'qualificationEmpty':True,'unusedImportBindings':unused,'unusedAuditLimit':'AST import references plus manual touched-owner inspection, not a whole-repo linter','sizes':source_size,'sizePressureDisposition':'Candidate/artifact reconciliation and remote publication each exceed220 delta; assessed as distinct cohesive owners. Final payload assembly/verification split into payload.py. Facade/identity/qualification/signing remain separate. No implementation file exceeds500 nonempty lines; tests excluded.'})
write('final-source-inputs.json',current)
# Preserve the emitted executable identities as local compile evidence, not assets.
S=Path((E/'scratch-path.txt').read_text().strip())
write('compile-identities.json',{p.name:{'sha256':digest(p.read_bytes()),'size':p.stat().st_size} for p in sorted((S/'out').iterdir()) if p.is_file()})
print('source scope/invariants/current-copy/import/size audit passed')
