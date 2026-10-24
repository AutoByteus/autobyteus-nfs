# IMP-09 | owned Ubuntu guest only; drain our self-mount, observe actual saved service remount.
# No explicit reconnect/check command is called until observation; no force/lazy unmount.
import subprocess,time,json,pathlib,hashlib,datetime
root=pathlib.Path.home()/'dashboard-probe';source=pathlib.Path.home()/'dashboard-data';mount='/Volumes/dashboard-docker';rows=[]
def run(args):
 p=subprocess.run(args,capture_output=True,text=True);r={'argv':args,'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr};rows.append(r);return r
result={'id':'IMP-09','date':datetime.datetime.now(datetime.timezone.utc).isoformat(),'step':'existing installed no-SUDO systemd service resumes owned drained self-mount without dashboard/explicit reconnect','observations':rows}
try:
 hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in source.glob('sentinel-*.txt')}
 before=run(['/usr/bin/sudo','--','/usr/bin/systemctl','show','autobyteus-nfs.service','--property=ActiveState,SubState,MainPID,Environment']);assert before['exit']==0 and 'ActiveState=active' in before['stdout']
 assert run(['/usr/bin/sudo','--','/usr/bin/umount',mount])['exit']==0
 started=time.monotonic();observed=[]
 while time.monotonic()-started<45:
  table=pathlib.Path('/proc/self/mountinfo').read_text();line=next((l for l in table.splitlines() if ' '+mount+' ' in l),None)
  observed.append({'afterSeconds':round(time.monotonic()-started,3),'mountEntry':line})
  if line:break
  time.sleep(.5)
 result['mountObservations']=observed
 assert observed[-1]['mountEntry'],'service did not restore exact mount within45s'
 assert ' - nfs4 192.168.64.8:' in observed[-1]['mountEntry']
 assert {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in pathlib.Path(mount).glob('sentinel-*.txt')}==hashes
 after=run(['/usr/bin/sudo','--','/usr/bin/systemctl','show','autobyteus-nfs.service','--property=ActiveState,SubState,MainPID,Environment']);assert after['stdout']==before['stdout']
 result['result']='Pass';result['scope']='actual service remount/identity and read-only sentinel check; bounded fixture, no boot/outage qualification'
except Exception as e:result['result']='Fail';result['error']=repr(e)
(root/'service-ui-result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
