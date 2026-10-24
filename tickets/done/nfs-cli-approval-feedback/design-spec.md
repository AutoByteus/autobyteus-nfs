# Design — NFS terminal approval feedback

## Solution And Approval Basis
**Ready / SR-002**, approved requirements **R1/SR-001**, Solution Designer within direction; approval message and exact scope in `requirements-doc.md`. Package `nfs-cli-approval-feedback` / `autobyteus-nfs-7`. Canonical investigation: `/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/nfs-cli-approval-feedback/tickets/in-progress/nfs-cli-approval-feedback/investigation-notes.md`. No behavior-defining supplements or Product design.

Authorities read 2026-10-24: solution-designer architecture-design.md, full design-principles.md, design-spec-template.md; current NFS root AGENTS/DESIGN/TESTING/RELEASE. No closer design authority, project glossary or principle conflict found. Design-examples not needed for this local change. Workspace/base/target are investigation bootstrap; no canonical checkout authoring.

## Current-State Read / Architecture Investigation Evidence
E02–E04 trace the complete actual OS/admin path; E05 reproduces the missing feedback with controlled ordinary-user pipes; E06–E07 establish the existing owner, call sites, lifecycle and browser consumer. Paths/lines are in the canonical investigation table. `Session.perform` owns explicit authorization and initial inspection; `authorize` validates hello; admin owns root admission and metadata inspection. Browser already listens before either. Successful and failed outcomes update browser operation state without terminal output. Child start is not confirmed access, and metadata success is not mounted storage health. Root/control source paths are unchanged from published source448cef83 to base456e5808 (read-only Git diff), not assumed from version naming.

## Intended Change
Project the existing authorization/initial-inspection lifecycle into concise terminal text, plus a bounded waiting reminder. Keep the operation sequence, OS authority, private wire/HTTP schemas and storage effects unchanged. Do not add root progress messages or parse sudo output.

## Relevant Behavior And Production-Path Map
| Behavior | Requirements / acceptance | Supported trigger | Existing evidence | Target path / preserved outcome |
|---|---|---|---|---|
| BEH-001 | REQ-001/002; AC-001 | SCN-001/002 role launch and explicit browser Authorize | E02–E05 | DS-001 + DS-002: confirmed handshake → preparing → successful inspect → browser next action; no claim of password entry or storage readiness |
| BEH-002 | REQ-003/004; AC-002–004 | SCN-003/004/005 pending/refused/failed operation | E03–E06 | DS-002/003: phase-driven waiting, safe categorical failure, no timer authority or automated retry |
| BEH-003 | REQ-005; AC-005/006 | SCN-006/007 Stop, duplicate request, explicit reauthorization | E06/E07 | DS-004 and existing submit admission: stop feedback without cancelling helper/storage; preserve privacy and dedup |

## Task Design Health Assessment
- Posture: focused usability/bug fix. Root cause **Local Implementation Defect** (missing terminal projection), not proven authentication or storage fault.
- Current structural design issue: No; Session is already the right attempt owner. Refactor needed now: **No broad refactor**. One small terminal-presentation file keeps timer/text/serialization out of transport and root policy.
- Triggers: capability-area reuse (extend dashboard presentation, not root/admin), several forms (server/client share owner and tests), example clarity (ready vs storage-ready). No schema, mixed-authority, duplicate coordination or oversized file trigger. Source sizes and calls in E06.
- Failure/status text must not become another operation state machine granting authority. Reporter is a disposable view of actual events; persisted/browser state remains authoritative where already owned.
- No deferred refactor or new follow-up identified. OS/password and field qualification limits remain explicit; they are not a new feature or prerequisite.

## Terminology
**Administrator access confirmed:** admitted same-binary, same-role private helper hello was successfully validated, not “password accepted.” **Setup controls ready / Dashboard ready:** initial metadata inspection completed successfully while the helper remains available; browser is ready for user decisions, not proof of storage health. **Waiting:** the current attempt has no completed result. **Stopped:** no new management admission; not disconnected storage. No project glossary found; no new wire/storage term.

## Data-Flow Spine Inventory, Primary Spines And Narratives
| ID / scope | Arrow chain (actual order; owners named) | End and reason |
|---|---|---|
| DS-001 Primary, both roles | Operator role command → cli host/TTY adapter → dashboard.Session loopback/private browser lifetime → browser explicit Authorize → Session.submit admitted serial operation → Session.perform → privilege.authorize fixed launcher → OS sudo → cli.InstallRoot/installed helper admission → admin.Session.ServePipe hello → parent validation | Validated helper permits metadata inspection, not storage mutation. Existing sequence stays intact; Session is governing management owner |
| DS-002 Return/event | Validated authorize return → Session records helper and emits confirmed/preparing → helper.call inspect → admin.InspectConfiguration under lock → correlated Reply → Session completes operation → terminal result and existing browser polling | Meaningful outcome is setup-control availability or explicit failure. Reporter observes only; browser schema/UI remains unchanged |
| DS-003 Bounded local | Session phase observation → terminalFeedback fixed text + one 10s timer → matching still-pending phase reminder OR next observed phase invalidates timer → completion/stop disables reminders | Presentation-only waiting, no control timeout/retry. One reporter owned by Session; no global event bus |
| DS-004 Primary shutdown | User Ctrl+C/HTTP Stop → Session.Stop admission boundary + feedback stop → Run existing shutdown message → HTTP shutdown → worker/helper drain → bootstrap/capability cleanup → opener lifetime completion | Preserve safe shutdown semantics and prohibit stale ready/continue messages. Existing root/service lifetime is not transferred |

### Spine Actors, Ownership Map And Thin Entry Facades
CLI owns ordinary-user/TTY/host and fixed launcher construction (E02), not browser state or log interpretation. Session owns operation sequence/result and closing. Private helper transport owns correlation/identity validation and safe process lifetime (E04), not readiness copy. Admin remains sole root operation owner, unchanged (E03/E04). New private `terminalFeedback` owns only text, synchronized writes and reminder lifetime. `Run` is the existing dashboard process lifetime entry, not a second authorization owner. HTTP and CLI cannot bypass Session admission or call root mechanisms through the reporter.

## Phase Projection And Concrete Message Examples
Exact prose may be polished while preserving these facts. No raw error interpolation, URL repetition, configuration/path data or password observation is needed.

| Observation | Required terminal projection / next action | Must not imply |
|---|---|---|
| Explicit admitted authorize begins, before helper launch | “Waiting for administrator approval and setup helper. Complete any approval prompt only in this terminal.” | Password is necessarily requested; browser is not already running |
| 10s in pre-confirmation phase, still pending | One reminder: “Still waiting for administrator approval or helper startup. Check this terminal for an approval prompt or diagnostic; do not start a second attempt.” | Elapsed time means denied/success/stalled; exact root subphase is known |
| `authorize` returns validated helper | “Administrator access confirmed.” then “Preparing setup controls—reading saved configuration…” | Password was entered, storage ready |
| 10s in initial inspection, still pending | One reminder: “Still reading saved configuration. Keep this terminal open; do not start another attempt.” | A timeout or permission to repair/restart |
| Initial inspect reply is correlated, no transport/reply error, helper available, not closing | “Dashboard ready—continue in your browser. Keep this terminal open. If needed, use the private URL above.” Then “Setup controls are ready; this has not created a share, connected storage or checked storage readiness.” | Existing configuration absent, wrong-role configuration usable for mutation, continuous health |
| Local command/plumbing start failure | “Could not start the administrator helper. Reopen this command as an ordinary user in an interactive terminal and authorize again; review the terminal diagnostic.” | Wrong password or a storage failure |
| Unconfirmed helper ends / invalid hello | “Administrator access was not confirmed. Approval may have been denied/cancelled or the helper failed to start. Review the terminal diagnostic, then reopen and authorize again.” Identity mismatch may instead use a fixed “helper identity could not be confirmed; close and reopen the installed tool” category | Diagnosis from a generic exit code or child PID; successful access |
| Confirmed helper inspect transport failure | “Setup controls could not be initialized. Waiting for the helper to finish safely; do not retry yet.” if cleanup is still required; after existing cleanup/result completion: “Setup controls unavailable. Reopen the dashboard and inspect configuration before deciding how to retry.” | Revoke historical confirmed event; automatic rollback/reconnect |
| Inspect returns refusal while helper remains available | “Administrator access is confirmed, but saved configuration could not be read. Review the dashboard error and use Inspect configuration before retrying setup.” No ready message | Root unavailable or exact private cause logged |
| Stop during any phase | Existing stopping/waiting/“Storage is NOT disconnected” text; no later confirmation/preparing/ready/reminder invitation | Cancellation of already admitted work, detach or killed helper |

The root may fail or take time between actual sudo approval and hello. Keep that interval honestly named approval/helper startup; **do not** add `sudo -v`, parse Password/child stderr, change the protocol, or bypass root admission to claim earlier confirmation. Empty, configured, pending and opposite-role saved state all use the same neutral readiness sentence; existing browser controls remain the authority for the next allowed action.

## Bounded Local Presentation Lifetime
Implement a private Session-owned `terminalFeedback` in `internal/dashboard/terminal.go`, initialized with discard output for tests/construction and assigned Run's writer before serving. It replaces `s.log` as the terminal sink. It may implement a synchronized writer/line methods, but must not retain private fallback strings or expose browser/root APIs.

- Session is the only authority that advances attempt phases. Start exactly once after submit's existing admission/dedup; reauthorization after expiry starts a new attempt. All operation completion/Stop notification ordering is linearized with the **existing Session mutex**, then the reporter mutex; never the reverse. Reporter never calls Session, helpers or admin.
- Per-attempt/phase generation, phase and one timer are sufficient private presentation state; no second stored readiness/authorization result. At10s, a callback emits one fixed phase-specific reminder only if the generation is still current and active. No tick loop or task-owned worker pool. Phase transition invalidates/stops the timer; no restart within that phase. Timer callbacks never make host calls, alter operation state or wait for helper completion.
- Stop invalidates all pending reminders under the same ordering and suppresses later lifecycle invitations. In-flight callbacks can finish before Stop returns; none can emit stale progress afterward. Do not wait for a callback while holding a mutex it needs. Drain already waits operation workers; the feedback mechanism adds no process to drain and must not force a child to stop.
- Preserve Run's one intended private URL fallback, opener diagnostics and stopping/opener-drain text. Serialize ordinary-user output through the same sink to prevent line interleaving; suppress late opener “continue/use URL” guidance after Stop. Do not redirect/inspect sudo's stderr or TTY input. That OS channel remains separate and unmodified.
- Writer failures must not grant success, retry work or interrupt storage cleanup. No new durable log sink. Tests can inject a private timer scheduling seam or invoke callback deterministically; no public timeout flag/environment configuration is needed.

## Ownership Boundaries, Dependency Rules And Interfaces
| Boundary | Encapsulated subject / explicit identities | Callers and constraints |
|---|---|---|
| `Session.submit/perform/Stop` | Existing request ID/fingerprint/role and operation/closing state | HTTP/Run; existing admission, state schema and operation sequencing unchanged |
| `authorize(launch, role)` | Fixed process launch and validated helper | Session sole production caller; remove obsolete logging argument/PID-only text, retain original pipe/digest checks and cleanup. Tests update call signature |
| private authorization error category | Local-start vs unconfirmed/identity result at known return sites | Transport returns private typed/wrapped category (underlying error preserved), Session projects fixed safe text. Never classify by fragile string/exit-code/password inference; no protocol/API schema extension |
| `terminalFeedback` | Presentation of current attempt/phase and owned output/timer | Session/Run only; explicit narrow lifecycle methods. No call back into operations, private state, root install or browser response |

Interface check: each subject is singular; request/role/attempt identities are explicit. No ambiguous selectors, exported new API, facade-only layer, admin→dashboard dependency or mixed-level root bypass. Existing `adminwire` and HTTP consumers unchanged. A notification callback is acceptable only for presentation; it must not perform the next administrative step.

## Off-Spine Concerns / Capability Reuse / Structures
Terminal text, one-shot reminder and line serialization extend **dashboard** presentation serving Session (DS-002/003/004). They are not an administrative progress service. Reuse existing observed helper/result/closing events; do not duplicate authentication, configuration parsing or storage checks. No shared/common module. Private typed start failure is a reporting category, not a competing authorization fact. No new persisted/shared DTO or derived browser consumer; data tightness: one phase/generation/timer, no duplicated ready bit. Domain names mean the same thing in messages, tests and docs.

## Final File Responsibility And Target Mapping
Draft mapping converges directly to the following small local mapping; no extra subsystem/module folder needed.
| Change / path | Concrete owner and responsibility | Must not contain |
|---|---|---|
| Add `internal/dashboard/terminal.go` | Private terminalFeedback: fixed phrases, synchronized sink, bounded generation-checked reminder | Root actions, stdin/password parsing, tokens in phase state, general event bus |
| Modify `internal/dashboard/session.go` | Observe start/confirmed/inspect-result/cleanup/Stop in existing operation owner; own reporter | New admission/operation state, storage probes, retry/cancel policy |
| Modify `internal/dashboard/privilege.go` | Remove PID-only log parameter/call; safe private error category at known boundaries; keep validation/wait semantics | New hello fields, `sudo -v`, retry, timeout/kill, raw diagnostic output |
| Modify `internal/dashboard/browser.go` | Route existing parent messages through sink, configure it before Serve, preserve fallback/shutdown | Public listener change, auto-authorization, new opener strategy |
| Add `internal/dashboard/terminal_test.go` / focused `session` feedback tests; modify `privilege_test.go` and affected test-only fixtures | Current phase order/negative/race/cleanup contracts and signature adaptation | Test-only product bypasses or inherited green verdict claims |
| Modify `docs/dashboard.md`, targeted TESTING.md guidance if needed | Source terminal lifecycle, wait/next action, limitations and reproducible tests | Claim v0.2.0 already contains this improvement or release promise |

Folder boundary: existing dashboard is ordinary-user presentation/control; a flat additional terminal file is clearer than new layers. Keep every growing source/test file under500 lines or split by concrete concern. No changes to cli launcher/install, admin/adminwire/config/setup/service/platform/backend/docker, browser JS/CSS/HTTP contracts, packaging/locks/workflows, application/superrepo or skills. If investigation proves those are required, return Design Impact before expanding.

## Legacy Removal Policy / Removal Plan / Compatibility Rejection
Remove the current misleading PID-only presentation at privilege.go:48 and now-unused `log` parameter/fmt import, replacing it with explicit Session-owned waiting/result messages. Update its sole production and test call sites (E06); no compatibility wrapper/old-message fallback. Replace obsolete raw `Session.log` field with owned terminal sink and adjust tests/probe capture. Keep all existing helper acquire/call/read/close methods: they are live. No dead code found by scoped call trace; Implementation confirms unused imports/call sites through compiler/search. No other removal or historical flow retention justified.

## Persisted Data / Migration / Derived Layering
**Not Affected**: changed state is in-memory terminal presentation only. No root metadata reader/writer/schema/path, saved plan, binary identity rule or migration admission changes. No migration/reset/history scan. Existing admin locked metadata inspection is preserved, including nonempty/pending/role semantics. Derived layering: ordinary-user presentation depends on its existing private transport; admin authority is unchanged. No additional layer or schema necessary.

## Change Sequence And Guidance For Implementation
1. Start from E05 baseline red; turn it into durable assertions on phase order, final outcome and fixed safe text. Adapt the internal output capture deliberately if the private sink changes; do not simply weaken the assertion or promote the fixture to root proof.
2. Add the narrow terminal presenter and connect Session observed phases/Stop plus Run output; remove obsolete PID logger/signature. Keep source validation/operation paths byte/semantically unchanged except specified error categorization.
3. Cover table cases and drain race. Use literal error categories; raw helpers/errors/configs must not flow into new lines. Keep output tests independent of source spelling except public message meaning.
4. Run current affected/full checks, realistic PTY flow and docs; record failures/limits and cleanup. No user-host sudo, mounts or installer invocation. Hand to API/E2E on the configured route after own checks.
5. Delivery later integrates fresh origin/main, verifies evidence and finalizes source/docs; NO RELEASE. User's installed v0.2.0 remains unchanged by this task.

## Verification Guidance (REQ/AC mapped above)
Required: current Go race tests (including actual private subprocess pipes, local HTTP admission/dedup), vet/build/version; applicable Python packaging/embedding/source-hash regressions and repository guards. Focus new tests on both roles, delayed hello, cached-like immediate hello (not OS cache proof), invalid identity/version, local start error, EOF, inspection refusal/transport loss, empty/configured/pending, duplicate request, explicit reauthorization and Stop-before-result. Show one real long-wait10s observation, use deterministic clock controls for the remaining timing branches. Assert no stale reminder after transition/stop, no success before correlated inspect, no goroutine/timer/helper leaks and no readiness after helper is already known dead.

API should drive a **real PTY and current Session/local HTTP** using an isolated protocol child for successful, held and failed authorization plus Ctrl+C/Stop. Preserve real terminal ordering, do not mock the feedback owner. Redact/avoid initial private URL in durable transcripts; never use real password/token canaries in logs. Controlled dummy prompt/child is explicitly not sudo/password verification. Since sudo/root contracts remain untouched, this ticket does **not** mandate a new VM/storage/field campaign. If a cheap already-owned disposable native guest is used to test actual sudo, keep it bootstrap/inspection-only with test identities and report NOPASSWD versus real prompt distinctly. Never modify operator sudo cache/policy or record password entry. If implementation requires a changed privileged contract, return for design/risk reassessment instead of treating doubles as sufficient proof.

Browser visual/layout changes are N/A; preserve a focused actual local-page authorize/status/Stop journey, not an unrelated full dashboard redesign. Existing broader native/storage evidence is historical scope only. Field task nfs-4 stays separate. Failed/blocked/untested cases stay truthful; no mandatory repeat user test or publication added.

## Key Tradeoffs And Risks
- Validated hello is later than password acceptance but trustworthy; explicit waiting covers that interval without new privileged protocol. Exact OS failure diagnosis remains unknown when only EOF is observed.
- A one-shot10s reminder bounds noise and has no authority; output-only timer/Stop ordering needs race tests. No timeout may interrupt hard-NFS/drain.
- Confirmed access followed by inspection refusal must not collapse into ready or wrong-password copy. Phase distinguishes these without scraping private diagnostics.
- Logging performs ordinary terminal I/O as today; no asynchronous durable queue or output-based recovery is introduced. No universal nonblocking-output SLA.

## Change Scope
UC-001–003 only; files above, focused tests/docs. Derived browser/persistence contracts N/A (unchanged). Nearby root/auth/storage/installer/visual/field work deliberately left alone because the observed events already carry the needed facts. Follow-ups **None**; no new external blocker. Remaining uncertainties are validation boundaries, not unmade product choices.

## Task Size And Architectural Risk (completed after design)
**task_size = Small; architectural_risk = Low.** Narrow local terminal feedback in one existing capability: three existing production files plus one private presentation file, focused tests and two docs. Content volume is not a release/architecture campaign. No public/wire contract, root/security authority, persistence, storage operation, deployment, process cancellation or ownership-boundary change. The small timer/sink is output-only; operation concurrency and Stop/drain authority remain unchanged. Actual error/hello/inspect facts were traced and safely reproduced; no material unknown premise blocks this delta.

Escalate if the fix needs new root/helper protocol, OS auth sequencing, process/lock cancellation, HTTP/schema changes, storage effects or live-user access. Do not silently broaden Low-risk work. Outcome **Architecture Design Complete**; configured handoff rules choose the next recipient, not this spec. No independent review or implementation verdict is invented.
