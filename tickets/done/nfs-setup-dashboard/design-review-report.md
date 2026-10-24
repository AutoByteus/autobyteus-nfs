# Design Review Report

## Review Round Meta

- Upstream Requirements Doc: `requirements-doc.md`, R1 / SR-001 Approved.
- Upstream Investigation Notes: `investigation-notes.md`, E01–14.
- Upstream Solution Revision Record: `solution-revision-record.md`.
- Reviewed Design Spec: `design-spec.md`, SR-003 Ready for affected re-review.
- Supplemental Task Artifacts Reviewed: `solution-design-handoff.md`; no behavior-defining supplements.
- Relevant Solution Revision IDs: SR-001, SR-002, SR-003.
- Architecture Review Revision Record: `architecture-review-revision-record.md`.
- Current Architecture Review Revision ID: **ARCH-REV-002**.
- Current Review Round: 2, 2026-10-24.
- Trigger: SR-003 correction of ARCH-F001 for autobyteus-nfs-2 / `project_task_f1264eb8-5a99-4a19-949f-09d141c955a1`.
- Prior Review Round Reviewed: ARCH-REV-001 / Fail at `d4d3cf0cc5548145e8525bd67ecdde76624945a2`; ARCH-F001 rechecked against current design/source, not accepted solely from the revision record.
- Latest Authoritative Round: This report.
- Current-State Evidence Basis: initial independent review at `48591a58d2e0413a18bbab8bbeb714cc034f7c95`, plus affected re-review at `f57dc52e779c37ad5a16aa393b0d020d49144f4b`. Only four Solution Designer documents changed since ARCH001; R1, reviewer history and all product source remain unchanged. Source base remains `52c17fb5480d23b89752a8ae201419e356b4c3fc`. Worktree `/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/nfs-setup-dashboard`, branch `codex/nfs-setup-dashboard`; initially clean.
- Review method: current role skill/principles/examples/template and repository AGENTS/DESIGN/TESTING/RELEASE applied; original source/caller/primary-contract evidence retained where unchanged. Round 2 read the revised design, investigation E13/E14, handoff/history and re-traced service/current reconnect boundaries; it did not repeat unrelated source review. No Go/browser/sudo/VM/mount execution, resource creation, live state inspection, remote repository mutation, or release action. No executable acceptance claim.

## Routing Classification Review

- Task size: **Large**.
- Architectural risk: **High**.
- Classification rationale reviewed: embedded UI, new browser/privilege transport and process lifetime, shared root administrative sequencing, and terminal/service migration. These are structural/security/concurrency changes, not content-volume inflation.
- Independent Architecture Review required by the classification: **Yes**.
- Classification evidence or correction required: Classification is sound. The bounded ownership correction is resolved in SR003; no product reapproval or field-test campaign is requested.

## Upstream Behavior And Production-Path Basis Confirmation

- Overall Basis Status: **Confirmed**. R1 intent and unchanged existing behavior remain established; SR003 completes the preserved installed-service target sequence as DS6.
- Approved requirements / intended behavior understood: ordinary-user `server`/`client` local dashboards, explicit terminal OS approval and exact-plan consent, same storage contracts, standalone source-only delivery.
- Relevant existing behavior and evidence confirmed: the terminal currently coordinates setup; the installed supervisor separately acquires/releases the global lock and invokes a reconciliation callback. SR003 explicitly relocates that entire loop/attempt under admin and removes the old callback contract (ARCH-F001 resolved).
- Scope guardrail confirmed: UC001–005 / SCN001–010; no app, skills, discovery, new backend, migration, release, live-user operation or nfs-4 field campaign. Preserved CLI/service/storage contracts remain in scope.
- Approved change, preserved behavior, and outside scope understood: Yes. Public terminal commands remain supported entry forms, not legacy compatibility paths.
- Every prospective blocking Design Impact finding is traceable to an approved REQ/AC/BEH: **Yes** — no new findings; resolved ARCH-F001 protected REQ-007/008, AC-008, BEH-006/007, SCN-010.
- Remaining material ambiguity: None. Implementation/executable evidence remains downstream; it is not being claimed by this design review.
- Existing-code claims opened at cited lines: `cli/run.go:19–188`, `inputs.go:24–78,103–165`, `interactive-setup.go:11–56`, `install.go:19–142`; `setup/plan.go:18–147`, `apply.go:15–172`, `pending.go:13–89`, `lifecycle.go:13–143`, `status.go:18–42`; `service/supervisor.go:13–30`, `probe.go:119–160`; `platform/lock.go:10–23`, `commands.go:19–40`, `source.go:14–66`, `mounts.go:13–160`, `jobs.go:29–113`; `config/store.go:13–123`, `state.go:13–60`, `installation_state.go:12–87`, `connection.go:17–145`; `cmd/autobyteus-nfs/main.go:13–25`, development release JSON, `packaging/release_support/identity.py:18–22,152–168`, current README/usage and CI. All paths here are repository-relative with `internal/` for Go packages unless stated otherwise.

| Behavior ID | Kind | Design Alignment With Approved Intent | Approved Trigger / Contract And Current-State Evidence | Target Outcome / Path / Spine Coherence | Status | Required Action |
| --- | --- | --- | --- | --- | --- | --- |
| BEH-001 | User | Pass | Pass: selected role commands; current parser lacks them | Pass: dispatch before elevation, embedded ordinary-user UI | Confirmed | None |
| BEH-002 | User | Pass | Pass: existing create, in-place source/self-mount and consent | Pass: BeginServer → retained Plan → Commit → Apply/Status | Confirmed | None |
| BEH-003 | User | Pass | Pass: existing Connection/target validators and connect | Pass: separate client input, no inferred identity or raw Plan authority | Confirmed | None |
| BEH-004 | Operational | Pass | Pass: active/pending recovery, actual Status, drained Detach | Pass for explicit dashboard/terminal operations; no automatic pending resume | Confirmed | None |
| BEH-005 | Contract | Pass | Pass: R1 local-management security and current trusted install/store/lock | Pass: nonroot HTTP, bounded private pipe, explicit OS consent | Confirmed | Native proof remains downstream |
| BEH-006 | System | Pass | Pass: installed service independent of terminal; job definitions call `service` | Pass: DS6 admin owns attempt, cleanup, retry/stop; dashboard lifetime remains separate | Confirmed | None; ARCH-F001 resolved |
| BEH-007 | Contract | Pass | Pass: standalone build/current records/preserved service contract | Pass: explicit service migration without SUDO/TTY, no schema/release change | Confirmed | None; ARCH-F001 resolved |

## Supplemental Artifact Coherence Verdict

**None.** Investigation explicitly inventories no supplements. Handoff/history agree on R1 approval, SR003 affected re-review, prior ARCH001 Fail, evidence limitations, source-only target and resolved historical extraction blocker. E13 records the design lesson and suggests a project-owned case location only; no shared-skill change or new deliverable gate is inferred. No requirement for a separate Product package is inferred.

## Task Design Health Assessment Verdict

| Assessment Area | Result | Evidence | Required Action |
| --- | --- | --- | --- |
| Assessment is present for current posture | Pass | Design:40–41 correctly treats this as a feature with ownership pressure | None |
| Root-cause classification explicit/evidence-backed | Pass | CLI root sequencing would otherwise be duplicated by dashboard | None |
| Refactor decision explicit | Pass | One admin owner, thin adapters, existing setup safety | None |
| Refactor reflected concretely | Pass | SR003 DS6:124–137 plus file/removal/sequence maps relocate the whole supervisor loop and sole caller | None; ARCH-F001 resolved |

## Spine Inventory Verdict

| Spine ID | Scope | Spine Is Readable? | Narrative Is Clear? | Facade Vs Governing Owner Is Clear? | Main Domain Subject Naming Is Clear? | One Owner Per Node, In Call Order? | Off-Spine Concerns Stay Off Main Line? | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DS1 | Role launch/authentication | Pass | Pass | Pass | Pass | Pass | Pass | Pass |
| DS2 | Server/client plan and commit | Pass | Pass | Pass | Pass | Pass | Pass | Pass |
| DS3 | Explicit inspect/check/reconnect/detach | Pass | Pass | Pass | Pass | Pass | Pass | Pass |
| DS6 | Installed repeated reconciliation and bounded loop | Pass | Pass | Pass | Pass | Pass | Pass | Pass |
| DS4 | Session/lease/operation return and stop | Pass | Pass | Pass | Pass | Pass | Pass | Pass |
| DS5 | Embedded build/identity | Pass | Pass | Pass | Pass | Pass | Pass | Pass |

Call-order check (not new requirements):
- Launch: role command → cli host/user/TTY gate → dashboard session/listener → private bootstrap → browser exchange → authorized form. Authorization is a separate dashboard → fixed sudo/install → root helper handshake path.
- Create/connect: authenticated browser input → dashboard admission → private codec → admin begin (lock/admit/identity/Docker) → setup.Plan → display projection; subsequent exact-lease commit → setup.Apply (intent before effects) → setup.Status → root result → dashboard snapshot → browser poll.
- Active reconnect: review under admin lock → consent → setup.Reconnect → InstallJob → observed result. Pending reconnect: saved-owner context → PendingPlan → fresh consent → Apply/Status. Detach: current/pending scope → review/drain → setup.Detach → retained-data/result. Status-only: locked check → cached observed result, never polling NFS in HTTP.
- Session loop: admit one request → worker/retained lease → result/state; cancel or expiry discards only an uncommitted lease; stop rejects work and drains committed work. Directory listing has its own single nonroot slot.
- **DS6 current → target re-trace:** current jobs → binary `service` → cli.Run → service.Supervise acquires lock → CLI callback admits/opens Docker/reconnects → supervisor closes/reports/waits. **Target:** fixed job → thin root CLI supplies signal context/log → `admin.Session.Supervise` → same-owner `reconcileOnce` → acquire once → standalone/binary admission → saved Docker → shared `reconnectActiveLocked` → existing setup.Reconnect → close Docker then lock → report → completion-relative 30s wait or stop. No passed reconciliation callback, nested acquisition or reverse import. Pending stays refused; service never invokes Apply/InstallJob/Detach. Explicit reconnect shares the active mechanism but keeps InstallJob/Status continuation. Stop prevents another attempt and drains an outstanding one before return (design:124–137).

## Boundary Encapsulation Verdict

| Boundary / Owner | Authoritative Public Entry Point Is Clear? | Internal Owned Mechanisms Stay Internal? | Caller Bypass Risk Is Controlled? | Verdict | Notes |
| --- | --- | --- | --- | --- | --- |
| dashboard.Session / admin.Session / setup.Service | Pass | Pass | Pass | Pass | Presentation and root storage authority separated; browser cannot supply Plan/User/Store/Runner |
| admin versus installed supervisor | Pass | Pass | Pass | Pass | DS6 owns both loop and full operation scope; service keeps only probe/source mechanisms |

## Dependency Direction / Forbidden Shortcut Verdict

| Owner / Boundary | Allowed Dependencies Are Clear? | Forbidden Shortcuts Are Explicit? | Direction Is Coherent With Ownership? | Verdict | Notes |
| --- | --- | --- | --- | --- | --- |
| CLI/dashboard/adminwire/admin/setup | Pass | Pass | Pass | Pass | Fixed transport, no root HTTP or dashboard→setup/config bypass |
| admin/service supervisor | Pass | Pass | Pass | Pass | Direct CLI→admin.Supervise; admin→setup/service probes; setup/service→admin explicitly forbidden |

## Interface Boundary Verdict

| Interface / API / Query / Command / Method | Subject Is Clear? | Responsibility Is Singular? | Identity Shape Is Explicit? | Generic Boundary Risk | Verdict |
| --- | --- | --- | --- | --- | --- |
| BeginServer / BeginClient | Pass | Pass | Pass | Low | Pass |
| Inspect / BeginReconnect / BeginDetach / CheckReadiness | Pass | Pass | Pass | Low | Pass |
| Commit / CancelReview / Close | Pass | Pass | Pass | Medium | Pass |
| Session exchange / directory-only selection / operation polling | Pass | Pass | Pass | Medium | Pass |
| admin.Session.Supervise(ctx,log) / private reconcileOnce | Pass | Pass | Pass | Low | Pass |

## Existing Capability / Subsystem Reuse Verdict

| Need / Concern | Existing Capability Area Was Checked? | Reuse / Extension Decision Is Sound? | New Support Piece Is Justified? | Verdict | Notes |
| --- | --- | --- | --- | --- | --- |
| Setup, state, backend, mount/source and nonroot probe | Pass | Pass | N/A | Pass | Keep existing authority and invariants |
| Browser/private helper | Pass | Pass | Pass | Pass | No existing HTTP owner; bounded stdlib adapters justified |
| Repeated service reconciliation | Pass | Pass | N/A | Pass | E13 matches source: relocate small loop, reuse setup.Reconnect and existing lock mechanism |

## Subsystem / Capability-Area Allocation Verdict

| Subsystem / Capability Area | Ownership Allocation Is Clear? | Reuse / Extend / Create-New Decision Is Sound? | Supports The Right Spine Owners? | Verdict | Notes |
| --- | --- | --- | --- | --- | --- |
| dashboard and adminwire | Pass | Pass | Pass | Pass | Local presentation/auth/process transport, not root policy |
| admin and existing setup/providers | Pass | Pass | Pass | Pass | Good target for explicit host operations |
| Admin supervision / service probes | Pass | Pass | Pass | Pass | Full attempt and repeat/stop belong to admin; service.Supervise is removed |

## Reusable Owned Structures Verdict

| Repeated Structure / Logic | Extraction Need Was Evaluated? | Shared File Choice Is Sound? | Ownership Of Shared Structure Is Clear? | Verdict | Notes |
| --- | --- | --- | --- | --- | --- |
| Connection / Request / Plan | Pass | Pass | Pass | Pass | Reuse config/setup types; Plan remains root memory |
| Wire/review/result projection | Pass | Pass | Pass | Pass | Current protocol and one vocabulary, not persisted copies |
| Lock/admission/Docker/operation sequence | Pass | Pass | Pass | Pass | Shared admin scope and active mechanism; no generic WithLock callback coordinator |

## Shared Structure / Data Model Tightness Verdict

| Shared Structure / Type / Schema | One Clear Meaning Per Field? | Redundant Attributes Removed? | Overlapping Representation Risk Is Controlled? | Shared Core Vs Specialized Variant / Composition Decision Is Sound? | Verdict | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Operation/request/lease/auth identities | Pass | Pass | Pass | Pass | Pass | Separate meanings; explicit server/client inputs; no arbitrary record selector |
| Configuration versus observed readiness | Pass | Pass | Pass | Pass | Pass | No persisted ready flag; failed post-apply check is not rollback |

Derived consumers listed with decisions: **Pass** for config/setup views, CLI rendering, wire/browser, tests, asset hash and docs. Supervisor coordination now has a complete DS6 migration while stored Attachment semantics remain unchanged (ARCH-F001 resolved).

Domain vocabulary: **Pass**. Server/client storage roles, launch/auth session, plan lease, operation and Connection are distinct. Naming normalization in code remains implementation work; no project glossary exists.

## File Responsibility Mapping Verdict

| File | Responsibility Is Singular And Clear? | Responsibility Matches Intended Owner? | Re-Tightened After Shared-Structure Extraction? | Verdict | Notes |
| --- | --- | --- | --- | --- | --- |
| Proposed admin session/operations/state/pipe and adminwire | Pass | Pass | Pass | Pass | Governing scope, projections and transport are separated |
| Proposed dashboard session/http/privilege/browser/directories/assets/web | Pass | Pass | Pass | Pass | No catch-all root web controller; cohesive concerns |
| CLI inputs/run/interactive/install/dashboard | Pass | Pass | Pass | Pass | Explicit input/output/privilege adapters |
| Existing service/supervisor.go → admin/supervisor.go | Pass | Pass | Pass | Pass | Old driver deleted; same-owner loop/attempt and focused tests explicitly mapped |
| Tests/docs/CI/packaging regression | Pass | Pass | Pass | Pass | Bounded source-only changes; runtime UI has no Node/CDN dependency |

## Subsystem / Folder / File Placement Verdict

| Path / Item | Target Placement Is Clear? | Folder Matches Owning Boundary? | Mixed-Layer Or Over-Split Risk | Verdict | Notes |
| --- | --- | --- | --- | --- | --- |
| internal/{admin,adminwire,dashboard}, embedded web | Pass | Pass | Low | Pass | Privilege/transport separation without generic manager chain |
| Supervisor loop after extraction | Pass | Pass | Low | Pass | internal/admin/supervisor.go, no reverse dependency or retained adapter |

## Removal / Decommission Completeness Verdict

| Item / Area | Redundant / Obsolete Piece To Remove Is Named? | Replacement Owner / Structure Is Clear? | Removal / Decommission Scope Is Explicit? | Verdict | Notes |
| --- | --- | --- | --- | --- | --- |
| CLI setup coordination/openSavedDocker | Pass | Pass | Pass | Pass | Production call sites verified in run.go and interactive-setup.go |
| Lock-owning supervisor callback contract | Pass | Pass | Pass | Pass | Sole production caller rechecked; old definition/callback deleted in the admin migration |
| Stale touched NFS doc wording | Pass | Pass | Pass | Pass | No application change implied |

No other dead path was established in the inspected touched scope. No unrelated cleanup/follow-up is invented.

## Legacy / Backward-Compatibility Verdict

| Area | Compatibility Wrapper / Dual-Path / Legacy Retention Exists? | Clean-Cut Removal Is Explicit? | Verdict | Notes |
| --- | --- | --- | --- | --- |
| Terminal/UI entry forms, wire and installed records | No | Pass | Pass | Public CLI is deliberately supported; additive stored-field reading is not a legacy fallback. Supervisor replacement is now clean-cut; no old/new execution switch |

## Persisted-Data Transition Verdict (When Applicable)

| Area / Stored Subject | Approved Decision | Reader / Semantic / Invariant Evidence Sufficient? | Choice Proportionate? | Migration Safety Complete If Required? | Verdict | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Attachment/hosted/pending/Docker/resource/recovery records and marker | Directly Usable — No Migration | Pass | Pass | N/A | Pass | Unchanged setup writers and bounded private readers; predecessor node obligations still refuse. No live data inspected or rewritten |
| Auth/operation/lease/UI draft | Not persisted | Pass | Pass | N/A | Pass | Process-local lifetime; no second transaction journal |

## Change / Refactor Safety Verdict

| Area | Sequence Is Realistic? | Temporary Seams Are Explicit? | Cleanup / Removal Is Explicit? | Verdict |
| --- | --- | --- | --- | --- |
| Admin-first extraction, IPC before browser mutation, native proof then docs | Pass | Pass | Pass | Pass |
| Installed-service extraction and regressions | Pass | Pass | Pass | Pass |

The design explicitly requires real owned sudo/host/browser proof and precise external blockers, not live-user fallback or synthetic Pass. No additional field qualification/release prerequisite is imposed by this review.

## Example Adequacy Verdict

| Topic / Area | Example Was Needed? | Example Present And Clear? | Bad / Avoided Shape Explained? | Verdict | Notes |
| --- | --- | --- | --- | --- | --- |
| Retained plan versus browser Plan; asynchronous readiness; common admin sequence | Yes | Pass | Pass | Pass | Design:208–213 is concrete |
| Installed supervisor and new admin owner | Yes | Pass | Pass | Pass | DS6 and good/bad call-order examples exclude held-lock callback and second acquisition |

## Material Premise Validation (Only When Needed)

**None beyond the established behavior basis.** Resolved ARCH-F001 follows the ordinary installed `service` entry (SCN010) and its directly verified current caller path, not an imagined race or outage. DS6 introduces no new recovery premise; helper-only SIGPIPE guidance implements existing SCN008/009 drain intent. SCN007–009 already authorize the origin, repeated-click, abandoned-review and shutdown mechanisms. No same-user compromise, arbitrary record tampering, distributed administrator workflow or new storage recovery scenario is added.

## Unresolved Approved-Behavior Or Current-State Gaps

None. ARCH-F001 is resolved by SR003; no new requirement, current-state or target-path gap identified in the affected review.

## Review Decision

**Pass — ARCH-REV-002.** R1/SR001 Approved + SR003 design are ready for implementation. The supervisor transition now has one complete governing owner, explicit removal and preservation checks. Unchanged browser/privilege/plan/storage and source-only boundaries retain their ARCH001 evidence. This is architecture readiness, not executed acceptance.

## Findings

**None open.** ARCH-F001 is **Resolved**; the resolution and verification are recorded in ARCH-REV-002 in `architecture-review-revision-record.md`. No new finding ID.

## Classification

**N/A — Pass, no unresolved finding.** Large / High retained. Prior Design Impact ARCH-F001 resolved without changing R1 or requiring user approval.

## Recommended Recipient

Implementation Engineer under the fresh primary Pass rule, carrying R1/SR001 + SR003 and ARCH-REV-002. Single downstream dispatch; do not send duplicate work to PM/API/Delivery. Preserve the source-only/no-release and isolated-resource boundaries.

## Residual Risks

- Native sudo/TTY/pipe/process behavior is still unproved. The installed `/usr/share/man/man8/sudo.8` (1.9.17p2) confirms terminal password handling and default retention of descriptors 0/1/2; it also documents signal relay. Online sudo manual fetch was robots-denied; no sudo action was executed. These contracts support the proposed transport, not acceptance of its implementation.
- EOF/close tests must exercise actual standard-pipe failure and safe child drain, not only a mock context cancellation. Go's default stdout/stderr broken-pipe behavior can terminate the process; honor the already-designed drain contract at the helper transport boundary. SR003:244/E14 now explicitly scopes this to the helper and real pipe tests; public CLI signal policy is not changed. This is implementation guidance under DS4, not a new recovery mechanism. [Go os/signal documentation](https://pkg.go.dev/os/signal#hdr-SIGPIPE).
- Go's CSRF helper alone permits safe methods and requests without Origin/Fetch metadata. The design correctly adds exact Host/origin and bearer controls rather than treating localhost/CSRF middleware as authentication. [Go CrossOriginProtection source](https://go.dev/src/net/http/csrf.go).
- Browser bootstrap associations, native Mac26+/Ubuntu guests, real privilege and each existing backend still require the specified bounded downstream proof. Public v0.1.0 is not this build; development Linux builds need measured engine/package inputs without release-gate bypass. Resource unavailability is a precise validation blocker, not implicit scope approval or a broad user questionnaire.
- No new follow-up Task identified. No test result, release authorization, field qualification, TaskDone or user verification is claimed here.

## Latest Authoritative Result

- Review Decision: **Pass** — ARCH-REV-002, approved R1/SR-001, design SR-003 (supersedes reviewed SR002).
- Material-Premise Gate: **Pass** — only supported/established scenarios used.
- Notes: ARCH-F001 **Resolved**; no open/new findings. **Large / High** retained. Only reviewer report/history changed in this round; no product/runtime action, acceptance result, release or upstream-authority edit.
