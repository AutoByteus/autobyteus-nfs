# Case C01; audit final API005 evidence/ownership, no product execution; product2c12ec6; local Macarm64;2026-10-19.
from pathlib import Path
import json,hashlib,datetime,subprocess,re
E=Path(__file__).resolve().parent;T=E.parent;N=T.parents[2]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=N,text=True)
own=json.loads((E/'C01-05-ownership.json').read_text());files=sorted(p for p in E.iterdir() if p.is_file() and re.match(r'^(?:R0[1-5]|C01)-05-',p.name))
assert git('diff','--name-only','2c12ec6','HEAD','--',':!tickets')=='' and git('diff','--name-only','--',':!tickets')==''
source=[p for p in git('ls-files').splitlines() if not p.startswith('tickets/')];assert len(source)==127
assert all(digest(N/p)==h for p,h in own['DeliveryFiles'].items())
history=(T/'api-e2e-revision-record.md').read_bytes();assert hashlib.sha256(history[:own['historyBytes']]).hexdigest()==own['historySha256']
progress=(T/'api-e2e-test-progress.md').read_text().split('## API-REV-005')[1]
assert all(len(re.findall(r'\| '+cid+r' \| Completed \| Pass \|',progress))==1 for cid in ['R01','R02','R03','R04','R05','C01'])
secret=[];whitespace=[]
for p in files:
 data=p.read_text()
 if p.suffix=='.json':json.loads(data)
 if p.suffix=='.jsonl':
  for line in data.splitlines():json.loads(line)
 if p.suffix=='.py':compile(data,str(p),'exec')
 if re.search(r'(?:ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----)',data):secret.append(p.name)
 if not p.name.startswith('R03-05-job-'):assert not data.endswith('\n\n'),p.name
 dirty=[i for i,l in enumerate(data.splitlines(),1) if l.rstrip()!=l]
 if dirty:
  assert p.name.startswith('R03-05-job-') or p.name.startswith('R03-05-excerpt-'),(p.name,dirty)
  whitespace.append({'file':p.name,'trailingWhitespaceLines':len(dirty),'reason':'Original raw captured log preserved, not authored-source waiver'})
assert not secret
report=(T/'api-e2e-execution-coverage-report.md').read_text();assert 'DR009' in report and 'NOT a signing/root-cause fix' in report and 'Pass95.00%' in report
out={'case':'C01','step':'Final own-evidence/ownership audit','date':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sourceCommit':'1c00b7afd6327fb4ba69dbc176c69d698a309fee','environment':'NFS ticket only; no product suite repeat','sourceInputsUnchanged':127,'DeliveryProtected':len(own['DeliveryFiles']),'priorHistoryPrefixPreserved':True,'sixCasesCompleted':True,'jsonAndOrchestratorSyntaxValid':True,'secretPatternHits':secret,'rawLogWhitespaceExceptions':whitespace,'pass':True}
(E/'C01-05-artifact-checks.json').write_text(json.dumps(out,indent=2)+'\n');print('ARTIFACT AUDIT PASS',len(files),'files',len(whitespace),'raw log whitespace exceptions')
