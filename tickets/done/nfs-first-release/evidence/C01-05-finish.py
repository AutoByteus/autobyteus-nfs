# Case C01; finalize actual API005 receipts only after all cases complete; product2c12ec6; local Macarm64;2026-10-19.
from pathlib import Path
import subprocess,json,hashlib,datetime
E=Path(__file__).resolve().parent;T=E.parent;N=T.parents[2]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def read(n):return json.loads((E/n).read_text())
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=N,text=True)
def save(n,o):(E/n).write_text(json.dumps(o,indent=2)+'\n')
f=read('R03-05-final.json');summary=read('R03-05-summary.json');c=read('R04-05-candidate.json');v=read('R04-05-verification.json');smoke=read('R05-05-smoke.json');ret=read('R04-05-retention.json');ref=read('R04-05-reference.json');own=read('C01-05-ownership.json');remote=read('R03-05-remote-after.json')
assert f['run']['conclusion']=='success' and v['pass'] and smoke['pass'] and smoke['scratchAbsent']
assert read('C01-05-candidate-final-verify-result.json')['pass']
native=[j for j in summary['jobs'] if j['name'].startswith('binaries ')]
assert len(native)==4 and all(len(j['nativePackagePassLines'])==7 and j['conclusion']=='success' for j in native)
assert all(any('Ran 56 tests' in l for l in j['pythonSummary']) for j in native)
assert all(remote[k+'Unchanged'] for k in ['tags','releases','main'])
assert remote['originalFailedRun']['conclusion']==remote['DR009FailedRun']['conclusion']=='failure'
assert len([x for x in git('ls-files').splitlines() if not x.startswith('tickets/')])==127
assert git('diff','--name-only','2c12ec6','HEAD','--',':!tickets')=='' and git('diff','--name-only','--',':!tickets')==''
assert all(digest(N/p)==h for p,h in own['DeliveryFiles'].items())
history=T/'api-e2e-revision-record.md';assert digest(history)==own['historySha256']
old=[]
for rev,root in [('002',Path('/Users/normy/nfs-first-candidate-api002-n940gd8s/candidate')),('003',Path('/Users/normy/nfs-first-candidate-api003-p_t67xqw/candidate')),('004',Path('/Users/normy/nfs-first-candidate-api004-a7bxyrbb/candidate'))]:
 record=read(f'api-e2e/api-rev-{rev}/actual-candidate.json') if rev!='004' else read('R04-04-candidate.json')
 reference=read(f'api-e2e/api-rev-{rev}/candidate-reference.json') if rev!='004' else read('R04-04-reference.json')
 assert digest(root/'candidate.json')==reference['recordSha256']
 for name,m in record['members'].items():assert digest(root/name)==m['sha256']
 old.append({'revision':rev,'candidate':str(root),'recordAndMembersPreserved':True})
# Explain freshly measured identity without relabelling the preserved engine/readiness.
manifest=json.loads((Path(ret['candidate'])/'engine/engine-manifest.json').read_text());prior=json.loads((N/'packaging/release-lock.json').read_text())['engine'];differences=[]
def compare(a,b,path=''):
 if isinstance(a,dict) and isinstance(b,dict):
  for key in sorted(set(a)|set(b)):compare(a.get(key),b.get(key),path+'/'+key)
 elif a!=b:differences.append({'path':path,'prior':a,'current':b})
compare(prior,manifest)
identity={'case':'R04','step':'Compare actual measured engine against preserved lock; no product mutation','date':now(),'sourceCommit':c['sourceCommit'],'environment':'read-only current candidate and lock','priorSourceHashWithPreservedEngine':'dd6cde88374cce42ec8b44c24e41abff3af6f01803890824dd783848e0d101a5','newSourceHash':c['sourceHash'],'engineManifestDifferences':differences,'scope':'Current actual candidate governs new readiness; no reproducible-build equality claim or promotion of old hash.'};save('R04-05-measured-identity.json',identity)
cleanup={'case':'C01','step':'Final candidate/ownership/cleanup audit, not product suite repeat','date':now(),'sourceCommit':c['sourceCommit'],'productCommit':'2c12ec61f6339d0d264280b7117787ec821425af','environment':'N worktree and completed hosted receipts','sourceCount':127,'nonTicketDelta':[],'DeliveryProtectedFiles':len(own['DeliveryFiles']),'DeliveryUnchanged':True,'priorAPIHistoryPrefixPreserved':True,'oldCandidates':old,'localNotaryDiagnostic':'Untouched, not accessed as current candidate or credential source','ownedRetainedCandidate':ret,'candidateReverified':True,'ownedNativeScratchAbsent':smoke['scratchAbsent'],'ownedPersistentRuntimeResources':[],'hosted':'All jobs completed; provider post-job logs retained, provider disposal not independently audited','pass':True};save('C01-05-cleanup.json',cleanup)
with (T/'api-e2e-test-progress.md').open('a') as p:p.write(f'| {now()} | C01 | Completed | Pass | Candidate reverified;127 source inputs and Delivery{len(own["DeliveryFiles"])} files preserved; oldAPI002/003/004 untouched; owned native scratch absent. |\n')
report=f'''# API/E2E Execution Coverage Report — nfs-first-release

## API-REV-005 / result and scope
**Pass95.00% — affected prepublication validation only; NOT a signing/root-cause fix or release Pass.** Task project_task_97c6ab09-83cb-46df-bf28-d07b39259dd5; Large/High/Reviewed; R3/SR004 Approved/Ready/ARCH002 unchanged. IR006 source2c12ec61f6339d0d264280b7117787ec821425af and CRR009 sourcePass100 diagnose codesign failure only. Actual DR00939204643596/1 remains failed; codesign cause UNKNOWN, signing/release unresolved. API004 historical result and candidate are not relabelled.

Canonical ticket `{T}` (archive is not completion). Plan/upstream inventory: api-e2e-coverage-investigation.md. History: api-e2e-revision-record.md. Progress: api-e2e-test-progress.md. No plan deviation, no API product or durable-test changes. New evidence flat `{E}` under case-prefixed `*-05-*`. Strict candidate/envelope JSON retains exact schema; companion command logs supply context. Long full job logs have excerpts. Original IMP evidence remains attributed, not copied or rerun for independence.

## Tested builds / environments
| Env | Exact input | Configuration / limitation |
|---|---|---|
| I — reused IMP |2c12ec6;127 current non-ticket files equal tested source|Implementation Checks Run: independent APFS/privateHOME+TMP; Darwinarm64/Python3.9.6/Bash3.2; actual shell with external doubles, not Apple|
| H — current hosted |{c['sourceCommit']}; run{c['runId']}/attempt{c['runAttempt']}, same source/workflow/dispatch|Ubuntu24.04arm64/amd64, macos15arm64/macos15-intelamd64, Go1.27.2; publish=false, no signing secrets or publication|
| A — current facade/native smoke |Same product; local docs descendant6bc8979 differs only ticket receipt|Local macOS26.5.2arm64/Python3.9.6/gh read-only Actions API; privateHOME for downloaded CLI; no setup/install/keychain|

## Cases
All evidence names relative to evidence folder. Reused cases leave commands/environment/evidence/quoted outcomes to implementation Checks Run, as skill requires.

| Case | AC | Command / steps | Env | Result | Evidence / look for | Notes |
|---|---|---|---|---|---|---|
| R01 |003/004/006/008|**Reused IMP-06-01/02/09/10**|See IMP row|Pass|See implementation Checks Run; R01-05-reuse.json is applicability audit|56collected55executed1expectedchildskip;21focused overlap;4detected mutants; expected original-signer11assertion failures. Initial46fixture-shadowing failures corrected by Implementation remain preserved, not current source failure. No API local suite repeat.|
| R02 |001/002/006/008|Reused IMP-06-03–08/11; additional `/usr/bin/python3 packaging/release.py --check-publish --candidate /Users/normy/nfs-first-candidate-api004-a7bxyrbb/candidate` from N|A; reused details per IMP|Pass|R02-05-stale-candidate.log: `Release refused: Candidate source/engine differs`; result.json exit1|Actual old retained candidate refusal, not mislabeled no-candidate control; no public effects.|
| R03 |001/005/006|`gh workflow run release-nfs.yml --repo AutoByteus/autobyteus-nfs --ref codex/nfs-first-release -f release_tag=v0.1.0 -f source_sha={c['sourceCommit']} -f publish=false`; exact attempt + full job logs|H|Pass|R03-05-dispatch.json, final.json, summary.json, job-*.log/excerpt-*.log, remote-after.json|10success/0failure/0cancel/2intended payload-publish skips. All4native race7packages/vet/Python56/build/version/archive; engine2/fullOCI/aggregation. Go nonverbose: no invented individual counts. Both old DR005/DR009 observed failed; main/tags/releases unchanged.|
| R04 |001/002/006|Actual facade candidate-envelope/fetch-candidate/verify-candidate, exact artifact{ret['artifact']}; copied wrong-wrapper refusal; exact argv in R04-05-*.log/results|A|Pass|R04-05-reference.json/candidate.json/verification.json/measured-identity.json; wrapper-refusal.log: `Release refused: Retained artifact envelope differs`|Complete{v['files']}files/{v['bytes']}bytes; wrong wrapper refuses before destination. Current real record, not fixture or hand-assembled partial artifacts.|
| R05 |005|Downloaded Darwinarm64 `version`; `verify-release <own release.json>` in privateHOME|A|Pass|R05-05-version.log: `v0.1.0`; candidate-refusal.log; smoke.json `"noHomeWrites": true`, `"scratchAbsent": true`|Exact version stdout/empty stderr; candidate admission expected exit1; no setup. Current native suites cover unchanged legacy/false/positive-notice controls.|
| C01 |008|Final facade candidate verify/source/history/Delivery/old-candidate preservation, cleanup|A|Pass|C01-05-cleanup.json `"candidateReverified": true`, `"DeliveryUnchanged": true`; candidate-final-verify-result.json|127input equality;Delivery{len(own['DeliveryFiles'])}files excluded; own smoke absent; priorAPI002/003/004 members unchanged; local diagnostic untouched.|
| Q01-01–Q06-07 (42) / U01 |007|Approved postpublication field/user plan|N/A|Not Tested — Deferred|postpublication-testing-plan.md / approval-record-sr004.md|43IDs not Passed, not prepublication/closure prerequisite; no questionnaire|
| D01/D02 |002–008|Genuine current readiness/freshmain/actual both-Mac signing+Accepted/finalpayload/public bytes+OCI/install/signatures/custody|Delivery|Not Tested — Downstream|packaging/RELEASE.md; DR009 actual failure receipts|Mandatory later gates; DR009 signing failure unresolved, not credited as Pass or waived|

**51IDs =6Pass/0Fail/0Blocked/45NotTested (43Deferred,2Downstream)** for this stage. Repeated platform suite executions/focused21 are not additional unique tests. No new API product/harness failure; prior IMP failures/mutants and DR005/009 stay historical and attributed.

## Acceptance-Criteria Proof
These are portioned proof statements, not a waiver or claim that the full signed-release acceptance is complete. No Only The User Can Check classification: field work is approved Deferred, actual current publication remains Delivery work.

| Criterion / portion | Critical | Cases | Result | Remaining boundary |
|---|---|---|---|---|
| AC001 complete current native4/engine/OCI candidate/no publication |Yes|R02/R03/R04|Proven|Exact real run/artifact|
| AC002 current check/reference/admission/stale identity controls |Yes|R01/R02/R04|Proven|Synthetic authority fixtures are not real readiness|
| AC002 genuine current stable readiness |Yes|D01|Not Proven|Delivery must accept NEW measured candidate, no old lock promotion|
| AC003 bounded diagnostic confidentiality/original exit/cleanup/Accepted-only controls |Yes|R01|Proven|Actual shell, mocked external commands; not a real signing repair|
| AC003 real both-Mac codesign/Accepted/signature and current diagnostic artifact on failure |Yes|D01/D02|Not Proven|DR009 failed at sign; unknown cause; DR007 development Accepted not substitute|
| AC004/006 immutable recovery/control integrity |Yes|R01/R02/R04|Proven|Actual artifact refusal plus current fixture controls|
| AC004/006 actual normal publication/OCI equality/final attributable bytes |Yes|D01/D02|Not Proven|Final metadata/signatures change binary bytes; new real receipts required|
| AC005 current native/installer/admission contract |Yes|R01/R03/R05|Proven|Current suites plus actual downloaded version/candidate refusal|
| AC005 actual final public install/notice/checksum/signature/version |Yes|D02|Not Proven|Unsigned candidate intentionally unadmitted|
| AC007 current prepublication proof/deferral/history |Yes|R01–R05/C01|Proven|Not overall release completion|
| AC007 completed signed release/plan custody |Yes|D01/D02|Not Proven|Delivery→terminalSD→requestingPM after actual release|
| AC008 API cleanup/input consistency/other-owner preservation |Yes|R01/R02/C01|Proven|No runtime/license/host changes|
| AC008 fresh finalization/docs/public receipts/custody |Yes|D01/D02|Not Proven|Already-finalized ancestors preserved, later Delivery fix-forward remains|

## Confidence / broader validation
Scores apply **only to affected prepublication validation**, not unresolved signing or deferred field support.

| Category | Post-repository | Final | Evidence and limit |
|---|---:|---:|---|
| Requirement/AC proof |50|95|Current API obligations R01–R05/C01 complete; full release portions explicitly outstanding|
| Changed-boundary directness |90|95|Current actual shell diagnostic controls reused; current hosted/new distribution bytes verified; real codesign remains separate|
| Cross-boundary realism/mock gap |75|95|Actual CI/engine/OCI/download/CLI; external Apple and publisher effects doubled in controls|
| Environment/configuration/identity |75|100|127input equality; exact remote workflow/run/attempt/envelope/members; native4; no identity ambiguity within scope|
| Failure/edge/lifecycle/recovery |90|90|Bound/privacy/parser/original-exit mutants plus real stale/wrapper refusals; bounded gap actual codesign diagnostic upload/Apple recovery belongs to signed run|
| User-surface (CLI) |75|95|New downloaded exact version/refusal and native admission tests; actual public installer later; browser/desktop N/A|
| Durable regression relevance |95|95|Changed signing tests directly expose diagnostic/privacy failures, four mutants; successful-test review next|

Simple mean postrepository550/7=78.57%; final665/7=95.00%, no final category below90. Current prepublication critical portions proven:Yes; FULL release acceptance proven:No. Score never authorizes publication/TaskDone or conceals DR009 failure. Broader **Required and executed**: hosted native matrix, Live API and downloaded CLI; repository doubles did not cover those. Browser not needed for shell/release-only delta. No field campaign. No secret reprovision asked. Real signing and final public effects remain mandatory ordered Delivery gates.

## Durable coverage / transitions / emulation
API added/updated/removed production or durable tests: **None**. IR006 changes only `scripts/tests/test_nfs_release_signing.py` in durable coverage; request proportional successful-test review of that file, not new full-source/architecture review. Workflow/runtime/installer/record tests Still Valid. No compatibility-only test, fallback or migration. Host persisted state NotAffected; generated candidate/readiness requires current rebuild/reacceptance, old history retained.

IMP executes real signer using fake security/codesign/notary/ditto commands and private fake credentials. It proves fixed categories/privacy/strict nonzero and cleanup, not real P12/chain/ACL/certificate/Apple behavior. A category is observation, never root diagnosis. Current build-only workflow does not enter signer, so its success is not evidence the DR009 cause was repaired or that new diagnostics uploaded on a real failure. Delivery owns that actual next signed run. Public registry/GitHub/installer controls are doubled as documented; Actions candidate facade here is real.

## Cleanup / identities / custody
Owned smoke extraction/HOME removed; no new local Go/toolchain/full-suite scratch or persistent runtime resources. No live storage, keychain, credential, registry mutation or app action. Hosted jobs complete with provider post-job logs; provider disposal not independently audited. OldAPI002/003/004 immutable records/members verified unchanged. `/Users/normy/nfs-local-notary-xq_ym2f6` untouched, not accessed for credentials. Delivery{len(own['DeliveryFiles'])}current files protected/excluded from API staging; source127inputs unchanged.

Retain NEW `{ret['candidate']}` (parent0700), {v['files']}files/{v['bytes']}bytes through Delivery release/recovery. Artifact{ret['artifact']}, expiry{ref['envelope']['expiresAt']}; wrapper{ref['envelope']['digest']}; recordSHA{ref['recordSha256']}. Exact measured sourceHash **{c['sourceHash']}**, engineManifestSHA **{c['engineManifestSha256']}**, OCIroot **{c['oci']['index']}**. R04-05-candidate.json contains full member/child identities. R04-05-measured-identity.json explains fresh engine differences from preserved lock; do not promote local preserved-engine hashdd6cde… automatically or infer deterministic build equality. No binaries/generated product metadata committed.

## Latest authoritative result / next
**API-REV-005 Pass95.00% — affected prepublication only.** IR006 diagnostics validated at executable control scope, not actual codesign root fix. DR009 and DR005 remain failed/unknown cause; official release remains unresolved. No speculative secret/keychain repair. No API push/mainreplay/signing/publication/deployment/TaskDone/user-verification/Terminal. DR010 staging prerequisite only, not full Delivery completion. Fresh routing after evidence commit: Large/High proportional changed-signing-test review, then normal Delivery continuation and unresolved signing gates. Full AC portions listed NotProven above remain mandatory.
'''
(T/'api-e2e-execution-coverage-report.md').write_text(report)
with history.open('a') as h:h.write(f'''\n\n## API-REV-005 — IR006 diagnostic-source continuation / new complete candidate\n- Trigger CRR009 sourcePass100, IR0062c12ec6 diagnostic-only change after DR009 actual codesign failure. R3/SR004/ARCH002 Large/High unchanged. Prior API004 prepublicationPass95 remains historical, not promoted.\n- Checks Run read first; reuse IMP06-01/02/09/10 +03–08/11 on exact127 current inputs. Full56collected55executed1expectedchildskip;21focused overlap,4mutants and expected original-signer11 assertion failures. Initial46 fixture-shadowing failures remain corrected historical implementation attempt. No duplicate local suite solely for independence; no API durable edit.\n- R02 actual old API004/current facade exit1 `Candidate source/engine differs`; no-candidate reuse is distinct. DR010 staged exact{c['sourceCommit']} only, local6bc docs descendant preserved. API dispatched NEW publish=false run{c['runId']}/{c['runAttempt']}, all4native/engine2/fullOCI/aggregation success; old DR005/009 remain failure and remote main/tags/releases unchanged.\n- Actual artifact{ret['artifact']} wrapper/reference/complete members verified, wrong copied envelope refused before destination; actual Darwinarm64 version/candidate refusal and owned-HOME cleanup pass. Measured source{c['sourceHash']}, engine{c['engineManifestSha256']}, OCI{c['oci']['index']}. Candidate retained `{ret['candidate']}`; old002/003/004 preserved.\n- Six current cases Pass,43approvedDeferred+2Downstream nottested. Confidence78.57→95 scoped affected prepublication; broaderRequired/executed. No new product failure. **DR009 real signing/root cause and release remain unresolved**; diagnostic-control proof does not repair actual codesign. BothMac Accepted/finalpayload/currentreadiness/immutablepublicbytes/signatures/install/freshfinalization/custody remain mandatory Delivery gates. Field/user Deferred notPassed, no questionnaire.\n- Canonical plan/report/history/progress updated, flat evidence *-05-*. No source/runtime/credential changes or other-repo work. Delivery{len(own['DeliveryFiles'])}files protected,127product inputs unchanged, own smoke removed; local notary diagnostic untouched. Proportional successful-test review of changed signing suite then Delivery; no main push/replay/publication/TaskDone/Terminal.\n''')
print('API005 report/history finalized',c['runId'],c['sourceHash'])
