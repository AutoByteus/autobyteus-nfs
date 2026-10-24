# Code Review Report — nfs-setup-dashboard

## Review Round Meta

- Date: 2026-10-24. **CRR-001 / round 1 / Implementation Review / Full Review**.
- Task: autobyteus-nfs-2 / project_task_f1264eb8-5a99-4a19-949f-09d141c955a1.
- Workspace: `/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/nfs-setup-dashboard`, branch `codex/nfs-setup-dashboard`, eventual target `origin/main`.
- Read authorities: `requirements-doc.md`, `investigation-notes.md`, `solution-revision-record.md`, `solution-design-handoff.md`, `design-spec.md`, `design-review-report.md`, `architecture-review-revision-record.md`, `implementation-handoff.md`, `implementation-revision-record.md`.
- Basis: **R1/SR-001 Approved; SR-003; ARCH-REV-002 Pass; IR-001**. ARCH-REV-001/ARCH-F001 is resolved design history, not an open implementation finding. Earlier handoff's pending-review wording is superseded by ARCH-REV-002.
- Supplemental behavior authority: None. Implementation evidence supplements proof, not intended behavior.
- Trigger: Implementation Engineer's initial completed Large/High package. Prior code-review result: **N/A**. This report and `code-review-revision-record.md` establish the baseline; no prior Pass inferred.
- Intake: `e5662dd1333192c66cf29bf27e6f82ccb14c2efd`; base `52c17fb5480d23b89752a8ae201419e356b4c3fc`; final production `5f8cabf8ee31318a38aa9c0ed94e9c6960b9c409`; source/tests `2445aabf61126b1bb64b05b5f925b140c67917b8`. Later intake commits contain ticket artifacts only.
- API/E2E investigation/report/revision, delivery revision, failing command and failure-origin fields: **N/A — initial source review**.
- Shared guidance: updated code-reviewer skill, design-principles, applicable design-examples, finding-the-cause, ticket-scope and handoff; project AGENTS.md, DESIGN.md and TESTING.md. No closer package instructions found.

## Routing Classification Review

**Large / High / Implementation Review / independent source review required.**
Embedded frontend, privileged private IPC, exact-plan retention and a common CLI/helper/service owner cross multiple subjects and introduce a security/lifecycle boundary. Classification is confirmed, not reduced because files are small. No approval or architecture recovery needed.

## Review Scope

Full cumulative 39 non-ticket paths versus the base: new `internal/admin`, `adminwire`, `dashboard` and embedded web assets; CLI adapters/dispatch; old supervisor removal; comment-only probe adjustment; tests and five NFS documentation paths. Traced unchanged setup/config/platform/backend/Docker contracts at their affected calls.

Only this NFS project is involved. Excluded: AutoByteus application/editor/Guide, workspace/agent/provider work, prior extraction/release tickets, broader field qualification, release or target finalization. No product/source/test fix performed by this reviewer. No privileged action, browser launch, VM, mount, container, credentials, build or test execution performed during review.

## Upstream Behavior And Production-Path Basis Confirmation

Approved intent is two ordinary-user local role commands backed by existing safe host NFS operations, not a second storage controller. Metadata, readiness, exact review/consent and storage lifetime must remain distinct. **Behavior basis Confirmed**; DS1–6 verified against the implementation. No newly discovered supported behavior or material ambiguity.

| Behavior | Status | Implementation path and lifecycle evidence | Contradiction |
|---|---|---|---|
| BEH-001 | Confirmed | Parse server/client → CheckHost → nonroot/TTY launch → ephemeral loopback HTTP → private bootstrap file/terminal fallback; no root HTTP | None |
| BEH-002 | Confirmed | server form → typed BeginServer → admin acquired scope → existing Plan → retained exact plan/lock → consented Commit → Apply/Status | None |
| BEH-003 | Confirmed | Connection JSON/manual override → ParseConnection/Plan → exact Connection in review → retained root plan; directory selection remains nonroot | None |
| BEH-004 | Confirmed | metadata Inspect separate from CheckReadiness; pending BeginReconnect resolves saved owner and PendingPlan; active reconnect/drained detach use existing setup authority | None |
| BEH-005 | Confirmed | literal Host/origin + one-use bootstrap + bearer → bounded strict typed frame → fixed sudo/installed helper/digest → admin scope; no browser Plan/user/command authority | None |
| BEH-006 | Confirmed | one asynchronous operation; root lease/operation drain; Stop closes management admission, not storage. Installed service owns its separate complete serial loop in admin | None |
| BEH-007 | Confirmed | CLI/service preserved through admin; unchanged persisted readers/writers and release owners; recursive source hashing includes embedded assets | None |

## Supported Product Scenario And Reachability Gate

Independent scenario authority is R1's SCN-001–010 and DS1–6, not the test fixtures or newly callable endpoints. All rows below are **Use**; Normal means Supported Normal Scenario, Edge means Supported Explicit Edge Scenario.

| Scenario / behavior | Kind / actor and coherent goal or event | Supported entry / independent trigger | Shape / validity | Forward path and lifecycle | Expected outcome / evidence |
|---|---|---|---|---|---|
| SCN-001 / BEH-001 | User launches selected local role | terminal `server` / `client`; R1 REQ-001 | Normal | CLI check → dashboard.New/Run → private fragment exchange | open local management without storage mutation; root/no-TTY refused; CLI/dashboard source, IMP10 controls |
| SCN-002 / BEH-002 | User shares selected safe folder | explicit server form/prepare/approve; REQ-002 | Normal | BeginServer → setup.Plan → lease → Commit/Apply | exact source/network/service summary and Connection before effects; operations.go, IMP06/09/10 |
| SCN-003 / BEH-003 | User joins existing shared storage | pasted Connection and optional local mount root; REQ-003 | Normal | BeginClient → existing parser/Plan → review → Apply | no discovery or arbitrary Plan; IMP10/11 actual native clients |
| SCN-004 / BEH-004 | Operator inspects, checks or reconnects configured storage | explicit distinct controls; REQ-004 | Normal | Inspect metadata / CheckReadiness probe / BeginReconnect+Commit | configured is not Ready; timestamped observations and current errors; state.go, operations.go, app.js |
| SCN-005 / BEH-004 | Operator resumes an interrupted setup | retained setup intent after effects failed; REQ-004 | Edge | pending metadata → saved owner → PendingPlan → new review → Apply | same stored intent, no implicit resume; setup/pending.go and admin tests |
| SCN-006 / BEH-004 | Operator safely disconnects after draining users | explicit review and drain acknowledgment; REQ-005 | Normal, with explicit busy/partial edge | BeginDetach → consumed consent → existing Detach | no force, busy/mismatch refusal, source/marker/private recovery preserved; IMP11/12 and unchanged hosted-config controls |
| SCN-007 / BEH-005 | Security contract: remote/untrusted origin or denied OS authority | R1 REQ-006 local-only management and terminal approval | Edge | host/origin/token/typed-wire checks precede root operation; OS identity and installed digest precede effects | refuse without arbitrary root authority; http/privilege/wire tests and IMP04; same-user compromise is excluded |
| SCN-008 / BEH-005–006 | User repeats click/abandons review; CLI/service competes; private pipe fails | R1 explicit overlap, lease, transport events | Edge | replay/current-ID gate → single worker → one global lock → retained lease/expiry; EOF/EPIPE drain | no duplicate effect or early lock release; admin pipe/session/resources tests, IMP04 |
| SCN-009 / BEH-006 | User stops management with admitted work outstanding | Stop/terminal signal during supported operation; REQ-007 | Edge | close admission → HTTP shutdown → worker/helper drain; storage untouched | honest waiting, no rollback/forced cancellation; browser stop fixture and real broken-fd test |
| SCN-010 / BEH-006–007 | Installed service tick/stop; existing CLI operation; standalone build | ordinary jobs call `service`, no interactive user required; REQ-008/010 | Normal, with busy/pending/stop edge | admin.Supervise → private reconcileOnce → acquire/admit/savedDocker/Reconnect/close → report/wait30s | one full owner/no nested lock; no pending auto-resume; admin tests, IMP09/12/13 |

### Candidate Finding And Mechanism Gate

Promoted mechanism rows below justify implemented mechanisms, **not defects**. No candidate is held unresolved.

| ID | Observation / mechanism | Independent basis / trigger | Forward path, lifecycle and consequence | Evidence | Disposition / scope | Proportionate judgment |
|---|---|---|---|---|---|---|
| CG-001 | Retain exact plan plus global lock; single-use consent and expiry | SCN002/003/008; user prepares then applies or abandons review | Begin retains actual Service/Plan; Commit consumes before effects; timer/cancel closes only uncommitted scope | operations.go/session.go, actual flock tests and IMP04 | Promote / This ticket | Required existing design contract, correctly bounded; no finding |
| CG-002 | Root/HTTP separation and strict local protocol | SCN007; untrusted browser origin/denied OS approval | nonroot HTTP authenticates; fixed sudo and checked installed executable receive typed pipe requests, not browser authority objects | dashboard/cli/adminwire source and negative tests | Promote / This ticket | Correct security boundary, no additional generic remote service needed |
| CG-003 | Serial worker, inherited lock and safe stop/EOF/EPIPE drain | SCN008/009; admitted host work outlives management request | no context kills mount/probe; closing output drains worker before scope close; cached HTTP remains independent | admin/pipe.go, TestHelperBrokenOutputDrain, browser slow/stop tests | Promote / This ticket | Supported shutdown contract; no force-cancel or false deadline claim |
| CG-004 | Complete supervisor ownership versus old outer callback | DS6/REQ008; installed job runs without TTY/SUDO | one admin-owned attempt/cleanup/report/wait loop; old service.Supervise and CLI callback absent | source diff, supervisor.go, tests, IMP09/12 | Promote / This ticket | ARCH-F001 correction implemented, not merely a moved inner call |
| CG-005 | operations.go exceeds 220 added lines | shared design/source-structure contract | 240 added / 236 nonempty lines coordinate one prepare/review/commit subject; underlying storage policy remains in setup | full file, source audit | Promote / This ticket | Pressure assessed, cohesion sufficient; no artificial split or finding |
| CG-006 | One-line reconnectActiveLocked might look like empty indirection | DS6 explicit shared active-reconnect sequence | private call names the already-held-scope invariant for explicit reconnect and supervisor; no second public owner or callback layer | operations.go, supervisor.go, design DS6 | Reject | Not a pass-through subsystem or boundary violation; no deduction |
| CG-007 | Arbitrarily missing attachment with surviving hosted metadata might demand a new repair mode | SCN006 governs real safe partial detach, not arbitrary record edits | current inspect refuses inconsistent authority; unchanged setup preflight likewise depends on attachment/pending; supported missing-backend-config retry remains in setup | inspect, setup.CheckConfiguration/Detach and hosted_config_test.go | Reject | No independently established new supported data state or caused regression; do not invent destructive record-repair machinery |

## Structural / Design Checks

| Check | Result | Evidence | Required action |
|---|---|---|---|
| Task design health assessment present, evidence-backed and preserved | Pass | SR003 DS1–6 and ARCH002 carried; actual complete DS6 owner (CG004) | None |
| Approved behavior-defining supplemental artifacts matched | Pass | None required; canonical R1/SR003 remain authority | None |
| Data-flow spine inventory clarity and preservation | Pass | terminal, browser/helper and installed-service entry traced to common admin then existing setup | None |
| Ownership boundary preservation and clarity | Pass | admin owns locked sequence, dashboard presentation/process lifetime, adminwire strict DTO/transport | None |
| Off-spine concern clarity | Pass | nonroot chooser/bootstrap, scoped Docker close and source hash stay in their owners | None |
| Existing capability/subsystem reuse | Pass | unchanged Plan/Apply/Status/Reconnect/Detach and platform/config validators reused | None |
| Reusable owned structures | Pass | one scope close, lease, snapshot, typed request/reply; no duplicate privileged policy | None |
| Shared data-model tightness | Pass | role inputs, opaque lease, display Configuration and operation Result each distinct; no wire Plan/User | None |
| Repeated coordination ownership | Pass | CLI/helper/service use Session; old CLI lock/Docker orchestration removed | None |
| Empty indirection | Pass | CG006 rejected; meaningful module subjects, no manager-chain forwarding | None |
| Scope-appropriate SoC / file responsibilities | Pass | operations/identity-state/pipe/supervisor separate by owned concern, not arbitrary line slicing | None |
| Ownership-driven dependencies | Pass | no setup/service reverse import into admin; transport does not call storage internals | None |
| Authoritative Boundary Rule | Pass | CLI delegates admin lifecycle; installer/internal probe remain separate existing entry subjects, not bypasses of a dashboard operation | None |
| File placement | Pass | internal/admin, adminwire, dashboard/web align with privilege and presentation boundaries | None |
| Flat versus over-split layout | Pass | compact subject files; no generic recovery/event/service framework | None |
| Interface/query/command clarity | Pass | Inspect versus CheckReadiness; Begin/Cancel/Commit; typed role/lease identity; fixed launcher | None |
| Naming-to-responsibility alignment | Pass | configuration, observation, review, authorization and storage lifetime kept distinct in source/UI/docs | None |
| No unjustified duplication | Pass | one common admission/lock/Docker/supervisor sequence, existing storage policy reused | None |
| Patch-on-patch complexity control | Pass | initial coherent extraction plus bounded UI/fixture corrections; no fallback mode stack | None |
| Dead code removed in touched scope | Pass | old supervisor file, callback, duplicated CLI coordination and obsolete inputs owner removed | None |
| Relevant test scenarios/assertions | Pass | public HTTP security, typed private protocol, real child fd1 drain/flock, consent/expiry/roles/service and renderer assertions | None |
| Fixtures/helper reuse and test structure | Pass | test Session, shared HTTP helper, controlled child process, tagged browser preview; boundaries named | None |
| No stale/duplicated/compatibility-only tests | Pass | repeated execution is disclosed rather than counted as unique coverage; existing CLI/storage controls remain intentional | None |
| API/E2E readiness | Pass | working package, explicit source attribution, commands/raw logs, native and browser evidence plus remaining limitations; acceptance owner still downstream | API/E2E next |

## Source File Size And Structure Audit

`evidence/CRR-01-source-audit.json` records each changed non-test implementation path, exact base/current nonempty counts and Git added/deleted lines. Tests/fixtures are excluded from thresholds. Every row passes the 500-line rule, SoC and placement; classification N/A and action None. Only operations.go exceeds 220 changed lines (CG005); maximum current source size 236.

| Source path (under internal/) | Before | After | Added/deleted | >220 delta / judgment |
|---|---:|---:|---:|---|
| admin/operations.go | 0 | 236 | 240/0 | Assessed: cohesive retained-review/commit subject |
| admin/pipe.go | 0 | 152 | 155/0 | Below |
| admin/session.go | 0 | 162 | 171/0 | Below |
| admin/state.go | 0 | 114 | 118/0 | Below |
| admin/supervisor.go | 0 | 40 | 42/0 | Below |
| adminwire/protocol.go | 0 | 138 | 144/0 | Below |
| adminwire/types.go | 0 | 46 | 49/0 | Below |
| cli/dashboard.go | 0 | 100 | 105/0 | Below |
| cli/inputs.go | 161 | 140 | 6/27 | Below; shrinks |
| cli/interactive-setup.go | 53 | 57 | 23/20 | Below |
| cli/run.go | 191 | 162 | 69/98 | Below; shrinks |
| dashboard/assets.go | 0 | 27 | 30/0 | Below |
| dashboard/browser.go | 0 | 99 | 101/0 | Below |
| dashboard/directories.go | 0 | 83 | 86/0 | Below |
| dashboard/http.go | 0 | 151 | 154/0 | Below |
| dashboard/privilege.go | 0 | 129 | 133/0 | Below |
| dashboard/session.go | 0 | 195 | 200/0 | Below |
| dashboard/web/api.js | 0 | 27 | 27/0 | Below |
| dashboard/web/app.js | 0 | 121 | 121/0 | Below |
| dashboard/web/forms.js | 0 | 47 | 47/0 | Below |
| dashboard/web/index.html | 0 | 69 | 69/0 | Below |
| dashboard/web/styles.css | 0 | 15 | 15/0 | Below; compact CSS manually read, not hidden policy |
| service/probe.go | 155 | 155 | 1/1 | Comment only |
| service/supervisor.go | 28 | 0 | 0/31 | Removed |

## Legacy / Backward-Compatibility Verdict

| Check | Result | Notes |
|---|---|---|
| No backward-compatibility mechanism in changed scope | Pass | preserved public CLI is approved behavior, not a legacy fallback |
| No obsolete old-behavior retention | Pass | supervisor callback removed rather than wrapped |
| Dead code removed in touched modules | Pass | one root lifecycle and one complete service owner |
| Approved persisted-data transition followed | Pass | Directly Usable — No Migration; existing config/setup serializers untouched |
| No version-specific dual reads/writes or old-shape fallback | Pass | strict ephemeral wire separate from existing version-agnostic config decoder |
| Transition mechanics match design | Pass | no new persistent dashboard journal or schema; root-private records/markers remain authoritative |

Dead/obsolete items requiring further removal: **None found**. No new follow-up added.

## Evidence Review And Checks Reused

Read implementation **Checks Run before execution**. No product suite rerun solely for independent credit. Reviewer performed source/caller/diff inspection, a read-only Git/file identity audit, direct raw-log inspection and inspection of retained images, not implementation's native work.

| Proof / source attribution | Reviewed evidence and result | Limit retained |
|---|---|---|
| Exact final source/tests | CRR-01-source-audit: 165 non-ticket files; no non-ticket difference from2445aab to intake. Unchanged config/setup/backend/Docker/platform/install/packaging/public scripts/workflows/module files versusbase | independent source audit, not runtime acceptance |
| Native package checks | IMP-02-phase4-final-all.{json,log}: Mac Go1.27.2 race10packages at2445; IMP-07-linux-go-final.log/result plus final affected admin cleanup rerun; final vet/build receipts | Linux full suite predates test-only cleanup, covered by affected native rerun; no invented individual Go count |
| Python and embedding | IMP-07-mac-python-clone.log and linux-python-final.log:78 collected,77 executed,1 expected child skip each; changed hash/asset tests inspected | copied Git context/initial failures retained; not78 executed |
| Build targets | IMP-07-final-builds.json: darwin/linux arm64/amd64 compile0 | compile-only, not AMD64 runtime |
| Private privilege | IMP-04-native-scope.md plus real pipe/digest/lock controls; current source corroborated by native Mac/client evidence and current tests | phase2 before browser; NOPASSWD fixture, no real password-entry proof |
| Rendered UI | IMP-05-feedback.md, current/result.json, error-final/result.json and browser.cjs | real Chromium/WebKit, doubled root/clipboard;18initial/10affected/2error executions overlap |
| Native storage and service | IMP06/09 earlier Linux server/native-Docker; IMP10 current Mac native/client; IMP11 current Linux client; IMP12 same installed Mac service and drained detach; IMP13 CLI continuations | earlier Linux runs not falsely relabelled current; VM arm64 HTTP/TTY controls, not native guest browser clicks or reboot/field qualification |
| Cleanup / audit | IMP14 cleanup and guest inventories; IMP15 final audit | source/marker/peer preservation before removal of owned guests; prior engine/candidates retained |

Viewed retained desktop Chromium server1280 and final WebKit client390 error images: labels/actions/hierarchy readable, no clipped body, error text literal, current incomplete banner explicit. This is **Read/visual inspection of implementation evidence**, not a new browser run. Read documented failed attempts; corrected preparation/probe errors are not attributed to product without evidence. Raw PTY whitespace exceptions remain unchanged. A review read initially guessed a nonexistent Linux log filename; listing identified `IMP-07-linux-go-final.log`, which was then read. No test was run by that mistaken lookup.

## Docs-Impact Verdict

**Yes.** README.md, docs/dashboard.md, docs/filesystem-usage.md, DESIGN.md and TESTING.md describe role launch, terminal approval, review/readiness/drain, standalone embedded build and test boundaries. Current released v0.1.0 is not represented as containing this unreleased dashboard. Delivery still owns final docs consistency and fresh source integration; no release is authorized here.

## Additional Material Premise Validation

ARCH-REV-002 states **None beyond the established behavior basis**; that decision is confirmed. No additional or reclassified material premise. CG001–005 use existing SCN/DS contracts; CG006–007 are rejected as findings. No unsupported race, arbitrary state corruption or new cross-session workflow drives the result.

## Review Scorecard

**10.0/10 — 100/100**, simple average for source-review summary only, not acceptance probability or API score. No evidenced in-scope weakness remains; uncertainty in downstream execution is retained below rather than invented as a source defect.

| Priority | Category | Score | Why | Weakness / drag | Expected improvement |
|---|---|---:|---|---|---|
| 1 | Data-Flow Spine Inventory and Clarity | 10 | DS1–6 actually traced, including installed outer loop | None identified | None required |
| 2 | Ownership Clarity and Boundary Encapsulation | 10 | common admin authority; nonroot presentation and typed IPC distinct | None identified | None required |
| 3 | API / Interface / Query / Command Clarity | 10 | explicit role inputs, inspect/check separation, opaque lease consent | None identified | None required |
| 4 | Separation of Concerns and File Placement | 10 | cohesive subjects, source threshold pressure assessed CG005 | None identified | None required |
| 5 | Shared-Structure / Data-Model Tightness and Reusable Owned Structures | 10 | one scope/lease/operation shape, no duplicated storage policy | None identified | None required |
| 6 | Naming Quality and Local Readability | 10 | configuration/readiness/review/stop meanings consistent | None identified | None required |
| 7 | API/E2E Readiness | 10 | complete handoff, executable surfaces/evidence and explicit limits | Acceptance not yet assigned, not a readiness defect | API/E2E judges affected coverage next |
| 8 | Runtime Correctness And Behavioral Fidelity | 10 | supported source paths and reused checks support expected behavior; no demonstrated defect | Native/browser evidence remains bounded, not full qualification | Downstream acceptance, no speculative source change |
| 9 | No Backward-Compatibility / No Legacy Retention | 10 | clean owner extraction, unchanged authoritative persistence | None identified | None required |
| 10 | Cleanup Completeness | 10 | old owner removed; scoped resource/source preservation evidence | None identified | None required |

## Findings / Follow-ups / Classification

- Findings: **None**. No failure classification; **N/A — clean source-review Pass**.
- Follow-ups this review added: **None**. Do not open or redispatch unrelated field/release/editor work.
- Prior findings: **None**, initial code-review baseline. ARCH-F001 belongs to resolved architecture history.

## Residual Risks And Next Boundary

- API/E2E owns current coverage/acceptance, including the integrated UI/helper/host journey and required supported edge cases. Reuse valid evidence; do not rerun merely for independence. Preserve phase2/earlier Linux/current Mac/current Linux-client attribution.
- Browser root/clipboard are doubled; native controls use real HTTP/TTY and NOPASSWD, not visible native browser clicking/password entry. Both layers are useful but not the same test. AMD64 builds are compile proof only.
- Hard NFS waits are intentionally not time-bounded; stop drains, not rollback/detach. Reported18.611/21.682s remount observations are neither SLA nor reboot qualification.
- No physical/field/user acceptance, release/signing/publishing or previous-task closure implied. Delivery still owns fresh integration, documentation completion and AC-008 finalization evidence.

## Latest Authoritative Result

- **Pass — CRR-001**, Implementation Review, Full Review, **Large / High**.
- Supported Product Scenario Gate: **Pass**. Material-Premise Gate: **Pass**.
- Score: **100/100 source review only**. API/E2E and Delivery: **N/A for this initial task stage**, not passed by implication.
- Recommended next owner: **/software_engineering_team/api_e2e_engineer**, selected by the fresh source-Pass rule in `evidence/CRR-01-routing.json`. Only that primary recipient is dispatched under the higher-priority single-recipient team instruction.
- Review changed only this ticket's reviewer documents/evidence. No product edit, target merge, push, release, TaskDone or user-verification claim.
