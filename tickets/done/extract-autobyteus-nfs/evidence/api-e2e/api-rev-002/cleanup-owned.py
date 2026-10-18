from common import *
import hashlib,shutil
P=Path(json.loads((E/'environment.json').read_text())['S']);R=P/'repo'
event('E02','Started','Verify exact assigned inputs/protected data and process quiescence before removing own archive')
assert P.parent==Path('/Users/normy') and P.name.startswith('nfs-extract-api002-S-') and P.resolve()==P
hashof=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
audit=json.loads((E/'input-audit.json').read_text());checks={}
for label,root in [('N',N),('S',S)]:
 mismatch=[p for p,h in audit[label]['paths'] if not (root/p).is_file() or hashof(root/p)!=h]
 checks[label]=dict(inputs=len(audit[label]['paths']),mismatches=mismatch);assert not mismatch
copy_mismatch=[p for p,h in audit['S']['paths'] if not (R/p).is_file() or hashof(R/p)!=h]
fixtures=json.loads((E/'fixture-inputs.json').read_text())['files']
fixture_mismatch=[f['path'] for f in fixtures if hashof(S/f['path'])!=f['sha256'] or hashof(R/f['path'])!=f['sha256']]
protected=json.loads((E/'protected-inputs.json').read_text())
protected_mismatch=[f['path'] for f in protected['files'] if hashof(Path(f['path']))!=f['sha256']]
ps=subprocess.check_output(['ps','-axo','pid,ppid,command'],text=True)
processes=[l for l in ps.splitlines() if str(P) in l]
cwd=subprocess.run(['/usr/sbin/lsof','-n','-P','-a','-d','cwd','-Fpn'],capture_output=True,text=True)
owned_cwds=[l for l in cwd.stdout.splitlines() if l.startswith('n') and (l[1:]==str(P) or l[1:].startswith(str(P)+'/'))]
D0=Path('/Users/normy/autobyteus_org/autobyteus-nfs')
d0_head=subprocess.run(['git','-C',str(D0),'rev-parse','--verify','HEAD'],capture_output=True,text=True).returncode
d0_branch=subprocess.check_output(['git','-C',str(D0),'symbolic-ref','HEAD'],text=True).strip()
result=dict(source=checks,copy_mismatches=copy_mismatch,fixture_count=len(fixtures),fixture_mismatches=fixture_mismatch,protected_count=len(protected['files']),protected_mismatches=protected_mismatch,owned_processes=processes,owned_cwds=owned_cwds,D0_head_exit=d0_head,D0_branch=d0_branch)
write('cleanup-preflight.json',result)
assert not any([copy_mismatch,fixture_mismatch,protected_mismatch,processes,owned_cwds])
assert d0_head==protected['D0_head'] and d0_branch==protected['D0_branch']
shutil.rmtree(P)
result.update(scratch=str(P),scratch_absent=not P.exists(),removed='Only API002-owned source/dependencies/builds/home/tmp/store; no assigned worktree or other owner resource',pass_=True)
write('cleanup.json',result)
event('E02','Completed','Owned S archive removed; no owned process/cwd;108 N/7307 S +11 replay inputs and protected PM/engine unchanged','Pass','cleanup.json; cleanup-preflight.json')
