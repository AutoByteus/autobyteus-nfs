# Implementation-scoped production HTTP/control journey on OWNED guest only.
# No fixture/root bypass; launches the actual public role in a controlling PTY.
import os,pty,select,threading,subprocess,sys,json,time,re,urllib.request,urllib.error,pathlib,hashlib,signal,datetime
root=pathlib.Path.home()/'dashboard-probe';binary=root/'autobyteus-nfs-ui'
record={'id':'IMP-09','date':datetime.datetime.now(datetime.timezone.utc).isoformat(),'platform':subprocess.check_output(['uname','-a'],text=True).strip(),'binarySha256':hashlib.sha256(binary.read_bytes()).hexdigest(),'cases':[]}
active=[]
def command(args):
 p=subprocess.run(args,capture_output=True,text=True);return {'argv':args,'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
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
 before={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in source.glob('sentinel-*.txt')}
 marker=(source/'.autobyteus-nfs/storage.json').read_bytes()
 ui=UI('server');auth=ui.op('authorize');assert auth['data']['backend']=='ganesha-native'
 rootpath=auth['data']['connection']['mountRoot']
 holder=subprocess.Popen(['/usr/bin/sleep','300'],cwd=rootpath)
 try:
  review=ui.op('beginDetach');failed=ui.op('commit',{'leaseId':review['data']['leaseId'],'consent':True,'drained':True},False)
  assert failed['state']=='incomplete',failed
  assert ui.op('inspect')['data']['state']=='configured'
  case('busy-native-detach-refused-with-configuration-retained',operation=failed)
 finally:holder.terminate();holder.wait()
 review=ui.op('beginDetach');detached=ui.op('commit',{'leaseId':review['data']['leaseId'],'consent':True,'drained':True});assert detached['data']['configuration']['state']=='empty'
 assert (source/'.autobyteus-nfs/storage.json').read_bytes()==marker
 assert {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in source.glob('sentinel-*.txt')}==before
 case('drained-native-detach-preserves-bytes-marker',operation=detached)
 review=ui.op('beginServer',{'source':str(source),'endpoint':'192.168.64.8','allowlist':['192.168.64.0/24'],'backend':'ganesha-docker','mountRoot':'/Volumes/dashboard-docker','dockerSocket':'/var/run/docker.sock'})
 result=ui.op('commit',{'leaseId':review['data']['leaseId'],'consent':True,'drained':False});assert result['data']['status']['hostReady']
 connection=result['data']['configuration']['connection'];mounted=pathlib.Path(connection['mountRoot'])
 assert {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in mounted.glob('sentinel-*.txt')}==before
 with (mounted/'sentinel-docker.txt').open('w') as f:f.write('owned Docker export nonroot mount write\n');f.flush();os.fsync(f.fileno())
 assert (source/'sentinel-docker.txt').read_text()=='owned Docker export nonroot mount write\n'
 assert (source/'.autobyteus-nfs/storage.json').read_bytes()==marker
 case('Linux-Docker-create-via-current-HTTP-native-RW',review=review,operation=result,uid=os.getuid(),gid=os.getgid())
 names=command(['/usr/bin/sudo','--','/usr/bin/docker','ps','--format','{{.ID}} {{.Image}} {{.Names}}']);assert names['exit']==0 and 'autobyteus-nfs-storage-' in names['stdout'];case('owned-immutable-engine-running',observation=names)
 checked=ui.op('checkReadiness');assert checked['data']['status']['hostReady']
 reconnect=ui.op('beginReconnect');done=ui.op('commit',{'leaseId':reconnect['data']['leaseId'],'consent':True,'drained':False});case('Docker-explicit-reconnect',operation=done)
 assert ui.close()==0
 assert (mounted/'sentinel-docker.txt').read_text()=='owned Docker export nonroot mount write\n'
 record['retained']={'source':str(source),'connection':connection,'reason':'owned Docker server for subsequent separate Mac client; final drained detach pending'}
 record['result']='Pass (bounded native Linux Docker mode; Mac/client/cleanup pending)'
except Exception as e:
 record['result']='Fail';record['error']=repr(e)
finally:
 record['dashboardProcesses']=[{'pid':ui.pid,'close':ui.close(),'terminal':ui.sanitized()} for ui in active]
 record['state']=command(['/usr/bin/sudo','--','/bin/ls','-la','/var/lib/autobyteus-nfs'])
 (root/'docker-ui-result.json').write_text(json.dumps(record,indent=2)+'\n')
 print(json.dumps(record))
