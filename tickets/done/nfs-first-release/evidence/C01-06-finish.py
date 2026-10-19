# Case C01; final actual API006 evidence/cleanup/report; product3f67e36; NFS local Macarm64;2026-10-19UTC. Run only after all observed cases complete.
from pathlib import Path
import subprocess,json,hashlib,datetime
E=Path(__file__).resolve().parent;T=E.parent;N=T.parents[2]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def read(n):return json.loads((E/n).read_text())
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=N,text=True)
def save(n,o):(E/n).write_text(json.dumps(o,indent=2)+'\n')
f=read('R03-06-final.json');summary=read('R03-06-summary.json');c=read('R04-06-candidate.json');v=read('R04-06-verification.json');smoke=read('R05-06-smoke.json');ret=read('R04-06-retention.json');ref=read('R04-06-reference.json');own=read('C01-06-ownership.json');remote=read('R03-06-remote-after.json')
assert f['run']['conclusion']=='success' and v['pass'] and smoke['pass'] and smoke['scratchAbsent']
assert read('C01-06-candidate-final-verify-result.json')['pass']
native=[j for j in summary['jobs'] if j['name'].startswith('binaries ')]
assert len(native)==4 and all(len(j['nativePackagePassLines'])==7 and j['conclusion']=='success' for j in native)
assert all(any('Ran 58 tests' in l for l in j['pythonSummary']) for j in native)
assert all(remote[k+'Unchanged'] for k in ['tags','releases','main'])
assert remote['originalFailedRun']['conclusion']==remote['DR009FailedRun']['conclusion']==remote['DR011FailedRun']['conclusion']=='failure'
assert len([x for x in git('ls-files').splitlines() if not x.startswith('tickets/')])==127
assert git('diff','--name-only','3f67e36','HEAD','--',':!tickets')=='' and git('diff','--name-only','--',':!tickets')==''
assert all(digest(N/p)==h for p,h in own['DeliveryFiles'].items())
history=T/'api-e2e-revision-record.md';assert digest(history)==own['historySha256']
old=[]
for rev,root in [('002',Path('/Users/normy/nfs-first-candidate-api002-n940gd8s/candidate')),('003',Path('/Users/normy/nfs-first-candidate-api003-p_t67xqw/candidate')),('004',Path('/Users/normy/nfs-first-candidate-api004-a7bxyrbb/candidate')),('005',Path('/Users/normy/nfs-first-candidate-api005-61mqnd8a/candidate'))]:
 record=read(f'api-e2e/api-rev-{rev}/actual-candidate.json') if rev in ['002','003'] else read(f'R04-{int(rev):02d}-candidate.json')
 reference=read(f'api-e2e/api-rev-{rev}/candidate-reference.json') if rev in ['002','003'] else read(f'R04-{int(rev):02d}-reference.json')
 assert digest(root/'candidate.json')==reference['recordSha256']
 for name,m in record['members'].items():assert digest(root/name)==m['sha256']
 old.append({'revision':rev,'candidate':str(root),'recordAndMembersPreserved':True})
manifest=json.loads((Path(ret['candidate'])/'engine/engine-manifest.json').read_text());prior=json.loads((N/'packaging/release-lock.json').read_text())['engine'];differences=[]
def compare(a,b,path=''):
 if isinstance(a,dict) and isinstance(b,dict):
  for key in sorted(set(a)|set(b)):compare(a.get(key),b.get(key),path+'/'+key)
 elif a!=b:differences.append({'path':path,'prior':a,'current':b})
compare(prior,manifest)
save('R04-06-measured-identity.json',{'case':'R04','step':'Actual measured engine vs preserved lock, no product mutation','date':now(),'sourceCommit':c['sourceCommit'],'environment':'read-only current candidate/lock','priorSourceHashWithPreservedEngine':'7cb7b6d25794cbacbcf0286d9d0760347d9f15999eb51e981765e4ba8ed37a1a','newSourceHash':c['sourceHash'],'engineManifestDifferences':differences,'scope':'New real measured candidate governs readiness; no reproducibility or old identity promotion.'})
save('C01-06-cleanup.json',{'case':'C01','step':'Candidate/cleanup/ownership audit, no product suite repeat','date':now(),'sourceCommit':c['sourceCommit'],'productCommit':'3f67e36193c246ca08b49cda818be5c0f94eba51','environment':'NFS worktree/actual completed hosted receipts','sourceCount':127,'nonTicketDelta':[],'DeliveryProtectedFiles':len(own['DeliveryFiles']),'DeliveryUnchanged':True,'priorAPIHistoryPrefixPreserved':True,'oldCandidates':old,'localNotaryDiagnostic':'Untouched; not accessed for credentials or current proof','ownedRetainedCandidate':ret,'candidateReverified':True,'ownedNativeScratchAbsent':smoke['scratchAbsent'],'ownedPersistentRuntimeResources':[],'hosted':'All jobs completed; provider post-job logs retained, provider disposal not independently audited','pass':True})
with (T/'api-e2e-test-progress.md').open('a') as p:p.write(f'| {now()} | C01 | Completed | Pass | Candidate reverified;127inputs/Delivery{len(own["DeliveryFiles"])}files preserved; oldAPI002–005 intact; owned native scratch absent. |\n')
report=f'''# API/E2E Execution Coverage Report — nfs-first-release

## API-REV-006 — Result
**Pass95.00% for affected prepublication validation only. NOT a signed-release Pass or closure of the original hosted cause.** R3/SR004 Approved/Ready, ARCH002, Large/High/Reviewed unchanged. Task project_task_97c6ab09-83cb-46df-bf28-d07b39259dd5. IR007 product3f67e36193c246ca08b49cda818be5c0f94eba51 / CRR011 sourcePass100 repaired owned-keychain lookup at the bounded source/mechanism scope. Actual original DR01139210821088/1 remains sign/exit1/cleanupcomplete/unclassified; root cause UNKNOWN. Old API005 is historical, not current-source evidence.

Plan/upstream inventory: api-e2e-coverage-investigation.md. History: api-e2e-revision-record.md. Progress: api-e2e-test-progress.md. Canonical `{T}` is archived but release unfinished. New flat evidence `{E}` uses case prefix *-06-*; original IMP evidence remains attributed, not copied or rerun. No product/durable-test changes by API, no plan deviation.

## Environments and identity
| Env | Input/setup | Boundary/limits |
|---|---|---|
| I — reused repository |Exact product3f67e36;127inputs equal current; see implementation Checks Run|Independent APFS/privateHOME+TMP, local Darwinarm64/Python3.9.6/Bash3.2; real shell, external command doubles|
| M — supporting native |IMP07-01–03 at intake79e3539; read exact probe source/results|Local macOS26.5.2arm64 synthetic imported identity; explicit keychain A/B/A, timestamp=none for nonrelease experiment only; not current real credentials|
| H — new hosted |Source/workflow/dispatch{c['sourceCommit']};run{c['runId']}/attempt{c['runAttempt']}|Ubuntu24.04 amd64/arm64, macos15arm64/macos15-intelamd64; Go1.27.2; publish=false, actual signer skipped|
| A — facade/native |Current NFS worktree, matching product; privateHOME for new downloaded CLI|Local macOS26.5.2arm64/Python3.9.6/gh read-only Actions API, no setup/install/keychain/credential work|

## Cases
Paths relative to evidence/. Reused checks use Implementation Checks Run for exact commands/environment/outcome lines; R01 audit proves applicability. Focused tests overlap the full suite. Repeated hosted platform runs are not unique additional tests.

| Case | AC portion | Command/steps | Env | Result | Evidence and what to look for |
|---|---|---|---|---|---|
| R01 |003/004/006/008 controls|**Reused IMP07-04/05/12/13**, supporting01–03; read native source/results and prior DR011 failure first|I/M|Pass|R01-06-reuse.json:127equalinputs; IMP-07-05-python.log `Ran 58 tests`/`OK (skipped=1)`=57executed;23focused overlap;4mutants detected; original signer control expected1failure. IMP-07-03-identity-probe.json: sign1→0/verify0/runtime→1, exact original list restored and owned scratch removed. No API suite/keychain repeat.|
| R02 |001/002/006/008 refusal|Reused IMP07-06–11/14; `/usr/bin/python3 packaging/release.py --check-publish --candidate /Users/normy/nfs-first-candidate-api005-61mqnd8a/candidate` from N|A|Pass|R02-06-stale-candidate.log/result.json: `Release refused: Candidate source/engine differs`, exit1. Actual stale candidate distinct from reused missing-candidate refusal.|
| R03 |001/005/006 current candidate|`gh workflow run release-nfs.yml --repo AutoByteus/autobyteus-nfs --ref codex/nfs-first-release -f release_tag=v0.1.0 -f source_sha={c['sourceCommit']} -f publish=false`; exact run/attempt/job logs|H|Pass|R03-06-dispatch.json/final.json/summary.json and job-*.log/excerpt-*.log:10success/0failure/0cancel/2intended payload/publish skips; all4native race7packages/vet/Python58/build/version/archive; engine2/fullOCI/aggregation. remote-after.json: main/tags/releases unchanged; DR005/009/011 still failure.|
| R04 |001/002/006 integrity|Actual facade candidate-envelope/fetch-candidate/verify-candidate; copied wrong envelope negative; exact argv in logs/results|A|Pass|R04-06-reference.json/candidate.json/verification.json:artifact{ret['artifact']}, {v['files']}files/{v['bytes']}bytes; wrapper-refusal.log `Release refused: Retained artifact envelope differs` before destination creation. measured-identity.json shows actual new engine difference, no relabel.|
| R05 |005 CLI candidate contract|Actual new downloaded Darwinarm64 `version` and `verify-release <own release.json>`, privateHOME|A|Pass|R05-06-version.log `v0.1.0`; candidate-refusal.log expectedexit1; smoke.json `"noHomeWrites": true`, `"scratchAbsent": true`. Exact version stdout/empty stderr; candidate intentionally unadmitted; no setup.|
| C01 |008 retention/cleanup|Final actual facade verify plus source/history/other-owner/old-candidate audits|A|Pass|C01-06-cleanup.json `"candidateReverified": true`, `"DeliveryUnchanged": true`; final-verify result.127inputs unchanged, Delivery{len(own['DeliveryFiles'])}files excluded, oldAPI002–005 bytes intact, own smoke removed.|
| Q01-01–Q06-07 (42)/U01 |007 field/user|Approved postpublication-testing-plan.md|N/A|Not Tested — Deferred|43IDs notPassed; no host questionnaire; not prepublication or closure prerequisites|
| D01/D02 |002–008 release|Current stable readiness/freshmain/actual bothMacAccepted/finalpayload/immutable public bytes+OCI/signatures/install/custody|Delivery|Not Tested — downstream|Mandatory ordered release work; real DR011 failure unresolved, not waived or credited Pass|

**51IDs=6Pass/0Fail/0Blocked/45NotTested (43Deferred+2Downstream)** in this stage. Go nonverbose package results do not establish individual test/skip counts. Hosted Python standalone Go-child skips remain explicit; Go suite exercises its child path as project guidelines describe. Expected mutant/original/stale/wrapper failures are controls, not product regressions. No new API product failure observed.

## Acceptance-Criteria Proof
Full release requirements are NOT complete. Each following proven statement is only its named API portion; outstanding portions stay mandatory. No Only The User Can Check designation: approved field deferral is distinct from downstream release execution.

| AC/portion | Critical | Cases/evidence | Status and limit |
|---|---|---|---|
| AC001 new exact current native4/engine2/wholeOCI candidate, no publication|Yes|R03/R04 run+record+remote inventory|Proven|
| AC002 current readiness/admission/stale-identity controls|Yes|R01/R02/R04 exact control evidence|Proven for controls; actual current stable readiness **Not Proven**, D01|
| AC003 temporary-list configure/order/failure/restore and strict signing/Accepted-only safeguards|Yes|R01 reused current shell suite/mutants, supporting native A/B/A|Proven at bounded control/mechanism scope; synthetic identity not actual DeveloperID|
| AC003 real BOTH Mac signed/Accepted/downloaded signatures|Yes|D01/D02|**Not Proven**; DR011 failure unchanged, no root-cause inference from local probe/build-only result|
| AC004 immutable conflict/partial-recovery controls|Yes|R01 current full suite/R04 real wrapper refusal|Proven controls; actual normal tag/release/assets/image **Not Proven**, D01/D02|
| AC005 native/installer/admission contract and downloaded candidate CLI|Yes|R01/R03/R05|Proven controls; actual final public download/install/deferred notice/signature/checksum **Not Proven**, D02|
| AC006 complete measured engine/OCI/candidate identity/refusal|Yes|R02/R03/R04|Proven prepublication; actual published equality and attributable signed-final bytes **Not Proven**, D01/D02|
| AC007 current prepublication evidence and truthful deferral|Yes|R01–R05/C01, approved plan|Proven portion; first signed release/completed custody **Not Proven**, D01/D02|
| AC008 API cleanup/claims/input/other-owner preservation|Yes|C01 plus Cases|Proven portion; fresh finalization/docs/public receipts/custody **Not Proven**, Delivery|

## Confidence and broader validation
Score **affected prepublication scope only**, never use it to assert signed-release readiness or resolved hosted cause.

| Mandatory category | Post-repository | Final | Support / remaining limit |
|---|---:|---:|---|
| Requirements/AC proof|75|95|Current API portions direct; full release portions explicitly pending|
| Changed-boundary directness|75|95|Current actual shell with doubles + real native synthetic mechanism; new exact hosted candidate bytes; real credentials later|
| Cross-boundary realism/mock gap|75|95|Actual CI/engine/OCI/API/download/CLI; Apple/publication effects not exercised by build-only|
| Environment/configuration/identity|90|100|127equalinputs, exact remote workflow/run/attempt/envelope/members, native4|
| Failure/edge/lifecycle/recovery|85|90|Four mutants, configuration/restore controls, native A/B/A, actual stale/wrapper refusals; bounded real signing failure recovery remains downstream|
| User surface (CLI)|75|95|New downloaded exact version/candidate refusal and current native/admission suites; public installer later; browser/desktop N/A|
| Durable regression relevance|95|95|Tests expose original lookup/list/order/strict failure/cleanup errors; successful-test review next|

Simple mean postrepository570/7=81.43%; final665/7=95.00%, each≥90. Critical API portions proven, FULL release acceptance not proven. Broader **Required and executed**: native hosted4, measured engine/fullOCI, actual artifact download/verification/native CLI. Repo doubles alone did not close that gap. No browser or field campaign. Real signing/publication stays ordered Delivery work, not a missing-host blocker or implicit Pass.

## Reuse, durable coverage and limits
API production/durable additions/updates/removals: **None**. Proportional successful-test review requested for IR007 `scripts/tests/test_nfs_release_signing.py`, not another full architecture/source review. Other current suites Still Valid. IMP07 full58 includes focused23; no double counting. Clear exact-input results reused under updated TESTING/skill rather than rerun for independence.

Native IMP07 probe is genuine local synthetic identity behavior, not signer execution with release credentials: valid-only identity query false, non-v explicit query true; original explicit-keychain sign fails, owned+saved search membership signs/strict-verifies/runtime, removed-again fails. Original list restored, inputs deleted. Timestamp=none ONLY in nonrelease probe, no production fallback. Source command still requires timestamp/runtime/DeveloperID/team/strictverify/Accepted. Probe supports local lookup correction but cannot establish original deleted DR011 raw output or its cause. DR007 development Accepted also separate. No repeat provisioning request.

No compatibility wrapper/migration/host-state change. Transient keychain state restoration covered by reused checks; API did not change host list/keychains. New generated candidate/readiness must be rebuilt/reaccepted; historical immutable candidate/failed results retained.

## Cleanup and handoff identities
Owned smoke HOME/extraction removed. No new local Go/full-suite/keychain/credential/process/storage/container resource. Hosted jobs completed with provider post-job logs retained; provider disposal not independently audited. Prior API002–005 record/member bytes unchanged; local development notary diagnostic untouched, never accessed for credentials. All127product inputs unchanged; Delivery{len(own['DeliveryFiles'])}files protected and excluded from API staging. No other repository work.

Retain **{ret['candidate']}** under parent0700, {v['files']}files/{v['bytes']}bytes for Delivery/recovery. Artifact{ret['artifact']}, expires{ref['envelope']['expiresAt']}; wrapper{ref['envelope']['digest']}; recordSHA{ref['recordSha256']}. NEW measured sourceHash **{c['sourceHash']}**, engineManifest **{c['engineManifestSha256']}**, OCIroot **{c['oci']['index']}**; full children/members in R04-06-candidate.json. Do not substitute preserved-engine sourcehash7cb7b6… or oldAPI005 readiness; actual measurement governs, no reproducibility assumption.

## Next / result authority
**API006 scoped prepublication Pass95.00%; original hosted cause and actual signed release still UNVERIFIED.** CRR011 source repair accepted; this build-only success does not execute signer or prove DR011 root cause resolved. DR005/009/011 remain failed history. Fresh most-specific successful-test route after committed evidence, then normal Delivery current readiness/fresh-main/signing+Accepted/finalpayload/immutable public bytes/signature/install/plan-custody gates. Preserve main72b8a4/f830/768 ancestry; no replay/reset. API made no push/real signing/publication/TaskDone/user-verification/Terminal claim.
'''
(T/'api-e2e-execution-coverage-report.md').write_text(report)
with history.open('a') as h:h.write(f'''\n\n## API-REV-006 — IR007 lookup repair / current complete candidate\n- Trigger CRR011 sourcePass100, product3f67e36; R3/SR004/ARCH002 Large/High unchanged. PriorAPI005 historical; original DR01139210821088/1 remains sign/exit1/cleanupcomplete/unclassified, cause UNKNOWN.\n- Checks Run first; exact127inputs validate reuse IMP07-04/05/12/13 +06–11/14. Full58collected57executed1expectedchildskip;23focused overlap;fourmutants and original-signer expectedfailure. Supporting native01–03 synthetic A/B/A validates local lookup mechanism/exact restoration, NOT realDeveloperID/hosted cause. No repeat keychain/product suite for independence.\n- Actual oldAPI005 refused source/engine mismatch. DR012 staged{c['sourceCommit']} only; NEW API publish=false run{c['runId']}/{c['runAttempt']} complete native4/engine2/fullOCI/aggregation;10success2intendedskips; main/tags/releases unchanged; DR005/009/011 still failure.\n- Actual artifact{ret['artifact']} complete envelope/record/member verification, wrong-wrapper refusal, new downloaded native version/candidate refusal and cleanup Pass. Measuredsource{c['sourceHash']}, engine{c['engineManifestSha256']}, OCI{c['oci']['index']}. Retain `{ret['candidate']}`; oldAPI002–005 preserved.\n- SixcasesPass,43Deferred+2Downstream nottested; confidence81.43→95 scoped prepublication; broaderRequired/executed. **Actual signed release/original hosted cause still unverified.** BothMacAccepted/finalpayload/currentreadiness/immutablepublicbytes/install/freshfinalization/custody remain mandatory Delivery. Field/user Deferred notPassed, no questionnaire.\n- No API production/durable edits; proportional successful-test review of IR007 signing test next. Own flat *-06-* evidence;127source/Delivery{len(own['DeliveryFiles'])}files preserved; owned smoke removed, localnotary untouched. No source/mainpush/replay/credential/realSigning/publication/TaskDone/Terminal.\n''')
print('API006 finalized',c['runId'],c['sourceHash'])

save('R03-06-prepublication-result.json',{'case':'R01/R02/R03/R04/R05/C01','step':'Current actual prepublication evidence plus attributed reuse; NOT release readiness','date':now(),'environment':'hosted native4/engine2/OCI, local Actions facade/native smoke; reused shell doubles/native synthetic mechanism','sourceCommit':c['sourceCommit'],'workflowCommit':c['workflowCommit'],'productCommit':'3f67e36193c246ca08b49cda818be5c0f94eba51','runId':c['runId'],'runAttempt':c['runAttempt'],'sourceHash':c['sourceHash'],'engineManifestSha256':c['engineManifestSha256'],'oci':c['oci'],'candidate':ref,'candidateDirectory':ret['candidate'],'native':{'status':'passed','targets':[j['name'] for j in native],'evidence':'R03-06-summary.json + full job logs/excerpts','scope':'Each native:race7packages/vet/Python58(57executed1expectedchildskip)/build/version/archive; not signing/physical'},'releaseControls':{'status':'passed','reused':read('R01-06-reuse.json')['reused']+read('R01-06-reuse.json')['R02Reused'],'supporting':'IMP07-01–03 native synthetic A/B/A and exact restoration','ownCases':['Actual stale candidate refusal','Actual wrapper refusal/envelope/fetch/verify','New native version/candidate admission refusal','Cleanup/ownership verification'],'limits':'Native synthetic mechanism not actual DeveloperID/hosted cause; Apple/publisher commands doubled in controls'},'result':'Pass','confidencePercent':95.0,'scope':'Affected prepublication validation only','notReadinessOrReleaseAuthorization':True,'signingFailure':'DR01139210821088/1 still failed/unclassified; original cause UNKNOWN, no build-only closure','downstream':'Delivery current readiness/freshmain/real bothMac signing+Accepted/finalpayload/immutablepublication/publicbytes+OCI/signatures/install/custody','fieldValidation':{'filesystem':'deferred','user':'deferred'}})
(E/'C01-06-evidence-guide.md').write_text(f"""# C01 / API006 evidence guide
Step: navigate committed current evidence, not a cumulative legacy index. Source {c['sourceCommit']}; NFS local/hosted4; {now()}.

- R01-06-reuse.json: exact127inputs and attributed IMP07 full58/57+1skip, focused23overlap, fourmutants; implementation-handoff Checks Run links original logs. IMP07-03-identity-probe.json is supporting native A/B/A, not real DeveloperID/hosted cause.
- R02-06-stale-candidate.log/result.json: actual API005 source/engine mismatch expected refusal.
- R03-06-dispatch.json/final.json/summary.json: actual new run/attempt10successfuljobs,2intendedskips; each full job log has short excerpt. prepublication-result.json assembles these current observations, not readiness authority.
- R03-06-remote-before/after.json: unchanged main/tags/releases and oldDR005/009/011failedhistory.
- R04-06-reference.json/envelope.json/candidate.json: facade-generated strict schemas; companion logs/results carry exact commands/commit/environment/date. verification.json and measured-identity.json: whole retained payload/new measurement; wrong-envelope.json deliberately corrupt COPY only, negative control.
- R05-06-smoke.json: actual downloaded binary version/refusal, ownHOME/extraction cleanup.
- C01-06-cleanup.json:127source/Delivery{len(own['DeliveryFiles'])}files/history/old002–005unchanged; no live runtime/keychain resources. Candidate retained for Delivery, not deleted.
- C01-06-artifact-checks.json: final own-artifact validation; raw hosted log whitespace remains exact capture, not authored source waiver.

OriginalDR011 cause still UNKNOWN. Current signer is skipped in publish=false. Actual bothMacAccepted/finalpayload/immutablepublicreceipt gates remain mandatory Delivery. No field/physical/user Pass or release completion inferred.
""")
