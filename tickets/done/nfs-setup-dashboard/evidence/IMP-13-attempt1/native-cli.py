# IMP-13 | preserved public CLI forms through shared admin on owned guests only.
# Run phases mac-create, linux-client, mac-detach sequentially; never user host.
import pathlib,subprocess,json,sys,hashlib,datetime,os,pty,threading,time,re
root=pathlib.Path.home()/'dashboard-probe';binary=root/'autobyteus-nfs-ui';phase=sys.argv[1];rows=[]
r={'id':'IMP-13','date':datetime.datetime.now(datetime.timezone.utc).isoformat(),'phase':phase,'binarySha256':hashlib.sha256(binary.read_bytes()).hexdigest(),'checks':rows}
def cmd(args):
 p=subprocess.run(args,capture_output=True,text=True,start_new_session=True);v={'argv':args,'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr};rows.append(v);assert p.returncode==0,v;return p.stdout
try:
 cmd([str(binary),'version'])
 if phase=='mac-create':
  source=pathlib.Path.home()/'dashboard-data';marker=(source/'.autobyteus-nfs/storage.json').read_bytes()
  hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in source.glob('sentinel-*.txt')}
  output=cmd([str(binary),'create','--source',str(source),'--endpoint','192.168.64.2','--allow','192.168.64.0/24','--backend','apple','--mount-root','/Volumes/dashboard-cli-server','--yes','--json']);data=json.loads(output);assert data['status']['hostReady'];r['connection']=data['connection']
  assert (source/'.autobyteus-nfs/storage.json').read_bytes()==marker
  assert {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in source.glob('sentinel-*.txt')}==hashes
  state=cmd(['/usr/bin/sudo','--','/usr/bin/env','-u','SUDO_UID','-u','SUDO_GID','-u','SUDO_USER','/Library/AutoByteusNFS/libexec/autobyteus-nfs','status']);assert json.loads(state)['hostReady']
  # Actual no-args terminal form. Choose its configured default status, never setup.
  pid,fd=pty.fork()
  if pid==0:os.execv(str(binary),[str(binary)])
  captured=[]
  def read():
   while True:
    try:b=os.read(fd,4096)
    except OSError:break
    if not b:break
    captured.append(b.decode(errors='replace'))
  t=threading.Thread(target=read,daemon=True);t.start();deadline=time.monotonic()+30
  while 'Configured storage' not in ''.join(captured) and time.monotonic()<deadline:time.sleep(.05)
  assert 'Configured storage' in ''.join(captured);os.write(fd,b'\n');_,code=os.waitpid(pid,0);os.close(fd);t.join(2);assert code==0
  rows.append({'step':'actual no-args configured terminal selects status','exit':code,'terminal':''.join(captured)})
 elif phase=='linux-client':
  connection=json.loads((root/'mac-cli-connection.json').read_text())
  data=json.loads(cmd([str(binary),'connect','--connection',json.dumps(connection),'--mount-root','/Volumes/dashboard-cli-client','--yes','--json']));assert data['status']['hostReady']
  mounted=pathlib.Path('/Volumes/dashboard-cli-client');assert (mounted/'sentinel-mac-original.txt').read_text()=='Mac ordinary source remains in place\n'
  with (mounted/'sentinel-cli-client.txt').open('w') as f:f.write('preserved CLI nonroot path\n');f.flush();os.fsync(f.fileno())
  assert json.loads(cmd([str(binary),'status','--yes']))['hostReady']
  assert json.loads(cmd([str(binary),'reconnect','--yes']))['hostReady']
  cmd([str(binary),'detach','--yes','--drained']);assert ' /Volumes/dashboard-cli-client ' not in pathlib.Path('/proc/self/mountinfo').read_text()
 elif phase=='mac-detach':
  source=pathlib.Path.home()/'dashboard-data';assert (source/'sentinel-cli-client.txt').read_text()=='preserved CLI nonroot path\n'
  hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in source.glob('sentinel-*.txt')};marker=(source/'.autobyteus-nfs/storage.json').read_bytes()
  assert json.loads(cmd([str(binary),'reconnect','--yes']))['hostReady']
  cmd(['/usr/bin/sudo','--','/usr/bin/env','-u','SUDO_UID','-u','SUDO_GID','-u','SUDO_USER','/Library/AutoByteusNFS/libexec/autobyteus-nfs','detach','--yes','--drained'])
  assert '/Volumes/dashboard-' not in subprocess.check_output(['/sbin/mount'],text=True)
  assert {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in source.glob('sentinel-*.txt')}==hashes and (source/'.autobyteus-nfs/storage.json').read_bytes()==marker
 else:raise ValueError('unknown phase')
 r['result']='Pass (bounded native preserved CLI entry forms)'
except Exception as e:r['result']='Fail';r['error']=repr(e)
(root/('cli-'+phase+'-result.json')).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
