# Case R01/R02; step: confirm current exact-input reuse; commit44e2487; local macOS arm64; 2026-10-19UTC.
from pathlib import Path
import subprocess,json,datetime,hashlib,os
E=Path(__file__).resolve().parent;T=E.parent;N=T.parents[2]
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def git(*args):return subprocess.check_output(['git',*args],cwd=N,text=True)
head=git('rev-parse','HEAD').strip();diff=git('diff','--name-only','75f4dbe5527a7159f536bafcf9448bc2d6a01604',head,'--',':!tickets');assert diff==''
assert git('diff','--name-only','--',':!tickets')==''
checks=json.loads((T/'implementation-evidence/ir-005/checks-result.json').read_text())
assert all(x['passed'] for x in checks)
for name,key in [('IMP-05-01-python-full.log','Ran 52 tests in 106.834s'),('IMP-05-02-signing-workflow.log','Ran 17 tests in 69.569s'),('IMP-05-09-baseline-control.log','FAILED (failures=1)')]:
    data=(E/name).read_text();assert data.startswith('Check: IMP-05-');assert key in data
receipt={'case':'R01','step':'Reuse current implementation Checks Run; no product suite rerun','utc':now(),'currentCommit':head,'testedProductCommit':'75f4dbe5527a7159f536bafcf9448bc2d6a01604','environment':'local read-only Git/evidence comparison','command':f"git diff --name-only 75f4dbe {head} -- ':!tickets'",'nonTicketDelta':[],'nonTicketCount':len([p for p in git('ls-files').splitlines() if not p.startswith('tickets/')]),'reused':['IMP-05-01','IMP-05-02','IMP-05-08','IMP-05-09'],'R02Reusable':['IMP-05-03','IMP-05-04','IMP-05-05','IMP-05-06','IMP-05-07'],'testCounts':{'fullCollected':52,'fullExecuted':51,'fullStandaloneSkip':1,'focusedOverlap':17},'currentChecksExpectedOutcomes':len(checks),'limits':'Command doubles, not real Apple/P12/hosted upload; baseline/mutants are expected failures. DR007 is local development diagnostic only.','pass':True}
(E/'R01-04-reuse.json').write_text(json.dumps(receipt,indent=2)+'\n')
p=T/'api-e2e-execution-coverage-report.md';s=p.read_text().replace('| R01 |003/004/006/008|Reuse IMP-05-01/02/08/09 after input comparison|See IMP Checks Run|Not Tested|See implementation handoff|Reuse decision pending identity audit|','| R01 |003/004/006/008|Reused IMP-05-01/02/08/09|See IMP Checks Run|Pass|See IMP Checks Run evidence/quoted outcomes; R01-04-reuse.json identity receipt|127 non-ticket files match tested75f4dbe; full52/51executed/1childskip, focused17 overlap,4 detected mutants and expected baseline diagnostic failure. Not independently rerun.|');p.write_text(s)
with (T/'api-e2e-test-progress.md').open('a') as f:f.write(f'| {now()} | R01 | Completed | Pass | Reused exact current IMP-05-01/02/08/09; all127 inputs unchanged; no duplicate product check. |\n| {now()} | R02 | Started | Not Tested | Reuse clear IMP-05-03–07; additionally execute actual old-candidate refusal (missing-input control did not cover it). |\n')
cmd=['/usr/bin/python3','packaging/release.py','--check-publish','--candidate','/Users/normy/nfs-first-candidate-api003-p_t67xqw/candidate']
env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1'
r=subprocess.run(cmd,cwd=N,env=env,text=True,capture_output=True,timeout=120)
(E/'R02-04-stale-candidate.log').write_text(f'# Case R02; command {cmd!r}; commit {head}; cwd {N}; local macOS arm64/Python3.9.6; {now()}\n'+r.stdout+r.stderr+f'\nExit: {r.returncode}\n')
print('STALE RESULT',r.returncode,r.stdout,r.stderr)
(E/'R02-04-stale-result.json').write_text(json.dumps({'case':'R02','step':'Actual retained old-candidate admission','utc':now(),'commit':head,'environment':'local macOS/current facade; read-only old API003 candidate','command':cmd,'exit':r.returncode,'stdout':r.stdout,'stderr':r.stderr},indent=2)+'\n')
