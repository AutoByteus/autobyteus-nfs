# Requirements — NFS terminal approval feedback

## Document Status
Approved **R1 / SR-001**; package `nfs-cli-approval-feedback`, Task `autobyteus-nfs-7`. Requested by `/project_task_manager` (run `project_task_manager_a5f6d9d306e54970bafdad895bdf731d`). Owner/approver: Solution Designer within the dispatched direction, 2026-10-24. Approval reference: conversation message beginning “I reproduced the feedback gap safely…” explaining actual lifecycle confirmation, waiting/failure guidance and storage-readiness distinction, then continuing without a questionnaire. No behavior-defining supplement or Product approval is required. Architecture is not prescribed by this baseline.

## Problem And Desired Outcome
An ordinary user running public v0.2.0 `~/.local/bin/autobyteus-nfs server` on macOS26.5.2 ARM64 reports silence after Password. The PM described the screenshot; it was not attached for independent inspection. Neither an authentication fault nor a stuck/broken share is established. The terminal must distinguish waiting, confirmed administrator access, preparation of setup controls, readiness for browser interaction and unsuccessful startup. Both role commands share this expectation. Starting management is not creating/connecting storage.

## Relevant Current And Desired Behavior
| Behavior | Kind / scenarios | Current evidence | Desired / preserved outcome |
|---|---|---|---|
| BEH-001 | User; SCN-001/002 | E02–E05: private page already listens before approval; helper launch logs PID only; configuration/result reaches browser | Actual confirmation and next action in terminal for either role, including cached approval; no claim a password was entered |
| BEH-002 | Operational; SCN-003/004/005 | E02–E05: blocking hello/inspect; sudo diagnostics on terminal; browser holds eventual incomplete result | Truthful pending phase and bounded long-wait reminder; concise unsuccessful outcome/retry guidance; preserve sudo's own retries and uncertain cause |
| BEH-003 | Contract; SCN-006/007 | E02–E04: exact-role/digest handshake; single operation/dedup; stop drains without detach | Privacy and authentication/storage/shutdown behavior unchanged; no late invitation to continue after Stop |

## Stakeholders, Actors, And Outcomes
Ordinary local server/client operator needs feedback without guessing or re-entering credentials unnecessarily. Browser remains setup interface; OS remains administrator-consent authority. Engineering must demonstrate messages at actual boundaries without touching the user's setup or turning subprocess tests into OS/field qualification.

## Scope Guardrail
### In-Scope Use Cases
- UC-001: normal/cached administrator confirmation and browser setup readiness (SCN-001/002).
- UC-002: waiting, unsuccessful approval/helper start, configuration initialization failure and next action (SCN-003/004/005).
- UC-003: unchanged privacy, explicit authorization, deduplication, stop/drain and storage effects during these flows (SCN-006/007).
### Out Of Scope
Release, installer/update/signing/qualification metadata; user-machine upgrades or live root state/mount/export/data operations; auth-model/protocol/backend/platform redesign; automatic repair/restart/reconnect; application/Guide/superrepo/skill changes; standalone visual redesign; field task autobyteus-nfs-4 or predecessor reopening.
### Non-Goals
A universal diagnosis of sudo/password failure, maximum authentication/NFS latency, continuous storage-health monitoring, artificial progress percentages or guaranteed automatic browser opening.
### Preserved Behavior Boundary
BEH-003 / REQ-005 / AC-005/006 apply throughout. Terminal feedback cannot authorize, replay or cancel a host operation. Existing metadata inspection may be empty, configured or pending: neither a stored record nor management readiness proves live storage readiness.
### Prerequisites
None identified. Safe validation uses isolated resources; inability to test a real OS/password boundary must be disclosed, not worked around on operator state.
### Review Authority
Findings must protect an approved REQ/AC/preserved behavior. New behavior, threat model, repair mechanism or policy is a Requirement Gap for Solution Designer, not automatically binding scope. Adjacent concerns are follow-ups unless genuine prerequisites. No reviewer can amend this approved basis.

## Relevant Scenarios And Journeys
| Scenario | Actor / goal / trigger | Starting state and product sequence | Expected/alternate outcome | Validity / independent basis |
|---|---|---|---|---|
| SCN-001 | Local server or client operator opens role command and chooses Authorize | Ordinary interactive terminal, page open; completes OS prompt; waits for setup controls | Confirm actual access, preparation and browser next action; no storage-ready claim | Supported Normal Scenario; user report and docs/dashboard.md Open and authorize |
| SCN-002 | Same operator authorizes with existing OS authorization | Same supported command/page; OS needs no password; controls initialize | Equivalent confirmation without claiming password entry | Supported Normal Scenario; existing sudo invocation permits cached consent; exact OS prompting is not controlled by NFS |
| SCN-003 | Operator is still completing approval or waiting for helper/configuration | Supported authorization remains pending | Phase stays visibly waiting; a bounded reminder after a sustained wait, never success/timeout/relaunch | Supported Explicit Edge Scenario; explicit PM requested longer-wait feedback |
| SCN-004 | Operator declines/exhausts actual OS approval, or helper startup fails | Explicit authorize attempt fails before confirmed access | No confirmation/readiness; concise phase/category and safe next action; preserve original terminal diagnostics/retry behavior; do not invent precise cause | Supported Explicit Edge Scenario; user direction expressly includes denied/cancelled/startup failure |
| SCN-005 | Operator's confirmed helper cannot finish reading configuration | Authorized workflow returns configuration refusal or loses helper | Confirmed access remains a historical fact; controls not declared ready; actionable inspection/reopen guidance | Supported Explicit Edge Scenario; requested startup failures and current metadata refusal contract |
| SCN-006 | Operator presses Ctrl+C or Stop while pending/initializing | Existing supported stop request races completion | Stop admission, retain safe drain/no-detach message, no later ready/continue instruction or leftover feedback timer | Supported Explicit Edge Scenario; user observed Ctrl+C, documented safe shutdown |
| SCN-007 | Operator authorizes again after expiry or browser retries same request | Existing explicit authorization or request-id duplicate | New genuine attempt gets fresh feedback; duplicate delivery cannot repeat execution or success messages; privacy retained | Supported Explicit Edge Scenario; existing documented expiry/dedup contracts |
No hidden-state corruption, new simultaneous-session workflow or arbitrary filesystem recovery scenario is added by test fixtures.

## Requirements And Acceptance Criteria
| REQ | Requirement / rationale / priority | Behavior / use case / source |
|---|---|---|
| REQ-001 | Acknowledge administrator access only when actually established, independent of whether a password was entered; show current setup phase without implying HTTP began afterward. Must. | BEH-001; UC-001; user/DEC-001 |
| REQ-002 | On successful initial configuration inspection, show browser next action, keep-terminal-open instruction and private-URL-above fallback. Explicitly distinguish setup-controls readiness from storage configuration/readiness; never assert an existing share is absent. Must. | BEH-001; UC-001; user/DEC-002 |
| REQ-003 | Show waiting before confirmation and during preparation, with at most one reminder per sustained phase; no artificial delay, success deadline, percentage, retry or process cancellation. Must. | BEH-002; UC-002; user/DEC-003 |
| REQ-004 | On unsuccessful approval/helper start/initial inspection, show concise phase-accurate outcome and next action. Distinguish known local start failure, unconfirmed access and post-confirmation preparation failure; preserve uncertainty when OS denial vs helper failure is not knowable. Never log arbitrary private payloads. Must. | BEH-002; UC-002; user/DEC-001/004 |
| REQ-005 | Preserve terminal-only sudo, role/digest/private HTTP admission, explicit plan consent, operation deduplication, root/storage state and safe stop/drain. No readiness invitation after stop, no sensitive new output, no feedback-owned resource leak. Must. | BEH-003; UC-003; task constraints |

| AC | REQ / scenario | Preconditions/trigger and observable outcome | Verification intent / alternative |
|---|---|---|---|
| AC-001 | 001/002; SCN-001/002 | For both roles, valid confirmed access emits confirmation then preparing and, only after successful initial inspection, ready/continue/keep-open/URL-above instructions once. Existing empty/configured/pending configurations get no invented storage status. Cached success wording does not claim password entry. | Current owner path plus subprocess event ordering and real PTY flow; native approval evidence separately labelled |
| AC-002 | 003; SCN-003 | With approval/helper or inspection deliberately held, terminal identifies that phase as waiting. Sustained phase produces one reminder; release of actual success advances immediately, not after a timer. No success on elapsed time. | Controlled hold/release and deterministic reminder tests; one real elapsed waiting observation; no forced root/storage work |
| AC-003 | 004; SCN-004 | Launch failure, handshake rejection and approval/helper exit produce no false confirmation/readiness; phase-accurate concise next action appears. Original sudo retry/diagnostic channel is unchanged; an ambiguous exit is reported as ambiguity, not “wrong password.” | Subprocess launch/EOF/identity controls; actual sudo negative case only in owned disposable guest |
| AC-004 | 004; SCN-005 | Confirmed helper followed by refused/failed inspection shows access confirmed but not dashboard-ready; user can see how to inspect/reopen appropriately, without automatic recovery or private error dumping. | Controlled reply error/transport loss; source-trace metadata-only inspection |
| AC-005 | 005; SCN-006/007 | Stop before completion suppresses late ready/continue and stops reminders while preserving existing drain/NOT-disconnected guidance. No premature helper kill/lock release. New explicit attempt works; same-request duplicate emits no repeated lifecycle. | Race-enabled local tests, PTY Ctrl+C/Stop cases with controlled child drain and existing regressions |
| AC-006 | 005; all | New feedback contains no password, capability token, private URL repetition, config data or uncontrolled child/error text; role commands and browser security/storage/CLI regressions pass with stated boundaries. Docs explain current source behavior, no release/upgrade promise. | Canary/log assertions, source diff and focused/full repository checks; no installed-user storage mutation |

## UI, Interaction, And Experience Requirements
Applicable: terminal text only. Concise plain lines (no colour/spinner dependency), usable with redirected stderr as well as TTY. Keep actual password input in OS terminal channel. Exact wording is engineering-owned; the lifecycle semantics above are normative. Product design artifacts/visual references/confirmation: N/A, not requested; existing browser UX is preserved. No Needs user decision.

## Quality And Non-Functional Requirements
QR-001 → REQ-001–004/AC-001–004: emit on observed events with no deliberate hold; bounded reminder is informational only, not SLA or fake progress.
QR-002 → REQ-005/AC-005/006: no new secrets/state logging, root action, automatic retry or changed cancellation policy; race and timer lifecycle checks required.

## Data Continuity And Acceptable Loss
Persisted/external data affected: No. No reset/deletion/loss authorized; root binary installation already belongs to explicit existing approval, not a new operation triggered by feedback. Config, source, mount, lock, pending plan and service behavior remain unchanged. No migration planned or needed by the requested behavior.

## External Contracts, Assumptions And Supplements
OS sudo owns password prompts, retry policy, cached authorization and diagnostics. A child PID is not authority; initial configuration is not a storage probe (E02–E04). Browser opener success is not a prerequisite to private fallback. No new platform support. Exact user's OS/password state not observed; safe reproduction is a protocol double, not authentication qualification. Evidence/probe inventory lives in investigation notes; none is a behavior-defining supplement. No material unresolved feasibility assumption remains for this feedback-only delta.

## Decisions (Solution Designer, all Decided within direction)
- DEC-001: Root installation/admission happens after sudo, so no trusted observation exists at the instant a password is entered. Use established administrative session as confirmation; until then say waiting for approval/helper, and retain OS diagnostics rather than infer a cause.
- DEC-002: Inspection only reads saved metadata and may return configured/pending. Ready means dashboard setup controls can proceed, never NFS health, absence of a share or completed setup. Say this explicitly.
- DEC-003: Initial phase plus one sustained-wait reminder is clearer than silence without a noisy spinner or deadline. Exact interval is a technical design detail; no timer can grant success or change execution.
- DEC-004: Classify by observed phase; ambiguous pre-confirmation termination remains ambiguous. Refer to existing terminal/browser diagnostics with safe retry after completion instead of copying private/raw details into new logs.

## Traceability And Architecture Phase Input
REQ/AC rows and scenario table are the traceability map; all UC-001–003 covered, no orphan requirement. Approved SCN-001–007 map to the actual command→browser authorization→OS helper→configuration→terminal lifecycle. Architecture must verify emission points, ownership, synchronized output/Stop ordering and per-attempt timer cleanup; choose minimum private presentation mechanism with unchanged administrative/protocol contracts. No new auth mechanism prescribed. Known risk is misleading timing/claims, not a proven NFS runtime defect.

## Readiness Check
Current evidence/desired-preserved outcomes/scope/traceability/scenarios/decisions/constraints: Yes. Applicable Product supplement: N/A. Content ready: Yes; blocker: None. Exact R1/SR-001 approval recorded above and user informed; ready for architecture design: Yes.
