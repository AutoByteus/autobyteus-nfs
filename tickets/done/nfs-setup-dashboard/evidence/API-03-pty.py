# API-03/04/05, 2026-10-24, source d9beb0f+review receipt only, owned Ubuntu.
# Public role in actual controlling PTY; secret transmitted privately, never logged.
import os,pty,threading,re,time,sys,json,pathlib,signal
role=sys.argv[1]; root=pathlib.Path.home()/'api-dashboard';binary=root/'autobyteus-nfs'; output=''
pid,fd=pty.fork()
if pid==0: os.execv(str(binary),[str(binary),role])
def read():
 global output
 while True:
  try: b=os.read(fd,4096)
  except OSError: break
  if not b:break
  output+=b.decode(errors='replace')
thread=threading.Thread(target=read,daemon=True);thread.start()
end=time.monotonic()+25
while time.monotonic()<end:
 m=re.search(r'(http://127\.0\.0\.1:\d+)/#([A-Za-z0-9_-]+)',output)
 if m:print(json.dumps({'pid':pid,'url':m.group(0)}),flush=True);break
 time.sleep(.05)
else:
 os.kill(pid,signal.SIGTERM)
 print(json.dumps({'error':'public launch failed','terminal':output}),flush=True)
_,status=os.waitpid(pid,0);os.close(fd);thread.join(2)
safe=re.sub(r'http://127\.0\.0\.1:\d+/#\S+','[PRIVATE URL REDACTED]',output)
print(json.dumps({'exit':os.waitstatus_to_exitcode(status),'terminal':safe}),flush=True)
