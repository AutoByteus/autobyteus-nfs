# Design Review Report

## Review Round Meta

- Upstream Requirements Doc: `requirements-doc.md`, R1 / SR-001 Approved.
- Upstream Investigation Notes: `investigation-notes.md`, E01–12.
- Upstream Solution Revision Record: `solution-revision-record.md`.
- Reviewed Design Spec: `design-spec.md`, SR-002 Ready.
- Supplemental Task Artifacts Reviewed: `solution-design-handoff.md`; no behavior-defining supplements.
- Relevant Solution Revision IDs: SR-001, SR-002.
- Architecture Review Revision Record: `architecture-review-revision-record.md`.
- Current Architecture Review Revision ID: **ARCH-REV-001**.
- Current Review Round: 1, 2026-10-24.
- Trigger: Solution Designer's Architecture Design Complete for autobyteus-nfs-2 / `project_task_f1264eb8-5a99-4a19-949f-09d141c955a1`.
- Prior Review Round Reviewed: None. Reviews of other NFS Tasks are not this Task's baseline.
- Latest Authoritative Round: This report.
- Current-State Evidence Basis: independent read of the five upstream documents and current source at `48591a58d2e0413a18bbab8bbeb714cc034f7c95`, whose only changes from `52c17fb5480d23b89752a8ae201419e356b4c3fc` are those documents. Worktree `/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/nfs-setup-dashboard`, branch `codex/nfs-setup-dashboard`; initially clean.
- Review method: current role skill/principles/examples/template and repository AGENTS/DESIGN/TESTING/RELEASE read; source/caller tracing and primary-contract inspection only. No Go/browser/sudo/VM/mount execution, resource creation, live state inspection, remote repository mutation, or release action. No executable acceptance claim.

## Routing Classification Review

- Task size: **Large**.
- Architectural risk: **High**.
- Classification rationale reviewed: embedded UI, new browser/privilege transport and process lifetime, shared root administrative sequencing, and terminal/service migration. These are structural/security/concurrency changes, not content-volume inflation.
- Independent Architecture Review required by the classification: **Yes**.
- Classification evidence or correction required: Classification is sound. One bounded design correction is required before implementation; no product reapproval or field-test campaign is requested.

## Upstream Behavior And Production-Path Basis Confirmation

- Overall Basis Status: **Contradicted**, narrowly in the target ownership/path completeness for the preserved installed-service entry. Approved intent and relevant existing behavior are understood; this is not an approval gap.
- Approved requirements / intended behavior understood: ordinary-user `server`/`client` local dashboards, explicit terminal OS approval and exact-plan consent, same storage contracts, standalone source-only delivery.
- Relevant existing behavior and evidence confirmed: the terminal currently coordinates setup; the installed supervisor separately acquires/releases the global lock and invokes a reconciliation callback. The latter part is not resolved in SR-002's shared-owner mapping (ARCH-F001).
- Scope guardrail confirmed: UC001–005 / SCN001–010; no app, skills, discovery, new backend, migration, release, live-user operation or nfs-4 field campaign. Preserved CLI/service/storage contracts remain in scope.
- Approved change, preserved behavior, and outside scope understood: Yes. Public terminal commands remain supported entry forms, not legacy compatibility paths.
- Every prospective blocking Design Impact finding is traceable to an approved REQ/AC/BEH: **Yes** — ARCH-F001 protects REQ-007/008, AC-008, BEH-006/007, SCN-010.
- Remaining material ambiguity: no intended-behavior ambiguity; the supervisor sequence's target owner/removal is incomplete.
- Existing-code claims opened at cited lines: `cli/run.go:19–188`, `inputs.go:24–78,103–165`, `interactive-setup.go:11–56`, `install.go:19–142`; `setup/plan.go:18–147`, `apply.go:15–172`, `pending.go:13–89`, `lifecycle.go:13–143`, `status.go:18–42`; `service/supervisor.go:13–30`, `probe.go:119–160`; `platform/lock.go:10–23`, `commands.go:19–40`, `source.go:14–66`, `mounts.go:13–160`, `jobs.go:29–113`; `config/store.go:13–123`, `state.go:13–60`, `installation_state.go:12–87`, `connection.go:17–145`; `cmd/autobyteus-nfs/main.go:13–25`, development release JSON, `packaging/release_support/identity.py:18–22,152–168`, current README/usage and CI. All paths here are repository-relative with `internal/` for Go packages unless stated otherwise.

| Behavior ID | Kind | Design Alignment With Approved Intent | Approved Trigger / Contract And Current-State Evidence | Target Outcome / Path / Spine Coherence | Status | Required Action |
| --- | --- | --- | --- | --- | --- | --- |
| BEH-001 | User | Pass | Pass: selected role commands; current parser lacks them | Pass: dispatch before elevation, embedded ordinary-user UI | Confirmed | None |
| BEH-002 | User | Pass | Pass: existing create, in-place source/self-mount and consent | Pass: BeginServer → retained Plan → Commit → Apply/Status | Confirmed | None |
| BEH-003 | User | Pass | Pass: existing Connection/target validators and connect | Pass: separate client input, no inferred identity or raw Plan authority | Confirmed | None |
| BEH-004 | Operational | Pass | Pass: active/pending recovery, actual Status, drained Detach | Pass for explicit dashboard/terminal operations; no automatic pending resume | Confirmed | None |
| BEH-005 | Contract | Pass | Pass: R1 local-management security and current trusted install/store/lock | Pass: nonroot HTTP, bounded private pipe, explicit OS consent | Confirmed | Native proof remains downstream |
| BEH-006 | System | Pass | Pass: installed service independent of terminal; job definitions call `service` | Fail: preserved service loop not assigned a complete target sequence alongside the new lock owner | Needs Correction | ARCH-F001 |
| BEH-007 | Contract | Pass | Pass: standalone build/current records/preserved service contract | Fail only for service caller migration; asset/schema/release boundaries otherwise coherent | Needs Correction | ARCH-F001 |

## Supplemental Artifact Coherence Verdict

**None.** Investigation explicitly inventories no supplements. Handoff/history agree on R1 approval, SR002 readiness, evidence limitations, source-only target and resolved historical extraction blocker. No requirement for a separate Product package is inferred.

## Task Design Health Assessment Verdict

| Assessment Area | Result | Evidence | Required Action |
| --- | --- | --- | --- |
| Assessment is present for current posture | Pass | Design:40–41 correctly treats this as a feature with ownership pressure | None |
| Root-cause classification explicit/evidence-backed | Pass | CLI root sequencing would otherwise be duplicated by dashboard | None |
| Refactor decision explicit | Pass | One admin owner, thin adapters, existing setup safety | None |
| Refactor reflected concretely | Fail | CLI extraction is mapped; existing supervisor lock/callback sequence is not | ARCH-F001 |

## Spine Inventory Verdict

| Spine ID | Scope | Spine Is Readable? | Narrative Is Clear? | Facade Vs Governing Owner Is Clear? | Main Domain Subject Naming Is Clear? | One Owner Per Node, In Call Order? | Off-Spine Concerns Stay Off Main Line? | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DS1 | Role launch/authentication | Pass | Pass | Pass | Pass | Pass | Pass | Pass |
| DS2 | Server/client plan and commit | Pass | Pass | Pass | Pass | Pass | Pass | Pass |
| DS3 | Explicit inspect/check/reconnect/detach | Pass | Pass | Pass | Pass | Pass | Pass | Pass |
| DS3/service entry | Installed repeated reconciliation | Fail | Fail | Fail | Pass | Fail | Fail | Fail |
| DS4 | Session/lease/operation return and stop | Pass | Pass | Pass | Pass | Pass | Pass | Pass |
| DS5 | Embedded build/identity | Pass | Pass | Pass | Pass | Pass | Pass | Pass |

Call-order check (not new requirements):
- Launch: role command → cli host/user/TTY gate → dashboard session/listener → private bootstrap → browser exchange → authorized form. Authorization is a separate dashboard → fixed sudo/install → root helper handshake path.
- Create/connect: authenticated browser input → dashboard admission → private codec → admin begin (lock/admit/identity/Docker) → setup.Plan → display projection; subsequent exact-lease commit → setup.Apply (intent before effects) → setup.Status → root result → dashboard snapshot → browser poll.
- Active reconnect: review under admin lock → consent → setup.Reconnect → InstallJob → observed result. Pending reconnect: saved-owner context → PendingPlan → fresh consent → Apply/Status. Detach: current/pending scope → review/drain → setup.Detach → retained-data/result. Status-only: locked check → cached observed result, never polling NFS in HTTP.
- Session loop: admit one request → worker/retained lease → result/state; cancel or expiry discards only an uncommitted lease; stop rejects work and drains committed work. Directory listing has its own single nonroot slot.
- **Current service path:** launchd/systemd → binary `service` → cli.Run → service.Supervise **acquire lock** → supplied CLI callback **admit/open Docker/assign Runner+Lock/setup.Reconnect/close Docker** → service.Supervise **close lock/report/wait30s**. SR002 does not draw the replacement for this full path. Merely changing the callback's body to call admin would retain split sequence ownership (ARCH-F001).

## Boundary Encapsulation Verdict

| Boundary / Owner | Authoritative Public Entry Point Is Clear? | Internal Owned Mechanisms Stay Internal? | Caller Bypass Risk Is Controlled? | Verdict | Notes |
| --- | --- | --- | --- | --- | --- |
| dashboard.Session / admin.Session / setup.Service | Pass | Pass | Pass | Pass | Presentation and root storage authority separated; browser cannot supply Plan/User/Store/Runner |
| admin versus installed supervisor | Fail | Fail | Fail | Fail | Admin claims lock/lifecycle ownership but existing supervisor acquires lock outside it; no explicit replacement in file/removal map |

## Dependency Direction / Forbidden Shortcut Verdict

| Owner / Boundary | Allowed Dependencies Are Clear? | Forbidden Shortcuts Are Explicit? | Direction Is Coherent With Ownership? | Verdict | Notes |
| --- | --- | --- | --- | --- | --- |
| CLI/dashboard/adminwire/admin/setup | Pass | Pass | Pass | Pass | Fixed transport, no root HTTP or dashboard→setup/config bypass |
| admin/service supervisor | Fail | Pass | Fail | Fail | Design:131 allows admin→service; moving callback into admin alone does not settle the service-owned lock/order |

## Interface Boundary Verdict

| Interface / API / Query / Command / Method | Subject Is Clear? | Responsibility Is Singular? | Identity Shape Is Explicit? | Generic Boundary Risk | Verdict |
| --- | --- | --- | --- | --- | --- |
| BeginServer / BeginClient | Pass | Pass | Pass | Low | Pass |
| Inspect / BeginReconnect / BeginDetach / CheckReadiness | Pass | Pass | Pass | Low | Pass |
| Commit / CancelReview / Close | Pass | Pass | Pass | Medium | Pass |
| Session exchange / directory-only selection / operation polling | Pass | Pass | Pass | Medium | Pass |
| Service reconciliation entry and held-lock contract | Fail | Fail | Fail | Medium | Fail |

## Existing Capability / Subsystem Reuse Verdict

| Need / Concern | Existing Capability Area Was Checked? | Reuse / Extension Decision Is Sound? | New Support Piece Is Justified? | Verdict | Notes |
| --- | --- | --- | --- | --- | --- |
| Setup, state, backend, mount/source and nonroot probe | Pass | Pass | N/A | Pass | Keep existing authority and invariants |
| Browser/private helper | Pass | Pass | Pass | Pass | No existing HTTP owner; bounded stdlib adapters justified |
| Repeated service reconciliation | Pass | Fail | N/A | Fail | E10/source read is correct, but reuse versus relocation of supervisor is undecided |

## Subsystem / Capability-Area Allocation Verdict

| Subsystem / Capability Area | Ownership Allocation Is Clear? | Reuse / Extend / Create-New Decision Is Sound? | Supports The Right Spine Owners? | Verdict | Notes |
| --- | --- | --- | --- | --- | --- |
| dashboard and adminwire | Pass | Pass | Pass | Pass | Local presentation/auth/process transport, not root policy |
| admin and existing setup/providers | Pass | Pass | Pass | Pass | Good target for explicit host operations |
| service.Supervise / admin reconcile | Fail | Fail | Fail | Fail | Complete loop must have one named governing sequence owner |

## Reusable Owned Structures Verdict

| Repeated Structure / Logic | Extraction Need Was Evaluated? | Shared File Choice Is Sound? | Ownership Of Shared Structure Is Clear? | Verdict | Notes |
| --- | --- | --- | --- | --- | --- |
| Connection / Request / Plan | Pass | Pass | Pass | Pass | Reuse config/setup types; Plan remains root memory |
| Wire/review/result projection | Pass | Pass | Pass | Pass | Current protocol and one vocabulary, not persisted copies |
| Lock/admission/Docker/operation sequence | Pass | Fail | Fail | Fail | Shared admin extraction incomplete for installed-service entry |

## Shared Structure / Data Model Tightness Verdict

| Shared Structure / Type / Schema | One Clear Meaning Per Field? | Redundant Attributes Removed? | Overlapping Representation Risk Is Controlled? | Shared Core Vs Specialized Variant / Composition Decision Is Sound? | Verdict | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Operation/request/lease/auth identities | Pass | Pass | Pass | Pass | Pass | Separate meanings; explicit server/client inputs; no arbitrary record selector |
| Configuration versus observed readiness | Pass | Pass | Pass | Pass | Pass | No persisted ready flag; failed post-apply check is not rollback |

Derived consumers listed with decisions: **Pass** for config/setup views, CLI rendering, wire/browser, tests, asset hash and docs. Supervisor is named as a consumer, but its sequencing migration is incomplete (ARCH-F001), not a missing schema consumer.

Domain vocabulary: **Pass**. Server/client storage roles, launch/auth session, plan lease, operation and Connection are distinct. Naming normalization in code remains implementation work; no project glossary exists.

## File Responsibility Mapping Verdict

| File | Responsibility Is Singular And Clear? | Responsibility Matches Intended Owner? | Re-Tightened After Shared-Structure Extraction? | Verdict | Notes |
| --- | --- | --- | --- | --- | --- |
| Proposed admin session/operations/state/pipe and adminwire | Pass | Pass | Pass | Pass | Governing scope, projections and transport are separated |
| Proposed dashboard session/http/privilege/browser/directories/assets/web | Pass | Pass | Pass | Pass | No catch-all root web controller; cohesive concerns |
| CLI inputs/run/interactive/install/dashboard | Pass | Pass | Pass | Pass | Explicit input/output/privilege adapters |
| Existing service/supervisor.go | Fail | Fail | Fail | Fail | Missing concrete move/modify/remove decision for its lock-owning loop |
| Tests/docs/CI/packaging regression | Pass | Pass | Pass | Pass | Bounded source-only changes; runtime UI has no Node/CDN dependency |

## Subsystem / Folder / File Placement Verdict

| Path / Item | Target Placement Is Clear? | Folder Matches Owning Boundary? | Mixed-Layer Or Over-Split Risk | Verdict | Notes |
| --- | --- | --- | --- | --- | --- |
| internal/{admin,adminwire,dashboard}, embedded web | Pass | Pass | Low | Pass | Privilege/transport separation without generic manager chain |
| Supervisor loop after extraction | Fail | Fail | Medium | Fail | Existing placement/contract cannot simply be assumed unchanged |

## Removal / Decommission Completeness Verdict

| Item / Area | Redundant / Obsolete Piece To Remove Is Named? | Replacement Owner / Structure Is Clear? | Removal / Decommission Scope Is Explicit? | Verdict | Notes |
| --- | --- | --- | --- | --- | --- |
| CLI setup coordination/openSavedDocker | Pass | Pass | Pass | Pass | Production call sites verified in run.go and interactive-setup.go |
| Lock-owning supervisor callback contract | Fail | Fail | Fail | Fail | Sole production Supervise caller is run.go:79; specify replacement and remove obsolete contract if moved |
| Stale touched NFS doc wording | Pass | Pass | Pass | Pass | No application change implied |

No other dead path was established in the inspected touched scope. No unrelated cleanup/follow-up is invented.

## Legacy / Backward-Compatibility Verdict

| Area | Compatibility Wrapper / Dual-Path / Legacy Retention Exists? | Clean-Cut Removal Is Explicit? | Verdict | Notes |
| --- | --- | --- | --- | --- |
| Terminal/UI entry forms, wire and installed records | No | Pass | Pass | Public CLI is deliberately supported; additive stored-field reading is not a legacy fallback. Supervisor issue is ownership incompleteness, not evidence of a compatibility scheme |

## Persisted-Data Transition Verdict (When Applicable)

| Area / Stored Subject | Approved Decision | Reader / Semantic / Invariant Evidence Sufficient? | Choice Proportionate? | Migration Safety Complete If Required? | Verdict | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Attachment/hosted/pending/Docker/resource/recovery records and marker | Directly Usable — No Migration | Pass | Pass | N/A | Pass | Unchanged setup writers and bounded private readers; predecessor node obligations still refuse. No live data inspected or rewritten |
| Auth/operation/lease/UI draft | Not persisted | Pass | Pass | N/A | Pass | Process-local lifetime; no second transaction journal |

## Change / Refactor Safety Verdict

| Area | Sequence Is Realistic? | Temporary Seams Are Explicit? | Cleanup / Removal Is Explicit? | Verdict |
| --- | --- | --- | --- | --- |
| Admin-first extraction, IPC before browser mutation, native proof then docs | Pass | Pass | Pass | Pass |
| Installed-service extraction and regressions | Fail | Fail | Fail | Fail |

The design explicitly requires real owned sudo/host/browser proof and precise external blockers, not live-user fallback or synthetic Pass. No additional field qualification/release prerequisite is imposed by this review.

## Example Adequacy Verdict

| Topic / Area | Example Was Needed? | Example Present And Clear? | Bad / Avoided Shape Explained? | Verdict | Notes |
| --- | --- | --- | --- | --- | --- |
| Retained plan versus browser Plan; asynchronous readiness; common admin sequence | Yes | Pass | Pass | Pass | Design:187–191 is concrete |
| Installed supervisor and new admin owner | Yes | Fail | Fail | Fail | Draw the real callback/lock order and its replacement, not just the browser path |

## Material Premise Validation (Only When Needed)

**None beyond the established behavior basis.** ARCH-F001 follows the ordinary installed `service` entry (SCN010) and its directly verified current caller path, not an imagined race or outage. SCN007–009 already authorize the origin, repeated-click, abandoned-review and shutdown mechanisms. No same-user compromise, arbitrary record tampering, distributed administrator workflow or new storage recovery scenario is added.

## Unresolved Approved-Behavior Or Current-State Gaps

| Item | Why It Matters | Required Action | Status |
| --- | --- | --- | --- |
| ARCH-F001: service entry's full target sequence | One preserved production entry still has a lock-owning callback driver outside the proposed shared admin authority | Resolve target call order, ownership, file/removal map and focused preservation checks | Open — Design Impact |

## Review Decision

**Fail — one bounded Design Impact.** The general browser/privilege/lease approach is coherent, but the design is not implementation-ready until its claimed common owner covers the installed-service sequence concretely. This does not withdraw R1 approval or assert a runtime defect in the existing supervisor.

## Findings

### ARCH-F001 — Complete the installed supervisor's shared-owner transition

- Type: **Design Impact**. Severity: **Medium**, blocking architecture readiness.
- Approved authority protected: **REQ-007/008, AC-008, BEH-006/007, SCN-010** — single administrative operation, preserved installed service behavior through shared policy, and independent storage lifetime.
- Scope status: **Within Approved Scope**. Changes approved behavior: **No**. No renewed user approval needed for this ownership clarification.
- Affected behavior: systemd/launchd runs the installed `service` command without SUDO_UID; active reconciliation must retain serial lock/admission, saved-user probes, no pending resume and safe in-flight shutdown.
- Evidence: `internal/platform/jobs.go:29–57` supplies the supported trigger. `internal/cli/run.go:76–90` passes the reconciliation body into `internal/service/supervisor.go:15–29`; the latter acquires/closes the lock and controls reporting/retry. This is a production path, not a test-only callback. Caller search found one production Supervise call at run.go:79. SR002 `design-spec.md:61,71,110,114,127–131,156–159,177–190,194` claims a single admin lock/operation owner and service migration but maps only “service reconcile calls,” retaining existing service mechanisms and omitting supervisor.go from changes/removals. Moving the existing callback body alone leaves Supervise → callback → admin/setup sequencing and split lock authority; having that callback invoke a normal lock-acquiring admin method instead causes self-contention. The design must choose the actual path rather than leave either interpretation to implementation.
- Material-premise ID: **N/A** — established SCN010 current path above; no additional failure premise required.
- Required update: make the installed service a fully drawn primary/bounded-loop path. **Admin must drive the common administrative sequence**: acquire global lock → standalone-state/binary admission → open saved Docker scope → active-only setup.Reconnect using stored identity → close Docker/lock → report result and wait/observe shutdown. State who owns the repeat/stop loop and its exact entry interface. A small supervisor-loop move into admin is sufficient; another design is acceptable only if it preserves one sequence owner without passing a lock-owning collaborator a function that calls back into admin. Do not make setup/service import admin or introduce a second reconciliation implementation. Update file/removal mapping for the old supervisor callback/sole caller and test mapping for no-SUDO service entry, busy-lock retry, no pending resume, cleanup and no overlapping check during shutdown. Retain current 30-second retry and hard-NFS/no-force semantics; no new watchdog required.
- Why proportionate: this is the already-authorized shared-lifecycle refactor's remaining entry form, a small existing loop/contract rather than a broader backend redesign. The correction prevents the implementation from choosing contradictory lock owners while preserving approved behavior.
- Recommended recipient: **Solution Designer**.

## Classification

**Design Impact**. Not a Requirement Gap, product prerequisite or out-of-scope recommendation.

## Recommended Recipient

Solution Designer under the fresh failure rule. Do not dispatch this failed basis to implementation/API/Delivery. Return R1/SR002 with ARCH-REV-001 / ARCH-F001; re-review only the affected service sequence and coherence after revision.

## Residual Risks

- Native sudo/TTY/pipe/process behavior is still unproved. The installed `/usr/share/man/man8/sudo.8` (1.9.17p2) confirms terminal password handling and default retention of descriptors 0/1/2; it also documents signal relay. Online sudo manual fetch was robots-denied; no sudo action was executed. These contracts support the proposed transport, not acceptance of its implementation.
- EOF/close tests must exercise actual standard-pipe failure and safe child drain, not only a mock context cancellation. Go's default stdout/stderr broken-pipe behavior can terminate the process; honor the already-designed drain contract at the helper transport boundary. This is implementation guidance under DS4, not a new recovery mechanism. [Go os/signal documentation](https://pkg.go.dev/os/signal#hdr-SIGPIPE).
- Go's CSRF helper alone permits safe methods and requests without Origin/Fetch metadata. The design correctly adds exact Host/origin and bearer controls rather than treating localhost/CSRF middleware as authentication. [Go CrossOriginProtection source](https://go.dev/src/net/http/csrf.go).
- Browser bootstrap associations, native Mac26+/Ubuntu guests, real privilege and each existing backend still require the specified bounded downstream proof. Public v0.1.0 is not this build; development Linux builds need measured engine/package inputs without release-gate bypass. Resource unavailability is a precise validation blocker, not implicit scope approval or a broad user questionnaire.
- No new follow-up Task identified. No test result, release authorization, field qualification, TaskDone or user verification is claimed here.

## Latest Authoritative Result

- Review Decision: **Fail** — ARCH-REV-001, SR-001/SR-002.
- Material-Premise Gate: **Pass** — only supported/established scenarios used.
- Notes: One open **ARCH-F001**; **Large / High** retained. R1 remains Approved. Reviewer changed only the two review documents; no product/runtime action or upstream-authority edit.
