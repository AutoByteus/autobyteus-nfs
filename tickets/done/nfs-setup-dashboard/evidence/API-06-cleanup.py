# API-06; 2026-10-24; current deeea2f; OWNED Ubuntu/scratch only.
from pathlib import Path
import subprocess,json,datetime,hashlib,os,shutil,time,sys
n=Path.cwd();e=n/'tickets/in-progress/nfs-setup-dashboard/evidence';r=Path('/Users/normy/nfs-dashboard-api-w47yo5sg');ip=(r/'ip').read_text().strip()
ssh=['/usr/bin/ssh','-i',str(r/'key'),'-o','IdentitiesOnly=yes','-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(r/'known_hosts'),'admin@'+ip]
script='''python3 - <<'INNER'
import subprocess,json,pathlib,hashlib,os
root=pathlib.Path('/home/admin/api-dashboard');source=root/'data'
def command(c):
 p=subprocess.run(c,capture_output=True,text=True);return {'argv':c,'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
record={'uid':os.getuid(),'files':{p:hashlib.sha256((source/p).read_bytes()).hexdigest() for p in ['original.txt','browser-write.txt','.autobyteus-nfs/storage.json']},'marker':json.loads((source/'.autobyteus-nfs/storage.json').read_text()),'binarySHA256':hashlib.sha256((root/'autobyteus-nfs').read_bytes()).hexdigest()}
assert (source/'original.txt').read_text()=='api-original-sentinel\\n';assert (source/'browser-write.txt').read_text()=='native-browser-docker\\n'
record['mounts']=command(['findmnt','-rn','-t','nfs,nfs4']);assert not record['mounts']['stdout']
record['containers']=command(['sudo','docker','ps','-aq']);assert record['containers']['exit']==0 and not record['containers']['stdout']
ps=command(['ps','-eo','pid,comm,args','--no-headers']);record['productProcesses']=[l for l in ps['stdout'].splitlines() if len(l.split())>1 and l.split()[1] in ['autobyteus-nfs','ganesha.nfsd']];assert not record['productProcesses']
record['jobs']=command(['systemctl','list-units','--all','--no-legend','autobyteus-nfs*']);assert 'running' not in record['jobs']['stdout']
record['privateInventory']=command(['sudo','find','/var/lib/autobyteus-nfs','-maxdepth','2','-printf','%m %u %p\\n'])
for name in ['attachment.json','hosted-filesystem.json','pending-setup.json']:
 p=subprocess.run(['sudo','test','!','-e','/var/lib/autobyteus-nfs/'+name]);assert p.returncode==0,name
record['occupiedSentinel']=command(['cat','/Volumes/api-occupied/sentinel']);assert 'occupied-original' in record['occupiedSentinel']['stdout']
record['dockerStop']=command(['sudo','systemctl','stop','docker.service','docker.socket']);assert record['dockerStop']['exit']==0
record['result']='Pass';print(json.dumps(record,indent=2))
INNER'''
p=subprocess.run(ssh+[script],capture_output=True,text=True,timeout=90)
(e/'API-06-guest-inventory.log').write_text('API-06 native guest preservation/inventory; current deeea2f; 2026-10-24\n'+p.stdout+'\n'+p.stderr)
assert p.returncode==0,p.stderr
inventory=json.loads(p.stdout);(e/'API-06-guest-inventory.json').write_text(json.dumps({'case':'API-06','date':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':script,'environment':ip,**inventory},indent=2)+'\n')
conn=json.loads((r/'connection.json').read_text());assert inventory['marker']['storageId']==conn['storageId']
record={'case':'API-06','date':datetime.datetime.now(datetime.timezone.utc).isoformat(),'commit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'scratch':str(r),'vm':'api-dashboard-ubuntu','preservation':'API06 guest inventory before removing disposable VM','steps':[]}
for args in [ssh+['sudo shutdown -h now']]:
 p=subprocess.run(args,capture_output=True,text=True,timeout=30);record['steps'].append({'command':args[:-1]+['sudo shutdown -h now'],'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
env={**os.environ,'HOME':str(r/'home'),'TART_HOME':str(r/'tart')};tart=str(r/'tools/tart.app/Contents/MacOS/tart')
for i in range(60):
 p=subprocess.run([tart,'list'],env=env,capture_output=True,text=True)
 if 'running' not in p.stdout.lower():break
 time.sleep(1)
else:raise RuntimeError('guest still running; retain, do not force-delete')
record['beforeDelete']=p.stdout
p=subprocess.run([tart,'delete','api-dashboard-ubuntu'],env=env,capture_output=True,text=True);assert p.returncode==0,p.stderr;record['deleteExit']=p.returncode
record['afterDelete']=subprocess.check_output([tart,'list'],env=env,text=True);assert 'api-dashboard-ubuntu' not in record['afterDelete']
original=Path('/Users/normy/nfs-first-candidate-api006-a8aune30/candidate/engine');sys.dont_write_bytecode=True;sys.path.insert(0,str(n/'packaging/engine'));import manifest
engine=json.loads((original/'engine-manifest.json').read_text());manifest.validate(engine,require_both=True)
for arch,bundle in engine['architectures'].items():manifest.verify_files(bundle,original/arch)
record['retainedEngineManifestSHA256']=hashlib.sha256((original/'engine-manifest.json').read_bytes()).hexdigest();assert record['retainedEngineManifestSHA256']=='95d275cff765d48d18978fef12d5a2c9f3d986998c9ff60836eb0ebcd86c5970';record['retainedEngineAllPackagesVerified']=True
assert r.parent==Path('/Users/normy') and r.name=='nfs-dashboard-api-w47yo5sg' and not r.is_symlink()
shutil.rmtree(r);record['scratchRemoved']=not r.exists();record['result']='Pass'
(e/'API-06-cleanup.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record))
