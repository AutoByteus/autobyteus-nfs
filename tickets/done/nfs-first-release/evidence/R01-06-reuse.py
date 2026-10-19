# Cases R01/R02; applicability/reuse and stale candidate; product3f67e36; local Macarm64/Python3.9.6;2026-10-19UTC.
from pathlib import Path
import subprocess,json,datetime,os,hashlib
E=Path(__file__).resolve().parent;T=E.parent;N=T.parents[2]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def git(*a):return subprocess.check_output(['git',*a],cwd=N,text=True)
def event(cid,kind,result,note):
 with (T/'api-e2e-test-progress.md').open('a') as f:f.write(f'| {now()} | {cid} | {kind} | {result} | {note} |\n')
def save(name,v):(E/name).write_text(json.dumps(v,indent=2)+'\n')
def row(cid,result,note):
 p=T/'api-e2e-execution-coverage-report.md';lines=p.read_text().splitlines()
 for i,l in enumerate(lines):
  if l.startswith('| '+cid+' |'):
   v=l.split('|');v[-3]=result;v[-2]=note;lines[i]='|'.join(v)
 p.write_text('\n'.join(lines)+'\n')
head=git('rev-parse','HEAD').strip();product='3f67e36193c246ca08b49cda818be5c0f94eba51'
assert git('diff','--name-only',product,head,'--',':!tickets')==''
assert git('diff','--name-only','--',':!tickets')==''
checks=json.loads((E/'IMP-07-results.json').read_text());assert checks['commit']==product and all(x['passed'] and x['exit']==x['expected'] for x in checks['checks'])
for name,key in [('IMP-07-05-python.log','Ran 58 tests'),('IMP-07-04-focused.log','Ran 23 tests'),('IMP-07-13-original-control.log','FAILED (failures=1)')]:
 data=(E/name).read_text();assert data.startswith('Check: IMP-07-') and key in data
native=json.loads((E/'IMP-07-03-identity-probe.json').read_text())
assert native['original']['signExit']==1 and native['with-owned-keychain']['signExit']==0 and native['with-owned-keychain']['verifyExit']==0 and native['removed-again']['signExit']==1
assert native['searchListExactlyRestored'] and native['ownedScratchRemoved'] and native['restoreExit']==native['deleteExit']==0
receipt={'case':'R01','step':'Read Checks Run, validate exact input applicability, preserve original failure; no local product or keychain repeat','date':now(),'commit':head,'testedCommit':product,'environment':'local read-only source/evidence audit','command':f"git diff --name-only {product} {head} -- ':!tickets'",'nonTicketDelta':[],'nonTicketCount':len([p for p in git('ls-files').splitlines() if not p.startswith('tickets/')]),'reused':['IMP-07-04','IMP-07-05','IMP-07-12','IMP-07-13'],'R02Reused':['IMP-07-06','IMP-07-07','IMP-07-08','IMP-07-09','IMP-07-10','IMP-07-11','IMP-07-14'],'supportingNative':['IMP-07-01','IMP-07-02','IMP-07-03'],'counts':{'fullCollected':58,'fullExecuted':57,'fullStandaloneSkip':1,'focusedOverlap':23,'detectedMutants':4},'nativeMechanism':'Actual synthetic identity absent→sign1; owned+original→sign0/verify0/runtime; removed→sign1, original list restored; timestamp=none nonrelease probe only','priorFailure':'DR01139210821088/1 bothMac sign/exit1/cleanupcomplete/unclassified; hosted original cause UNKNOWN','limits':'Full suite doubles external signing commands. Synthetic native mechanism does not prove real DeveloperID/P12/password/Intel/timestamp/notary or earlier hosted root cause. Native probe attributed Implementation, not rerun.','pass':True};save('R01-06-reuse.json',receipt)
row('R01','Pass','R01-06-reuse.json: exact127inputs; IMP07 full58/57executed/1skip,23focused overlap,4mutants. Supporting native A/B/A mechanism only; original DR011 cause UNKNOWN.')
event('R01','Completed','Pass','IMP07 exact127input applicability confirmed; R01-06-reuse.json; reuse not product/keychain rerun.')
event('R02','Started','Not Tested','Reuse IMP07 static/hash/no-candidate controls; execute actual old API005 admission refusal.')
cmd=['/usr/bin/python3','packaging/release.py','--check-publish','--candidate','/Users/normy/nfs-first-candidate-api005-61mqnd8a/candidate']
r=subprocess.run(cmd,cwd=N,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},text=True,capture_output=True,timeout=120)
(E/'R02-06-stale-candidate.log').write_text(f'# Case R02; command {cmd!r}; cwd {N}; commit{head}; local Macarm64/Python3.9.6; {now()}\n'+r.stdout+r.stderr+f'\nExit: {r.returncode}\n')
save('R02-06-stale-result.json',{'case':'R02','step':'Actual old retained candidate/current facade admission','date':now(),'commit':head,'environment':'local read-only facade; API005 retained candidate unchanged','command':cmd,'exit':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
assert r.returncode==1 and 'Candidate source/engine differs' in r.stderr
row('R02','Pass','R02-06-stale-result.json/log: actual old API005 refused Candidate source/engine differs; static/refusal controls reused with exact source.')
event('R02','Completed','Pass','Actual API005 source/engine mismatch refusal; no stale evidence promotion; static/hash controls reused.')
p=T/'api-e2e-execution-coverage-report.md'
with p.open('a') as f:f.write('''\n## Post-repository confidence and decision\nScores over current API prepublication scope: requirements75, directness75, integration75, identity90, failure85, CLI75, durable95;570/7=81.43%. Exact current repository controls and supporting native mechanism are useful but do not supply a fresh complete candidate. Broader validation Required: all four hosted native checks, two-architecture engine/full OCI/aggregation, actual envelope/download/integrity and native smoke. Actual signed release remains separately Not Proven/downstream, not implied by this scope.\n''')
print('R01/R02 PASS; actual stale refusal:',r.stderr.strip())
