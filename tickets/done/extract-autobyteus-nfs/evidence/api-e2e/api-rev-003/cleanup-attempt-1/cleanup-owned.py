from common import *
import shutil
cfg=json.loads((E/'environment.json').read_text());P=Path(cfg['scratch']);name=cfg['container'];audit=json.loads((E/'input-audit.json').read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
event('E02','Started','Confirm source/protected-state exactness and native quiescence, then remove only API003-owned resources')
source_mismatch=[str(root/p) for root in [N,P/'candidate'] for p,h in audit['inputs'].items() if sha(root/p)!=h]
protected_mismatch=[p for p,h in audit['protected_ticket'].items() if sha(N/p)!=h]
cache_mismatch=[p for p,h in audit['ignored_cache'].items() if sha(N/p)!=h]
pm_mismatch=[p for p,h in audit['PM'].items() if sha(Path(p))!=h]
D0=Path('/Users/normy/autobyteus_org/autobyteus-nfs');d0={k:subprocess.check_output(['git','-C',str(D0),*v],text=True).strip() for k,v in [('head',['rev-parse','HEAD']),('branch',['symbolic-ref','HEAD'])]}
assert d0==audit['D0'];assert not Path('/Users/normy/autobyteus_org/autobyteus-worktrees/extract-autobyteus-nfs').exists()
assert not any([source_mismatch,protected_mismatch,cache_mismatch,pm_mismatch])
# Recheck the candidate inside the container after mutated copies ran elsewhere.
run('linux-final-inputs',['docker','exec','--user','1001:1001',name,'python3','-c',"import pathlib,hashlib,json; root=pathlib.Path('/home/checker/candidate'); expected="+repr(audit['inputs'])+"; bad=[p for p,h in expected.items() if hashlib.sha256((root/p).read_bytes()).hexdigest()!=h]; print(json.dumps({'inputs':len(expected),'mismatches':bad})); assert not bad"],P)
inspection=json.loads(subprocess.check_output(['docker','inspect',name]))[0]
created=json.loads((E/'container.json').read_text())['details'][0]
assert inspection['Id']==created['Id'] and inspection['Config']['Labels']['autobyteus.validation']=='api003'
proc=subprocess.check_output(['docker','exec',name,'ps','-eo','pid,user,args'],text=True);(E/'linux-final-processes.log').write_text(proc)
assert not any('checker' in l for l in proc.splitlines()),proc
run('remove-container',['docker','rm','-f',name],P)
left=subprocess.run(['docker','inspect',name],capture_output=True,text=True);assert left.returncode!=0
ps=subprocess.check_output(['ps','-axo','pid,ppid,command'],text=True);owned=[l for l in ps.splitlines() if str(P) in l];assert not owned,owned
cwd=subprocess.run(['/usr/sbin/lsof','-a','-d','cwd','-Fn'],capture_output=True,text=True);owned_cwd=[l for l in cwd.stdout.splitlines() if l.startswith('n'+str(P))];assert cwd.returncode==0 and not owned_cwd
result=dict(inputs=108,source_mismatches=source_mismatch,protected_ticket_count=len(audit['protected_ticket']),protected_ticket_mismatches=protected_mismatch,ignored_cache_mismatches=cache_mismatch,PM_count=len(audit['PM']),PM_mismatches=pm_mismatch,D0=d0,S_still_retired=True,owned_host_processes=owned,owned_host_cwds=owned_cwd,container=name,container_id=created['Id'],container_removed=True,immutable_base_image='Shared immutable cache retained; not a built/published image',scratch=str(P))
write('cleanup-preflight.json',result)
assert P.parent==Path('/Users/normy') and P.name.startswith('nfs-extract-api003-') and P.resolve()==P
shutil.rmtree(P);result.update(scratch_removed=not P.exists(),pass_=True);write('cleanup.json',result)
event('E02','Completed','Own container/archive/toolchains/caches removed;108 inputs +535 upstream artifacts +PM/ignored cache preserved; D0 populated main unchanged, S retired','Pass','cleanup.json; cleanup-preflight.json; linux-final-inputs.log; linux-final-processes.log')
event('N01-linux','Clarification','Focused Linux selector executed30 hosted-config pass records; extra no-live-source-detach case is Darwin-only (31 there), not Linux coverage','N/A','test-counts.json; linux-focused.log; darwin-focused.log')
