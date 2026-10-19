# Case R01/R02; exact-input reuse and actual stale-candidate refusal; reviewed1c00b7a/product2c12ec6; local Macarm64/Python3.9.6;2026-10-19.
from pathlib import Path
import subprocess,json,datetime,os
E=Path(__file__).resolve().parent;T=E.parent;N=T.parents[2]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def git(*a):return subprocess.check_output(['git',*a],cwd=N,text=True)
def event(cid,kind,result,note):
 with (T/'api-e2e-test-progress.md').open('a') as f:f.write(f'| {now()} | {cid} | {kind} | {result} | {note} |\n')
def save(name,v):(E/name).write_text(json.dumps(v,indent=2)+'\n')
head=git('rev-parse','HEAD').strip();product='2c12ec61f6339d0d264280b7117787ec821425af'
assert git('diff','--name-only',product,head,'--',':!tickets')==''
assert git('diff','--name-only','--',':!tickets')==''
checks=json.loads((E/'IMP-06-results.json').read_text());assert checks['commit']==product and all(x['passed'] and x['exit']==x['expected'] for x in checks['checks'])
for name,key in [('IMP-06-02-python.log','OK (skipped=1)'),('IMP-06-01-focused.log','Ran 21 tests in 85.765s'),('IMP-06-10-original-control.log','FAILED (failures=11)')]:
 data=(E/name).read_text();assert data.startswith('Check: IMP-06-') and key in data
receipt={'case':'R01','step':'Read prior DR009 actual failure and reuse exact current implementation checks; no local product rerun','date':now(),'commit':head,'testedCommit':product,'environment':'local read-only source/evidence audit','command':f"git diff --name-only {product} {head} -- ':!tickets'",'nonTicketDelta':[],'nonTicketCount':len([p for p in git('ls-files').splitlines() if not p.startswith('tickets/')]),'reused':['IMP-06-01','IMP-06-02','IMP-06-09','IMP-06-10'],'R02Reused':['IMP-06-03','IMP-06-04','IMP-06-05','IMP-06-06','IMP-06-07','IMP-06-08','IMP-06-11'],'counts':{'fullCollected':56,'fullExecuted':55,'fullStandaloneSkip':1,'focusedOverlap':21,'detectedMutants':4},'priorFailure':'DR00939204643596/1 bothMac sign/exit1/cleanupcomplete unresolved; cause UNKNOWN; diagnostic source only','limits':'External commands doubled; initial fixture-shadowing46 failures preserved/corrected by Implementation, not current product failure. No Apple/release proof.','pass':True};save('R01-05-reuse.json',receipt)
p=T/'api-e2e-execution-coverage-report.md';s=p.read_text().replace('|Not Tested|Pending audit; no product rerun planned|','|Pass|Reused current exact127inputs; R01-05-reuse.json. Original evidence/outcomes in IMP Checks Run;56/55executed/1expectedskip,21focused overlaps,4mutants detected; no local product rerun.|');p.write_text(s)
event('R01','Completed','Pass','IMP06 exact127input applicability confirmed; R01-05-reuse.json. Reused, not rerun.')
event('R02','Started','Not Tested','Reused03–08/11; actual old API004 candidate admission additionally exercised.')
cmd=['/usr/bin/python3','packaging/release.py','--check-publish','--candidate','/Users/normy/nfs-first-candidate-api004-a7bxyrbb/candidate']
r=subprocess.run(cmd,cwd=N,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},text=True,capture_output=True,timeout=120)
(E/'R02-05-stale-candidate.log').write_text(f'# Case R02; command {cmd!r}; cwd {N}; commit{head}; local Macarm64/Python3.9.6; {now()}\n'+r.stdout+r.stderr+f'\nExit: {r.returncode}\n')
save('R02-05-stale-result.json',{'case':'R02','step':'Actual old retained candidate/current facade admission','date':now(),'commit':head,'environment':'local read-only facade; API004 retained candidate unchanged','command':cmd,'exit':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
print('STALE',r.returncode,r.stderr)
