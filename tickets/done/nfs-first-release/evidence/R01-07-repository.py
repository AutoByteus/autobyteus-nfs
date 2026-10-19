# Cases R01–R03; read applicable IMP evidence, current refusals/carried original identity;6cb497f/22205cc; macOS26.5.2arm64 Python3.9.6;2026-10-19UTC.
from pathlib import Path
import sys,json,subprocess,datetime,hashlib
E=Path(__file__).resolve().parent;T=E.parent;N=T.parents[2];sys.path.insert(0,str(N/'packaging'))
from release_support import candidate,publication,source_context as sc,identity as i

def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def git(*a):return subprocess.check_output(['git',*a],cwd=N,text=True)
def save(cid,name,obj):(E/f'{cid}-07-{name}.json').write_text(json.dumps(obj,indent=2)+'\n')
def event(cid,kind,result,note):
 with (T/'api-e2e-test-progress.md').open('a') as f:f.write(f'| {now()} | {cid} | {kind} | {result} | {note} |\n')
def row(cid,result,note):
 p=T/'api-e2e-execution-coverage-report.md';lines=p.read_text().splitlines()
 for idx,l in enumerate(lines):
  if l.startswith('| '+cid+' |'):
   a=l.split('|');a[-3]=' '+result+' ';a[-2]=' '+note+' ';lines[idx]='|'.join(a)
 p.write_text('\n'.join(lines)+'\n')
H=git('rev-parse','HEAD').strip();source='22205cc84a29e6aa66ba5673b0a60c8db95ddc80';prod='4c665e0eb23adf1f9bb45363a496b7786e76b138';P='238bdc183e8affac99ffdee9be9cb333b0eb126f'
assert git('diff','--name-only',source,H,'--',':!tickets')=='' and git('diff','--name-only','--',':!tickets')==''
assert git('diff','--name-only',prod,source,'--',':!tickets').splitlines()==['scripts/tests/test_nfs_release_publication.py']
for x in ['06','10']:
 r=i.read_json(E/f'IMP-09-{x}-checks.json');assert r['result']=='pass' and all(c['exit']==0 for c in r['checks'])
mut=i.read_json(E/'IMP-09-05-mutations.json');assert len(mut['checks'])==6 and all(x['detected'] and x['exit']==1 for x in mut['checks'])
assert 'Ran 72 tests' in (E/'IMP-09-06-python.log').read_text() and 'OK (skipped=1)' in (E/'IMP-09-06-python.log').read_text()
assert 'Ran 15 tests' in (E/'IMP-09-10-python.log').read_text() and 'OK' in (E/'IMP-09-10-python.log').read_text()
meta={'date':now(),'commit':H,'environment':'macOS26.5.2arm64 current source/read-only evidence audit','command':'R01-07-repository.py'}
save('R01','reuse',meta|{'case':'R01','exactInputs':130,'reused':['IMP-09-06','IMP-09-10','IMP-09-05','IMP-09-07','IMP-09-11'],'fullAtProduction':{'collected':72,'executed':71,'skip':1},'finalPublicationSuite':15,'onlySubsequentTestDelta':'scripts/tests/test_nfs_release_publication.py','noClaimFull76Rerun':True,'mutantsDetected':6,'priorAttempts':'IMP09-01 alias2errors corrected;03 interrupted no verdict;07 saved endpoints not fresh API','pass':True})
row('R01','Pass','R01-07-reuse.json; IMP09 full72/71+1skip and current publication15 overlap,6mutants;130sameinputs. Attributed reuse, not rerun.')
event('R01','Completed','Pass','IMP09 exact applicability confirmed; no duplicate suite for independence.')
event('R02','Started','Not Tested','Current facade strict candidate and real tag-derived absent-authority refusal; no effects.')
C=Path('/Users/normy/nfs-first-candidate-api006-a8aune30/candidate')
cmd=['/usr/bin/python3','packaging/release.py','--operation','verify-candidate','--directory',str(C)]
p=subprocess.run(cmd,cwd=N,text=True,capture_output=True,timeout=180)
(E/'R02-07-candidate-refusal.log').write_text(f'# R02; {cmd!r}; commit{H}; cwd{N}; local Macarm64;{now()}\n'+p.stdout+p.stderr+f'\nExit:{p.returncode}\n')
assert p.returncode==1 and 'Candidate source/engine differs' in p.stderr
calls=[];original=publication.api
def observe(endpoint,method='GET',body=None,missing=False):
 assert method=='GET' and body is None
 result=original(endpoint,method,body,missing);calls.append({'endpoint':endpoint,'method':method,'result':result});return result
publication.api=observe
try:
 with publication.context_for('v0.1.0',dispatch=False):raise AssertionError('No real authority must exist')
except ValueError as error:
 assert str(error)=='Reviewed recovery authorization required';refusal=str(error)
finally:publication.api=original
save('R02','refusals',meta|{'case':'R02','date':now(),'candidateExit':p.returncode,'candidateStderr':p.stderr,'authorityRefusal':refusal,'actualReadOnlyRequests':calls,'realAuthorizationAbsent':not (N/'packaging/recovery/v0.1.0/authorization.json').exists(),'pass':True})
row('R02','Pass','R02-07-refusals.json/log: current candidate source/engine differs; actual tag-bound path refuses Reviewed recovery authorization required before effects.')
event('R02','Completed','Pass','Current strict candidate/absent real authority refuse, GET-only; no authorization created.')
event('R03','Started','Not Tested','Carry API006 original product build/candidate by exact record/member identity; not new executor build.')
record=i.read_json(E/'R04-06-candidate.json');ref=i.read_json(E/'R04-06-reference.json');assert i.sha(C/'candidate.json')==ref['recordSha256']
for name,entry in record['members'].items():assert i.file_record(C/name)==entry
with sc.frozen(sc.current(),P) as sourcectx:assert sourcectx.source_hash()==record['sourceHash']
save('R03','carried',meta|{'case':'R03','originalProductSource':P,'candidateRecordSha256':ref['recordSha256'],'runId':record['runId'],'sourceHash':record['sourceHash'],'memberBytesUnchanged':True,'priorEvidence':'API006 R03/R04 (native4/engine2/fullOCI, run39213489075/1)','scope':'Original product only, not current executor native build or recovery publication','pass':True})
row('R03','Pass — Reused','R03-07-carried.json; original API006 candidate/native4/engine2/OCI bytes exact to P; no E rebuild claim.')
event('R03','Completed','Pass','Original API006 record/members/hash matchP; unchanged exact product evidence carries.')
with (T/'api-e2e-execution-coverage-report.md').open('a') as f:f.write('\n## Post-repository confidence / broader gate\nCurrent recovery scope: AC75/directness85/integration75/identity90/failure90/CLI90/durable95 =600/7=85.71%. Broader Required: saved endpoints are not fresh retention/draft proof; run actual read-only inspect-bound and discovery then current full path with real bytes/emulated effects. Actual recovery authorization/public effects remain separate mandatory Delivery work.\n')
print('R01–R03 PASS')
