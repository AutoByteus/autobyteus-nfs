from pathlib import Path
import subprocess,os,json,hashlib,shutil,datetime
E=Path(__file__).resolve().parent
roots=[Path((E/name).read_text().strip()) for name in ['scratch-path.txt','consumer-scratch-path.txt','standalone-final-root.txt']]
assert [p.name.split('-')[:3] for p in roots]==[['nfs','extract','ir001'],['nfs','consumer','ir001'],['nfs','extract','ir001']]
assert all(p.is_dir() and not p.is_symlink() for p in roots)
processes=subprocess.check_output(['ps','-axo','pid,ppid,command'],text=True)
active=[line for line in processes.splitlines() if any(str(p) in line or str(p.resolve()) in line for p in roots)]
assert not active,active
out={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'ownedActiveBefore':active,'resources':'No VM/container/mount/export/credential/provider actions; owned Guide browser and Nuxt already stopped','roots':[]}
# Capture versions before deleting owned tools.
env=dict(os.environ,HOME=str(roots[1]/'home'),TMPDIR=str(roots[1]/'tmp'),PATH='/Users/normy/.nvm/versions/node/v22.21.1/bin:/opt/homebrew/bin:/usr/bin:/bin')
versions={}
for name,cmd in [('node',['node','--version']),('pnpm',['pnpm','--version']),('python',['python3','--version']),('go',[str(roots[0]/'tools/go/bin/go'),'version']),('actionlint',['actionlint','--version'])]:
 r=subprocess.run(cmd,cwd=roots[1]/'repo',env=env,capture_output=True,text=True);versions[name]={'exit':r.returncode,'output':r.stdout+r.stderr}
(E/'final-toolchain.json').write_text(json.dumps(versions,indent=2)+'\n')
# These three scripts are from this implementation; all other /tmp/r2* files belong elsewhere.
scripts=E/'editing-attempts';scripts.mkdir(exist_ok=True);out['temporaryEditors']=[]
for name in ['r2-tests.py','r2-test-cleanup.py','r2-fixture-docs.py']:
 p=Path('/tmp')/name;data=p.read_bytes()
 assert b'extract-autobyteus-nfs' in data
 shutil.copy2(p,scripts/name);p.unlink()
 out['temporaryEditors'].append({'path':str(p),'sha256':hashlib.sha256(data).hexdigest(),'removed':not p.exists()})
for p in roots:
 shutil.rmtree(p);out['roots'].append({'path':str(p),'removed':not p.exists()})
out['protected']={}
for row in json.loads((E/'input-audit.json').read_text())['pm']+json.loads((E/'input-audit.json').read_text())['retainedEngine']:
 out['protected'][row['path']]=hashlib.sha256(Path(row['path']).read_bytes()).hexdigest()==row['sha256']
assert all(out['protected'].values())
out['D0Status']=subprocess.check_output(['git','-C','/Users/normy/autobyteus_org/autobyteus-nfs','status','--short'],text=True)
out['result']='Complete for enumerated task-owned resources; unrelated scratch/assets/worktrees preserved'
(E/'cleanup.json').write_text(json.dumps(out,indent=2)+'\n')
print(out['result'])
