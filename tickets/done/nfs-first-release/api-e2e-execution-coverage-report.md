# API/E2E Execution Coverage Report — nfs-first-release

## API-REV-006 — Result
**Pass95.00% for affected prepublication validation only. NOT a signed-release Pass or closure of the original hosted cause.** R3/SR004 Approved/Ready, ARCH002, Large/High/Reviewed unchanged. Task project_task_97c6ab09-83cb-46df-bf28-d07b39259dd5. IR007 product3f67e36193c246ca08b49cda818be5c0f94eba51 / CRR011 sourcePass100 repaired owned-keychain lookup at the bounded source/mechanism scope. Actual original DR01139210821088/1 remains sign/exit1/cleanupcomplete/unclassified; root cause UNKNOWN. Old API005 is historical, not current-source evidence.

Plan/upstream inventory: api-e2e-coverage-investigation.md. History: api-e2e-revision-record.md. Progress: api-e2e-test-progress.md. Canonical `/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/nfs-first-release/tickets/done/nfs-first-release` is archived but release unfinished. New flat evidence `/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/nfs-first-release/tickets/done/nfs-first-release/evidence` uses case prefix *-06-*; original IMP evidence remains attributed, not copied or rerun. No product/durable-test changes by API, no plan deviation.

## Environments and identity
| Env | Input/setup | Boundary/limits |
|---|---|---|
| I — reused repository |Exact product3f67e36;127inputs equal current; see implementation Checks Run|Independent APFS/privateHOME+TMP, local Darwinarm64/Python3.9.6/Bash3.2; real shell, external command doubles|
| M — supporting native |IMP07-01–03 at intake79e3539; read exact probe source/results|Local macOS26.5.2arm64 synthetic imported identity; explicit keychain A/B/A, timestamp=none for nonrelease experiment only; not current real credentials|
| H — new hosted |Source/workflow/dispatch7bd486e2e27743441a870f7cd8db1f6c4ee0b493;run39213489075/attempt1|Ubuntu24.04 amd64/arm64, macos15arm64/macos15-intelamd64; Go1.27.2; publish=false, actual signer skipped|
| A — facade/native |Current NFS worktree, matching product; privateHOME for new downloaded CLI|Local macOS26.5.2arm64/Python3.9.6/gh read-only Actions API, no setup/install/keychain/credential work|

## Cases
Paths relative to evidence/. Reused checks use Implementation Checks Run for exact commands/environment/outcome lines; R01 audit proves applicability. Focused tests overlap the full suite. Repeated hosted platform runs are not unique additional tests.

| Case | AC portion | Command/steps | Env | Result | Evidence and what to look for |
|---|---|---|---|---|---|
| R01 |003/004/006/008 controls|**Reused IMP07-04/05/12/13**, supporting01–03; read native source/results and prior DR011 failure first|I/M|Pass|R01-06-reuse.json:127equalinputs; IMP-07-05-python.log `Ran 58 tests`/`OK (skipped=1)`=57executed;23focused overlap;4mutants detected; original signer control expected1failure. IMP-07-03-identity-probe.json: sign1→0/verify0/runtime→1, exact original list restored and owned scratch removed. No API suite/keychain repeat.|
| R02 |001/002/006/008 refusal|Reused IMP07-06–11/14; `/usr/bin/python3 packaging/release.py --check-publish --candidate /Users/normy/nfs-first-candidate-api005-61mqnd8a/candidate` from N|A|Pass|R02-06-stale-candidate.log/result.json: `Release refused: Candidate source/engine differs`, exit1. Actual stale candidate distinct from reused missing-candidate refusal.|
| R03 |001/005/006 current candidate|`gh workflow run release-nfs.yml --repo AutoByteus/autobyteus-nfs --ref codex/nfs-first-release -f release_tag=v0.1.0 -f source_sha=7bd486e2e27743441a870f7cd8db1f6c4ee0b493 -f publish=false`; exact run/attempt/job logs|H|Pass|R03-06-dispatch.json/final.json/summary.json and job-*.log/excerpt-*.log:10success/0failure/0cancel/2intended payload/publish skips; all4native race7packages/vet/Python58/build/version/archive; engine2/fullOCI/aggregation. remote-after.json: main/tags/releases unchanged; DR005/009/011 still failure.|
| R04 |001/002/006 integrity|Actual facade candidate-envelope/fetch-candidate/verify-candidate; copied wrong envelope negative; exact argv in logs/results|A|Pass|R04-06-reference.json/candidate.json/verification.json:artifact12168544425, 19files/128137754bytes; wrapper-refusal.log `Release refused: Retained artifact envelope differs` before destination creation. measured-identity.json shows actual new engine difference, no relabel.|
| R05 |005 CLI candidate contract|Actual new downloaded Darwinarm64 `version` and `verify-release <own release.json>`, privateHOME|A|Pass|R05-06-version.log `v0.1.0`; candidate-refusal.log expectedexit1; smoke.json `"noHomeWrites": true`, `"scratchAbsent": true`. Exact version stdout/empty stderr; candidate intentionally unadmitted; no setup.|
| C01 |008 retention/cleanup|Final actual facade verify plus source/history/other-owner/old-candidate audits|A|Pass|C01-06-cleanup.json `"candidateReverified": true`, `"DeliveryUnchanged": true`; final-verify result.127inputs unchanged, Delivery10files excluded, oldAPI002–005 bytes intact, own smoke removed.|
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
Owned smoke HOME/extraction removed. No new local Go/full-suite/keychain/credential/process/storage/container resource. Hosted jobs completed with provider post-job logs retained; provider disposal not independently audited. Prior API002–005 record/member bytes unchanged; local development notary diagnostic untouched, never accessed for credentials. All127product inputs unchanged; Delivery10files protected and excluded from API staging. No other repository work.

Retain **/Users/normy/nfs-first-candidate-api006-a8aune30/candidate** under parent0700, 19files/128137754bytes for Delivery/recovery. Artifact12168544425, expires2027-01-17T07:02:55Z; wrappersha256:f6294686e10c8c4c3dac98122dd2adbccfab1d78f1846dd56473f8ec68705ef8; recordSHA67eb4dd2f120a0d33a3d99eeac3cb055162ad7d3a9a3d66821e8f7686afff58b. NEW measured sourceHash **3e1af43a4191c17ddf8a5d6043a1e374c5cd0101f2ac18dd6ee9fee79c131086**, engineManifest **95d275cff765d48d18978fef12d5a2c9f3d986998c9ff60836eb0ebcd86c5970**, OCIroot **sha256:e39b1b13d09c6c6c604de470023a8c3d6ba834d127f2df5e2dbb79e931a585ec**; full children/members in R04-06-candidate.json. Do not substitute preserved-engine sourcehash7cb7b6… or oldAPI005 readiness; actual measurement governs, no reproducibility assumption.

## Next / result authority
**API006 scoped prepublication Pass95.00%; original hosted cause and actual signed release still UNVERIFIED.** CRR011 source repair accepted; this build-only success does not execute signer or prove DR011 root cause resolved. DR005/009/011 remain failed history. Fresh most-specific successful-test route after committed evidence, then normal Delivery current readiness/fresh-main/signing+Accepted/finalpayload/immutable public bytes/signature/install/plan-custody gates. Preserve main72b8a4/f830/768 ancestry; no replay/reset. API made no push/real signing/publication/TaskDone/user-verification/Terminal claim.
