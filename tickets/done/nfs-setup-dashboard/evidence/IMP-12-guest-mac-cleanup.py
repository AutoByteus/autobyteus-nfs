# IMP-12 | owned Mac native service and drained storage cleanup.
import os,pty,select,threading,subprocess,sys,json,time,re,urllib.request,urllib.error,pathlib,hashlib,signal,datetime
root=pathlib.Path.home()/'dashboard-probe';binary=root/'autobyteus-nfs-ui'
record={'id':'IMP-12','date':datetime.datetime.now(datetime.timezone.utc).isoformat(),'platform':subprocess.check_output(['uname','-a'],text=True).strip(),'binarySha256':hashlib.sha256(binary.read_bytes()).hexdigest(),'cases':[]}
active=[]
def command(args):
 p=subprocess.run(args,capture_output=True,text=True,start_new_session=True);return {'argv':args,'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
class UI:
 def __init__(self,role):
  self.output='';self.seq=0;self.token='';self.done=False;self.base='';self.secret=''
  pid,fd=pty.fork()
  if pid==0:os.execv(str(binary),[str(binary),role])
  self.pid=pid;self.fd=fd;active.append(self)
  def drain():
   while True:
    try:b=os.read(fd,4096)
    except OSError:break
    if not b:break
    self.output+=b.decode(errors='replace')
  self.thread=threading.Thread(target=drain,daemon=True);self.thread.start()
  until=time.monotonic()+20
  while time.monotonic()<until:
   m=re.search(r'(http://127\.0\.0\.1:\d+)/#([A-Za-z0-9_-]+)',self.output)
   if m:self.base,self.secret=m.groups();break
   time.sleep(.05)
  assert self.base,'no dashboard fallback: '+self.sanitized()
  self.token=self.req('/api/session',{'secret':self.secret})['token']
  s=self.req('/api/state');assert s['role']==role and not s['authorized'],s
 def sanitized(self):return re.sub(r'http://127\.0\.0\.1:\d+/#\S+','[PRIVATE LOCAL URL REDACTED]',self.output)
 def req(self,path,value=None):
  h={'Origin':self.base,'Content-Type':'application/json'}
  if self.token:h['Authorization']='Bearer '+self.token
  r=urllib.request.Request(self.base+path,headers=h,data=None if value is None else json.dumps(value).encode())
  with urllib.request.urlopen(r,timeout=10) as response:return json.load(response)
 def op(self,kind,payload=None,expect=True):
  self.seq+=1;op=self.req('/api/operations',{'id':self.seq,'kind':kind,'payload':payload or {}})
  until=time.monotonic()+600
  while op['state']=='running' and time.monotonic()<until:time.sleep(.25);op=self.req('/api/state')['operation']
  if expect:assert op['state']=='succeeded',op
  return op
 def close(self):
  if self.done:return
  try:self.req('/api/stop',{})
  except Exception:pass
  until=time.monotonic()+20
  while time.monotonic()<until:
   pid,status=os.waitpid(self.pid,os.WNOHANG)
   if pid:self.done=True;os.close(self.fd);self.thread.join(2);return status
   time.sleep(.1)
  return 'outstanding; not force-killed'
def case(name,**v):record['cases'].append({'name':name,'result':'Pass',**v})
try:
 source=pathlib.Path.home()/'dashboard-data';mounted=pathlib.Path('/Volumes/dashboard-apple')
 assert (source/'sentinel-from-linux-client.txt').read_text()=='Linux nonroot client of native Mac server\n'
 hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in source.glob('sentinel-*.txt')};marker=(source/'.autobyteus-nfs/storage.json').read_bytes()
 job=command(['/usr/bin/sudo','--','/bin/launchctl','print','system/com.autobyteus.nfs']);assert job['exit']==0 and 'state = running' in job['stdout'];pid=re.search(r'\n\s*pid = (\d+)',job['stdout']).group(1)
 unmount=command(['/usr/bin/sudo','--','/sbin/umount',str(mounted)]);assert unmount['exit']==0,unmount
 started=time.monotonic();rows=[]
 while time.monotonic()-started<45:
  table=subprocess.check_output(['/sbin/mount'],text=True);line=next((l for l in table.splitlines() if ' on '+str(mounted)+' ' in l),None)
  rows.append({'afterSeconds':round(time.monotonic()-started,3),'mountEntry':line})
  if line:break
  time.sleep(.5)
 assert rows[-1]['mountEntry'] and rows[-1]['mountEntry'].startswith('192.168.64.2:/Users/admin/dashboard-data on '),rows[-1]
 after=command(['/usr/bin/sudo','--','/bin/launchctl','print','system/com.autobyteus.nfs']);assert re.search(r'\n\s*pid = (\d+)',after['stdout']).group(1)==pid
 assert {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in mounted.glob('sentinel-*.txt')}==hashes
 case('actual-Mac-same-service-restores-drained-selfmount',pid=pid,unmount=unmount,observations=rows)
 ui=UI('server');auth=ui.op('authorize');assert auth['data']['state']=='configured'
 review=ui.op('beginDetach');refused=ui.op('commit',{'leaseId':review['data']['leaseId'],'consent':True,'drained':False},False);assert refused['state']=='incomplete'
 result=ui.op('commit',{'leaseId':review['data']['leaseId'],'consent':True,'drained':True});assert result['data']['configuration']['state']=='empty';assert ui.close()==0
 assert (source/'.autobyteus-nfs/storage.json').read_bytes()==marker
 assert {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in source.glob('sentinel-*.txt')}==hashes
 assert '/Volumes/dashboard-' not in subprocess.check_output(['/sbin/mount'],text=True)
 job=command(['/usr/bin/sudo','--','/bin/launchctl','print','system/com.autobyteus.nfs']);assert job['exit']!=0
 case('Mac-drained-detach-preserves-source-marker-peer-write',review=review,missingDrain=refused,operation=result,sourceHashes=hashes,removedJob=job)
 record['result']='Pass (Mac storage safely detached; no task mounts/job remain; owned VM removal still pending)'
except Exception as e:record['result']='Fail';record['error']=repr(e)
finally:
 record['dashboardProcesses']=[{'pid':ui.pid,'close':ui.close(),'terminal':ui.sanitized()} for ui in active]
 record['state']=command(['/usr/bin/sudo','--','/bin/ls','-la','/Library/Application Support/AutoByteusNFS'])
 (root/'mac-cleanup-result.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record))
