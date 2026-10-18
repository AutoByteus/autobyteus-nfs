from common import *
import hashlib,shutil
c=json.loads((E/'environment.json').read_text());audit=json.loads((E/'input-audit.json').read_text());protected=json.loads((E/'protected-inputs.json').read_text())
event('E02','Started','Check source/protected data and own runtime process quiescence, then remove only two API archives')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
mismatches=[]
for label in ['N','S']:
 for p,h in audit[label]['paths']:
  f=Path(audit[label]['root'])/p
  if not f.is_file() or sha(f)!=h:mismatches.append(label+':'+p)
assert not mismatches,mismatches
fixtures=json.loads((E/'fixture-restoration.json').read_text())['files']
for row in fixtures:
 assert sha(S/row['path'])==row['sha256']
 assert sha(Path(c['S'])/'repo'/row['path'])==row['sha256']

private_changes=[x['path'] for x in protected['files'] if not Path(x['path']).is_file() or sha(Path(x['path']))!=x['sha256']]
assert not private_changes,private_changes
ps=subprocess.check_output(['ps','-axo','pid=,ppid=,command='],text=True)
matches=[x for x in ps.splitlines() if any(c[label] in x for label in ['N','S'])]
write('cleanup-preflight.json',dict(source_mismatches=mismatches,protected_mismatches=private_changes,owned_process_matches=matches))
assert not matches,'Owned paths still referenced by processes; inspect before cleanup'
result=[]
for label in ['N','S']:
 p=Path(c[label])
 assert p.parent==Path('/Users/normy') and p.name.startswith('nfs-extract-api001-'+label+'-') and not p.is_symlink()
 shutil.rmtree(p)
 result.append(dict(path=str(p),removed=not p.exists()))
# no source ticket authorities changed; only API-owned area may be dirty
status={}
for label,root in [('N',N),('S',S)]:status[label]=subprocess.check_output(['git','-C',str(root),'status','--porcelain'],text=True)
d0=Path('/Users/normy/autobyteus_org/autobyteus-nfs')
head=subprocess.run(['git','-C',str(d0),'rev-parse','--verify','HEAD'],capture_output=True,text=True)
branch=subprocess.check_output(['git','-C',str(d0),'symbolic-ref','HEAD'],text=True).strip()
assert head.returncode==protected['D0_head'] and branch==protected['D0_branch']
write('cleanup.json',dict(removed=result,source_inputs_verified={x:len(audit[x]['paths']) for x in ['N','S']},source_mismatches=[],protected_files_verified=len(protected['files']),protected_changes=[],D0_unborn_main_unchanged=True,owned_process_matches=[],source_status=status,live_resource_actions='None; no VM/Docker/mount/user app/provider actions',shared_tool_cache_actions='None; tools/node_modules/cache/generated output removed only within owned archives'))
event('E02','Completed','Both API scratch roots removed; 108 N/7215 S source inputs and nine protected PM/engine files unchanged; no owned process remains','Pass','cleanup.json; cleanup-preflight.json')
