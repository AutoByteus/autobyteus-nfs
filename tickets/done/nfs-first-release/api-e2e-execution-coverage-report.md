# API/E2E Execution Coverage Report — nfs-first-release

## API-REV-007 — Result and scope
**Pass95.00% for affected SR005 executor validation only. NOT actual publication or Task completion.** R3/SR004 Approved, SR005 Ready/ARCH003 Pass, Large/High/Reviewed. Task project_task_97c6ab09-83cb-46df-bf28-d07b39259dd5. IR009 final source/tests22205cc84a29e6aa66ba5673b0a60c8db95ddc80, production4c665e0eb23adf1f9bb45363a496b7786e76b138; current tested executor 6cb497f4a0bb83d52ddfc41b5aaad95a8e482440, all130 product inputs identical. CRR013 sourcePass100 and API006/CRR012 histories remain separate authorities.

Plan and upstream inventory: api-e2e-coverage-investigation.md. History: api-e2e-revision-record.md; progress append-only api-e2e-test-progress.md. Canonical archived ticket `/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/nfs-first-release/tickets/done/nfs-first-release` is not completion. Evidence flat `/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/nfs-first-release/tickets/done/nfs-first-release/evidence` under R01–R07/C01-07-*. No API production/durable test edits.

**Changed fact since API006:** DR013 successfully signed/notarized BOTH actual Mac binaries, then failed publication after creating the immutable tag and empty draft. Those exact signed-byte successes carry; original overall run39215470944/1 remains failed. The live corrected discovery now finds the exact draft read-only. Actual same-byte hosted recovery/publication remains Delivery work and has NOT run here.

## Routing classification
- Task size: **Large**; architectural risk: **High**; input: **Reviewed**.
- Successful output: **Code Review**; Proportional test-code review: **Required** for the seven IR009 paths listed below. Fresh rule selects `/software_engineering_team/code_reviewer` only; see evidence/C01-07-routing.json. Evidence commit `66ba73a38321656b223b34fd51d2248d5f47cb5d`.

## Environments / identities / emulation
| Environment | Exact execution | Limits |
|---|---|---|
| I — reused repository |IMP09-06 at4c665,10 at22205cc; current130 equal. IndependentMac26.5.2arm64/Python3.9.6/Bash3.2/privateHOME+TMP|Full72collected71executed1expectedGochildskip; current publication15 after4additional tests; overlap, not full76 rerun.6mutants. Go parent not rerun|
| A — actual read-only |Current source6cb497f4a0bb83d52ddfc41b5aaad95a8e482440; localMac26.5.2arm64/Python3.9.6, gh API; actual tag-derived P and exact Actions downloads; owned APFS temp/TMP|GET-only, no authorization/effects; snapshot bytes data only, current code executes|
| M — actual bytes/emulated effects |Independent current Git clone/privateHOME+TMP, H=6cb497f4a0bb83d52ddfc41b5aaad95a8e482440; synthetic E=9a830501c689f3bee9f4c5a8b792cc8bb00b983f|ONLY scratch synthetic authorization; full current prepare/publish/admission/Git/full validators real; candidate transport uses exact fresh downloaded bytes; release/jobs modeled from fresh R06; HTTP upload adapter consumes actual file stream but no network; OCI/public-download effects doubled|
| Carried original product |P238bdc183e8affac99ffdee9be9cb333b0eb126f, API006 candidate7bd486e/run39213489075/1; DR013 payload/run39215470944/1|Exact product/hash/bytes unchanged, not current executor build or new signing|

## Cases
Evidence names relative to evidence/. Reused Implementation exact commands/exits are in implementation-handoff Checks Run; API reuse audit records applicability. Current commands/harnesses are retained and their logs/JSON contain inputs/date/environment.

| Case | AC portion | Command / scenario | Env | Result | Evidence / exact look-for and limits |
|---|---|---|---|---|---|
| R01 |002/004/006/008|Reused IMP09-06/10/05/static/07/11|I|Pass — Reused|R01-07-reuse.json; `Ran 72 tests`/`OK (skipped=1)` at4c665, `Ran 15 tests`/`OK` at22205cc. Only subsequent delta publication test. Six mutants detected; saved IMP09-07 endpoints NOT fresh. Initial alias/interrupted implementation attempts remain preserved.|
| R02 |001/002/006|Current facade `--operation verify-candidate --directory <actual API006>`; actual tag-derived context_for(dispatch=False) without authority|A|Pass|R02-07-candidate-refusal.log: `Release refused: Executed workflow differs from hashed source`, exit1; refusals.json: `Reviewed recovery authorization required`, actualGET tag. Correct refusal before effects.|
| R03 |001/006|Reuse original API006 candidate/build4/engine2/OCI; record/member hashes and sourceP applicability|Carried|Pass — Reused|R03-07-carried.json: memberBytesUnchanged, original hash3e1af43a…; API006 R03/R04. No new executor native qualification|
| R04 |002/003/006|`/usr/bin/python3 packaging/release.py --operation inspect-bound --tag v0.1.0 --directory <owned/new> --output <report>` from N|A|Pass|R04-07-command.json/log/inspection.json/verified.json: actual retained envelopes downloaded/full P validators; `verifiedPayloadJobId:117940491787`; `executorPublicationAdmission:not performed`; authorization null. Snapshot TMP empty|
| R05 |003/005|Match newly downloaded original Mac archives/binaries/provenance to DR013 Accepted/strict signature evidence, no re-sign|Carried/A|Pass — Reused|R05-07-carried-signatures.json: archiveAndBinaryMatchesFreshDownload; original DR013 retained-payload-verification and codesign logs. BOTH actual Accepted statuses/binaryhashes match. Not public download/install|
| R06 |004/006|Actual current discover(expected417014769)/inventory/payload_jobs and GET tag/main/run/artifacts|A|Pass|R06-07-observations.json: publishedByTag null; unique exact draft417014769, original body/directID match, assets0; payloadjob and4native/bothsignsteps success inside overallfailed run; wrappers not expired; writes0|
| R07 |002/004/006/008|`R07-07-run.py` → isolated `R07-07-worker.py`; real old bytes/current full admission→prepare→publish→completed retry; known-missing/excluded-drift controls|M|Pass — Emulated|R07-07-result.json/console.log/cleanup.json:18 actual-byte streams via production upload code to fake HTTPS; sameID/no tag or draft create; completedRetryNoWrites; known missing refuses; hash-excluded drift refuses full-tree admission. Synthetic E/result published is NOT real publication; clone/authority deleted|
| C01 |008|Final current remote correlation, exact own/retained hashes, source/other-owner/history checks and own cleanup|A|Pass|C01-07-cleanup.json/remote-after.json: originalpayload/C equal fresh downloads, older002–005 intact,130inputs/67otherowner files unchanged; own inspection+clone absent; realAuthorizationAbsent/remoteUnchanged|
| Q01-01–Q06-07/U01 |007|Approved postpublication field/user plan|N/A|Not Tested — Deferred|43IDs notPassed, no host questionnaire, not publication/closure prerequisites|
| D01/D02 |002–008|Delivery genuine stable authorization for reviewedH, freshE integration, actual same-byte hosted recovery/OCI/public downloads/install/signatures/custody|Delivery|Not Tested — downstream|Mandatory remaining release proof; DR013 publication Blocked is not overridden|

Eight scoped cases Pass (includes attributed reuse/emulation),43Deferred+2Downstream NotTested. No new product failure. **One API harness expectation correction:** initial R01-07 orchestrator expected later source/engine mismatch, but current candidate correctly refused earlier at changed workflow identity. R02-07-attempt-note.json preserves it; original script/log retained. No product weakening or repeat completed R01/CLI. This is not a passing initial harness run.

## Acceptance-Criteria Proof
Full release acceptance remains incomplete; proven statements below are named affected portions, not waivers. No Only The User Can Check designation. Field tests are approved Deferred, actual publication is ordered Delivery responsibility.

| Criterion / portion | Critical | Evidence | Disposition |
|---|---|---|---|
| AC001 fresh unbound candidate strictness; original candidate applicability |Yes|R01/R02/R03|Proven; no oldcandidate promotion as executor/newbuild|
| AC002 complete P readiness/source/engine/OCI verification + separate E/H admission/refusal |Yes|R01/R02/R04/R07|Proven executor validation; genuine real authorization **Not Proven**, Delivery creates after judgement|
| AC003 original both-Mac DeveloperID/runtime/timestamp/Accepted exact bytes |Yes|R04/R05/R06 + DR013 original logs|Proven by exact attributed carry and fresh original-byte/job verification; new signing unnecessary|
| AC003 final publicly downloaded signatures |Yes|D02|Not Proven; retained Actions downloads are not public release downloads|
| AC004 fixed draft-ID discovery/no recreation, admission/effect sequencing/retry/no-clobber controls |Yes|R01/R06/R07|Proven at actual read-only + real-byte/emulated effect boundary|
| AC004 actual immutable normal public release/asset writes |Yes|D01/D02|Not Proven; actual draft417014769 still0assets, no API publication|
| AC005 unchanged original installer/native bytes and safeguards |Yes|R03/R05/DR013|Carried; actual released-target public install/notice/version **Not Proven**, D02|
| AC006 unchanged whole candidate/payload/engine/OCI, dual identities, refused stale/excluded drift |Yes|R02/R03/R04/R07/C01|Proven affected verification; actual public OCI/equality/publication **Not Proven**, D01/D02|
| AC007 current affected checks/truthful field deferral |Yes|Cases + approved plan|Proven portion; completed first signed public release/custody **Not Proven**|
| AC008 cleanup/preservation/current executor bounded claims |Yes|C01 + Cases|Proven API portion; fresh target finalization/actual release docs/public receipts/custody **Not Proven**, Delivery|

## Confidence / broader decision
Scope is current affected executor validation, not whole task or actual public release. Simple mean; every score tied to evidence.

| Category | Post-repository | Final | Evidence / residual limit |
|---|---:|---:|---|
| Requirement/AC proof|75|95|Affected explicit portions direct; remaining publication separated, not waived|
| Changed-boundary directness|85|95|Actual current inspect/discover/full original validators; current full admitted path on actual bytes in clone|
| Cross-boundary realism/mock gap|75|90|Fresh real GitHub retention/draft/job visibility and real byte stream; mutations/registry/public-download boundaries still emulated here and require actual Delivery|
| Environment/configuration/identity|90|100|Exact130inputs, P/H/E separation, actual original wrapper/job/member/signing hashes; no identity ambiguity|
| Failure/edge/lifecycle/recovery|90|95|Six mutants, real absent authority, existing known draft, complete retry/no-write and hash-excluded drift refusal with actual bytes|
| User-surface (CLI)|90|95|Actual inspect facade/current refusal; original CLI/distribution proof carried; browser/desktop N/A; public install later|
| Durable regression relevance|95|95|Seven changed test/fixture paths match SR005; full current production coverage carried + actual-byte integration; proportional review next|

Postrepository600/7=85.71%; final665/7=95.00%, no category below90. Broader **Required and executed**: actual read-only inspector/discovery and current complete actual-byte emulation. Saved endpoint tests alone were insufficient. No new native/engine/candidate/signing campaign, no browser/live storage/credential action. No score authorizes remote effects or marks whole-release critical portions complete.

## Durable tests / transition / cleanup
API added/updated/removed durable paths: **None**. IR009 changed seven durable test/fixture paths: scripts/tests/nfs_release_fixture.py, test_nfs_packaging.py, test_nfs_release_publication.py, test_nfs_release_records.py, test_nfs_release_recovery.py, test_nfs_release_workflow.py, test_nfs_source_identity.py. Request proportional successful-test review of that cumulative SR005 delta and evidence, not new full source/architecture round. No claim one full76 suite ran; full72 and finalpublication15 overlap. Expected standalone Go-child skip remains; no Go parent runtime rerun.

Original bound candidate/readiness/payload directly usable without migration under verified P; no global ROOT override, old-code execution or regenerated metadata. E hash is **e3e814176d8315f0426df379035a995b6c0e6d5f89f82483f121b074c79eea21**, distinct from original product **3e1af43a4191c17ddf8a5d6043a1e374c5cd0101f2ac18dd6ee9fee79c131086**. Missing real recovery authorization correctly refuses. Synthetic record only existed in removed isolated clone, never real packaging/recovery or authority evidence.

Owned inspection `/Users/normy/nfs-api007-inspect-m50i0aqe` and R07 clone removed. No persistent runtime/resources, no new toolchains/Go/keychains/signing/live nodes. Original `/Users/normy/nfs-first-final-dr013-gmvotux9/payload`, API006 candidate and older002–005 remain byte-identical, local notary diagnostic untouched. All67 protected Delivery files/hash and prior API history prefix preserved;130product inputs unchanged. Actual main/tag/draft0assets unchanged before/after. No push/merge/tagmove/reset/dispatch/release/publication/TaskDone/userverification/Terminal.

## Remaining Delivery custody / immutable identity
Retain P238bdc183e8affac99ffdee9be9cb333b0eb126f; tagf4a04fd0c80a6625708ba002b4cef5507a03f514; draft417014769; run39215470944/1/payloadjob117940491787/artifact12169472209. Original wrapper b552faeaf6de1337ef8cf3056878b9bf0f1822faed5645033a8d5145fd1d0336; publicationSHA3b0cbedd15782871e0c88c51b6847abcf276e7db00aab6f10c4dd387b4133dc8; expiry2027-01-17T07:21:36Z. API006 candidate remains run39213489075/1/artifact12168544425. Full exact binding in actual R04 inspection, not synthetic R07 authority.

Delivery must judge evidence, record genuine stable reviewed-H authorization, integrate/fresh-check actual E/main with no executable drift, run authorized same-byte recover and verify real assets/OCI/anonymous downloads/install/signatures and custody. No need to repeat successful signing/candidate/native campaigns solely for this executor correction; preserve original bytes and all main ancestry. Field/user stays Deferred, Delivery→terminalSD→requestingPM plan unchanged. **API007 affected executor Pass95; actual DR013 publication remains Blocked until its owner proves recovery.**
