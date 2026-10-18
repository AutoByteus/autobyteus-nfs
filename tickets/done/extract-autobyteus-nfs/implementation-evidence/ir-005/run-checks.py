from pathlib import Path
import subprocess,json,time,sys,os
E=Path(__file__).resolve().parent;P=Path((E/'scratch-path.txt').read_text().strip());mode=sys.argv[1]
container=json.loads((E/'linux-container.json').read_text())['name']
if mode=='linux':
 prefix=['docker','exec','--user','1001:1001','--workdir','/home/checker/candidate',container,'env','-i','PATH=/usr/local/go/bin:/usr/bin:/bin','HOME=/home/checker','TMPDIR=/home/checker/tmp','GOTOOLCHAIN=local']
 checks=[('baseline-hosted',['go','test','-race','./internal/setup','-run','TestHostedConfig','-count=1','-v'],1),
 ('environment',['sh','-c','id; uname -a; cat /etc/os-release; go version; gcc --version | head -1; python3 --version'],0),
 ('focused',['go','test','-race','./internal/setup','-run','TestHostedConfig','-count=1','-v'],0),
 ('race',['go','test','-race','./...'],0),('vet',['go','vet','./...'],0),
 ('build',['go','build','-o','/home/checker/autobyteus-nfs','./cmd/autobyteus-nfs'],0),
 ('version',['/home/checker/autobyteus-nfs','version'],0),
 ('python',['python3','-m','unittest','discover','-s','scripts/tests','-p','test_nfs_*.py','-v'],0),
 ('shell',['bash','-n','scripts/public/nfs/install.sh'],0),
 ('source-hash',['python3','packaging/release.py','--source-hash'],0),
 ('publish-refusal',['python3','packaging/release.py','--check-publish'],1)]
 env=None;cwd=P
else:
 prefix=[];cwd=P/'candidate'
 env={'PATH':str(P/'tools/go/bin')+':/opt/homebrew/bin:/usr/bin:/bin','HOME':str(P/'mac-home'),'TMPDIR':str(P/'mac-tmp'),'GOCACHE':str(P/'mac-cache'),'GOTOOLCHAIN':'local'}
 checks=[('environment',['sh','-c','id; uname -a; go version; cc --version | head -1; python3 --version'],0),
 ('focused',['go','test','-race','./internal/setup','-run','TestHostedConfig|TestDetachDoesNotRequireLiveSource','-count=1','-v'],0),
 ('race',['go','test','-race','./...'],0),('vet',['go','vet','./...'],0),
 ('source-hash',['python3','packaging/release.py','--source-hash'],0),
 ('publish-refusal',['python3','packaging/release.py','--check-publish'],1)]
results=[]
for name,cmd,expected in checks:
 pre=prefix.copy()
 if name=='baseline-hosted':pre=[s.replace('/home/checker/candidate','/home/checker/baseline') for s in pre]
 t=time.time()
 with (E/(mode+'-'+name+'.log')).open('w') as log:
  log.write('$ '+' '.join(pre+cmd)+'\n');log.flush()
  run=subprocess.run(pre+cmd,cwd=cwd,env=env,stdout=log,stderr=subprocess.STDOUT)
 results.append(dict(name=name,command=pre+cmd,exit=run.returncode,expected_exit=expected,seconds=round(time.time()-t,3)))
 (E/(mode+'-checks-result.json')).write_text(json.dumps(results,indent=2)+'\n')
 print(mode,name,run.returncode,flush=True)
 if run.returncode!=expected:raise SystemExit(1)
