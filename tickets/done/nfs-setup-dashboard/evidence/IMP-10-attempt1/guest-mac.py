# IMP-10 | actual owned Mac guest, current development binary, no root/mount doubles.
# Scope: native client of owned Linux Docker, then native Apple server; not field proof.
import os,pty,select,threading,subprocess,sys,json,time,re,urllib.request,urllib.error,pathlib,hashlib,signal,datetime
root=pathlib.Path.home()/'dashboard-probe';binary=root/'autobyteus-nfs-ui'
record={'id':'IMP-10','date':datetime.datetime.now(datetime.timezone.utc).isoformat(),'platform':subprocess.check_output(['uname','-a'],text=True).strip(),'binarySha256':hashlib.sha256(binary.read_bytes()).hexdigest(),'cases':[]}
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
 assert os.geteuid()!=0
 record['osVersion']=command(['/usr/bin/sw_vers'])
 for role in ['server','client']:
  denied=command([str(binary),role]);assert denied['exit']!=0 and 'terminal' in denied['stderr'];case('no-TTY-'+role,observation=denied)
 denied=command(['/usr/bin/sudo','--',str(binary),'server']);assert denied['exit']!=0 and 'ordinary user' in denied['stderr'];case('root-dashboard-refused',observation=denied)
 connection=json.loads((root/'linux-connection.json').read_text())
 ui=UI('client');auth=ui.op('authorize');assert auth['data']['state']=='empty'
 case('Mac-public-client-terminal-authorization',operation=auth)
 review=ui.op('beginClient',{'connection':json.dumps(connection),'mountRoot':'/Volumes/dashboard-linux-client'})
 rejected=ui.op('commit',{'leaseId':review['data']['leaseId'],'consent':False,'drained':False},False);assert rejected['state']=='incomplete'
 result=ui.op('commit',{'leaseId':review['data']['leaseId'],'consent':True,'drained':False});assert result['data']['status']['hostReady']
 mounted=pathlib.Path('/Volumes/dashboard-linux-client')
 assert (mounted/'sentinel-docker.txt').read_text()=='owned Docker export nonroot mount write\n'
 with (mounted/'sentinel-from-mac-client.txt').open('w') as f:f.write('Mac nonroot client of Linux Docker\n');f.flush();os.fsync(f.fileno())
 case('Mac-client-Linux-Docker-mounted-read-write',review=review,operation=result,uid=os.getuid(),gid=os.getgid())
 check=ui.op('checkReadiness');assert check['data']['status']['hostReady']
 review=ui.op('beginReconnect');result=ui.op('commit',{'leaseId':review['data']['leaseId'],'consent':True,'drained':False});case('Mac-client-explicit-reconnect',operation=result)
 assert ui.close()==0
 assert (mounted/'sentinel-from-mac-client.txt').read_text()=='Mac nonroot client of Linux Docker\n'
 ui=UI('client');auth=ui.op('authorize');assert auth['data']['state']=='configured'
 review=ui.op('beginDetach');refused=ui.op('commit',{'leaseId':review['data']['leaseId'],'consent':True,'drained':False},False);assert refused['state']=='incomplete'
 detached=ui.op('commit',{'leaseId':review['data']['leaseId'],'consent':True,'drained':True});assert detached['data']['configuration']['state']=='empty'
 case('Mac-client-drained-detach',missingDrain=refused,operation=detached);assert ui.close()==0
 source=pathlib.Path.home()/'dashboard-data';source.mkdir(exist_ok=True);(source/'sentinel-mac-original.txt').write_text('Mac ordinary source remains in place\n')
 original=hashlib.sha256((source/'sentinel-mac-original.txt').read_bytes()).hexdigest()
 ui=UI('server');auth=ui.op('authorize');assert auth['data']['state']=='empty'
 endpoint=(root/'mac-ip.txt').read_text().strip()
 review=ui.op('beginServer',{'source':str(source),'endpoint':endpoint,'allowlist':['192.168.64.0/24'],'backend':'apple','mountRoot':'/Volumes/dashboard-apple','dockerSocket':''})
 result=ui.op('commit',{'leaseId':review['data']['leaseId'],'consent':True,'drained':False});assert result['data']['status']['hostReady']
 connection=result['data']['configuration']['connection'];mounted=pathlib.Path(connection['mountRoot'])
 assert hashlib.sha256((mounted/'sentinel-mac-original.txt').read_bytes()).hexdigest()==original
 with (mounted/'sentinel-mac-self.txt').open('w') as f:f.write('Mac mounted nonroot self write\n');f.flush();os.fsync(f.fileno())
 assert (source/'sentinel-mac-self.txt').read_text()=='Mac mounted nonroot self write\n'
 case('Mac-native-Apple-source-selfmount-RW',review=review,operation=result,uid=os.getuid(),gid=os.getgid(),originalSHA256=original)
 check=ui.op('checkReadiness');assert check['data']['status']['hostReady']
 review=ui.op('beginReconnect');result=ui.op('commit',{'leaseId':review['data']['leaseId'],'consent':True,'drained':False});case('Mac-server-explicit-reconnect',operation=result)
 job=command(['/usr/bin/sudo','--','/bin/launchctl','print','system/com.autobyteus.nfs']);assert job['exit']==0 and 'state = running' in job['stdout'];case('Mac-installed-service-observation',observation=job)
 assert ui.close()==0
 assert (mounted/'sentinel-mac-self.txt').read_text()=='Mac mounted nonroot self write\n'
 record['retained']={'source':str(source),'connection':connection,'reason':'owned native Mac server for subsequent separate Linux client; final drained detach pending'}
 record['result']='Pass (bounded Mac native client/server; Linux-client/cleanup pending)'
except Exception as e:
 record['result']='Fail';record['error']=repr(e)
finally:
 record['dashboardProcesses']=[{'pid':ui.pid,'close':ui.close(),'terminal':ui.sanitized()} for ui in active]
 record['state']=command(['/usr/bin/sudo','--','/bin/ls','-la','/Library/Application Support/AutoByteusNFS'])
 (root/'mac-ui-result.json').write_text(json.dumps(record,indent=2)+'\n')
 print(json.dumps(record))
