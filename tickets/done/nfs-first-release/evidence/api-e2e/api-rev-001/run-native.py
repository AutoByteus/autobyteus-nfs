from pathlib import Path
import hashlib,subprocess,os,json,time,datetime
E=Path(__file__).resolve().parent;T=E.parents[2];P=Path(json.loads((E/'scratch.json').read_text())['path']);S=P/'source'
with (T/'api-e2e-coverage-investigation.md').open('a') as f:f.write('\nPost-local checkpoint: R01/R02 local checks green. R03 reviewed ref absent remotely; requested Delivery-owned staged availability, not qualification/publication. No test-owned physical endpoints identified; user asked only for resource inventory, not new requirements or credential entry. While staged availability is pending, add R02-native fresh native Darwin Go1.27.2 race/vet/build/version in existing owned APFS copy; root testing commands, no new runtime changes or source qualification claim.\n')
results=[]
env={'HOME':str(P/'home'),'TMPDIR':str(P/'tmp')+'/','PATH':str(P/'go/bin')+':/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin','LC_ALL':'C','PYTHONDONTWRITEBYTECODE':'1','GOCACHE':str(P/'cache/go'),'GOMODCACHE':str(P/'cache/mod'),'GOTOOLCHAIN':'local'}
def run(name,args,cwd=S,expected=0):
 t=time.time()
 with (E/(name+'.log')).open('w') as f:
  f.write('$ '+' '.join(map(str,args))+'\ncwd '+str(cwd)+'\n');f.flush();p=subprocess.run(args,cwd=cwd,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=900)
 r=dict(name=name,command=list(map(str,args)),cwd=str(cwd),exit=p.returncode,expected=expected,seconds=round(time.time()-t,3),passed=p.returncode==expected);results.append(r)
 (E/'native-results.json').write_text(json.dumps(results,indent=2)+'\n');print(name,p.returncode,flush=True)
 with (T/'api-e2e-test-case-ledger.md').open('a') as f:f.write('| '+datetime.datetime.now(datetime.timezone.utc).isoformat()+' | R02-native | '+('Pass checkpoint' if r['passed'] else 'Fail')+' | '+name+'.log |\n')
 assert r['passed'],r
archive=P/'go1.27.2.darwin-arm64.tar.gz'
run('go-download',['curl','-fsSL','https://go.dev/dl/go1.27.2.darwin-arm64.tar.gz','-o',str(archive)],P)
actual=hashlib.sha256(archive.read_bytes()).hexdigest();expected='76812b213b1b2302c978d28fa52fa92d541704b9e7d9d5db8002c50e4018c4c5';assert actual==expected
(E/'go-download-identity.json').write_text(json.dumps(dict(sha256=actual,expected=expected,source='Official go.dev Go1.27.2 darwin-arm64 artifact; matches independently verified IR001/pinned toolchain',native='darwin-arm64'),indent=2)+'\n')
run('go-extract',['tar','-xzf',str(archive),'-C',str(P)],P)
run('go-version',[str(P/'go/bin/go'),'version'])
run('go-race',[str(P/'go/bin/go'),'test','-race','-json','-count=1','./...'])
run('go-vet',[str(P/'go/bin/go'),'vet','./...'])
(P/'out').mkdir()
run('go-build',[str(P/'go/bin/go'),'build','-o',str(P/'out/autobyteus-nfs'),'./cmd/autobyteus-nfs'])
run('native-version',[str(P/'out/autobyteus-nfs'),'version'])
assert (E/'native-version.log').read_text().splitlines()[-1]=='development-unqualified'
