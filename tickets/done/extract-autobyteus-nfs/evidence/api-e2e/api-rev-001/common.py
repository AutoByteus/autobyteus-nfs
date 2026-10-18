from pathlib import Path
import json,subprocess,datetime,time,os
E=Path(__file__).resolve().parent;T=E.parents[2]
N=T.parents[2];S=Path('/Users/normy/autobyteus_org/autobyteus-worktrees/extract-autobyteus-nfs')
def write(name,value): (E/name).write_text(json.dumps(value,indent=2)+'\n')
def event(case,kind,observation,result='N/A',evidence=''):
 stamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with (T/'api-e2e-test-case-ledger.md').open('a') as f:f.write('| '+' | '.join([stamp,case,kind,observation.replace('|','/').replace('\n',' '),result,evidence])+' |\n')
 print(case,kind,observation,result,flush=True)
def run(name,cmd,cwd,env,expected=0,timeout=1200):
 start=time.time()
 with (E/(name+'.log')).open('w') as f:
  f.write('$ '+' '.join(map(str,cmd))+'\nCWD '+str(cwd)+'\n');f.flush()
  try:
   r=subprocess.run(cmd,cwd=cwd,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=timeout);code=r.returncode
  except subprocess.TimeoutExpired:code=124
 result=dict(name=name,command=list(map(str,cmd)),cwd=str(cwd),exit=code,expected=expected,seconds=round(time.time()-start,3),pass_=code==expected,log=name+'.log')
 with (E/'commands.jsonl').open('a') as f:f.write(json.dumps(result)+'\n')
 print(name,code,'expected',expected,flush=True)
 if code!=expected:raise RuntimeError(name+' exit '+str(code))
 return result
def envfor(p,go=False):
 env=dict(PATH=('/Users/normy/.nvm/versions/node/v22.21.1/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin'),HOME=str(p/'home'),TMPDIR=str(p/'tmp'),CI='true',COREPACK_ENABLE_DOWNLOAD_PROMPT='0',NO_COLOR='1')
 if go:env.update(PATH=str(p/'tools/go/bin')+':'+env['PATH'],GOCACHE=str(p/'go-cache'),GOMODCACHE=str(p/'go-mod-cache'),GOTOOLCHAIN='local')
 return env
