# IMP-06 | current IR001 source | 2026-10-24 | Macarm64 actual PTY/current Session+HTTP, protocol doubles
import os,sys,pathlib,pty,select,time,subprocess,json,shutil
R=pathlib.Path(sys.argv[1]);E=pathlib.Path(sys.argv[2]);results=[]
for role,mode in [('server','success'),('client','success'),('server','denied'),('client','refused'),('server','hold-hello'),('client','hold-inspect')]:
 d=R/('preview-'+role+'-'+mode);d.mkdir(mode=0o700)
 env=dict(os.environ,HOME=str(R/'home'),TMPDIR=str(R/'tmp'),NFS_FB_DIR=str(d),NFS_FB_ROLE=role,NFS_FB_MODE=mode,PLAYWRIGHT_BROWSERS_PATH=str(R/'browsers'),NFS_PLAYWRIGHT_MODULE=str(R/'browser-tools/node_modules/playwright/index.js'))
 if mode!='hold-hello':(d/'hello').touch()
 if mode not in ('hold-inspect','hold-hello'):(d/'inspect').touch()
 pid,fd=pty.fork()
 if pid==0:os.execve(str(R/'dashboard-preview'),['dashboard-preview','-test.run=^TestFeedbackPreview$','-test.timeout=60s'],env)
 output='';node=None;status=None
 def pump():
  global output
  if select.select([fd],[],[],0.03)[0]:
   try:output+=os.read(fd,65536).decode('utf8','replace')
   except OSError:pass
 def wait(check):
  end=time.monotonic()+25
  while not check():
   pump()
   if node and node.poll() is not None and node.returncode!=0:
    stdout,stderr=node.communicate();raise AssertionError('browser failed: '+stderr)
   if time.monotonic()>end:raise AssertionError('fixture wait timed out; '+output)
 try:
  wait(lambda:(d/'connection.json').exists())
  node=subprocess.Popen(['node',str(E/'IMP-06-browser.cjs')],env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
  wait(lambda:'Waiting for administrator approval' in output)
  if mode=='hold-hello':
   assert 'Administrator access confirmed.' not in output
   os.write(fd,b'\x03');wait(lambda:'Fixture stopping admission' in output)
   before=output;(d/'hello').touch();(d/'inspect').touch();(d/'browser-go').touch()
  elif mode=='hold-inspect':
   wait(lambda:'Preparing setup controls' in output);assert 'Dashboard ready' not in output
   (d/'browser-go').touch();wait(lambda:'Fixture stopping admission' in output)
   before=output;(d/'inspect').touch()
  wait(lambda:'Fixture drain complete.' in output)
  _,status=os.waitpid(pid,0);status=os.waitstatus_to_exitcode(status)
  stdout,stderr=node.communicate(timeout=10)
  assert status==0 and node.returncode==0,(status,node.returncode,stderr)
  if mode.startswith('hold-'):assert 'Dashboard ready' not in output and 'Still ' not in output.split('Fixture stopping admission',1)[1]
  elif mode=='success':assert output.index('Administrator access confirmed.')<output.index('Preparing setup controls')<output.index('Dashboard ready')
  elif mode=='denied':assert 'Administrator access was not confirmed.' in output and 'Administrator access confirmed.' not in output
  elif mode=='refused':assert 'saved configuration could not be read' in output and 'Dashboard ready' not in output
  assert '/#' not in output and 'Bearer ' not in output
  log=E/f'IMP-06-{role}-{mode}.log';log.write_text(f'# IMP-06 | IR001 source | Macarm64 PTY/current Session, no sudo | 2026-10-24\n'+output+'\n'+stdout)
  if (d/'ready.png').exists():shutil.copyfile(d/'ready.png',E/f'IMP-06-{role}-ready.png')
  results.append(dict(role=role,mode=mode,fixtureExit=status,browserExit=node.returncode,result='pass'))
 finally:
  (E/f'IMP-06-{role}-{mode}-transcript.log').write_text('# IMP-06 | 459c02f | current Session/PTY fixture | 2026-10-24\n'+output)
  # Release only owned fixture gates; never kill admitted work to claim drain.
  (d/'hello').touch();(d/'inspect').touch();(d/'browser-go').touch()
  if status is None:
   os.write(fd,b'\x03');os.waitpid(pid,0)
  if node and node.poll() is None:node.communicate(timeout=30)
  os.close(fd);shutil.rmtree(d)
(E/'IMP-06-result.json').write_text(json.dumps(dict(check='IMP-06',date='2026-10-24',scope='Current Session/HTTP/assets+PTY and owned Chromium; signal/Stop fixture driver, NOT Run/OS opener/sudo/password/storage proof',cases=results),indent=2)+'\n')
print(json.dumps(results))
