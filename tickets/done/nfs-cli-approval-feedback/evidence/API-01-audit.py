# API01 | 2026-10-24 | input4cf2eaa / finaltests e15e5e8 | local read-only Git/log/assertion audit, no product test rerun.
import pathlib,subprocess,json,re,datetime
n=pathlib.Path.cwd();t=n/'tickets/in-progress/nfs-cli-approval-feedback';e=t/'evidence'
def text(p):return (e/p).read_text()
def diff(a):return subprocess.check_output(['git','diff','--name-only',a,'HEAD','--',':!tickets'],text=True).splitlines()
assert diff('459c02f')==['internal/dashboard/feedback_fixture_test.go'];assert diff('e15e5e8')==[]
full=text('IMP-04-go-race.log');final=text('IMP-04-dashboard-final.log');red=text('IMP-02-original-red.log');green=text('IMP-03-focused-first.log')
counts={'baselineRed':len(re.findall(r'--- FAIL: TestApprovalFeedbackProbe/',red)),'adaptedGreen':len(re.findall(r'--- PASS: TestApprovalFeedbackProbe/',green)),'racePackages':len(re.findall(r'^ok\s+github.com/AutoByteus/autobyteus-nfs/',full,re.M)),'finalRoleOutcomes':len(re.findall(r'--- PASS: TestAuthorizationFeedbackBothRolesAndOutcomes/',final))}
assert counts=={'baselineRed':12,'adaptedGreen':12,'racePackages':10,'finalRoleOutcomes':20},counts
assert 'Ran 78 tests' in text('IMP-05-python.log') and 'OK (skipped=1)' in text('IMP-05-python.log')
checks=['IMP-04-go-race.log','IMP-04-dashboard-final.log','IMP-04-go-vet.log','IMP-04-build.log','IMP-04-version.log','IMP-05-python.log','IMP-05-shell.log','IMP-05-source-hash-final.log']
checks += ['IMP-04-compile-'+x+'.log' for x in ['darwin-arm64','darwin-amd64','linux-arm64','linux-amd64']]
for f in checks:assert '# exit=0' in text(f),f
rec={'case':'API-01','date':datetime.datetime.now(datetime.timezone.utc).isoformat(),'input':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'environment':'API local read-only audit; reused execution Mac26.5.2arm64 Go1.27.2/Python3.9.6','command':'python3 evidence/API-01-audit.py from NFS worktree','reused':'IMP02/03/04/05; actual raw results and durable assertions inspected','productionDeltaSinceChecks':[],'finalTestDelta':diff('e15e5e8'),'earlierTestOnlyDelta':diff('459c02f'),'counts':counts,'python':{'collected':78,'executed':77,'expectedChildSkip':1},'sourceHash':'fbc95116f926879d24075493d82426226e08cec33508c13e7423c2719ad1ae46','result':'Pass','limits':['No Go/Python/browser suite rerun by API','Four targets compile only; Macarm64 runtime only','Protocol children are ordinary-user doubles, not OS approval/storage qualification'],'inspectionAttempt':'Initial interactive grep treated a dash-prefixed pattern as an option and failed before inspecting counts; this audit uses Python regex. No test/product failure.'}
assert rec['sourceHash'] in text('IMP-05-source-hash-final.log')
(e/'API-01-reuse.json').write_text(json.dumps(rec,indent=2)+'\n');print(json.dumps(rec,indent=2))
p=t/'api-e2e-test-progress.md';p.write_text(p.read_text()+f'| {rec["date"]} | API-01 | Completed | Pass reused current repository proof;12red/12green,10racepackages,20finalroleoutcomes; Python77executed1skip |\n| {rec["date"]} | API-02 | Started | Verify timer/Stop/drain/dedup/current mutation evidence and assertions |\n')
p=t/'api-e2e-execution-coverage-report.md';p.write_text(p.read_text()+'| API-01 | AC001/003/004/006 | Reused IMP02–05; Git/input/assertion/raw-log audit (`python3 evidence/API-01-audit.py`) | IMP handoff rows | Pass | API-01-reuse.json: finalTestDelta=[];12red/12green;10racepackages;20finaloutcomes; raw paths in handoff | No rerun; final affected test refinement covered; Python77executed1skip, targets compile only |\n')
