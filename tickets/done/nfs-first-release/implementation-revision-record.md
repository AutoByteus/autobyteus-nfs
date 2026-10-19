# Implementation Revision Record — nfs-first-release

Current code and implementation-handoff.md are authoritative; this record locates
implementation rounds, not independent acceptance. Prior extraction/filesystem
records do not belong to this new Task.

## Revision Index

| Revision ID | Triggering Role / Report / Round | Finding IDs | Classification | Related Revision IDs | Result |
| --- | --- | --- | --- | --- | --- |
| IR-001 | Architecture Reviewer / design-review-report.md / ARCH-REV-001 | N/A | Initial Baseline | R2/SR002, SR003, ARCH-REV-001; CRR/API/DR N/A | Implementation Complete; local checks passed; source review required |

## Revision Entries

### IR-001 — Identity-bound candidate and normal-release publication

- Trigger: original ARCH-REV-001 Pass resumed after poweroff; not a duplicate round.
- Task: autobyteus-nfs-3 / project_task_97c6ab09-83cb-46df-bf28-d07b39259dd5.
- Prior authoritative result: **N/A** (initial implementation baseline).
- Current result: **Implementation Complete**, Large/High confirmed; independent
  source review next. No actual hosted/qualified/signed/published result claimed.
- Related solution: R2/SR002 Approved, SR003 Ready. Architecture: ARCH-REV-001.
  Code/API/Delivery revisions and triggering findings: **N/A** for this Task.
- Input review commit2051fd9559f4f4fa7beae68723429f8199b50004; source commit
  **886b55e1cf88f3f696334bd5e7b8c374946a594d** on codex/nfs-first-release.
- Baseline reason: implement BEH001–006 / REQ001–010 / AC001–008's release-control
  paths without pretending that implementation-local tests satisfy actual release
  acceptance. Default qualification remains empty.
- Delta: manual candidate/fresh/resume workflow; exact source/run/attempt/artifact,
  two-arch engine and complete OCI identities; structured mode/physical/user evidence
  validator; isolated signing with Accepted gate; retained final payload; annotated
  exact tag/draft/non-clobber/digest-preserving/public-download reconciliation;
  bounded installer manifest/checksum integrity; normal-version independent docs.
- Main areas: .github/workflows/release-nfs.yml; packaging/release.py,
  release_support/{identity,candidate,qualification,payload,publication}.py,
  sign-macos.sh; scripts/public/nfs/install.sh; scripts/tests/test_nfs_*.py;
  root/packaging release/testing/README documentation. Go runtime, engine recipes,
  pins, licensing and ordinary CI are byte-preserved.
- Local validation: final independent Mac/Linux arm64 native race7packages,
  vet/build/version; Python38 (Mac37executed+1skip; Linux35+3); four compile targets;
  workflow/Bash/shellcheck; expected empty-lock refusal; real nonroot skopeo on
  synthetic OCI; six detected mutations; scope/hash/import/size audit.
  implementation-evidence/ir-001/checks-and-limits.md owns detailed attribution.
- Local corrections: protected-source and host-bridged-lock harness placement;
  skopeo rootless archive-reader issue corrected using verified unchanged bytes in
  an owned layout. No runtime guard or design-policy change. All attempts retained.
- Next route: configured Large/High independent Code Review, selected by fresh
  rules in implementation-evidence/ir-001/routing.json before handoff.
- Remaining risks: actual hosted four-target candidate, physical/current-user
  qualification, provisioned credential validation/Accepted notarization, current
  main finalization, registry visibility/recovery, public downloads/install/signature
  and actual first normal v0.1.0 release remain API/Delivery responsibilities.
  No push/tag/release/deployment/TaskDone/user verification or terminal claim.

## Revision Index Addition

| Revision ID | Triggering Role / Report / Round | Finding IDs | Classification | Related Revision IDs | Result |
| --- | --- | --- | --- | --- | --- |
| IR-002 | Code Reviewer / code-review-report.md / CRR002 | CR-001 = API R03-F001 | Local Fix | R2/SR002, SR003, ARCH001, CRR001–002, API001, DR001 staging context | Correction complete; local checks pass; targeted source re-review required |

### IR-002 — Nonempty native metadata argv under supported Mac Bash

- Trigger: CRR002 failure-origin review ca048be893516d79bc1ea895b929af17580e25dd,
  confirming actual candidate39111348848/attempt1 fails both Mac jobs before
  metadata/native tests. CR-001 = API R03-F001; earlier local/source review gap.
- Classification: **Local Fix**, existing **Large/High** unchanged. No requirement
  or design change; R2/SR002 Approved / SR003 Ready / ARCH001 retained.
- Prior authoritative implementation: IR001 source886b55e; historical CRR001
  sourcePass100. Current review is CRR002 Fail and API001 Fail62.86%; those verdicts
  remain owned by those specialists, not silently replaced by these local results.
- Current implementation result: **Local Fix Complete / ready for targeted source
  re-review**, source8436d0cf6048cd3b4cadbf28815e3d9f82ba6b34. Related DR001 only
  staged reviewed branch518f4b51 for candidate execution, not finalization or release.
- Approved basis: SCN001/BEH001/REQ001–002/AC001 and dependent AC007; fresh qualified
  invocation preserves BEH002/003. No runtime/storage/signing policy deviation.
- Delta: `.github/workflows/release-nfs.yml` native metadata array now begins with
  all mandatory arguments, then appends exact fresh flags; quoted expansion is
  always nonempty under Bash3.2 nounset. No masking or shell/target replacement.
- Durable test: `scripts/tests/test_nfs_release_workflow.py` executes actual strict
  prefix/JSON pipeline under /bin/bash with inert release-command boundary; exact
  argv candidate/fresh, metadata-error propagation, missing input and pipefail.
  TESTING.md records this new scope and limitations.
- Validation: original workflow fails new regression (7tests,5assertion failures),
  corrected7pass; independent full41tests/40executed+1child skip; actionlint,
  prefix syntax/shellcheck, empty-lock refusal and three guard mutations pass their
  expected outcomes. Local shell3.2.57 arm64; TARGET strings are not amd64 execution.
- Preservation: other116/119 source inputs, all eight Delivery untracked files and
  earlier history unchanged. Owned scratch removed; no new live/remote resources.
- Next: fresh Large/High Local Fix source-review rule (ir-002/routing.json), then
  API-owned NEW current hosted candidate/full aggregation. Workflow source hash
  changed; do not qualify or relabel failed fragments. Current empty-lock hash
  26af7e5bcab00ae22d4bdebe1820c6d38b0dc51a44f1b834036334ea79528298.
- Remaining: physical/genuine-user/signing/current-main/publication/download gates;
  six secrets already provisioned, not reprovisioned or proven. No target merge,
  push, publication, TaskDone/user verification/Terminal claim. Detailed commands,
  raw results and limits: implementation-evidence/ir-002/checks-and-limits.md.

## Revision Index Addition

| Revision ID | Triggering Role / Report / Round | Finding IDs | Classification | Related Revision IDs | Result |
| --- | --- | --- | --- | --- | --- |
| IR-003 | Solution Designer SR004 replacement; Architecture Reviewer ARCH002 Pass | N/A — approved behavior change | Implementation complete | R3/SR004, ARCH002; historical IR002/CRR003/API002/DR003 context | Local checks pass; independent source review required |

### IR-003 — Release-first readiness and explicit deferred field validation

- Trigger: reviewed e08e078a3303c1ef073c45c9e0b5a044e5dd898c, SD bc1f1bb;
  direct user approved official signed normal v0.1.0 first, testing/fixes afterward.
  SR004/ARCH002 supersede old physical/user prepublication sequencing, not signing,
  integrity or host protections. Not another CR-001 local fix or retrospective failure.
- Prior implementation IR002 complete/source8436d0c, CRR003 Pass; API002 Blocked73.57
  and complete old candidate remain historical exact-input outcomes. Current new
  CRR/API result N/A — not executed yet; DR003 source of changed user direction.
- Current source3d2710b30ec1a8106faeb2f7c4f2e70183a25cd3. **Large/High confirmed**.
  Implementation complete; no approval/design deviation or scope widening.
- BEH001–006 / UC001–005 / AC001–008 mapped in current handoff. New readiness.py
  replaces qualification.py; lock exact fields/engine invalidation, --release and
  schema2 releaseTargets + deferred fieldValidation replace old authority aliases.
  All metadata/preflight/payload/publication/resume consumers use the one owner.
- Go release-only strict schema/unknown/duplicate/status/target/equality admission,
  named FieldValidation and post-success stderr notice; exact version stdout and
  installer pre-write integrity retained. Host config.Decode/state/consent/storage
  owners unchanged. No live setup, arbitrary override or old-schema fallback.
- Provenance schema2 binds readiness/deferred state; mandatory public notes disclosure
  verified even after a tampered payload is rehashed. Signing/immutable same-byte
  retry/exact engine/whole OCI sequence retained; four targets unchanged. Guides
  aligned with approved release-first policy and explicit postpublication custody.
- Local evidence: independent native Mac arm64 and owned Linux arm64 container
  Go1.27.2 race7packages/vet/build/version pass; four-target compile only; final
  Python45 with44 executed+1skip Mac and42+3skips Linux; actionlint/Bash3.2/shellcheck;
  eight detected mutants; null-readiness refusal; preservation/size/source audit.
  Last change after native checks was a fetch docstring only, then current Python
  rerun; exact sequence/limits in ir-003/checks-and-limits.md, no hidden failures.
- Source default-null-engine/readiness hash
  d75c50c83a5848d45209e85511f271f36d5d99362fd87f41b8e24263203591ac;
  future measured-engine hash differs. Real readiness remains null, not fixtures.
- Protected16 Delivery files and old API002 candidate untouched; prior IR prefix
  retained. Owned scratch/containers removed (cleanup.json). No remote write,
  credential access, engine rebuild, public download/signature or mounted-NFS proof.
- Next: fresh configured Code Review route, then affected API/new complete actual
  hosted candidate and Delivery actual readiness/signed publication/public receipts.
  Field/shared-filesystem/physical/user tests deferred—not publication/closure gates;
  Delivery→terminalSD→requestingPM owns the approved plan. No TaskDone/Terminal claim.

## Revision Index Addition

| Revision ID | Triggering Role / Report / Round | Finding IDs | Classification | Related Revision IDs | Result |
| --- | --- | --- | --- | --- | --- |
| IR-004 | Code Reviewer / code-review-report.md / CRR004 | CR-002 | Local Fix | R3/SR004, ARCH002, CRR004; API002/DR003 historical context | Two-import cleanup complete; local checks pass; targeted source re-review required |

### IR-004 — Remove two unused Python local bindings

- Trigger CRR004 Fail99, review484c85c and receipt0d8d927. Prior IR003 implementation
  complete/source3d2710b; current reviewer Fail99 solely mandatory Core7 cleanup.
  No runtime/design defect established, no new approval or broad unused-code work.
- Current result **Local Fix Complete / ready for targeted source re-review**;
  source850dfeb97e2ec396b2b134e760dc9ee802873d6b. R3/SR004 Approved / SR004 Ready / ARCH002,
  **Large/High confirmed**. No requirement/design/behavior change.
- Delta: only manifest.py `LOCK` and nfs_release_fixture.py `readiness` local import
  bindings removed. Live source.py/build.py LOCK, readiness module/consumers and all
  assertions preserved. BEH001–006/AC001–008 unchanged; recipe/source identity changes
  affect BEH001/002/AC001 next-candidate provenance, not intended runtime behavior.
- Fresh checks: independent120-input/private HOME/TMP copy, Python3.9.6 full45
  collected44 executed1 expected Go-child skip; all executed tests pass. AST/use
  and reference checks, otherwise identical AST, current source/recipe hashes and
  expected null-readiness refusal pass. No fresh Go/Linux/hosted/signing/field run.
- Current default source hash c7fd64e87b62509165d8655cc576fba9261867a306f13a93ad420776304e4a60;
  recipe hash 299db7012dcc543f8606632695d286548d1513c13ace8b108eb712984fd39274. Both
  changed; no new engine built. Other118 source inputs unchanged. NEW complete
  current-source candidate/affected API still required; old API002 remains historical.
- Prior history byte prefix and16 Delivery untracked files preserved; own scratch
  removed. No new resources, source push, target merge, release or credential work.
- Next fresh configured Large/High Local Fix source-review route (ir-004/routing.json).
  API current-delta N/A—not executed; DR003 remains context, no outcome overwritten.
  Both Mac actual signatures/Accepted notarization, final payload/publication/download
  and current-main gates remain. Deferred field/user plan is not a closure hold.
  No TaskDone/user verification/Terminal. Detailed evidence: ir-004/checks-and-limits.md.

## Revision Index Addition

| Revision ID | Triggering Role / Report / Round | Finding IDs | Classification | Related Revision IDs | Result |
| --- | --- | --- | --- | --- | --- |
| IR-005 | Delivery / release-deployment-report.md / DR005 | N/A — named signing diagnostic boundary | Local Fix | R3/SR004, ARCH002; CRR005/006, API003 exact-input context; DR005 | Diagnostic correction locally complete; targeted source review required; actual signing remains unresolved |

### IR-005 — Safe signing-stage and cleanup failure diagnostics

- Trigger DR005 Blocked after actual publish=true run39121007787/1 failed both Mac
  signing steps without any stage/notary receipt. Inputb2c6fdf, already-finalized
  main7683494 retained. Canonical ticket now tickets/done/nfs-first-release; not TaskDone.
- Prior IR004 complete/source850dfeb, CRR005sourcePass100/CRR006testPass and API003
  prepublication95 retain their scope; no actual signing pass established. Current
  source 75f4dbe5527a7159f536bafcf9448bc2d6a01604; **Large/High confirmed**, no new design/approval.
- Current result Local Fix complete for diagnostics, ready for source review. Actual
  signing stage/cause remains unknown until authorized hosted continuation; no false
  root-cause/credential diagnosis. Current-delta CRR/API N/A—not executed.
- BEH003/AC003/004/006/008: fixed stage+exit+cleanup on safe stderr and exclusive
  failure JSON; private output suppressed. Workflow retains only sanitized notary/
  failure JSON. Accepted/notary exit0/cleanup success still required; original command
  exit preserved. Failed search-list capture cannot be restored during cleanup.
- Only existing sign shell/workflow, two affected tests and TESTING/package release
  guidance changed. No Go/runtime/host guard/engine/installer/authorization change.
- Validation: baseline missing receipt detected; current17 focused and independent52
  Python tests (51exec+1expectedGo-childskip) pass; Bash3.2 syntax/ShellCheck/actionlint;
  four mutants detected. Attempts disclosed, no actual Apple/hosted/field execution.
- Source hash bf6b1732ad6561da15d610afb2c5e6b8d83982fbf23f20e0684eda18b9d1ba62;
  prior a425e3f887f3156d920d022801df9069ba5bc2d49bdb0e4dd8097ee76a01fe9e; engine recipe
  299db7012dcc543f8606632695d286548d1513c13ace8b108eb712984fd39274 unchanged. Stable
  readiness/engine/candidates preserved but stale for new source; no invented records.
- Own scratch removed; no live keychain/storage/credentials/remote effects. Prior
  history byte prefix retained; Delivery documents and previously pushed main untouched.
- Next fresh Large/High Local Fix source-review route, then current affected API/new
  complete candidate and Delivery-owned readiness/actual signed release. Field/user
  deferral unchanged, not a blocker; both-Mac Accepted/signature/public receipts still
  required. No TaskDone/Terminal. Evidence: implementation-evidence/ir-005/.

#### IR-005 supplemental receipt — DR-006, no new implementation round

Delivery8f05549 records user-requested actual local existing-identity signing Pass
on independent9fa4e69 (product identical75f4dbe): native arm64 development build,
Developer ID/runtime/timestamp signature, strict verify and signed version passed;
normal keychain search list unchanged and owned scratch removed. Evidence belongs
to Delivery, not a new implementation execution. See delivery-evidence/dr-006/
summary.md/checks.json/local-result.json/verify.log/details.log/cleanup.json.
P12/password/ephemeral hosted keychain, Intel signing and notary remain unproven;
DR005 actual cause unknown and full Delivery Blocked. Carry into existing source
review/API continuation without restart, new source/approval, speculative secret
changes or new IR classification. Only current handoff/history updated on receipt.

#### IR-005 supplemental receipt — DR-007, no new implementation round

Delivery14a5661 records actual local Apple Accepted/exit0 at2026-10-19T04:57:21Z,
submission16cd8853-b4f7-41a3-b676-e99029765633, for the arm64 development diagnostic
on unchanged75f4dbe product. Delivery verified binary/ZIP and9 preparation-log
hashes; implementation only read the saved evidence. DR006 local signing evidence
now has this supplemental local notary result; failed attempt1 HTTP401 is retained.
User requests official-release continuation and reports updating GitHub password;
metadata time04:58:54Z does not prove value equality or hosted authentication.
See delivery-evidence/dr-007/summary.md, verification.json,
apple-accepted-response.json and github-secret-update-metadata.json.

Prior/current implementation result and Large/High/R3/ARCH002 classification are
unchanged: IR005 diagnostics locally complete, existing targeted source review and
current affected API/new complete candidate still required. No new code/tests/IR
round or duplicate dispatch. DR005 original cause, hosted import/keychain and both
Mac final signing/Accepted/publication remain unresolved; full Delivery Blocked.
Retained local diagnostic/candidates, Delivery evidence and pushed main preserved;
no credential read/change, remote action or field questionnaire. Only own handoff
and revision record updated; supplemental receipt goes to the existing reviewer.


## Revision Index Addition

| Revision ID | Triggering Role / Report / Round | Finding IDs | Classification | Related Revision IDs | Result |
| --- | --- | --- | --- | --- | --- |
| IR-006 | Delivery / release-deployment-report.md / DR009 | N/A — actual codesign stage failure | Local Fix | R3/SR004, ARCH002; IR005/CRR007/008/API004 scoped prior results | Diagnostic portion complete; source review required; actual hosted cause/release unresolved |

### IR-006 — Allowlisted codesign failure observations

- Trigger DR009: run39204643596/1 at finalized mainf830c50, both Mac sign/exit1/
  cleanup complete; notary not reached. Intakeb279d55, source2c12ec61f6339d0d264280b7117787ec821425af.
- Prior IR005 diagnostics complete, CRR007 sourcePass100 / CRR008 testPass /
  API004 prepublication95 retained. Current result diagnostic Local Fix portion
  complete, ready for targeted review; **DR009 actual root cause not resolved**.
  R3/SR004/ARCH002 and Large/High unchanged; no design/approval or field-test loop.
- BEH003/AC003/004/006/008: existing signer captures codesign output privately,
  classifies bounded exact messages to fixed observations, preserves original exit
  across parsing failure, and deletes capture with existing cleanup. Other stages
  report not-collected. Command/keychain/trust/notary/publication semantics unchanged.
- Four paths only: sign-macos.sh, signing tests, TESTING.md, packaging/RELEASE.md.
  No Go/app/host/engine/workflow/lock/readiness change. No speculative credential
  replacement, chain import, unlock/search-list tweak, fallback or new framework.
- Current local21 focused and56 full tests (55 executed/1 expected Go-child skip),
  Bash syntax/ShellCheck/actionlint pass;4 mutations and original-code control
  detected; source/recipe/preservation checks pass. Attempt1 fixture shadowing46
  failures preserved; corrected without product change. No actual Apple/hosted run.
- Current source hashdd6cde88374cce42ec8b44c24e41abff3af6f01803890824dd783848e0d101a5; priord5aac8cd30dd41526436c52cbc73d74ee5e15b8fb701d07d8ccf8a0cf0e976fd; recipe299db7012dcc543f8606632695d286548d1513c13ace8b108eb712984fd39274 unchanged.
  Existing actual candidate/readiness now stale, preserved rather than relabelled.
- Own source/HOME/TMP scratch removed, no live keychain/credentials/remote action.
  Prior history byte prefix and mainf830 ancestry preserved; other owners untouched.
- Next configured targeted source review → affected API/new complete current-source
  candidate → Delivery-owned readiness/hosted diagnostics and actual signed release.
  Current-delta CRR/API pending; no DR009 resolution/TaskDone/Terminal claim.
  Evidence: evidence/IMP-06-*; former handoff and failed-attempt raw evidence in
  implementation-evidence/ir-006/. No new cumulative upstream inventory.

- Supplemental user-requested reference: read-only superrepo5096011 and exact
  Apple-Actions63fff01 comparison recorded in IMP-06-18. Search-list difference
  remains a lead, not actual root proof; no -A/timestamp weakening/raw-output or
  Electron behavior copied. Same IR006/source, no new dispatch or approval.
