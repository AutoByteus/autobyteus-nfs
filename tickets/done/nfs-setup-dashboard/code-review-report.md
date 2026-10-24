# Code Review Report — CRR-003

## Review Round Meta

- Date: 2026-10-24. Task **nfs-setup-dashboard / autobyteus-nfs-2 / project_task_f1264eb8-5a99-4a19-949f-09d141c955a1**.
- Entry: **Implementation Review**, round3, **Targeted Delta Review**.
- Trigger: IR-002 completed implementation-owned Local Fix for **CR-001 = API-F001**.
- Prior result: CRR-002 Fail (focused failure origin); CRR-001 full-source Pass100 remains historical.
- Latest authoritative source result: **CRR-003 Pass, 100/100**. This is not an API/E2E Pass.
- Basis: R1/SR001 approved `requirements-doc.md`; SR003 `design-spec.md`, `solution-revision-record.md`, `investigation-notes.md`; ARCH-REV-002 `design-review-report.md` and `architecture-review-revision-record.md`. Unchanged context carries from CRR001/002; affected chooser contract rechecked.
- Current implementation: `implementation-handoff.md` Checks Run read first; IR002 in `implementation-revision-record.md`. Reviewer history: `code-review-revision-record.md`.
- Triggering API context: API-REV-001 / API07 in `api-e2e-execution-coverage-report.md`, coverage investigation and revision record; `evidence/API-07-finding.md` and runtime trace. Delivery revision: **N/A**.
- Worktree: `/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/nfs-setup-dashboard`, branch `codex/nfs-setup-dashboard`, target origin/main.
- Intake629f7f008f6ada3f539ca854a1add82ca08f7dbd; source/tests7b0577a4f2637ddf12a74a0156e4243a41a3719c; evidence88c27bc14471fadb299350bd9d4b47c2300fe4ad.
- Recorded current sourceHash: `2703d4bf972ab2070fcfbc0f1b175fd70c258963c706fffad591cd5dc70d6903` (IMP19/20).

## Routing Classification / Review Scope

**Large / High confirmed; independent source review required.** The complete dashboard still crosses browser, private transport, privilege and shared lifecycle owners. A small corrective delta does not change the task classification.

Exactly four non-ticket paths changed since CRR002: `internal/dashboard/web/forms.js`, new `internal/dashboard/__tests__/chooser.cjs`, its existing `browser.cjs` runner, and `TESTING.md`. The only production change is chooser-local edit/listing ownership. No shared interfaces, serialized shapes, backend or data-flow spine changed; targeted review is justified. Between checked7b0577a4 and intake, only TESTING.md adds focused instructions; executable source/tests are identical. See `evidence/CRR-03-delta-review.json`.

Rechecked the prior unresolved finding first, the actual input/HTTP/listing/selection path, durable regression and recorded results. Unaffected CRR001 structural/security/service conclusions carry for byte-unchanged owners, not as newly executed checks. Full baseline report remains in commit d9beb0f796894c37a371217768b9e33afcde315a; CRR002 in4abea65b56791801db40ccf22d9693c3df791379.

Excluded: new source audit of storage/admin/IPC/service, old app/editor/release tasks, native VM reruns and physical/field campaigns. NFS repository only. No reviewer implementation/test edits or product test reruns.

## Upstream Behavior And Production-Path Basis

Approved requirement authority remains R1 UC002, REQ009/AC007 and DEC004: ordinary-user directory-only chooser plus explicit path entry, keyboard interaction and narrow layout. No behavior decision, design revision or approval needed. Persisted data remains **Directly Usable — No Migration**; this correction is ephemeral UI state only.

| Behavior | Status | Current path / evidence |
|---|---|---|
| BEH002 / SCN002 folder selection; REQ009/AC007 | Confirmed at source-review boundary | Browse → explicit list(source/home) → ordinary-user HTTP DirectoryListing → background render updates listing/message/buttons only → active text retained → explicit List verifies path → Choose copies listed path to source → existing prepare/review flow |
| BEH001,003–007 / DS1–6 | Confirmed, unchanged evidence carried | No Go/admin/wire/setup/config/backend/service/CLI or remaining UI file changes since CRR001/API001. Prior native and renderer proof keep their exact-input limits. |

### Supported Product Scenario And Reachability Gate

| Scenario / contract | Kind / actor | Independent goal and entry | Shape / lifecycle | Expected consequence | Evidence / disposition |
|---|---|---|---|---|---|
| SCN002 / BEH002 / REQ009 / AC007 / DEC004 | User, server operator | Choose a share folder through Browse and its enabled absolute-path field | Supported Normal Scenario: begin typing while initial listing completes; then deliberately list/select a folder | Preserve exact draft, never silently select an unrelated listed path; explicit parent/child/List remains usable | Approved chooser contract, API07 real failure/control, current forms.js:23–55, directories.go and HTML. **Use**. |

The original source review missed this normal edit path. That acknowledged gap remains in CRR002 history; it is not erased by the fix or represented as a storage defect.

### Candidate Finding And Mechanism Gate

| Candidate | Independent trigger / contract | Forward path / lifecycle / consequence | Evidence | Disposition / scope |
|---|---|---|---|---|
| CG-008 / CR-001 resolution | SCN002 typing during ordinary listing completion | render no longer assigns editable value; only deliberate navigation seeds it; later keys append to unchanged prefix | forms.js:25–46; IMP17 red/IMP18 green, original API07 | **Promote / This ticket**, correction verified; finding resolved at source boundary |
| CG-009 / selection consistency | Same SCN002 user corrects/types a folder then chooses it; selector must represent that folder | oninput/render recalculate eligibility; null/running/error/differing path disables Choose, successful explicit matching List enables it | forms.js:25–26,31,44–46,53; chooser.cjs exact assertions | **Promote / This ticket**, proportionate local invariant; no new finding |

Both gates Pass. No new/reclassified upstream material premise; existing ARCH002 decisions remain confirmed within unchanged scope. No unsupported recovery/concurrency framework, follow-up or held candidate.

## Prior Finding Resolution

**CR-001 (Medium, implementation Local Fix): Resolved in source.** The unconditional render setter was removed, not masked by disabling required typing or delaying it in the test. `list` seeds text only for Browse, explicit List, parent and child navigation. `selection` separates successful listing identity from editable text. Errors retain the user's correction and keep selection disabled.

API-F001 / API001 Fail81.43 remains API-owned pending affected validation. Local green checks and this source Pass do not overwrite it. No remaining source finding.

## Structural / Design Checks

All unaffected rows carry the CRR001 basis after bounded Git impact verification; affected chooser/test rows are revalidated here. No action required in any row.

| Check | Result | Evidence | Required action |
|---|---|---|---|
| Task design health assessment present, evidence-backed and preserved | Pass | Existing admin/DS6 refactor untouched; correction stays in local chooser owner | None |
| Approved behavior-defining supplements matched | Pass | DEC004 keyboard/path entry restored, no new product semantics | None |
| Data-flow spine inventory clarity/preservation | Pass | Same Browse→directory HTTP→listing→explicit selection→setup path; no new spine | None |
| Ownership boundary preservation/clarity | Pass | Draft belongs to input; listing belongs to response; explicit navigation owns seed | None |
| Off-spine concern clarity | Pass | No new production helper owner or coordinator | None |
| Existing capability/subsystem reuse | Pass | Existing chooser/listDirectories reused | None |
| Reusable owned structures | Pass | Single selection rule shared by input/render; test scenario reused across methods/engines | None |
| Shared data-model tightness | Pass | DirectoryListing shape unchanged; no redundant shared state added | None |
| Repeated coordination ownership | Pass | chooser alone owns navigation/render/selection; admin ownership unaffected | None |
| Empty indirection | Pass | selection derives eligibility, not a pass-through layer | None |
| Separation of concerns/file responsibility | Pass | forms.js remains UI form/chooser behavior; test separated by coherent scenario | None |
| Ownership-driven dependencies | Pass | UI still uses request boundary; no imports/cycles into privilege/backend | None |
| Authoritative Boundary Rule | Pass | No direct filesystem/root access in browser; directory producer and admin boundaries unchanged | None |
| File placement | Pass | Existing dashboard web owner and adjacent __tests__ directory | None |
| Flat versus over-split layout | Pass | No production fragmentation; one reusable browser scenario | None |
| Interface/query/command/service-method clarity | Pass | Existing path request and DirectoryListing response unchanged | None |
| Naming and vocabulary | Pass | list/render/selection and directory-path describe distinct existing responsibilities | None |
| No unjustified duplication | Pass | Selection rule not repeated; POST/GET tests parameterized | None |
| Patch-on-patch complexity | Pass | Removes destructive setter, adds simple eligibility invariant; no version/fallback flags | None |
| Dead code removed in touched scope | Pass | Replaced old setter/eligibility logic removed; current imports/handlers used | None |
| Relevant test scenarios/assertions | Pass | Prefix before delivery, exact draft/suffix/focus, settled control and explicit selection | None |
| Test fixtures/helpers reusable/coherent | Pass | Existing real embedded preview reused; scheduling helper serves one normal chooser journey | None |
| No stale/duplicated/compatibility-only tests | Pass | Original normal flows retained; new cases cover previously absent initial POST/later GET boundary | None |
| API/E2E readiness | Pass | Durable red/green and current identity available; affected API remains required | None |

## Source File Size And Structure

| Changed source | Nonempty task-base | Prior round | Current | >500 | >220 delta | Ownership / placement | Classification / action |
|---|---:|---:|---:|---|---|---|---|
| internal/dashboard/web/forms.js |0 (new in task)|47|55|Pass|11 added/3 removed this round; cumulative55, below trigger|Cohesive existing form/chooser owner|N/A / None|

Test files are not subject to source size thresholds. Unchanged CRR001 max236 and operations240-added structural judgement carry; no expansion of those owners.

## Legacy / Persisted Data / Cleanup Verdict

| Check | Result | Notes |
|---|---|---|
| No backward-compatibility mechanism | Pass | One current chooser behavior |
| No old-behavior retention | Pass | Async input assignment removed |
| Dead code removed | Pass | Touched imports/handlers/functions used; no obsolete branch |
| Approved persisted transition followed | Pass | Existing records/readers/writers untouched; no migration |
| No dual reads/writes or old-shape fallback | Pass | No wire/storage shape change |
| Transition mechanics match design | Pass | No migration mechanics required or introduced |

Dead/obsolete items requiring removal: **None**. Cleanup: IMP20 records private preview/browser/toolchain removal and no owned executables. Reviewer created no runtime resources/scratch and changed only review documents/evidence; no cleanup action needed.

## Checks / Evidence Reuse And Rendered Result

| Evidence | Exact scope and result | Review judgement |
|---|---|---|
| IMP17 red/result.json | Original4abea65b plus new test: Chromium1280 fails `background listing replaced the active draft` | Correct baseline assertion, not harness failure |
| IMP18 green/result.json + feedback | Checked7b0577a4; Macarm64 Chromium156/WebKit27.2 at1280/390; 8chooser +8normal =16/16 Pass | Actual UI/HTTP; holds real POST/GET response delivery, does not forge contents/status. Root protocol and clipboard doubled. Not native storage proof. |
| IMP19 focused.log | Exact checked source; dashboard race/vet and2 embedding/hash Python checks Pass | Reused; initial malformed timeout command is retained setup failure, not a test/product failure |
| IMP20 checks-cleanup.json |166 copied inputs verified; private scratch/toolchain/processes removed | Read with current Git check; later non-ticket delta is TESTING instructions only |
| CRR001 + API001 passed cases | Unchanged owners and scoped native storage/pending/expiry/service/CLI evidence | Carry with recorded limits; do not promote the overall failed API001 to Pass |

Read the durable runner's actual trigger and assertions, including original normal flows and cleanup. Inspected retained `IMP-18-green/webkit-server-390-chooser-poll.png`: usable labelled input, visible focus, buttons and status in narrow modal; long path remains input-scrollable. This is retained-image inspection, not a new browser execution. No new Linux browser or native/AMD64/field/physical/user/release qualification is claimed.

No recorded check was rerun merely for independent credit. Reviewer performed source/evidence read, Git scope/size audit and retained-image inspection only.

## Docs Impact

**Yes, addressed:** TESTING.md adds focused chooser scenarios/selector and controlled-timing limits. No release/runtime/API policy or public usage contract changed. General final documentation synchronization remains Delivery-owned after executable acceptance.

## Review Scorecard

10.0/10 = **100/100**, simple mean for visibility, not an acceptance substitute. Current bounded review finds no unresolved source issue; unchanged categories carry CRR001 evidence. The earlier CRR002 failure remains in history.

| Priority | Category | Score | Rationale | Weakness / required improvement |
|---|---|---:|---|---|
|1|Data-Flow Spine Inventory and Clarity|10|Existing path preserved and explicitly traced|None established|
|2|Ownership Clarity and Boundary Encapsulation|10|Draft/listing authority no longer conflated|None established|
|3|API / Interface / Query / Command Clarity|10|No contract change or bypass|None established|
|4|Separation of Concerns and File Placement|10|Bounded fix in current owner|None established|
|5|Shared-Structure / Data-Model Tightness and Reusable Owned Structures|10|No shared shape growth; coherent eligibility/test reuse|None established|
|6|Naming Quality and Local Readability|10|Small explicit edit-versus-result distinction|None established|
|7|API/E2E Readiness|10|Current red/green and controls available for affected execution|API execution still required, not a source defect|
|8|Runtime Correctness And Behavioral Fidelity|10|Prior normal typing defect addressed with exact regression and selection controls|API-owned closure pending|
|9|No Backward-Compatibility / No Legacy Retention|10|Destructive old path removed; no migration/fallback|None established|
|10|Cleanup Completeness|10|Owned test resources removed; no reviewer runtime resources|None established|

## Latest Authoritative Result / Routing / Residual Limits

- **Pass**, Implementation Review / CRR-003. Supported-scenario and material-premise gates **Pass**. No current failure classification or new findings/follow-ups.
- CR-001 resolved at source boundary; **API001 Fail81.43 remains until its owner validates the correction**.
- Fresh most-specific source-Pass route: API/E2E Engineer (recorded in `evidence/CRR-03-routing.json`). Request affected chooser validation and controls, using existing valid checks. No whole storage/field campaign absent material impact; no new approval loop.
- Single primary recipient only under the team's higher-priority handoff instruction; do not additionally dispatch an informational outcome to implementation.
- No source/test fixes by reviewer, target merge/push/tag/release, TaskDone, terminal completion or user verification. Source-only NFS task; no other project touched.
