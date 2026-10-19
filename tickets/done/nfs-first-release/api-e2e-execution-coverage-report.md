# API/E2E Execution Coverage Report — nfs-first-release

## API-REV-005 / result and scope
**Pass95.00% — affected prepublication validation only; NOT a signing/root-cause fix or release Pass.** Task project_task_97c6ab09-83cb-46df-bf28-d07b39259dd5; Large/High/Reviewed; R3/SR004 Approved/Ready/ARCH002 unchanged. IR006 source2c12ec61f6339d0d264280b7117787ec821425af and CRR009 sourcePass100 diagnose codesign failure only. Actual DR00939204643596/1 remains failed; codesign cause UNKNOWN, signing/release unresolved. API004 historical result and candidate are not relabelled.

Canonical ticket `/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/nfs-first-release/tickets/done/nfs-first-release` (archive is not completion). Plan/upstream inventory: api-e2e-coverage-investigation.md. History: api-e2e-revision-record.md. Progress: api-e2e-test-progress.md. No plan deviation, no API product or durable-test changes. New evidence flat `/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/nfs-first-release/tickets/done/nfs-first-release/evidence` under case-prefixed `*-05-*`. Strict candidate/envelope JSON retains exact schema; companion command logs supply context. Long full job logs have excerpts. Original IMP evidence remains attributed, not copied or rerun for independence.

## Tested builds / environments
| Env | Exact input | Configuration / limitation |
|---|---|---|
| I — reused IMP |2c12ec6;127 current non-ticket files equal tested source|Implementation Checks Run: independent APFS/privateHOME+TMP; Darwinarm64/Python3.9.6/Bash3.2; actual shell with external doubles, not Apple|
| H — current hosted |1c00b7afd6327fb4ba69dbc176c69d698a309fee; run39208967217/attempt1, same source/workflow/dispatch|Ubuntu24.04arm64/amd64, macos15arm64/macos15-intelamd64, Go1.27.2; publish=false, no signing secrets or publication|
| A — current facade/native smoke |Same product; local docs descendant6bc8979 differs only ticket receipt|Local macOS26.5.2arm64/Python3.9.6/gh read-only Actions API; privateHOME for downloaded CLI; no setup/install/keychain|

## Cases
All evidence names relative to evidence folder. Reused cases leave commands/environment/evidence/quoted outcomes to implementation Checks Run, as skill requires.

| Case | AC | Command / steps | Env | Result | Evidence / look for | Notes |
|---|---|---|---|---|---|---|
| R01 |003/004/006/008|**Reused IMP-06-01/02/09/10**|See IMP row|Pass|See implementation Checks Run; R01-05-reuse.json is applicability audit|56collected55executed1expectedchildskip;21focused overlap;4detected mutants; expected original-signer11assertion failures. Initial46fixture-shadowing failures corrected by Implementation remain preserved, not current source failure. No API local suite repeat.|
| R02 |001/002/006/008|Reused IMP-06-03–08/11; additional `/usr/bin/python3 packaging/release.py --check-publish --candidate /Users/normy/nfs-first-candidate-api004-a7bxyrbb/candidate` from N|A; reused details per IMP|Pass|R02-05-stale-candidate.log: `Release refused: Candidate source/engine differs`; R02-05-stale-result.json exit1|Actual old retained candidate refusal, not mislabeled no-candidate control; no public effects.|
| R03 |001/005/006|`gh workflow run release-nfs.yml --repo AutoByteus/autobyteus-nfs --ref codex/nfs-first-release -f release_tag=v0.1.0 -f source_sha=1c00b7afd6327fb4ba69dbc176c69d698a309fee -f publish=false`; exact attempt + full job logs|H|Pass|R03-05-dispatch.json, final.json, summary.json, job-*.log/excerpt-*.log, remote-after.json|10successful jobs/0failed jobs/0cancelled jobs/2intended payload-publish job skips. All4native race7packages/vet/Python56(55executed/1expectedchildskip)/build/version/archive; native signing and signing-receipt upload steps intentionally skipped. engine2/fullOCI/aggregation. Go nonverbose: no invented individual counts. Both old DR005/DR009 observed failed; main/tags/releases unchanged.|
| R04 |001/002/006|Actual facade candidate-envelope/fetch-candidate/verify-candidate, exact artifact12166434040; copied wrong-wrapper refusal; exact argv in R04-05-*.log/results|A|Pass|R04-05-reference.json/candidate.json/verification.json/measured-identity.json; wrapper-refusal.log: `Release refused: Retained artifact envelope differs`|Complete19files/128137599bytes; wrong wrapper refuses before destination. Current real record, not fixture or hand-assembled partial artifacts.|
| R05 |005|Downloaded Darwinarm64 `version`; `verify-release <own release.json>` in privateHOME|A|Pass|R05-05-version.log: `v0.1.0`; candidate-refusal.log; smoke.json `"noHomeWrites": true`, `"scratchAbsent": true`|Exact version stdout/empty stderr; candidate admission expected exit1; no setup. Current native suites cover unchanged legacy/false/positive-notice controls.|
| C01 |008|Final facade candidate verify/source/history/Delivery/old-candidate preservation, cleanup|A|Pass|C01-05-cleanup.json `"candidateReverified": true`, `"DeliveryUnchanged": true`; candidate-final-verify-result.json|127input equality;Delivery10files excluded; own smoke absent; priorAPI002/003/004 members unchanged; local diagnostic untouched.|
| Q01-01–Q06-07 (42) / U01 |007|Approved postpublication field/user plan|N/A|Not Tested — Deferred|postpublication-testing-plan.md / approval-record-sr004.md|43IDs not Passed, not prepublication/closure prerequisite; no questionnaire|
| D01/D02 |002–008|Genuine current readiness/freshmain/actual both-Mac signing+Accepted/finalpayload/public bytes+OCI/install/signatures/custody|Delivery|Not Tested — Downstream|packaging/RELEASE.md; DR009 actual failure receipts|Mandatory later gates; DR009 signing failure unresolved, not credited as Pass or waived|

**51IDs =6Pass/0Fail/0Blocked/45NotTested (43Deferred,2Downstream)** for this stage. Repeated platform suite executions/focused21 are not additional unique tests. No new API product failure; own initial artifact audit had an overbroad filename glob, retained/corrected without product or prior raw-evidence changes (C01-05-audit-attempts.log). prior IMP failures/mutants and DR005/009 stay historical and attributed.

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
Owned smoke extraction/HOME removed; no new local Go/toolchain/full-suite scratch or persistent runtime resources. No live storage, keychain, credential, registry mutation or app action. Hosted jobs complete with provider post-job logs; provider disposal not independently audited. OldAPI002/003/004 immutable records/members verified unchanged. `/Users/normy/nfs-local-notary-xq_ym2f6` untouched, not accessed for credentials. Delivery10current files protected/excluded from API staging; source127inputs unchanged.

Retain NEW `/Users/normy/nfs-first-candidate-api005-61mqnd8a/candidate` (parent0700), 19files/128137599bytes through Delivery release/recovery. Artifact12166434040, expiry2027-01-17T06:16:31Z; wrappersha256:212bf6bf33719abd0ba6f69f138f69f11f7a6a3b1aa49097a5e8d32ec8bc2e01; recordSHA59bab38d340db74491fb080f5b203efe6dc18f3674aee1ffd79de99133989f76. Exact measured sourceHash **0a209d1efe327e13feeabe426c90e411728813a7261467c0428271eeee1db8e3**, engineManifestSHA **bcb213bbb72e1698622afce9d7e6cc456dbe06268798b9336085227b5967bcc3**, OCIroot **sha256:dc8fe178c5e2f2efb33cafc164a4aefe5afa097a488e94f6998ce6d6a5cb796e**. R04-05-candidate.json contains full member/child identities. R04-05-measured-identity.json shows only the two buildInventory SHA256 values changed from preserved engine lock; package/source fields and recipe299db7012dcc543f8606632695d286548d1513c13ace8b108eb712984fd39274 unchanged. do not promote local preserved-engine hashdd6cde… automatically or infer deterministic build equality. No binaries/generated product metadata committed.

## Latest authoritative result / next
**API-REV-005 Pass95.00% — affected prepublication only.** IR006 diagnostics validated at executable control scope, not actual codesign root fix. DR009 and DR005 remain failed/unknown cause; official release remains unresolved. No speculative secret/keychain repair. No API push/mainreplay/signing/publication/deployment/TaskDone/user-verification/Terminal. DR010 staging prerequisite only, not full Delivery completion. Fresh routing after evidence commit: Large/High proportional changed-signing-test review, then normal Delivery continuation and unresolved signing gates. Full AC portions listed NotProven above remain mandatory.

Compact prepublication receipt: evidence/R03-05-prepublication-result.json (not readiness or release authorization). Own evidence audit: evidence/C01-05-artifact-checks.json; raw-log whitespace exceptions preserved explicitly.

Precommit whitespace check also caught five header-only generated excerpts with blank EOF; excerpts were populated from existing full raw artifact/digest lines and formatting corrected. No original job log or product/test edit, no test rerun, no failed commit or outcome handoff. See C01-05-audit-attempts.log.
