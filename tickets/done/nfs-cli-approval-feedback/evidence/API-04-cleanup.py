# API04 | 2026-10-24 | current4cf2eaa | read-only source/privacy audit and removal of own restored control scratch.
from pathlib import Path
import subprocess,os,hashlib,json,datetime,shutil,re
n=Path.cwd();t=n/'tickets/in-progress/nfs-cli-approval-feedback';e=t/'evidence';r=json.loads((e/'API-02-control.json').read_text());s=Path(r['scratch']);assert s.parent==Path('/Users/normy') and s.name.startswith('nfs-feedback-api-') and r['mutantRestored'] and r['result']=='Pass'
processes=[x for x in subprocess.check_output(['ps','-axo','pid=,command='],text=True).splitlines() if str(s) in x];assert not processes,processes
mismatch=[]
for row in r['inputs']:
 for base in [n,s/'source']:
  if hashlib.sha256((base/row['path']).read_bytes()).hexdigest()!=row['sha256']:mismatch.append(str(base/row['path']))
assert not mismatch
assert subprocess.check_output(['git','diff','--name-only','e15e5e8','--',':!tickets'],text=True).strip()==''
delta=subprocess.check_output(['git','diff','--name-only','456e5808','HEAD','--',':!tickets'],text=True).splitlines()
assert set(delta)=={'TESTING.md','docs/dashboard.md','internal/dashboard/browser.go','internal/dashboard/session.go','internal/dashboard/privilege.go','internal/dashboard/terminal.go','internal/dashboard/feedback_test.go','internal/dashboard/feedback_fixture_test.go','internal/dashboard/terminal_test.go','internal/dashboard/privilege_test.go'}
sourcehash=subprocess.check_output(['python3','packaging/release.py','--source-hash'],cwd=s/'source',env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','HOME':str(s/'home'),'TMPDIR':str(s/'tmp')},text=True).strip();assert sourcehash=='fbc95116f926879d24075493d82426226e08cec33508c13e7423c2719ad1ae46'
old=json.loads((e/'IMP-09-cleanup.json').read_text());assert old['ownedRootRemoved'] and not Path(old['ownedRoot']).exists()
shutil.rmtree(s)
rec={'case':'API-04','date':datetime.datetime.now(datetime.timezone.utc).isoformat(),'input':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'command':'python3 evidence/API-04-cleanup.py from worktree','environment':'Macarm64 own source/toolchain/cache; no browser/native/privileged resources','verifiedCurrentInputs':len(r['inputs']),'mismatches':mismatch,'sourceHash':sourcehash,'changedNonTicketPaths':delta,'unmodifiedProtectedOwners':'admin/adminwire/CLI/config/setup/service/platform/backend/docker/assets/HTTP/installer/workflows/locks','ownedProcessesBeforeRemoval':processes,'ownedScratch':str(s),'scratchRemoved':not s.exists(),'implementationScratchStillAbsent':True,'result':'Pass','cleanup':'Restored mutant, verified all inputs, removed only own private source/Go/build/cache/HOME/TMP. No operator/installed/PM/canonical/retained assets touched.'}
(e/'API-04-cleanup.json').write_text(json.dumps(rec,indent=2)+'\n');print(json.dumps(rec,indent=2))
p=t/'api-e2e-execution-coverage-report.md';p.write_text(p.read_text()+'| API-04 | AC006/all preserved | `python3 evidence/API-04-cleanup.py`; current input/protected-path/hash/privacy/docs + own cleanup; reuse IMP08/09 removal | API read-only Mac audit + own control scratch | Pass | API-04-cleanup.json:179inputs, mismatches=[], sourceHash expected, ownedProcessesBeforeRemoval=[], scratchRemoved=true | No production/durable edits; historical IMP09 cleanup verified absent; no VM/root/storage/browser/OS action |\n')
p=t/'api-e2e-test-progress.md';p.write_text(p.read_text()+f'| {rec["date"]} | API-04 | Completed | Pass179inputs unchanged; protected boundaries unchanged; restored mutant/new scratch removed; no owned process |\n')
