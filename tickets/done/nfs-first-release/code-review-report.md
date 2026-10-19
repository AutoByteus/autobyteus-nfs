# Code Review Report — nfs-first-release

## Review Round Meta

- Date **2026-10-19**; task **autobyteus-nfs-3 / project_task_97c6ab09-83cb-46df-bf28-d07b39259dd5**.
- **Implementation Review / CRR-007 / round7 / Full Re-Audit of the affected release boundary.** The requested review remains bounded to IR005. Full structural checklist and scorecard are re-evaluated because the new signing failure/cleanup lifecycle is beyond the prior CR-002 import finding; this does not reopen architecture, unrelated source, or field testing.
- Current intake **55e45c13297e9f588a61461c41ddb8a754eb647c**; product **75f4dbe5527a7159f536bafcf9448bc2d6a01604**; implementation evidence **9fa4e6968f3239ad1517fc33077eb527d0d76502** plus docs-only DR006/007 supplements. All127 non-ticket inputs match the tested product tree.
- Worktree `/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/nfs-first-release`, branch `codex/nfs-first-release`, target origin/main. Canonical ticket **tickets/done/nfs-first-release**; archival does not imply completed release.
- Authority: **R3/SR004 Approved/Ready; ARCH-REV-002 Pass**. Requirements, design, approval/postpublication supplement, investigation/solution history, design review/architecture history, implementation handoff/IR005 and prior canonical reviews form the unchanged basis. Updated code-reviewer SKILL and handoff-references, shared principles, NFS AGENTS/DESIGN/TESTING applied. No guideline conflict.
- Trigger **DR005 Blocked / Local Fix**, actual publish run39121007787/1 at7683494: both Mac signing commands exited1 without stage/notary receipt. Trigger evidence is `delivery-evidence/dr-005/failure-assessment.json`; source/path assessment `implementation-evidence/ir-005/diagnosis.md`. This is not a new API failure-origin or successful-test review.
- Prior source result **CRR005 Pass100** and separate **CRR006 test Pass / API003 prepublication95** retain their exact-input scope. Their results do not qualify IR005. DR006/007 local diagnostics are bounded supplemental evidence, not final release acceptance.

## Routing Classification Review

**Large / High / Reviewed confirmed.** Overall release/signing/immutable-publication risk is unchanged. Independent source review is required. Current result **Pass100 — source scope only**, no failure classification. Fresh most-specific source-Pass rule determines next recipient; normal continuation is affected API validation, not direct publication.

## Review Scope

Exactly six NFS-only paths versus b2c6fdf: `packaging/sign-macos.sh`, `.github/workflows/release-nfs.yml`, their two existing Python suites, `TESTING.md`, and `packaging/RELEASE.md`. Rechecked the complete relevant caller path through workflow native job, signer, upload, payload/signing proof, readiness and publication gates; unchanged owners use prior source evidence plus current identity verification. No test/source edits by reviewer.

No application/frontend/Guide/superrepo/PM changes. No Go, installed host state, engine recipe/pins, installer, target/channel, authorization or field-test change. No reviewer credentials/keychain/signing/notary action, retained candidate access, remote fetch/push/dispatch, main merge, release/tag, live storage, TaskDone or Terminal. No delegation. Existing published-source finalization7683494 must not be replayed or undone.

## Upstream Behavior And Production-Path Basis Confirmation

**Confirmed**, no changed intended behavior or material ambiguity for this bounded correction. R3 signed-release-first remains governing; field/shared-filesystem/physical/user testing is Deferred, not a release prerequisite. Actual signing, identity, public bytes and completion gates remain.

| Behavior | Status | Current path / lifecycle evidence |
| --- | --- | --- |
| BEH001 | Confirmed | Manual candidate → four native checks and complete engine/OCI retention. Production signing/workflow hash changed; NEW complete candidate required. |
| BEH002 | Confirmed | Candidate verification → readiness exact source/engine/refs → final admission. Existing recorded a425e3 source differs from bf6b17; no automatic lock rewrite. |
| BEH003 | Confirmed | Fresh native metadata → signer private commands → cleanup → safe diagnostic on failure or Accepted proof on success → archive → payload → immutable publication. Failed signer/cleanup blocks archive/payload; upload is diagnostic only. |
| BEH004 | Confirmed | Existing versioned download/checksum/manifest → strict CLI admission → deferral notice/install/version unchanged. |
| BEH005 | Confirmed | All host source/config/pending/consent/mount/detach guards byte-preserved; no migration or live invocation. |
| BEH006 | Confirmed | Updated testing/release prose describes receipt limits; approved postpublication custody and truthful release status retained. |

## Supported Product Scenario And Reachability Gate

| Scenario / contract | Independent actor / event and goal | Supported entry → forward path / lifecycle / expected consequence | Validity / use |
| --- | --- | --- | --- |
| SCN001 / REQ001/002 | Maintainer requests current candidate | Manual publish=false → fixed source/workflow → engine/OCI/native checks → retained identified candidate without public effects | Supported Normal Scenario; Use |
| SCN002/003 / REQ004/006 | Maintainer requests authorized signed v0.1.0 | Manual fresh publish → readiness/native metadata → real signing/keychain/notary → successful cleanup → retained payload/publication; only actual Accepted allows success | Supported Normal Scenario; Use |
| SCN003/007 / REQ004/010; design D3 cleanup/privacy contract | Observed signing job failure during authorized release; operator needs precise unfinished stage without leaking credentials | Real run39121007787 → script exits before notary → cleanup → fixed diagnostic stderr/receipt → always-upload → next bounded diagnosis; no publication from failure | Supported Explicit Edge Scenario; Use; actual failure independent of new fixture |
| SCN005 / REQ006; D3 | Signing command or cleanup operation fails under the retained fail-closed/resource-preservation contract | Native signing → search-list capture/ephemeral keychain → unsuccessful operation → restore only completed snapshot/delete owned resources → preserve primary code, reject cleanup failure | Supported Explicit Edge Scenario; Use; command failure is an existing signing contract, not a fabricated user action |
| SCN006 / REQ006 | Operator resumes interrupted publication | Same-input dispatch → original bound payload → exact missing-stage reconciliation or conflict/expiry refusal; no rebuild/re-sign of bound payload | Supported Explicit Edge Scenario; Use; unchanged owner |
| SCN004/007/008 | User downloads or Delivery reports/releases and hands off later testing | Verified versioned bytes → no-setup smoke → actual receipt → terminal SD → requesting PM plan custody | Supported Normal Scenario; Use; downstream obligations, not local test claims |

### Candidate Finding And Mechanism Gate

| Candidate | Observation / mechanism | Independent basis → path / consequence | Evidence | Disposition / scope |
| --- | --- | --- | --- | --- |
| CG013 | Safe fixed diagnostic surviving cleanup | Actual DR005 failure + SCN003/007 privacy/diagnosability; private tool output was deleted, so failure stage unavailable. New saved stderr and exclusive sidecar expose only stage/code/cleanup. | sign-macos.sh:6–45,46–125; IMP-05-09 baseline missing receipt; IMP-05-01/02/08 controls | Promote mechanism — this ticket, satisfactory; no new finding |
| CG014 | Pending search-list capture and cleanup failure status | D3 preservation/fail-closed contract during real signing: failed strict pipeline can leave partial JSON; applying it would restore an untrusted snapshot. Only successful capture moves into cleanup eligibility; primary failure survives cleanup error. | script:19–31,57–59; command-failure/cleanup tests; failed-capture and errexit mutants | Promote mechanism — this ticket, satisfactory; not alleged as DR005 root cause |
| CG015 | Preserve rejected/nonzero notary result and prevent diagnostic artifact promotion | REQ004/006 signing gate: command exit and Accepted status are both required. Notary receipt can exist on failure but workflow native success/payload gates still block. | script:100–120; workflow native/always-upload/payload conditions; payload.signing_proof; notary/cleanup controls | Promote mechanism — this ticket, satisfactory; no gate weakened |

No new actionable finding or held premise affecting the source verdict. The original hosted cause remains unestablished: this review does not diagnose credentials from duration, local success or a secret-update timestamp, and prescribes no secret changes. That outstanding execution result does not invalidate the independently established diagnostic correction.

## Prior Finding Resolution

| Finding / boundary | Previous status | Current verification |
| --- | --- | --- |
| CR-001 / API001 Mac Bash3.2 empty array | Source resolved CRR003; actual candidate green API003 | Remains resolved: native nonempty args and strict invocation unchanged; existing actual-prefix controls retained in reused Python suite. |
| CR-002 unused imports | Resolved CRR005/IR004 | Remains resolved; import-owning files unchanged. No new dead binding in touched shell/tests found. |
| DR005 diagnostic/cleanup boundary (no prior CR ID) | Unlocalized actual signing failure; Local Fix requested | IR005 diagnostic and cleanup correction accepted at source scope. Original run remains failed and actual hosted cause unresolved, not marked fixed. |

## Structural / Design Checks

All24 mandatory checks and full scorecard re-evaluated for the affected release boundary. Byte-identical unrelated owners retain earlier evidence; no repeated product execution is claimed.

| Check | Result | Evidence | Required action |
| --- | --- | --- | --- |
| Task design health assessment is present, evidence-backed, and preserved by the implementation | Pass | R3 release-first design-health decision preserved; DR005 adds only bounded diagnosis/cleanup within the existing signing owner. | None |
| Implementation matches approved behavior-defining supplemental artifacts | Pass | Approval SR004 and postpublication plan preserved; no restored physical/user gate, no unsigned fallback. | None |
| Data-flow spine inventory clarity and preservation under shared principles | Pass | DS1 candidate → DS2 readiness → DS3 final metadata/signing/payload/publication; DS4 installer and DS5 original-payload resume retained. Local failure return path now explicit. | None |
| Ownership boundary preservation and clarity | Pass | Shell owns ephemeral signing lifecycle; workflow schedules and retains allowlisted results; payload verifies final proof; publication owns external effects. | None |
| Off-spine concern clarity (off-spine concerns serve clear owners and stay off the main line) | Pass | Fixed diagnostics observe signing without becoming admission authority or exposing private command output. | None |
| Existing capability/subsystem reuse check (no fresh helper where an existing subsystem should own it) | Pass | Existing signing script and upload step extended; no second signer, secret handler or framework. | None |
| Reusable owned structures check (repeated structures extracted into the right owned file instead of copied across files) | Pass | One cleanup trap and reusable run_case/FAKE fixtures; no repeated command-failure implementation per stage. | None |
| Shared-structure/data-model tightness check (no kitchen-sink base, no overlapping parallel shapes, specialization/composition used meaningfully) | Pass | Failure sidecar has only schema/status/stage/exitCode/cleanup. Existing sanitized notary shape remains separate, not a merged success/failure authority. | None |
| Repeated coordination ownership check (shared policy has a clear owner instead of being repeated across callers) | Pass | Signing acceptance remains command success + Accepted + successful cleanup; downstream payload retains independent exact-binary proof. | None |
| Empty indirection check (no pass-through-only boundary) | Pass | sign_and_notarize owns private-output/strict-command boundary, not pass-through indirection. | None |
| Scope-appropriate separation of concerns and file responsibility clarity | Pass | Two production paths remain cohesive: shell for local signing; YAML for job sequencing. No host/runtime change. | None |
| Ownership-driven dependency check (no forbidden shortcuts or unjustified cycles) | Pass | Workflow calls signer; payload reads sanitized proof. No runtime or application imports, registry effects or alternate signing caller. | None |
| Authoritative Boundary Rule check (callers do not depend on both an outer owner and that owner's internal manager/repository/helper/lower-level concern) | Pass | Public release entry still uses facade/readiness/payload; diagnostic sidecar cannot bypass those owners or authorize publication. | None |
| File placement check (file/folder path matches owning concern or explicitly justified shared boundary) | Pass | packaging/sign-macos.sh and its existing tests are appropriate owners; no new generic helper folder. | None |
| Flat-vs-over-split layout judgment (layout is readable for the scope and not artificially fragmented) | Pass | 126-line script and existing test fixture are readable without arbitrary splitting. | None |
| Interface/API/query/command/service-method boundary clarity (one subject, one responsibility, explicit identity shape) | Pass | BINARY and SANITIZED_RECEIPT interface unchanged; separate exclusive failure JSON and numeric exit contract explicit. | None |
| Naming quality and naming-to-responsibility alignment check (files, folders, APIs, types, functions, parameters, variables) | Pass | Fixed stage labels map to concrete operations; pending versus completed search snapshot distinguishes cleanup eligibility. | None |
| No unjustified duplication of code / repeated structures in changed scope | Pass | One trap handles cleanup and one fixed formatter emits diagnostics; tests share fixture machinery. | None |
| Patch-on-patch complexity control | Pass | Replaces deleted/private-only failure logging with one bounded diagnostic path; preserves nonconditional errexit, no fallback or retry overlay. | None |
| Dead code removed in the touched files and modules (Core Principle 7) | Pass | Replaced private import/partition/sign logs and old failure test removed; current stage variables/functions/imports have direct uses. No obsolete owner or disabled control found. | None |
| Relevant test scenarios and assertions are clear and requirement-aligned | Pass | Actual shell tests cover exact stage/code, hostile output exclusion, notary rejection, signals and cleanup; upload patterns exclude private files. | None |
| Test fixtures/helpers are reasonably reusable and test structure remains coherent | Pass | Owned TemporaryDirectory plus fake security/codesign/xcrun/ditto/openssl; only external effects doubled, actual Bash execution retained. | None |
| No stale, duplicated, or compatibility-only tests are retained in changed scope | Pass | Old coarse failure case replaced by specific controls; accepted path and six-input preflight retained. No compatibility-only or unexplained skip added. | None |
| API/E2E readiness for the next workflow stage | Pass | IMP05 final checks reuse exact127 unchanged inputs; new hosted current-source candidate and affected API are still needed, not replaced by fixtures. | None |

## Source File Size And Structure Audit

Conservative nonempty lines include comments. Current-delta basis b2c6fdf; `code-review-evidence/crr-007/source-audit.json` records exact Git deltas. Test/fixture/docs sizes are exempt.

| Changed source | Before | After | >500 | Added+deleted / >220 | Ownership / placement | Action |
| --- | --- | --- | --- | --- | --- | --- |
| packaging/sign-macos.sh | 75 | 126 | Pass | 125, below trigger | Cohesive existing signer and ephemeral lifecycle | None |
| .github/workflows/release-nfs.yml | 359 | 361 | Pass | 4, below trigger | Existing orchestration; receipt allowlist only | None |

Earlier cumulative workflow delta above220 was already reviewed; this change does not fragment ownership. No forced split is warranted.

## Legacy / Backward-Compatibility Verdict

| Check | Result | Notes |
| --- | --- | --- |
| No backward compatibility mechanism | Pass | One current signer; no alternate shell/version/signing fallback. |
| No legacy old-behavior retention | Pass | Old private-only failure logging replaced; no unsigned bypass. |
| Dead code removed in touched files | Pass | Obsolete local logs/coarse fixture replaced; all current variables/functions/imports have live use. |
| Approved persisted transition followed | Pass | Host state Not Affected; generated release evidence rebuilt/reaccepted for new source. |
| No version-specific dual reads/writes/fallback | Pass | New failure sidecar is a diagnostic, not a compatibility admission shape. |
| Transition mechanics match design | Pass | Preserve old candidates/readiness/history; no relabeling or migration. |

## Dead / Obsolete Items Requiring Removal

None found in this review's touched scope. No unrelated cleanup expansion.

## Docs-Impact Verdict

**Yes, addressed** in TESTING.md and packaging/RELEASE.md: fixed diagnostic fields, exclusive receipts, pending-capture cleanup and mocked-versus-real limits are described. Caught EXIT/INT/TERM cleanup is covered; no SIGKILL or physical-host guarantee is claimed by the review. Delivery retains official finalization/release docs and actual public evidence ownership.

## Additional Material Premise Validation

No new architecture premise or scenario reclassification. Prior immutable-payload/current-source/signing premises remain confirmed. CG013–015 contain the new bounded diagnostic/cleanup mechanism evidence. DR007 does not establish the hosted exported-P12/import path or original failure cause.

## Review Scorecard

**10.0/10 = 100.00/100**, simple mean of ten categories for source-quality visibility only; not an execution confidence or release acceptance percentage. No in-scope evidenced defect warrants a deduction. Scores do not waive downstream gates.

| Priority | Category | Score | Evidence / weakness / improvement |
| --- | --- | --- | --- |
| 1 | Data-Flow Spine Inventory and Clarity | 10 | Full signing-to-publication path and failure return explicit; no source deficiency found. |
| 2 | Ownership Clarity and Boundary Encapsulation | 10 | Existing signer owns cleanup; workflow/payload/publisher roles remain separate. |
| 3 | API / Interface / Query / Command Clarity | 10 | Stable two-argument invocation; explicit fixed diagnostic and exit contract. |
| 4 | Separation of Concerns and File Placement | 10 | Bounded existing script/workflow ownership, no application coupling. |
| 5 | Shared-Structure / Data-Model Tightness and Reusable Owned Structures | 10 | Small distinct diagnostic/notary shapes and shared test fixture. |
| 6 | Naming Quality and Local Readability | 10 | Fixed stages and pending snapshot clearly describe lifecycle. |
| 7 | API/E2E Readiness | 10 | Current local evidence reusable; package ready for new hosted candidate/affected API, not release. |
| 8 | Runtime Correctness And Behavioral Fidelity | 10 | Strict failure, privacy, cleanup and Accepted-only semantics preserved at reviewed boundary. Actual hosted cause remains execution work. |
| 9 | No Backward-Compatibility / No Legacy Retention | 10 | Single path, obsolete logging removed, no bypass. |
| 10 | Cleanup Completeness | 10 | Owned scratch cleanup and error handling covered; no source cleanup finding. |

## Evidence And Checks

The implementation **Checks Run was read before any check execution**. No repeated product check is needed: inputs unchanged, outcomes clear, no new finding requires a reproduction. Reviewer executed **zero product tests/builds/lints/signing/hosted checks**. Only read-only review identity/size and reviewer-artifact checks are new.

| ID / owner | Scope and exact source | Result / limits | Primary evidence |
| --- | --- | --- | --- |
| IMP-05-01/02, implementation | 75f4dbe; full Python and focused actual shell/workflow with external command doubles | 52 collected/51 executed/1 standalone Go-child skip; focused17 overlap. Bash3.2.57. Not Apple/hosted proof. | evidence/IMP-05-01-python-full.log; IMP-05-02-signing-workflow.log |
| IMP-05-03–07, implementation | Same tree; Bash syntax/ShellCheck/actionlint/source/recipe/required-input refusal | Final checks pass. No-candidate refusal says only missing candidate, NOT an executed stale-candidate test. | Headered evidence/IMP-05-03 through07; ir-005/checks-result.json |
| IMP-05-08/09, implementation | Four deliberately mutated copies; baseline production + corrected new fixture | Four intended assertion failures detected; baseline missing receipt fails. These are negative controls, not candidate failures. | evidence/IMP-05-08-summary.md and mutations.log; IMP-05-09-baseline-control.log |
| IMP-05-10/11, implementation | Retained iterations, final exact-input/cleanup audit | Earlier hidden stderr/fake-input/ShellCheck corrections disclosed; raw15 diagnostic-whitespace exceptions retained. | evidence/IMP-05-10-attempts.md; IMP-05-11-final-audit.log |
| DR006/007, Delivery and user | Current development arm64 build, existing local Developer ID key; subsequent actual Apple submission | Local sign/verify/version passed; actual Accepted/exit0 at2026-10-19T04:57:21Z, submission16cd8853-b4f7-41a3-b676-e99029765633. First HTTP401 preserved. Not official release/hosted P12/Intel proof. | delivery-evidence/dr-007/summary.md, verification.json, apple-accepted-response.json; dr-006/local-result.json |
| CR-07-01, reviewer | Current55e45c1 vs tested75f4dbe; Git identity/current-byte inspection | All127 non-ticket inputs identical; exact six-path delta and two-source size audit. | code-review-evidence/crr-007/source-audit.json |

Original raw logs remain at their linked paths. No new cumulative manifest, copied retained binary or inferred suite count. The read-only attempt to open a nonexistent ir-005/source-audit.json was corrected to actual source-check.json/final-checks.json; it was not a product/test failure.

## Findings / Follow-ups

**None new.** CR-001 and CR-002 remain resolved. No follow-up Task or duplicate notification required; approved postpublication plan already has custody route.

## Classification / Recommended Recipient

Review outcome **Pass**; failure classification **N/A**. Next is existing reviewed **affected API/new current-source candidate** route, exact recipient selected by fresh handoff rules. No new design/approval loop or direct reviewer publication. Only one most-specific outcome recipient under controlling team instructions.

## Residual Risks

- Current sourcehash **bf6b1732ad6561da15d610afb2c5e6b8d83982fbf23f20e0684eda18b9d1ba62** differs from recorded **a425e3f887f3156d920d022801df9069ba5bc2d49bdb0e4dd8097ee76a01fe9e**. Recipe **299db7012dcc543f8606632695d286548d1513c13ace8b108eb712984fd39274** unchanged. Existing candidates/readiness preserved, not current acceptance.
- NEW complete current-source candidate/affected API required. Delivery owns staging/fresh main/genuine readiness and actual both-Mac Developer ID + Accepted, final payload and immutable public bytes/OCI/download/signature/install evidence.
- DR007 secret-update timestamp2026-10-19T04:58:54Z proves metadata change only, not password equality or hosted authentication. Six secrets already provisioned; no speculative reprovisioning.
- DR005 original failed run stays failed; local development signing/notarization does not close it or prove finalv0.1.0. Retained private local diagnostic and prior candidates untouched.
- Field/shared-filesystem/physical/user tests Deferred, not release blockers or Passed. Postpublication plan custody remains Delivery → terminal Solution Designer → requesting PM. Overall release incomplete.

## Latest Authoritative Result

**CRR-007 / Implementation Review / Pass100.00**, supported-scenario and material-premise gates **Pass**. IR005 diagnostic/cleanup correction accepted, original hosted signing cause not attributed. Full24 structural checks/ten-category scorecard complete; current API/signing/publication evidence remains downstream. Canonical successful-test report CRR006 and API/Delivery authorities are not overwritten. Only NFS review artifacts changed; no TaskDone/user verification/Terminal claim.
