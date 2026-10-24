"""Own-PTY launch of final installed public binary. Actual Run; sandbox refuses sudo before execution, never touch storage."""
import datetime,hashlib,json,os,pathlib,pty,re,select,signal,subprocess,time
E=pathlib.Path(__file__).resolve().parent
S=pathlib.Path(json.loads((E/'resources.json').read_text())['root'])
# This file must only be executed after public install identity checks succeed.
receipt=json.loads((E/'public-install.json').read_text())
assert receipt['result']=='Pass' and receipt['version']=='v0.2.1'
binary=pathlib.Path(receipt['installedBinary']);home=pathlib.Path(receipt['home'])
assert binary.is_relative_to(S) and home.is_relative_to(S)
assert hashlib.sha256(binary.read_bytes()).hexdigest()==receipt['binarySHA256']
results=[]
for role in ('server','client'):
    private=S/('role-'+role);private.mkdir(mode=0o700);tmp=private/'tmp';tmp.mkdir(mode=0o700)
    env=dict(os.environ,HOME=str(home),TMPDIR=str(tmp),XDG_CONFIG_HOME=str(private/'config'),XDG_CACHE_HOME=str(private/'cache'))
    pid,fd=pty.fork()
    if pid==0:
        os.chdir(private)
        os.execve('/usr/bin/sandbox-exec',['sandbox-exec','-p','(version 1)(allow default)(deny process-exec (literal "/usr/bin/open"))(deny process-exec (literal "/usr/bin/sudo"))',str(binary),role],env)
    raw=b'';status=None;url=None;start=time.monotonic();browser_exit=None
    try:
        while time.monotonic()-start<30:
            if select.select([fd],[],[],1)[0]:
                try:raw+=os.read(fd,65536)
                except OSError:break
                match=re.search(rb'http://127\.0\.0\.1:[0-9]+/#[A-Za-z0-9_-]+',raw)
                if match:url=match.group().decode();break
        assert url,'No private fallback URL observed (private log retained only in owned scratch)'
        inp=private/'launch.json';inp.write_text(json.dumps({'url':url,'role':role,'home':str(home)}));os.chmod(inp,0o600)
        node_env=dict(env,PLAYWRIGHT_BROWSERS_PATH=str(S/'browsers'),NFS_SMOKE_PLAYWRIGHT=str(S/'browser-tools/node_modules/playwright/index.js'),NFS_SMOKE_PRIVATE_INPUT=str(inp),NFS_SMOKE_EVIDENCE=str(E))
        proc=subprocess.run(['node',str(E/'public-feedback-browser.cjs')],env=node_env,capture_output=True,text=True,timeout=90)
        browser_exit=proc.returncode
        (E/('public-'+role+'-browser.log')).write_text(proc.stdout+proc.stderr+'\nexit='+str(proc.returncode)+'\n')
        assert proc.returncode==0,'Browser launch smoke failed; see sanitized log'
        for _ in range(60):
            ended,code=os.waitpid(pid,os.WNOHANG)
            if ended:status=code;break
            if select.select([fd],[],[],0.2)[0]:
                try:raw+=os.read(fd,65536)
                except OSError:pass
            time.sleep(0.1)
        assert status is not None and os.waitstatus_to_exitcode(status)==0,'Dashboard did not stop cleanly'
        while select.select([fd],[],[],0.1)[0]:
            try:
                part=os.read(fd,65536)
                if not part:break
                raw+=part
            except OSError:break
        assert b'Waiting for administrator approval and setup helper.' in raw
        assert b'Could not start the administrator helper.' in raw
        assert b'Administrator access confirmed.' not in raw and b'Dashboard ready' not in raw
        assert b'Storage is NOT disconnected.' in raw
    finally:
        if status is None:
            # Only own non-admin UI process; graceful stop, never forced storage cancel.
            try:os.kill(pid,signal.SIGINT)
            except ProcessLookupError:pass
            for _ in range(50):
                ended,code=os.waitpid(pid,os.WNOHANG)
                if ended:status=code;break
                time.sleep(0.1)
        os.close(fd)
        safe=re.sub(rb'http://127\.0\.0\.1:[0-9]+/#[A-Za-z0-9_-]+',b'http://127.0.0.1:[owned-port]/#[redacted]',raw)
        (E/('public-'+role+'-terminal.log')).write_bytes(safe)
        results.append({'role':role,'pid':pid,'exit':os.waitstatus_to_exitcode(status) if status is not None else None,'browserExit':browser_exit,'result':'Pass' if status==0 and browser_exit==0 else 'Fail','bootstrapFilesRemaining':len(list(tmp.rglob('open-dashboard.html'))),'sandbox':'Deny OS opener and sudo exec; explicit authorization request fails locally before child starts; no elevation/storage'})
        (E/'public-feedback-smoke.json').write_text(json.dumps({'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'binarySHA256':receipt['binarySHA256'],'version':'v0.2.1','roles':results,'limits':'Current Mac ARM64 published install launch only; no root/storage/field proof'},indent=2)+'\n')
    assert not list(tmp.rglob('open-dashboard.html'))
print('Both final published role feedback/launch/Stop controls passed; inspect screenshots separately')
