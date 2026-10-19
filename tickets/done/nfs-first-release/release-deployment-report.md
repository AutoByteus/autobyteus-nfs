# Delivery / Release / Deployment Report

## DR-009 — Blocked: both hosted Mac signing commands failed

**Source finalization Completed; official signed v0.1.0 publication Blocked — Local Fix. Not Delivery Completed, TaskDone or Terminal.** Task nfs-first-release / autobyteus-nfs-3 / project_task_97c6ab09-83cb-46df-bf28-d07b39259dd5. Large / High / Reviewed; R3/SR004 Approved/Ready, ARCH002, CRR007 sourcePass100, CRR008 testPass and API004 prepublicationPass95 remain distinct authorities.

### Integrated evidence and completed source finalization

Initial fresh origin/main `7683494050b85a298ed08a55592e70f86a010a7a` was already ancestor of intake `5eba0339b0f8fa23feb42f653475eff979623b2f`; all127 product inputs matched IR00575f4dbe. No base integration delta or redundant base-only rerun. Delivery followed API AC Proof→Cases→raw evidence/reused IMP checks, verified ten hosted log hashes/summary lines, real candidate/envelope/refusals/version/cleanup and exact engine/OCI. Current measured readiness is genuine, not fixture-derived.

Candidate39202907777/1/artifact12165175911 at44e2487 is retained at `/Users/normy/nfs-first-candidate-api004-a7bxyrbb/candidate`. SourceHash `d5aac8cd30dd41526436c52cbc73d74ee5e15b8fb701d07d8ccf8a0cf0e976fd`; engine manifest `ffeb62714b4853ae8f71b3bddd385451da407de21073de331f38e9bc96a8c179`; OCI `sha256:2ab8d6aa1ac7cd387f5a48bac17e6c9560c3b4a5b574474c4399c746a980b20e`. Only both measured engine buildInventory hashes differ from the prior lock; recipe/source/package pins unchanged. No reproducibility or old-candidate equality claim.

Stable readiness/native/control/review records and engine lock updated; authorization/plan/public notes unchanged. Independent actual-readiness data regression passed52collected/51executed/1expected Go-childskip. Owned scratch removed. check-publish/new source hash and portable paths passed. Ticket `e8012cc9876e3d5a4e5f5960809079ece8cf449b` pushed; fresh unchanged target --no-ff merged as `f830c50bf1238270343afce151dd05b65b10237a`, identical tree, postmerge readiness/hash and remote/workflow bytes verified, main pushed. Local codex/nfs-first-release includes f830. Canonical checkout untouched. **Do not undo or replay this completed source finalization.**

### Actual release result and bounded repair

[Release run39204643596](https://github.com/AutoByteus/autobyteus-nfs/actions/runs/39204643596)/attempt1 on exact f830, normalv0.1.0, publish=true, candidate39202907777 completed **failure**:3success/2failure/6skipped. Four native race7packages/vet/Python52(51executed/1expectedskip)/build/version checks passed. Both Linux native/archive jobs succeeded. Both actual Mac jobs failed at **`stage=sign exit=1 cleanup=complete`**, before notarization. New sanitized artifact upload succeeded; both ZIP digests and exact single JSON members independently verified. This is useful real hosted diagnostic proof, not a signing Pass.

The ordinary strict-errexit path reached `codesign --force --timestamp --options runtime --keychain ... --sign ...` after P12 import, key partition and selected-identity checks returned successfully. Its underlying cause remains **unknown**: private tool output is suppressed. No evidence of a notary rejection or bad app-specific password in this run; notary was never reached. Do not speculate about certificate chain/keychain/ACL or reprovision secrets without evidence. DR007 local development-arm64 Apple Accepted remains valid only for that diagnostic, not this hosted path; DR005 failed run stays historical with original unknown cause.

Implementation owns a **bounded packaging Local Fix**: diagnose the exact codesign command safely, minimally repair the evidenced cause and add focused regression proof. Preserve secret-safe cleanup, real DeveloperID/Accepted-only gates and four targets. If additional diagnostics are necessary, expose only controlled allowlisted cause categories, never raw private stderr, xtrace, credentials, account/identity text or keychain/P12 material. Follow normal proportional review/affected API; changed hashed production needs a new applicable candidate/readiness. No source/architecture/field campaign or new approval loop is requested.

### Preserved effects, cleanup and custody

Payload/publisher jobs skipped; no final signed payload or public release from this run. Fresh authenticated tagv0.1.0/release/exact package endpoints returned404; main stillf830, remote ticket e801. Developer Checks39204616155 and39204622206 both completed success. Preflight12164918633, Linux intermediates12164879147/12164923851 and sanitized signing diagnostics12165705122/12165337638 are retained Actions artifacts, **not release assets**. No blind repeat dispatch, tag/asset mutation, package visibility change or new credential action.

Source finalization evidence `source-finalization.json` describes the earlier pre-dispatch moment; `dispatch.json` and `publication-run-final.json` are its later outcome. Primary current receipts: `delivery-evidence/dr-009/failure-assessment.json`, `publication-execution-summary.json`, `publication-log-index.json`, `signing-artifact-receipts.json`, `remote-after-failure.json`, `triggered-runs-final.json`, `verification.json` and `source-finalization.json`. Prior polling snapshots/failed helper attempts remain historical, not current verdicts.

Own readiness scratch removed; bounded process/scratch check found no active run monitor or dr009 scratch. Hosted receipts report cleanup complete; this is the script's attestation, not independent keychain forensics. Retain active ticket worktree/branches and all candidates/private local diagnostic for recovery. No live host storage, mount, application, canonical checkout or PM data action. Field/filesystem/physical/user tests remain **Deferred**, not failed and not publication prerequisites. Plan custody remains Delivery→terminal Solution Designer→requesting PM after successful completion. No duplicate task or premature terminal. Current failure documents are a local ticket checkpoint, not a second main publication.

### Current guide, verification and completion gates

Guides: root `RELEASE.md` last changed3d2710b30ec1a8106faeb2f7c4f2e70183a25cd3; `packaging/RELEASE.md` last changed75f4dbe5527a7159f536bafcf9448bc2d6a01604; both read at final f830. Deviations **None**, proposed guide changes None. Release decision **normal/stable v0.1.0** from explicit user signed-release-first direction, not the older extraction no-release decision. Notes `release-notes.md` remain prepared/unpublished; publisher never used them.

| Gate / acceptance criterion | Current evidence judgment |
| --- | --- |
| AC001 candidate / AC002 current readiness | Proven within prepublication scope; verification.json and actual-readiness rerun |
| AC003 actual hosted signing/notary | **Not Proven — actual codesign failed on both Macs**, no notary submission |
| AC004 immutable public release | Not Proven — publisher skipped, current remote404 |
| AC005 public installation/signature/notice/version | Not Proven — public bytes unavailable; candidate/version refusal proof remains scoped |
| AC006 final payload/wholeOCI/public equality | Not Proven — no final payload; actual candidate integrity remains proven |
| AC007 release completion/plan custody | Not Proven — explicit deferral retained, completion/custody awaits release |
| AC008 source finalization/docs/cleanup | Source finalization and owning docs sync completed; safe recovery retention, final release/cleanup/terminal outstanding |

No user check or physical-host questionnaire required under R3. Applicable release/rollout **Blocked**. Deployment/persisted-data transition **Not required/None**. Worktree/branch retirement deferred for unresolved repair, not forcibly cleaned. No rollback/deletion of published artifacts; there are no publication effects from this run. Current downstream classification **Local Fix**, recommended recipient Implementation Engineer via fresh rule, not a requirement gap or missing API campaign. Successful terminal eligibility **No**; terminal package sent **No**.

---

## Latest DR-008 — reviewed source available for API004; publication pending

Execution prerequisite **Completed**; full Delivery **Blocked / not yet eligible**. Requested by API004 after IR005/CRR007 source Pass100, not an API result or publication handoff. Large/High/Reviewed, R3/SR004 Approved/Ready and ARCH002 unchanged.

Fresh origin/main `7683494050b85a298ed08a55592e70f86a010a7a` already ancestor; no integration delta/rerun or main finalization replay. All127 non-ticket inputs equal IR005 `75f4dbe5527a7159f536bafcf9448bc2d6a01604`. Fast-forwarded ONLY origin/codex/nfs-first-release fromb599e476 to `44e2487b4b30da99797c149c17fa0c8bcaa6a87f`. Exact remote ref and GitHub workflow bytes verified: blob `dc9acc3b3390806b80db759fc38038c5b675bae8`, SHA256 `f759931a10aaf88cbf43b49e37a0272c2acf2b06cf26a4fd6fa6bc0c902f6e35`; workflow388178899 active. Current production source hash `bf6b1732ad6561da15d610afb2c5e6b8d83982fbf23f20e0684eda18b9d1ba62`.

API dispatch inputs: ref `codex/nfs-first-release`, `release_tag=v0.1.0`, `source_sha=44e2487b4b30da99797c149c17fa0c8bcaa6a87f`, `publish=false`. API owns the NEW complete candidate dispatch and current affected validation, reusing unchanged IMP checks where evidenced. Delivery performed no candidate dispatch, main merge/push, readiness change, signing/notary, secret reprovisioning, publication, deployment, TaskDone or Terminal. Main/tags/releases unchanged. DR005 failed run and old API003 candidate remain historical; DR007 local Accepted does not prove hosted cause/import/both-Mac/final payload.

API-owned uncommitted plan/report/progress untouched/unstaged; before/after API-doc hashes equal at push observation. Own reports and dr008 receipt remain uncommitted so exact requested HEAD stays fixed. No runtime scratch created; retain worktree/candidates. Field/user tests remain Deferred, not gates; current review/API, actual both-Mac signing/Accepted, final immutable payload/publication/download/custody gates retained. No new approval/review loop or duplicate recipient. Exact proof: `delivery-evidence/dr-008/staged-source-receipt.json`, `commands.json`, `verified-remote-workflow.yml`. No long-lived guide/notes impact for source availability. Earlier rounds below are history.

---

## Latest DR-007 — actual local notarization Accepted; official release pending

Apple accepted the real local arm64 development diagnostic on attempt2 (exit0), submission `16cd8853-b4f7-41a3-b676-e99029765633`. Saved response/receipt, binary/ZIP and9 preparation log hashes verified. Attempt1 HTTP401 is preserved. User-generated new app-specific password worked locally; user reports updating GitHub and metadata confirms `APPLE_APP_SPECIFIC_PASSWORD` updated2026-10-19T04:58:54Z. Delivery read no secret value/clipboard/private key and cannot prove the GitHub value from its timestamp.

**Diagnostic Pass; overall Delivery Blocked**, not official release or field/user verification. Fresh origin/main7683494 is already ancestor of8317316;127 product inputs still equal IR00575f4dbe. No integration delta or rerun. Current IR005 diagnostics await already-started targeted review and affected API/new candidate; previous API003/readiness cannot qualify changed production. Continue that existing sequence, then Delivery readiness/main/fresh hosted signing/publication/download checks. Do not restart source review or bypass it, replay prior finalization, speculate about P12, or request field/user approval. Hosted original cause still unknown; local Apple acceptance does not prove hosted import/keychain/both-Mac signing.

Evidence: `delivery-evidence/dr-007/summary.md`, `verification.json`, `apple-accepted-response.json`, `notarization-result-attempt-002.json`, `github-secret-update-metadata.json`. Signed diagnostic/ZIP retained privately for user's local request; build scratch/toolchain/cache already removed. No source/test/guide/notes changes, remote push/tag/release/TaskDone/Terminal. R3/SR004 Approved/Ready, ARCH002, Large/High/Reviewed retained. No long-lived docs impact; no published behavior changed. The following older rounds remain historical, not current status.

---

## DR-005 completed round — Blocked; source finalized, signing failed

Task **nfs-first-release / autobyteus-nfs-3 / project_task_97c6ab09-83cb-46df-bf28-d07b39259dd5**. **Large / High / Reviewed**, R3/SR004 Approved/Ready, ARCH-REV-002 Pass, IR004/CRR005 source Pass100, CRR006 successful-test Pass; API-REV-003 **prepublication Pass95.00%**, not a public-release result.

DR-001–004 remain historical; DR-005 is now the authoritative Blocked delivery result. This is not terminal. Project guides `RELEASE.md` and `packaging/RELEASE.md` at reviewed product850dfeb; packaging opening prose synchronized only. **No deviations.** Staged main finalization before signed execution is explicitly permitted.

## Initial integration and verification

Fetched origin/main7e375984 before edits, already ancestor of41714c79; no base advance/new merge or checkpoint required. All120 product inputs matched review. No redundant base-only rerun; affected genuine-readiness data independently tested45collected/44executed/1expectedskip, exit0. Owned source/HOME/TMP removed. Readiness check and exact measured source hash pass. Delivery followed API proof/cases and actual raw lines/hashes, not summary alone (`delivery-evidence/dr-005/verification.json`). API95 and reviews100/Pass accepted only within their scope.

| Acceptance criterion | Evidence judgement at prepublication |
| --- | --- |
| AC001 | R02-R04 Proven: current complete actual candidate, source/run/engine/OCI/native identity |
| AC002 | R01-R05 Proven contract and current checks; actual stable readiness prepared in this round |
| AC003 | R01 signing fixtures only; actual signing/notary/download pending D01/D02 |
| AC004 | R01/R02 controls proven; actual public immutable effects pending D01 |
| AC005 | R01/R03/R05 admission/version/refusal proven; public signed install pending D02 |
| AC006 | R01/R04 candidate integrity/provenance proven; published equality pending D01/D02 |
| AC007 | R01-R05/C01 prepublication/honest deferral proven; release/custody pending |
| AC008 | R01/R02/C01 source/API cleanup proven; docs/main/final receipts/cleanup pending |

Cases R01–R05/C01 are linked by API execution report. All10 actual candidate logs hashes and literal summary lines checked,4native7packages/Python45 each,2engine/completeOCI; actual candidate wrapper/source/native refusals/version independently verified. Apple/GitHub/final-positive-install fixtures doubled. Field/user deferred, not proven, no user check required before release per explicit R3 approval. D01/D02 actual signing/public evidence remains Delivery's next gate; no duplicate upstream validation cycle.

## Release decision

**Stable / normal v0.1.0**, user: “please publish first, then we could test. and if we found problem, then we fix”; “create one official signed release first. please”. Exact authorization in stable record and dr003. Six secrets already provisioned; no re-request absent actual failure. Actual Developer ID/Accepted notary not inferred from configuration.

## Documentation / staged finalization

Docs sync Updated; README/packaging guide/readiness/lock and own handoff/notes updated (docs-sync-report.md). Archive to tickets/done/nfs-first-release before final ticket commit; archive is not a TaskDone claim. Branch codex/nfs-first-release, target origin/main. Fresh --no-ff finalize branch and exact remote receipts pending. Canonical checkout/PM files and old histories are protected. No tag/release created yet.

## Authorized publication method

After source finalization: manual release-nfs.yml on exact main, release_tag=v0.1.0, candidate_run_id=39118784695, publish=true. Validate stable readiness/source equality; actual final native/signing/payload precedes public effects. Monitor every pipeline. Retain exact candidate and signed payload for recovery. Never move tag/clobber assets/rebuild or resign bound outputs. Specific package public visibility only if needed; no broad permission changes.

Actual release/download/signature/OCI equality receipts **Pending**. Field/filesystem/physical/user tests **Deferred** with approved plan, not pending publication prerequisites. No deployment/live setup/migration. Persisted-data action None. Rollback is not deletion of published artifacts; actual postpublication defects fix forward to approved new version.

## Cleanup / final status

Owned readiness-test scratch removed; active worktree/branches/candidate retained for unfinished publication/recovery. Cleanup after actual final receipts pending. Historical candidates remain distinct and not promoted. No source/test reroute needed at present. Final verification, release and safe cleanup not yet complete; successful terminal package **Not eligible / not sent**. Postpublication plan custody follows Delivery → terminal SD → requesting PM, not premature parallel dispatch.

## Actual DR-005 finalization and release outcome (supersedes pending-stage descriptions above)

Source finalization **Completed**: ticketb599e476 pushed, current-base --no-ff merge7683494050b85a298ed08a55592e70f86a010a7a pushed/remote verified, identical tree, unchanged measured productiona425e3f8, check-publish pass. Archived ticket path tickets/done/nfs-first-release. Portable-name check1455paths/no errors, tracked prose diff check clean. Historical raw log whitespace retained. Guides followed; no deviation.

Actual manual publish=true run39121007787/1 **Failed**, not partial public release: both Mac signing boundaries exit1 without diagnostic stage/notary receipt; Linux jobs and four-target native checks pass, payload/publish skipped. Developer CI39120986961 and39120991701 success. No actual Apple rejection, certificate mismatch or Accepted status inferred. No generated final signed payload. No tag/release/package observed (404); existing main remains intact. `failure-assessment.json`, raw failed jobs117656510844/117656510925, `publication-execution-summary.json`, `publication-artifacts.json`, `remote-after-failure.json` govern.

Verification: prepublication sufficient; AC003 real signature/notary Not Proven; AC004 actual public immutable release Not Proven; AC005 actual public signed install Not Proven; AC006 final public equality Not Proven; AC007 release/custody Not Proven; AC008 actual release-doc/cleanup remainder pending. No user/field check request: explicitly deferred R3. Current native/release-boundary API evidence not invalidated by this separate actual signing failure; it never claimed actual signing success.

**Escalation classification: Local Fix — packaging signing diagnostic boundary.** Implementation Engineer owns a bounded sanitized stage/exit failure receipt and actual-boundary correction; root cause not yet established because the script suppresses then deletes diagnostics. This known code-local diagnosability fix requires no product decision. Preserve cleanup/secrets/Accepted-only protections, no xtrace/raw secret output, no speculative secret re-provision, no unsigned fallback. Normal affected review/API gates apply if production hash changes; do not reuse current candidate as new-source proof. Fresh applicable rule selects implementation only, no duplicate SD/API dispatch.

Cleanup **safely deferred for recovery**: isolated test scratch removed; active ticket/finalize branches/worktree and candidate retained, no live processes/storage effects owned here. Hosted post-job cleanup succeeded, keychain scratch removal not independently visible in masked logs. Canonical checkout/PM/unrelated worktrees untouched. No deployment/persisted-data change. Release notes prepared but not published. Rollback not applicable to absent public effects; finalized source not undone.

Final status: evidence verification only prepublication complete; repository finalization Yes; actual release No; recovery retention intentional; terminal eligibility **No**, successful terminal not sent. DR005 Blocked local-fix handoff, not TaskDone. Field/user plan stays under Delivery custody until release succeeds then terminalSD→requestingPM.

## DR-006 — actual local diagnostic; no public effects

User authorized local build/sign/log inspection. Fresh tracked main7683494 already ancestor; no integration delta/source finalization replay. Exact diagnostic input9fa4e6968f3239ad1517fc33077eb527d0d76502, same127 non-ticket inputs as IR00575f4dbe. Go1.27.2/checksum verified; fresh native arm64 development build plus version pass, real existing-keychain Developer ID sign (hardened runtime/timestamp) exit0, strict signature/details and signed version pass. Raw logs/check hashes and actual binary SHA in delivery-evidence/dr-006. Independent owned scratch removed; before/after keychain search list unchanged. No credentials read/exported, keychain settings altered, notary submission or public effects.

AC003 gains bounded local key/signature evidence only: GitHub P12/password import, temporary keychain and actual both-Mac Accepted notarization/download evidence still Not Proven. Hosted failure root cause remains Unknown; local success does not prove an export-password mismatch. No full API/current-candidate/readiness acceptance, release metadata or public install claim. IR005 source diagnostics require normal existing review/API continuation; no duplicate dispatch. Full delivery result **Blocked**, terminal ineligible; retain DR005 main/release-attempt history, worktree/candidates for recovery. No long-lived doc impact. Supplemental result goes only to existing local-fix owner under fresh most-specific rule; user notified of accurate limited result.
