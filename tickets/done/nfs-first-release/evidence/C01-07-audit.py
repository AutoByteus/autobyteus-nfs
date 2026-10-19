# C01; final own evidence/ownership audit, no product execution; source22205cc/current6cb497f; localmacOSarm64;2026-10-19UTC.
from pathlib import Path
import json,hashlib,datetime,subprocess,re
E=Path(__file__).resolve().parent;T=E.parent;N=T.parents[2]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=N,text=True)
owned=re.compile(r'^(?:R0[1-7]|C01)-07-')
files=sorted(p for p in E.iterdir() if p.is_file() and owned.match(p.name))
base=json.loads((E/'C01-07-ownership.json').read_text())
assert not git('diff','--name-only','22205cc84a29e6aa66ba5673b0a60c8db95ddc80','HEAD','--',':!tickets')
assert not git('diff','--name-only','--',':!tickets')
source=[p for p in git('ls-files').splitlines() if not p.startswith('tickets/')];assert len(source)==130
assert all(digest(N/p)==h for p,h in base['protected'].items())
history=(T/'api-e2e-revision-record.md').read_bytes()
assert hashlib.sha256(history[:base['historyBytes']]).hexdigest()==base['historySha256']
assert history.count(b'## API-REV-007')==1
progress=(T/'api-e2e-test-progress.md').read_text().split('## API-REV-007')[1]
assert all(len(re.findall(r'\| '+cid+r' \| Completed \| Pass \|',progress))==1 for cid in ['R01','R02','R03','R04','R05','R06','R07','C01'])
assert 'Initial orchestrator expected later hash guard' in progress
secret=[]
for p in files:
 data=p.read_text()
 if p.suffix=='.json':json.loads(data)
 if p.suffix=='.jsonl':
  for line in data.splitlines():json.loads(line)
 if p.suffix=='.py':compile(data,str(p),'exec')
 if re.search(r'(?:ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----)',data):secret.append(p.name)
 assert all(l.rstrip()==l for l in data.splitlines()),p.name
assert not secret
cleanup=json.loads((E/'C01-07-cleanup.json').read_text());assert cleanup['pass'] and cleanup['realWrites']==0
assert not Path(cleanup['inspectionRoot']).exists()
clone=json.loads((E/'R07-07-cleanup.json').read_text());assert clone['absent'] and not Path(clone['root']).exists()
assert not (N/'packaging/recovery/v0.1.0/authorization.json').exists()
emulation=json.loads((E/'R07-07-result.json').read_text())
assert emulation['pass'] and emulation['syntheticAuthorityOnly'] and not emulation['realAuthorizationCreated']
assert emulation['completedRetryNoWrites'] and emulation['publicAssetCount']==18
assert emulation['excludedDriftRefusal'].startswith('Unreviewed recovery change:')
report=(T/'api-e2e-execution-coverage-report.md').read_text()
for clause in ['Pass95.00% for affected SR005 executor validation only','DR013 publication remains Blocked','BOTH actual Mac binaries','43Deferred+2Downstream','Not Proven','not full76 rerun','Required and executed','Proportional test-code review: **Required**']:
 assert clause in report,clause
canonical={'api-e2e-coverage-investigation.md','api-e2e-execution-coverage-report.md','api-e2e-revision-record.md','api-e2e-test-progress.md'}
for line in git('status','--porcelain','--untracked-files=all').splitlines():
 p=Path(line[3:]);assert (p.parent==T.relative_to(N) and p.name in canonical) or (p.parent==E.relative_to(N) and owned.match(p.name)),str(p)
result={'case':'C01','step':'Final own artifact/identity/ownership audit; no product rerun','date':datetime.datetime.now(datetime.timezone.utc).isoformat(),'commit':git('rev-parse','HEAD').strip(),'environment':'NFS ticket only/localMacarm64','sourceInputsUnchanged':130,'otherOwnerFilesPreserved':len(base['protected']),'historyPrefixPreserved':True,'eightScopedCasesCompleted':True,'evidenceFilesChecked':len(files),'jsonAndOrchestratorSyntaxValid':True,'secretPatternHits':secret,'whitespaceExceptions':[],'ownedResourcesAbsent':True,'syntheticAuthorityNeverReal':True,'realPublicationNotClaimed':True,'pass':True}
(E/'C01-07-artifact-checks.json').write_text(json.dumps(result,indent=2)+'\n')
print('C01 API007 ARTIFACT AUDIT PASS',len(files),'files; real publication remains unproven')
