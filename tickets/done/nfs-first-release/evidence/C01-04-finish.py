# Case C01; finalize verified API004 outcomes/cleanup; source44e2487; local macOS/Actions evidence;2026-10-19UTC.
from pathlib import Path
import subprocess,json,hashlib,datetime
E=Path(__file__).resolve().parent;T=E.parent;N=T.parents[2]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def read(name):return json.loads((E/name).read_text())
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=N,text=True)
f=read('R03-04-final.json');s=read('R03-04-summary.json');c=read('R04-04-candidate.json');v=read('R04-04-verification.json');smoke=read('R05-04-smoke.json');ret=read('R04-04-retention.json');ref=read('R04-04-reference.json');own=read('C01-04-ownership.json');remote=read('R03-04-remote-after.json')
assert f['run']['conclusion']=='success' and v['pass'] and smoke['pass'] and smoke['scratchAbsent']
assert read('C01-04-candidate-final-verify-result.json')['pass']
native=[j for j in s['jobs'] if j['name'].startswith('binaries ')]
assert len(native)==4 and all(len(j['nativePackagePassLines'])==7 and j['conclusion']=='success' for j in native)
assert all(any('Ran 52 tests' in l for l in j['pythonSummary']) for j in native)
assert all(remote[k+'Unchanged'] for k in ['tags','releases','main'])
assert git('diff','--name-only','75f4dbe', 'HEAD','--',':!tickets')=='' and git('diff','--name-only','--',':!tickets')==''
assert all(digest(N/p)==h for p,h in own['DeliveryFiles'].items())
history=T/'api-e2e-revision-record.md';assert digest(history)==own['historySha256']
# Read-only preservation check of earlier immutable candidates; never promote them.
old=[]
for rev,root in [('002',Path('/Users/normy/nfs-first-candidate-api002-n940gd8s/candidate')),('003',Path('/Users/normy/nfs-first-candidate-api003-p_t67xqw/candidate'))]:
 record=read(f'api-e2e/api-rev-{rev}/actual-candidate.json');reference=read(f'api-e2e/api-rev-{rev}/candidate-reference.json')
 assert digest(root/'candidate.json')==reference['recordSha256']
 for name,m in record['members'].items():assert digest(root/name)==m['sha256']
 old.append({'revision':rev,'candidate':str(root),'recordAndMembersPreserved':True})
cleanup={'case':'C01','step':'Final identity/ownership/retention audit, not repeated product suite','utc':now(),'sourceCommit':c['sourceCommit'],'productCommit':'75f4dbe5527a7159f536bafcf9448bc2d6a01604','environment':'N worktree/local APFS; completed hosted evidence','sourceCount':127,'nonTicketDeltaFromTestedSource':[],'DeliveryProtectedFiles':len(own['DeliveryFiles']),'DeliveryUnchanged':True,'priorAPIHistoryPrefixPreserved':True,'oldCandidates':old,'localNotaryDiagnostic':'Untouched; not accessed as current candidate or credential source','ownedRetainedCandidate':ret,'candidateReverified':True,'ownedNativeScratchAbsent':smoke['scratchAbsent'],'ownedPersistentRuntimeResources':[],'hosted':'All jobs completed; provider post-job logs retained, provider disposal not independently audited','pass':True}
(E/'C01-04-cleanup.json').write_text(json.dumps(cleanup,indent=2)+'\n')
with (T/'api-e2e-test-progress.md').open('a') as p:p.write(f'| {now()} | C01 | Completed | Pass | Current candidate reverified;127 source unchanged, Delivery10 files excluded, old candidates preserved, native scratch removed; C01-04-cleanup.json. |\n')
# Report results only after all actual receipts above are present and checked.
report=f'''# API/E2E Execution Coverage Report — nfs-first-release

## Round / classification
**API-REV-004 — Pass95.00%, affected prepublication validation only.** Task project_task_97c6ab09-83cb-46df-bf28-d07b39259dd5. Canonical archive tickets/done/nfs-first-release is not TaskDone. Large/High/Reviewed; next successful-output gate is proportional test review, then Delivery. No API production/durable edits.

Plan/upstream inventory: api-e2e-coverage-investigation.md. History: api-e2e-revision-record.md. Append-only progress: api-e2e-test-progress.md. Trigger IR005 signing diagnostic/cleanup fix, CRR007 sourcePass100, DR005 failure and DR006/007 local diagnostic supplements. R3/SR004 Approved/Ready, ARCH002 unchanged. Prior API003 prepublication95 and failed DR005 remain exact-input history. No new architecture or field campaign.

Evidence folder: `{E}`; new files start with case ID and `-04-`. Strict actual candidate/envelope/reference JSON is kept unmodified; companion command logs supply header context. Reused IMP evidence remains at its original path. This round reuses clear current checks as instructed, rather than rerunning them for independence. Full job logs have short excerpts alongside them.

## Environments / builds
| Env | Exact build | Runtime / configuration |
|---|---|---|
| I — reused implementation |75f4dbe5527a7159f536bafcf9448bc2d6a01604;127 current non-ticket inputs identical|IMP Checks Run: independent APFS source/privateHOME+TMP, macOSarm64/Python3.9.6/Bash3.2.57. Command doubles, not actual Apple.|
| H — new hosted |{c['sourceCommit']} exact source/workflow/dispatch; run{c['runId']}/attempt{c['runAttempt']}|Ubuntu24.04arm64/amd64, macos15arm64/macos15-intelamd64, Go1.27.2; publish=false. No signing secrets or public effects.|
| A — actual facade/native smoke |Same current source; actual new candidate retained at {ret['candidate']}|Local macOS26.5.2arm64/Python3.9.6; read-only Actions API; smoke privateHOME, no setup/keychain/installation.|

## Cases
Evidence files relative to folder above. A reused row leaves command/environment/evidence details to the cited implementation Checks Run as the updated skill requires.

| Case | Criteria | Command / steps | Env | Result | Evidence / exact line to find | Notes |
|---|---|---|---|---|---|---|
| R01 |AC003/004/006/008|**Reused IMP-05-01/02/08/09**|See IMP row|Pass|See implementation Checks Run; R01-04-reuse.json records applicability|127inputs match75f4dbe; full52collected51executed1expected Go-childskip; focused17 overlaps.4detected mutants and expected baseline diagnostic failure. API did not rerun these local suites.|
| R02 |AC001/002/006/008|Reused IMP-05-03–07; additional `/usr/bin/python3 packaging/release.py --check-publish --candidate /Users/normy/nfs-first-candidate-api003-p_t67xqw/candidate` from N|A; reused Env per IMP row|Pass|R02-04-stale-candidate.log: `Release refused: Executed workflow differs from hashed source`; R02-04-stale-result.json exit1|Actual old candidate is refused at workflow binding before public effects. No-candidate IMP refusal was not stale proof.|
| R03 |AC001/005/006|`gh workflow run release-nfs.yml --repo AutoByteus/autobyteus-nfs --ref codex/nfs-first-release -f release_tag=v0.1.0 -f source_sha={c['sourceCommit']} -f publish=false`; exact attempt monitored and full logs collected|H|Pass|R03-04-dispatch.json; R03-04-final.json `"conclusion": "success"`; R03-04-summary.json; R03-04-job-*.log and R03-04-excerpt-*.log; R03-04-remote-after.json|10success/0failure/0cancel/2intended payload/publish skips. Both engine builders/fullOCI/aggregation and all4 native race7packages/vet/Python52/build/version/archive passed. Go output nonverbose: no invented individual counts. Original DR005 run still failure; tags/releases/main unchanged.|
| R04 |AC001/002/006|Actual facade `candidate-envelope`, `fetch-candidate`, `verify-candidate` for exact run/attempt/unique artifact{ret['artifact']}; corrupt copied wrapper must refuse. Exact argv in R04-04-*.log and *-result.json|A|Pass|R04-04-reference.json, R04-04-candidate.json, R04-04-verification.json; R04-04-wrapper-refusal.log: `Release refused: Retained artifact envelope differs`|Complete{v['files']}files/{v['bytes']}bytes verified; copied wrong envelope cannot create destination. No metadata/receipt substitution or old artifact aggregation.|
| R05 |AC005|Actual downloaded Darwinarm64 `autobyteus-nfs version`, `verify-release <own release.json>` in privateHOME|A|Pass|R05-04-version.log: `v0.1.0`; R05-04-candidate-refusal.log; R05-04-smoke.json `"noHomeWrites": true` and `"scratchAbsent": true`|Exact stdout/empty stderr for version; candidate admission refuses exit1. No install/setup. Unchanged false/legacy/positive-notice coverage remains in current native suites; not repeated as unnecessary local probes.|
| C01 |AC008|Final candidate verification, source/history/Delivery/old-candidate preservation and owned cleanup|A|Pass|C01-04-cleanup.json `"candidateReverified": true`, `"DeliveryUnchanged": true`; C01-04-candidate-final-verify-result.json|127source inputs unchanged;10Delivery-owned files excluded; local-notary diagnostic untouched; older candidates retain original record/member hashes. New candidate retained through release.|
| Q01-01–Q06-07 (42) / U01 |AC007/REQ003|Not run, approved postpublication plan|N/A|Not Tested — Deferred|postpublication-testing-plan.md / approval-record-sr004.md at ticket root|43 IDs remain not Passed, no host questionnaire, not a release/closure prerequisite.|
| D01/D02 |AC002–008|Delivery genuine readiness/freshmain/both-Mac signing+Accepted/finalpayload/immutable publication/public downloads+signatures/install/custody|N/A|Not Tested — Downstream|packaging/RELEASE.md; implementation-handoff.md Downstream Work|Mandatory later release acceptance, not a completed API build-only result.|

**51 unique IDs:6Pass/0Fail/0Blocked/45NotTested (43Deferred,2Downstream).** Native Python repeats across platforms are not additional unique tests; focused17 overlaps52. All current API cases completed. No local product suite repeated solely for independent credit.

## Acceptance-Criteria Proof
Split portions show actual current API proof versus still-required later release effects; criteria are not waived or changed. No Only The User Can Check classification is needed: field/user work is approved Deferred; provisioning is not re-requested.

| Criterion / portion | Critical | Cases | Result | Limit / remaining owner |
|---|---|---|---|---|
| AC001 exact new complete candidate/no publication |Yes|R02/R03/R04|Proven|Actual current-source hosted/artifact evidence.|
| AC002 current check/reference/admission and stale identity contract |Yes|R01/R02/R04|Proven|Current reused fixtures and actual stale/wrapper refusal.|
| AC002 genuine current stable readiness acceptance |Yes|D01|Not Proven|Delivery must reaccept new candidate/source/engine/OCI; old readiness is stale.|
| AC003 signing diagnostic/privacy/cleanup/Accepted-only control |Yes|R01|Proven|Current actual shell with external command doubles; expected baseline/mutants fail.|
| AC003 actual both-Mac hosted P12/import/signing/Accepted/downloaded signatures |Yes|D01/D02|Not Proven|DR007 local development arm64 Accepted is not this proof; original hosted cause UNKNOWN.|
| AC004/006 immutable recovery/control implementation |Yes|R01/R02/R04|Proven|Control fixtures plus actual current artifact integrity/refusals.|
| AC004/006 real normal public release/wholeOCI equality and attributable final bytes |Yes|D01/D02|Not Proven|Final metadata/signatures change binaries; actual final proof required.|
| AC005 current native/installer/claim integrity contract |Yes|R01/R03/R05|Proven|Reused/current hosted suites and downloaded version/refusal.|
| AC005 actual final public install/notice/checksum/signature/version |Yes|D02|Not Proven|Candidate intentionally unadmitted, not an installable release.|
| AC007 prepublication checks/deferral/history preservation |Yes|R01–R05/C01|Proven|New result and unmodified prior failures/candidates, plan retained.|
| AC007 first signed public release completion/custody |Yes|D01/D02|Not Proven|Delivery→terminal SD→requesting PM after actual release.|
| AC008 API-owned cleanup/control consistency |Yes|R01/R02/C01|Proven|No runtime/host source or license change; owned scratch removed.|
| AC008 currentmain/final docs/public receipt/plan transfer |Yes|D01/D02|Not Proven|Earlier finalized source preserved; Delivery owns later fix-forward.|

## Confidence / broader decision
Scores are for **affected prepublication validation**, not the uncompleted signed release or deferred filesystem support.

| Category | Post-repository | Final | Support and remaining uncertainty |
|---|---:|---:|---|
| Requirement / AC proof |50|95|R01–R05/C01 current API obligations complete; actual full release criteria explicitly outstanding.|
| Changed-boundary directness |90|95|Actual current shell exercised by IMP fixtures plus new hosted workflow/native/artifact; external signing not yet run by this stage.|
| Cross-boundary realism / mock gap |75|95|Real CI/engine/OCI/download/CLI; Apple/publication remained explicit doubles in local controls.|
| Environment/configuration/identity fidelity |75|100|Exact127input reuse, verified remote workflow/source/run/attempt/wrapper/record/members; native4 and owned smoke. No material identity ambiguity within this stage.|
| Failure/edge/lifecycle/recovery |90|90|Specific cleanup/error/mutant controls plus actual stale/wrapper rejection; bounded gap is real credential/notary/diagnostic-upload recovery deferred to Delivery's signed run.|
| User-surface (CLI) |75|95|Actual new version and candidate refusal plus current native admission tests; final released installer later. Browser/desktop not applicable.|
| Durable regression relevance |95|95|Current signing/workflow additions target observed diagnostic loss and cleanup; source bytes/test evidence clear; successful-test review next.|

Simple means:550/7=78.57% postrepository;665/7=95.00% final; no final category below90. Current API-stage critical obligations directly proven:Yes. Full release acceptance all proven:No. The scoped result cannot authorize task completion or waive missing critical release gates; project sequence is API evidence→successful-test review→Delivery genuine readiness/actual publication.

Broader **Required and executed** via actual hosted candidate, Live API and downloaded CLI. It closes the new-source/native/artifact uncertainty left by reused local checks. Browser unnecessary, no UI change. Field/user tests remain explicitly deferred, no missing-host blocker. Real signing diagnostics upload/Apple and public effects remain ordered later Delivery work, not falsely credited to build-only execution.

## Durable coverage / transitions / mocks
API durable additions/updates/removals: **None**. IR005 changed `scripts/tests/test_nfs_release_signing.py` and `scripts/tests/test_nfs_release_workflow.py`; attach for proportional successful-test review, not full-source re-review. Existing receipt/candidate/runtime tests Still Valid. No compatibility-only coverage or version fallback. Host state NotAffected; generated distribution/readiness must be rebuilt/reaccepted, never reinterpret historical records. No migration required or executed.

IMP tests execute actual signer with fake security/codesign/notary commands, private fixture credentials, and failure/signal/cleanup controls. They prove fixed diagnostics and fail-closed ordering, not P12/password/Apple acceptance. Workflow fixture allowlist is not actual failure-receipt artifact upload. Public registry/GitHub/installer controls are doubled where documented in IMP and prior API003; actual artifact facade here uses real Actions. DR006/007 remain Delivery/user local diagnostic evidence, not API-run tests, not proof of GitHub secret equality or Intel signing.

## Cleanup / candidate custody
All local executable smoke copies/privateHOME removed; no local Go download or duplicate local suite scratch created this round. No live mounts/exports/VM/container/registry/keychain action. All hosted jobs complete; provider post-job cleanup logged, provider disposal not independently audited. Temporary orchestrators complete. Source127inputs and Delivery10file hashes checked; only API-owned files staged. Old API002/API003 record/member hashes preserved. `/Users/normy/nfs-local-notary-xq_ym2f6` untouched and not read for credentials.

New candidate retained at `{ret['candidate']}` (private parent0700), {v['files']}files/{v['bytes']}bytes. Artifact{ret['artifact']}, expiry{ref['envelope']['expiresAt']}; wrapper{ref['envelope']['digest']}; recordSHA{ref['recordSha256']}. Exact candidate sourceHash **{c['sourceHash']}**, measured engine manifestSHA **{c['engineManifestSha256']}**, OCI **{c['oci']['index']}**. `R04-04-candidate.json` holds both child digests/full member bindings. Keep through signing/publication/recovery; no generated binaries/metadata committed in product tree. No old measured/default-source hash is promoted automatically.

## Latest authoritative result
**API-REV-004 Pass95.00% — current affected prepublication validation.** No new product finding. IR005 diagnostic correction validated at local executable control scope; original DR005 hosted root cause is still UNKNOWN and that run remains failed. Current candidate is new, not relabeled API003. No speculative secret change request.

AC002 final readiness, AC003 actual hosted/signature evidence, AC004/006 actual publication/equality, AC005 public install, AC007 completion/custody and AC008 finalization portions remain NotProven downstream. D01/D02 must complete before release/task success. Field/user Q42/U01 Deferred, not Passed. No API main push/replay, signing, publication, deployment, TaskDone, user-verification or Terminal.

Next: fresh rules after evidence commit; Large/High proportional successful-test review, then normal Delivery fix-forward. Delivery DR008 staging was prerequisite only, not full Delivery completion.
'''
(T/'api-e2e-execution-coverage-report.md').write_text(report)
with history.open('a') as h:h.write(f'''\n\n| Revision | Trigger | Upstream | Prior result/confidence | Current result/confidence |\n|---|---|---|---|---|\n| API-REV-004 | IR005/CRR007 signing diagnostics and cleanup | R3/SR004/ARCH002; DR005–008 | API003 prepublicationPass95 | **Pass95 — current affected prepublication only** |\n\n## API-REV-004 — current diagnostic controls reused, new complete candidate executed\n- Updated skill read before continuation. IMP Checks Run read first; R01 reuse IMP-05-01/02/08/09 and R02 reuse03–07 because127non-ticket inputs equal tested75f4dbe and evidence is clear.52collected51executed1expected childskip; focused17 overlaps;4mutants/expected baseline retained. No repeated local suite for independence, no API source/durable edits.\n- Additional actual old API003 candidate rejected with `Executed workflow differs from hashed source` before effects. This is real stale-input proof; reused no-candidate refusal is not mislabeled.\n- Delivery DR008 staged exact reviewed44e2487 only; API personally dispatched NEW publish=false run{c['runId']}/attempt{c['runAttempt']}.10success/0failure/0cancel/2intended skips. All4 native race7packages/vet/Python52/build/version/archive plus engine2/fullOCI/aggregation pass. Old DR005 run39121007787 remains failure/causeUNKNOWN; local DR007 AppleAccepted only development arm64, not hosted closure.\n- Actual artifact{ret['artifact']} downloaded/verified via facade, corrupt copied wrapper refused before destination; actual downloaded Darwinarm64 version/candidate refusal pass, privateHOME removed. New measured sourceHash{c['sourceHash']}; exact candidate `{ret['candidate']}` retained {v['files']}files/{v['bytes']}bytes. OldAPI002/003 record/member hashes preserved; local notary diagnostic untouched.\n- Cases51=6Pass/0Fail/0Blocked/45NotTested(43Deferred,2Downstream). Confidence78.57→95 over current API-stage scope, broaderRequired/executed. No new failure. Full actual signing/readiness/publication/publicdownload/finalization/custody remains NotProven and mandatory downstream; field/user remains Deferred notPassed, no questionnaire.\n- Canonical plan/report/history/progress updated; ledger left historical. Flat case-prefixed evidence per new evidence-files skill. Production127inputs unchanged,10Delivery-owned files preserved/excluded. No API push/mainreplay/signing/release/TaskDone/Terminal. Fresh proportional two-file durable-test review then Delivery.\n''')
print('API004 report/history complete',c['runId'],c['sourceHash'],flush=True)
