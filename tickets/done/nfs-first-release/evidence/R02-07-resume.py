# Cases R02/R03 resume; original R01 complete, initial R02 expected wrong first refusal; read applicable IMP evidence, current refusals/carried original identity;6cb497f/22205cc; macOS26.5.2arm64 Python3.9.6;2026-10-19UTC.
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
observed='Executed workflow differs from hashed source'
log=(E/'R02-07-candidate-refusal.log').read_text();assert 'Release refused: '+observed in log and 'Exit:1' in log
C=Path('/Users/normy/nfs-first-candidate-api006-a8aune30/candidate')
meta={'date':now(),'commit':H,'environment':'macOS26.5.2arm64 current facade; actual read-only API','command':'R02-07-resume.py; reuse earlier actual CLI refusal, no repeat'}
save('R02','attempt-note',meta|{'case':'R02','initialHarnessAssertion':'Expected later source/engine differs but actual earlier guard says Executed workflow differs from hashed source','classification':'Test-orchestrator expectation corrected, no product failure or guard weakening','preserved':'R01-07-repository.py and R02-07-candidate-refusal.log','cliRerun':False})
event('R02','Checkpoint','Not Tested','Initial orchestrator expected later hash guard; actual workflow guard correctly refuses first. Preserve raw result; resume without repeating completed R01/CLI.')
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
save('R02','refusals',meta|{'case':'R02','date':now(),'candidateExit':1,'candidateStderr':observed,'authorityRefusal':refusal,'actualReadOnlyRequests':calls,'realAuthorizationAbsent':not (N/'packaging/recovery/v0.1.0/authorization.json').exists(),'pass':True})
row('R02','Pass','R02-07-refusals.json/log: current candidate workflow mismatch; actual tag-bound path refuses Reviewed recovery authorization required before effects.')
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
