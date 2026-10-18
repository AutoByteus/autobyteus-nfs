from pathlib import Path
import os,subprocess,tempfile,json,datetime,hashlib,shutil,time
E=Path(__file__).resolve().parent;N=E.parents[5];T=E.parents[2]
a=json.loads((E/'input-audit.json').read_text())
P=Path(tempfile.mkdtemp(prefix='nfs-first-api001-',dir=Path.home()));S=P/'source';S.mkdir()
for name,h in a['source'].items():
 p=S/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(N/name,p);assert hashlib.sha256(p.read_bytes()).hexdigest()==h
for name in ['home','tmp','cache']: (P/name).mkdir()
(E/'scratch.json').write_text(json.dumps(dict(path=str(P),source=str(S),owner='API001 personal local release checks',head=a['head']),indent=2)+'\n')
env={'HOME':str(P/'home'),'TMPDIR':str(P/'tmp')+'/','PATH':'/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin','LC_ALL':'C','PYTHONDONTWRITEBYTECODE':'1','XDG_CACHE_HOME':str(P/'cache')}
results=[]
def event(case,state,evidence):
 with (T/'api-e2e-test-case-ledger.md').open('a') as f:f.write('| '+datetime.datetime.now(datetime.timezone.utc).isoformat()+' | '+case+' | '+state+' | '+evidence+' |\n')
def run(name,args,expected=0):
 t=time.time()
 with (E/(name+'.log')).open('w') as f:
  f.write('$ '+' '.join(args)+'\ncwd '+str(S)+'\n');f.flush();p=subprocess.run(args,cwd=S,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=600)
 r=dict(name=name,command=args,cwd=str(S),exit=p.returncode,expected=expected,seconds=round(time.time()-t,3),passed=p.returncode==expected)
 results.append(r);(E/'local-results.json').write_text(json.dumps(results,indent=2)+'\n')
 print(name,p.returncode,flush=True)
 event('R01' if name.startswith('python-') else 'R02','Pass checkpoint' if r['passed'] else 'Fail',name+'.log')
 assert r['passed'],r
run('python-version',['/usr/bin/python3','--version'])
for part in ['release_records','release_publication','release_signing','release_workflow','installer_fixture']:
 run('python-'+part,['/usr/bin/python3','-m','unittest','discover','-s','scripts/tests','-p','test_nfs_'+part+'.py','-v'])
run('python-all',['/usr/bin/python3','-m','unittest','discover','-s','scripts/tests','-p','test_nfs_*.py','-v'])
run('actionlint',['/opt/homebrew/bin/actionlint','.github/workflows/release-nfs.yml','.github/workflows/ci.yml'])
run('installer-syntax',['/bin/bash','-n','scripts/public/nfs/install.sh'])
run('signing-syntax',['/bin/bash','-n','packaging/sign-macos.sh'])
run('shellcheck',['/opt/homebrew/bin/shellcheck','packaging/sign-macos.sh','scripts/public/nfs/install.sh'])
run('source-hash',['/usr/bin/python3','packaging/release.py','--source-hash'])
run('publish-refusal',['/usr/bin/python3','packaging/release.py','--check-publish'],expected=1)
assert 'No qualified release targets: exactly all four required' in (E/'publish-refusal.log').read_text()
assert (E/'source-hash.log').read_text().splitlines()[-1]=='8c1bcc13194f919c41cf4de9ad825a48acb4281bd558374ac77cbb1426820bac'
event('R01','Pass LOCAL fixtures only; 38collected/37executed/1Go-child skip; narrow counts overlap broad','python-all.log')
event('R02','Pass LOCAL static/hash/default refusal; no measured-engine identity or host/CI qualification','local-results.json')
