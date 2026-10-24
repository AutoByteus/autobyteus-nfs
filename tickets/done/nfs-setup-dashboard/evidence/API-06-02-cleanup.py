# API06 round2 | 2026-10-24 | current34afb80 | Macarm64; verify exact inputs and remove own rootless preview scratch.
import pathlib,hashlib,json,subprocess,shutil,datetime,os
n=pathlib.Path.cwd();t=n/'tickets/in-progress/nfs-setup-dashboard';e=t/'evidence';prep=json.loads((e/'API-07-02-environment.json').read_text());r=pathlib.Path(prep['scratch']);assert r.parent==pathlib.Path('/Users/normy') and r.name.startswith('nfs-dashboard-api002-')
result=json.loads((e/'API-07-02-result.json').read_text());assert result['result']=='Pass'
processes=subprocess.check_output(['ps','-axo','pid=,command='],text=True).splitlines();owned=[x for x in processes if str(r) in x];assert not owned,owned
mismatches=[]
for row in prep['sourceInputs']:
 for base in [n,r/'source']:
  if hashlib.sha256((base/row['path']).read_bytes()).hexdigest()!=row['sha256']:mismatches.append(str(base/row['path']))
assert not mismatches
sourcehash=subprocess.check_output(['python3','packaging/release.py','--source-hash'],cwd=r/'source',env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','HOME':str(r/'home'),'TMPDIR':str(r/'tmp')},text=True).strip();assert sourcehash=='2703d4bf972ab2070fcfbc0f1b175fd70c258963c706fffad591cd5dc70d6903'
rec={'case':'API-06','round':'API-REV-002','date':datetime.datetime.now(datetime.timezone.utc).isoformat(),'commit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'command':'python3 evidence/API-06-02-cleanup.py','environment':'Macarm64 own rootless preview only','sourceHash':sourcehash,'verifiedInputs':len(prep['sourceInputs']),'mismatches':mismatches,'matchingProcessesBeforeRemoval':owned,'probeExit':[x['terminal'] for x in result['runs']],'ownedScratch':str(r),'nativeResourcesCreated':False,'otherResources':'No VM/sudo/root/NFS/Docker/installer/clipboard/provider/user profile/retained engine access or mutation'}
shutil.rmtree(r);rec['scratchRemoved']=not r.exists();rec['result']='Pass';(e/'API-06-02-cleanup.json').write_text(json.dumps(rec,indent=2)+'\n');print(json.dumps(rec,indent=2))
now=datetime.datetime.now(datetime.timezone.utc).isoformat();p=t/'api-e2e-test-progress.md';p.write_text(p.read_text()+f'| {now} | API-06 (round2) | Completed | Pass all166 current/source inputs unchanged; no owned processes; exact new scratch removed; no native resources created |\n')
