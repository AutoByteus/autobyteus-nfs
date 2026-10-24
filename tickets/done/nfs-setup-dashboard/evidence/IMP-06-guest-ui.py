# Implementation-scoped production HTTP/control journey on OWNED guest only.
# No fixture/root bypass; launches the actual public role in a controlling PTY.
import os,pty,select,threading,subprocess,sys,json,time,re,urllib.request,urllib.error,pathlib,hashlib,signal,datetime
root=pathlib.Path.home()/'dashboard-probe';binary=root/'autobyteus-nfs-ui'
record={'id':'IMP-06','date':datetime.datetime.now(datetime.timezone.utc).isoformat(),'platform':subprocess.check_output(['uname','-a'],text=True).strip(),'binarySha256':hashlib.sha256(binary.read_bytes()).hexdigest(),'cases':[]}
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
 assert os.geteuid()!=0,'run as fixture ordinary admin'
 for role in ['server','client']:
  denied=command([str(binary),role]);assert denied['exit']!=0 and 'terminal' in denied['stderr'];case('no-TTY-'+role,observation=denied)
 denied=command(['/usr/bin/sudo','--',str(binary),'server']);assert denied['exit']!=0 and 'ordinary user' in denied['stderr'];case('root-dashboard-refused',observation=denied)
 source=pathlib.Path.home()/'dashboard-data';source.mkdir(exist_ok=True);(source/'sentinel-before.txt').write_text('owned dashboard fixture original\n')
 original=hashlib.sha256((source/'sentinel-before.txt').read_bytes()).hexdigest()
 ui=UI('server');case('public-server-loopback-no-auto-admin',state=ui.req('/api/state'))
 auth=ui.op('authorize');case('public-authorize-private-helper-metadata',operation=auth)
 assert auth['data']['state']=='empty',auth
 # Actual root authority refuses invalid source before intent or storage effects.
 bad=ui.op('beginServer',{'source':'/','endpoint':'192.168.64.8','allowlist':['192.168.64.0/24'],'backend':'ganesha-native','mountRoot':'/Volumes/dashboard-native','dockerSocket':''},False)
 assert bad['state']=='incomplete' and not bad['error']['effectsMayHaveStarted'];case('invalid-source-no-effects',operation=bad)
 review=ui.op('beginServer',{'source':str(source),'endpoint':'192.168.64.8','allowlist':['192.168.64.0/24'],'backend':'ganesha-native','mountRoot':'/Volumes/dashboard-native','dockerSocket':''})
 assert review['data']['configuration']['connection']['protocol']=='4.1'
 denied=ui.op('commit',{'leaseId':review['data']['leaseId'],'consent':False,'drained':False},False);assert denied['state']=='incomplete'
 applied=ui.op('commit',{'leaseId':review['data']['leaseId'],'consent':True,'drained':False})
 case('actual-Linux-native-create-through-HTTP',review=review,missingConsent=denied,operation=applied)
 connection=applied['data']['configuration']['connection'];assert applied['data']['status']['hostReady']
 mounted=pathlib.Path(connection['mountRoot']);assert hashlib.sha256((mounted/'sentinel-before.txt').read_bytes()).hexdigest()==original
 with (mounted/'sentinel-client.txt').open('w') as f:f.write('ordinary-user mounted write\n');f.flush();os.fsync(f.fileno())
 assert (source/'sentinel-client.txt').read_text()=='ordinary-user mounted write\n'
 case('native-mounted-nonroot-read-write',uid=os.getuid(),gid=os.getgid(),connection=connection,originalSHA256=original)
 observed=ui.op('checkReadiness');case('explicit-current-readiness',operation=observed)
 other=UI('client');op=other.op('authorize');assert op['data']['role']=='server'
 refused=other.op('beginReconnect',expect=False);assert refused['state']=='incomplete';case('actual-wrong-role-no-mutation',operation=refused);assert other.close()==0
 reconnect=ui.op('beginReconnect');done=ui.op('commit',{'leaseId':reconnect['data']['leaseId'],'consent':True,'drained':False});case('explicit-reconnect-status-continuation',operation=done)
 job=command(['/usr/bin/sudo','--','/usr/bin/systemctl','show','autobyteus-nfs.service','--property=ActiveState,SubState,MainPID,ExecStart']);assert job['exit']==0 and 'ActiveState=active' in job['stdout'];case('installed-no-SUDO-service-active',observation=job)
 assert ui.close()==0
 assert (mounted/'sentinel-client.txt').read_text()=='ordinary-user mounted write\n';case('dashboard-stop-keeps-host-storage')
 # Retain owned mounted server for the later independent Mac client journey.
 record['retained']={'source':str(source),'connection':connection,'reason':'owned Ubuntu native server for required separate guest client; stop/drained detach pending after that journey'}
 record['result']='Pass (bounded Linux native server only; separate client/Mac/Docker pending)'
except Exception as e:
 record['result']='Fail';record['error']=repr(e)
finally:
 record['dashboardProcesses']=[{'pid':ui.pid,'close':ui.close(),'terminal':ui.sanitized()} for ui in active]
 record['state']=command(['/usr/bin/sudo','--','/bin/ls','-la','/var/lib/autobyteus-nfs'])
 (root/'native-ui-result.json').write_text(json.dumps(record,indent=2)+'\n')
 print(json.dumps(record))
