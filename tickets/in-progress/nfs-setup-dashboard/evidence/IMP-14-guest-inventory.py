# IMP-14 | 2026-10-24 | current production5f8cabf | owned Mac/Ubuntu only
# Read-only post-drain inventory before graceful shutdown/removal of owned guests.
import pathlib,subprocess,json,platform,hashlib,datetime,sys
mac=platform.system()=='Darwin';root=pathlib.Path.home()/'dashboard-data';rows=[]
def run(argv):
 p=subprocess.run(argv,capture_output=True,text=True);v={'argv':argv,'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr};rows.append(v);return v
r={'id':'IMP-14','date':datetime.datetime.now(datetime.timezone.utc).isoformat(),'platform':platform.platform(),'commands':rows}
mounts=run(['/sbin/mount' if mac else '/usr/bin/mount']);assert '/Volumes/dashboard-' not in mounts['stdout']
ps=run(['/bin/ps','-axo','pid,ppid,command']);active=[line for line in ps['stdout'].splitlines() if ('/libexec/autobyteus-nfs' in line or '/dashboard-probe/autobyteus-nfs-ui' in line)];assert not active,active
base='/Library/Application Support/AutoByteusNFS' if mac else '/var/lib/autobyteus-nfs'
files=run(['/usr/bin/sudo','--','/bin/ls','-la',base]);assert files['exit']==0
assert not any('attachment.json' in l or 'pending.json' in l for l in files['stdout'].splitlines()),files
job=run(['/usr/bin/sudo','--','/bin/launchctl','print','system/com.autobyteus.nfs'] if mac else ['/usr/bin/sudo','--','/usr/bin/systemctl','is-active','autobyteus-nfs.service']);assert job['exit']!=0,job
if not mac:
 containers=run(['/usr/bin/sudo','--','/usr/bin/docker','ps','-a','--format','{{.Names}}']);assert containers['exit']==0 and not containers['stdout'].strip(),containers
else:
 exports=run(['/usr/bin/sudo','--','/bin/cat','/etc/exports']);assert not any(l.strip() and not l.strip().startswith('#') for l in exports['stdout'].splitlines()),exports
r['sourcePreserved']={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file()}
r['activeTaskProcesses']=active;r['result']='Pass (task mounts/jobs/helper/UI/engine absent; source and marker preserved before owned VM removal)'
p=pathlib.Path.home()/'dashboard-probe/final-inventory.json';p.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
