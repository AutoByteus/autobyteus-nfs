from pathlib import Path
import subprocess,json,hashlib,shutil
E=Path(__file__).resolve().parent;N=E.parents[4];P=Path((E/'scratch-path.txt').read_text().strip())
input_data=json.loads((E/'candidate-inputs.json').read_text())
mismatch=[]
for f in input_data['files']:
 for root in [N,P/'candidate']:
  if hashlib.sha256((root/f['path']).read_bytes()).hexdigest()!=f['sha256']:mismatch.append(str(root/f['path']))
assert not mismatch
changed=subprocess.check_output(['git','-C',str(N),'diff','--name-only','56c0c59efdd3b963b2fc11ba07bda7410b4067b2','HEAD'],text=True).splitlines()
assert changed==['internal/setup/hosted_config_test.go'],changed
for osname in ['linux','darwin']:
 r=json.loads((E/(osname+'-checks-result.json')).read_text());assert all(x['exit']==x['expected_exit'] for x in r)
assert all(x['expected_failure'] for x in json.loads((E/'mutation-results.json').read_text()))
initial=json.loads((E/'input-audit.json').read_text())
for x in initial['ignored_pycache']:
 assert hashlib.sha256((N/x['path']).read_bytes()).hexdigest()==x['sha256']
for x in initial['files']:
 assert hashlib.sha256((E.parent.parent/x['path']).read_bytes()).hexdigest()==x['sha256']
audit=dict(candidate=input_data['commit'],changed_paths=changed,production_unchanged=True,workflow_unchanged=True,config_safety_unchanged=True,source_copy_inputs=len(input_data['files']),mismatches=mismatch,source_hash_unchanged=initial['source_hash'],preexisting_ignored_cache_unchanged=True,S_impact='None; worktree not recreated',target_operations='No fetch/merge/push/reset; completed DR002 paired pushes preserved',initial_handoff_history_sha256=next(x['sha256'] for x in initial['files'] if x['path']=='implementation-revision-record.md'))
(E/'source-audit.json').write_text(json.dumps(audit,indent=2)+'\n')
(E/'source.diff').write_bytes(subprocess.check_output(['git','-C',str(N),'diff','--unified=3','56c0c59','HEAD','--','internal/setup/hosted_config_test.go']))
name=json.loads((E/'linux-container.json').read_text())['name']
# Snapshot nonroot process inventory before removing only the owned development container.
proc=subprocess.check_output(['docker','exec',name,'ps','-eo','pid,user,args'],text=True)
(E/'linux-final-processes.log').write_text(proc)
assert not any('checker' in line and ('go test' in line or 'go vet' in line) for line in proc.splitlines())
removed=subprocess.run(['docker','rm','-f',name],capture_output=True,text=True); assert removed.returncode==0,removed.stderr
left=subprocess.run(['docker','inspect',name],capture_output=True,text=True);assert left.returncode!=0
ps=subprocess.check_output(['ps','-axo','pid=,command='],text=True)
active=[l for l in ps.splitlines() if str(P) in l];assert not active,active
cwd=subprocess.run(['/usr/sbin/lsof','-a','-d','cwd','-Fn'],capture_output=True,text=True)
active_cwd=[l for l in cwd.stdout.splitlines() if l.startswith('n'+str(P))];assert cwd.returncode==0 and not active_cwd
assert P.parent==Path('/Users/normy/autobyteus_org') and P.name.startswith('nfs-extract-ir005-') and not P.is_symlink()
shutil.rmtree(P)
(E/'cleanup.json').write_text(json.dumps(dict(scratch=str(P),scratch_removed=not P.exists(),container=name,container_removed=True,host_command_matches=active,host_cwd_matches=active_cwd,immutable_base_image='Retained only as shared Docker pull cache; no built image or live resources retained',protected='D0/PM/canonical app/retained engine/ignored cache not modified or removed'),indent=2)+'\n')
print('Source integrity passed; owned container and scratch removed.')
