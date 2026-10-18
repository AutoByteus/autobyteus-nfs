from pathlib import Path
import json,subprocess,datetime,time,os,hashlib
E=Path(__file__).resolve().parent;T=E.parents[2];N=T.parents[2]
def write(name,value):(E/name).write_text(json.dumps(value,indent=2)+'\n')
def event(case,kind,observation,result='N/A',evidence=''):
 with (T/'api-e2e-test-case-ledger.md').open('a') as f:f.write('| '+' | '.join([datetime.datetime.now(datetime.timezone.utc).isoformat(),case,kind,observation.replace('|','/').replace('\n',' '),result,evidence])+' |\n')
 print(case,kind,observation,result,flush=True)
def run(name,cmd,cwd=None,env=None,expected=0,timeout=1200):
 t=time.time()
 with (E/(name+'.log')).open('w') as log:
  log.write('$ '+' '.join(map(str,cmd))+'\nCWD '+str(cwd)+'\n');log.flush()
  try:code=subprocess.run(cmd,cwd=cwd,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=timeout).returncode
  except subprocess.TimeoutExpired:code=124
 r=dict(name=name,command=list(map(str,cmd)),cwd=str(cwd),exit=code,expected=expected,seconds=round(time.time()-t,3),pass_=code==expected,log=name+'.log')
 with (E/'commands.jsonl').open('a') as f:f.write(json.dumps(r)+'\n')
 print(name,code,'expected',expected,flush=True)
 if code!=expected:raise RuntimeError(name+' exit '+str(code))
 return r
