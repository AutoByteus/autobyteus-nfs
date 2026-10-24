# IMP-11 | owned Ubuntu24.04 native client of owned Mac26.6.2 server.
# Old matching dashboard drains Docker before installing current development build.
import os,pty,select,threading,subprocess,sys,json,time,re,urllib.request,urllib.error,pathlib,hashlib,signal,datetime
root=pathlib.Path.home()/'dashboard-probe';binary=root/'autobyteus-nfs-ui'
record={'id':'IMP-11','date':datetime.datetime.now(datetime.timezone.utc).isoformat(),'platform':subprocess.check_output(['uname','-a'],text=True).strip(),'binarySha256':hashlib.sha256(binary.read_bytes()).hexdigest(),'cases':[]}
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
 source=pathlib.Path.home()/'dashboard-data'
 assert (source/'sentinel-from-mac-client.txt').read_text()=='Mac nonroot client of Linux Docker\n'
 before={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in source.glob('sentinel-*.txt')};marker=(source/'.autobyteus-nfs/storage.json').read_bytes()
 ui=UI('server');auth=ui.op('authorize');assert auth['data']['backend']=='ganesha-docker'
 review=ui.op('beginDetach');result=ui.op('commit',{'leaseId':review['data']['leaseId'],'consent':True,'drained':True});assert result['data']['configuration']['state']=='empty';assert ui.close()==0
 assert (source/'.autobyteus-nfs/storage.json').read_bytes()==marker
 assert {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in source.glob('sentinel-*.txt')}==before
 case('Docker-drained-detach-preserves-source-and-peer-write',operation=result,sourceHashes=before)
 # Actual old job/helper ended; no live installed binary is overwritten directly.
 os.replace(root/'autobyteus-nfs-next',binary)
 record['currentClientBinarySha256']=hashlib.sha256(binary.read_bytes()).hexdigest()
 connection=json.loads((root/'mac-connection.json').read_text())
 ui=UI('client');auth=ui.op('authorize');assert auth['data']['state']=='empty'
 review=ui.op('beginClient',{'connection':json.dumps(connection),'mountRoot':'/Volumes/dashboard-mac-client'})
 result=ui.op('commit',{'leaseId':review['data']['leaseId'],'consent':True,'drained':False});assert result['data']['status']['hostReady']
 mounted=pathlib.Path('/Volumes/dashboard-mac-client')
 assert (mounted/'sentinel-mac-original.txt').read_text()=='Mac ordinary source remains in place\n'
 assert (mounted/'sentinel-mac-self.txt').read_text()=='Mac mounted nonroot self write\n'
 with (mounted/'sentinel-from-linux-client.txt').open('w') as f:f.write('Linux nonroot client of native Mac server\n');f.flush();os.fsync(f.fileno())
 case('Linux-native-client-Mac-source-mounted-RW',review=review,operation=result,uid=os.getuid(),gid=os.getgid())
 check=ui.op('checkReadiness');assert check['data']['status']['hostReady']
 review=ui.op('beginReconnect');result=ui.op('commit',{'leaseId':review['data']['leaseId'],'consent':True,'drained':False});case('Linux-client-explicit-reconnect',operation=result)
 assert ui.close()==0
 assert (mounted/'sentinel-from-linux-client.txt').read_text()=='Linux nonroot client of native Mac server\n'
 ui=UI('client');auth=ui.op('authorize');assert auth['data']['state']=='configured'
 holder=subprocess.Popen(['/usr/bin/sleep','300'],cwd=str(mounted))
 try:
  review=ui.op('beginDetach');busy=ui.op('commit',{'leaseId':review['data']['leaseId'],'consent':True,'drained':True},False);assert busy['state']=='incomplete';case('Linux-client-busy-detach-refusal',operation=busy)
 finally:holder.terminate();holder.wait()
 review=ui.op('beginDetach');result=ui.op('commit',{'leaseId':review['data']['leaseId'],'consent':True,'drained':True});assert result['data']['configuration']['state']=='empty';case('Linux-client-drained-detach',operation=result);assert ui.close()==0
 assert {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in source.glob('sentinel-*.txt')}==before
 mounts=pathlib.Path('/proc/self/mountinfo').read_text();assert not any(' /Volumes/dashboard-' in l for l in mounts.splitlines())
 containers=command(['/usr/bin/sudo','--','/usr/bin/docker','ps','-a','--format','{{.Names}}']);assert containers['exit']==0 and 'autobyteus-nfs-storage-' not in containers['stdout'];case('Linux-owned-mounts-engine-removed',observation=containers)
 record['result']='Pass (native Linux client; Linux storage/client drained; Mac server remains for cleanup)'
except Exception as e:record['result']='Fail';record['error']=repr(e)
finally:
 record['dashboardProcesses']=[{'pid':ui.pid,'close':ui.close(),'terminal':ui.sanitized()} for ui in active]
 record['state']=command(['/usr/bin/sudo','--','/bin/ls','-la','/var/lib/autobyteus-nfs'])
 (root/'linux-client-result.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record))
