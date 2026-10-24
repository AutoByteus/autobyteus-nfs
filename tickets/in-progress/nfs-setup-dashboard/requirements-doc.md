# Requirements — Standalone NFS setup dashboard

## Document status and authority
- Package: `nfs-setup-dashboard`; Task `autobyteus-nfs-2` / `project_task_f1264eb8-5a99-4a19-949f-09d141c955a1`.
- Requested by: `/project_task_manager`, run `project_task_manager_a5f6d9d306e54970bafdad895bdf731d`.
- Owner: Solution Designer. Date: 2026-10-24. Baseline **R1 / SR-001, Approved**.
- Approval: Solution Designer within the user's direction; user informed in this conversation on 2026-10-24 (“The plan is to keep everything in the NFS executable … administrator passwords out of the browser … exact setup plan … Closing the page won’t disconnect storage … no release”). User's explicit selected commands and dispatch in PM message are original authority. No unresolved Needs user decision.
- Behavior-defining supplements: None. This document is the complete approval basis. No Product Team/design package was requested or invented.
- Reading gate: solution-designer SKILL, requirements-engineering, finding-the-cause, ticket-scope, requirements/investigation/revision templates; current repository AGENTS, DESIGN, TESTING, RELEASE (2026-10-24). Evidence: `investigation-notes.md`.

## Problem and desired outcome
Current NFS is a standalone Go CLI. It has safe host setup operations but no `server`/`client` dashboard launch. A person should run one command on each participating computer, then use a local UI to share or connect, inspect status, reconnect and safely disconnect. Installation of the program remains a prerequisite; this source-only task does not update published v0.1.0 assets.

Actors: ordinary local operator with administrator approval available; another trusted computer's operator receiving connection details; maintainer validating isolated resources. No AutoByteus application or remote management actor.

## Relevant current and desired behavior
| ID | Kind / scenarios | Current evidence | Desired | Preserved |
|---|---|---|---|---|
| BEH-001 | User / SCN-001 | E02: parser rejects server/client; noargs offers terminal create/connect | Exact role commands open a local dashboard from one program | Existing public CLI commands remain supported headless/terminal entry forms |
| BEH-002 | User / SCN-002 | E03–05: chosen source/backend/private network, exact plan, admin consent, host self-mount | Server form, folder selection, review/consent and share details | One share per installation, in-place data, source identity, permissions, explicit network trust and self-mount |
| BEH-003 | User / SCN-003 | E03–05: bounded Connection JSON and mount path | Client pastes server's details, selects mount location, reviews/connects | No discovery, shell evaluation, inferred UUID or trust bypass |
| BEH-004 | Operational / SCN-004–006 | E06–08: status can stall; explicit reconnect/pending resume; drained detach | Clear configured/checking/ready/incomplete/error states and deliberate recovery/disconnect | Pending evidence, nonroot probe, no force-unmount/fake readiness/data deletion |
| BEH-005 | Contract / SCN-007–008 | E03/E09: root binary, private records and administrative lock | Authenticated local management with explicit OS privilege approval and operation consent | No root HTTP exposure, password collection in browser, arbitrary host command/file interface or unattended storage changes |
| BEH-006 | System / SCN-009 | E10: installed storage job independent of terminal/application | UI lifetime distinct from storage; orderly stop/relaunch | Closing page/UI never silently detaches, restarts or deletes storage; no guaranteed hard-NFS cancellation |
| BEH-007 | Contract / SCN-010 | E01/E11: published v0.1.0, current development metadata, deferred field tests | Independently buildable embedded dashboard, truthful docs/test evidence | Same platform/backend contracts, release provenance and independent field-test custody |

## Scope Guardrail
| Use case | Authorized scope | Scenarios |
|---|---|---|
| UC-001 | Launch/stop role dashboard | 001,009 |
| UC-002 | Share a selected source and transfer connection details | 002,007,008 |
| UC-003 | Connect a host to that share | 003,007,008 |
| UC-004 | Inspect status, reconnect/resume and safely disconnect | 004–008 |
| UC-005 | Preserve terminal/supervisor behavior, independently build/check/document UI | 010 |

Out of scope: AutoByteus app, its Guide, workspace/agent skills, nodes/descriptors/launcher integration, automatic discovery, protocol replacement, new OS/backend support, public/LAN management, automatic upgrades, multiple shares, filesystem redesign, field campaign autobyteus-nfs-4, new release/tag/signing/publication/deployment, and live-user mounts/data/config. No privileged action on this operator's production computer as a test.
Non-goals: physical/platform-wide qualification, a desktop-app wrapper, native OS file-dialog parity, unattended UI automation as a public API, multiuser collaboration, guaranteed outage cancellation, editing an active share's identity/network in place.
Preserved boundary: BEH-002–007. The browser selects and confirms existing host operations; it does not grant unrestricted administrative authority. Existing old active/pending node obligations continue to refuse, not migrate.
Prerequisites: None currently identified. Go is absent from the investigator's PATH; provisioning an owned test toolchain is task preparation, not a separate product dependency. Actual isolated host resources remain a validation obligation, not presumed available/proven.
Review authority: blockers must cite an approved REQ/AC/BEH. New behavior/threat model/migration/platform promises are Requirement Gaps, not automatic corrections. Reviewer proposals do not amend R1.

## Requirements
| ID | Requirement | Behavior / priority | Rationale and source |
|---|---|---|---|
| REQ-001 | `autobyteus-nfs server` and `autobyteus-nfs client` start the respective UI as the ordinary local user, attempt browser opening, and provide a usable local fallback. No separate install/start of UI or backend; no storage change merely from opening. Root-start/no-terminal/unsupported-host failures explain the next action without silently elevating a browser. | 001,005,006 / Critical | Explicit user syntax; DEC-001/002 |
| REQ-002 | Server offers existing or a single new source folder, explicit private IPv4 endpoint and trusted hosts/subnet, default native backend plus existing Linux Docker option, and local mount location. Show validated exact source/network/permission/service/package effects and limitations before applying. On success show actual path and copyable Connection JSON for another computer. | 002 / Critical | Existing create contract, E04–05 |
| REQ-003 | Client accepts the server's bounded Connection JSON, displays endpoint/export/protocol/identity, permits local mount path override, and requires exact-plan consent before connecting. Invalid/missing details or unsafe/occupied targets produce actionable refusal and no fallback mount. | 003 / Critical | Existing connection/target contracts |
| REQ-004 | Both roles expose configuration status separately from a freshly requested readiness check. Existing configuration is not overwritten by first-use forms. Wrong-role launch explains the matching command; pending setup offers review/resume of the same intent, not new setup. Reconnect is explicit. | 004 / Critical | One-installation/current/pending lifecycle |
| REQ-005 | Disconnect identifies the affected mount/export, requires affirmative drain acknowledgment and confirmation, and uses existing safe detach. Busy/mismatched/partial failures remain visible; source, marker and recovery evidence are preserved. Server warns all remote users must stop using the export; UI cannot discover or prove their drain. | 004,005 / Critical | Existing detach contract |
| REQ-006 | Management is local to the initiating user, with per-launch authorization, strict browser-origin/request checks and bounded typed operations. No remotely exposed management, browser password, generic command/file execution, arbitrary config path, or browser-supplied user identity/plan authority. OS approval and exact operation consent are separate. | 005 / Critical | Explicit task security boundary; DEC-002 |
| REQ-007 | At most one administrative operation can act at a time. Repeated clicks/late responses do not duplicate effects. Plan review has a visible bounded lifetime; expired/cancelled plans cannot apply. UI remains responsive while an operation/check waits, distinguishes running from unknown/failed and does not claim cancellation succeeded when host work can still run. Closing browser/management does not detach storage. | 004–006 / Critical | Existing administrative lock and hard-NFS limitation |
| REQ-008 | Existing create/connect/status/reconnect/detach/version, noninteractive consent, installed service behavior, metadata and source/mount/permission/refusal contracts retain their meaning through shared operation policy. No migration, new persistent ready flag or application coupling. | 002–007 / Critical | Current supported consumers/entry forms |
| REQ-009 | Accessible labelled forms, review/status panels, keyboard/focus/error handling and a readable narrow layout; English consistent with current CLI. Folder chooser operates with ordinary-user permissions, exposes directories only and never uploads file contents. Fields permit explicit paths when browsing is unavailable. Copy failure leaves selectable text. | 001–005 / Important | DEC-003/004, local browser ergonomics |
| REQ-010 | Embed UI in independently built Go program; document launch/auth/lifetime/recovery and current version availability. Verify browser/IPC/admin refusals plus relevant isolated real host interactions; clearly separate fakes, native execution, mounted checks and deferred field qualification. Source finalization only, no public release. | 007 / Critical | Task Done, TESTING/RELEASE |

## Acceptance criteria
| ID | REQs / scenarios | Observable expected outcome and failure control | Verification intent |
|---|---|---|---|
| AC-001 | 001,009,010 / 001,009 | Both exact commands open correct UI from built executable without external web assets; fallback works; unauthorized/root/unsupported launch cannot administer. Launch/close alone changes no storage. | Built-binary launch/browser, opener failure, no-root-effects controls |
| AC-002 | 002,006,009 / 002,007 | Server chosen source/native platform and existing Linux Docker option feed the real planner; precise review and consent; resulting connection details match saved host state. Invalid source/network/privilege refusal causes no setup effects. | Forms + real planner + owned guest setup and file/identity proof, each backend separately |
| AC-003 | 003,006,009 / 003,007 | Pasted details/local override produce exact intended mount; malformed/wrong-source/occupied/nonempty targets refuse. Copy/paste round trip preserves Connection values. | Browser-to-controller plus owned client mount; real config validators and negative cases |
| AC-004 | 004,007,008 / 004,005,008 | Empty/configured/wrong-role/pending states honest. Recheck and reconnect use current state; pending resume needs fresh consent and retains identity. Stalled operation UI remains usable with no duplicate work or false readiness. | Production controller with controlled failures plus native guest lifecycle; explicit timing/status evidence |
| AC-005 | 005,007 / 006,008 | Drain acknowledgment required; busy/unrelated unmount refuses; retry of supported partial detach preserves data and evidence. Browser/UI exit is not detach. | Controller + underlying safety regressions and owned guest drain/detach |
| AC-006 | 006,007 / 007,008 | Requests without session authorization, cross-origin/foreign Host, malformed/oversized bodies, forged plan/user/path authority and expired/replayed plans cannot cause effects; password remains in terminal/OS channel. Lock and auth-denial controls pass. | Real HTTP/browser/pipe boundaries plus isolated sudo/privileged process tests, not mocks alone |
| AC-007 | 007,009 / 001,004,008,009 | Keyboard/labels/error focus/manual-copy; desktop/narrow responsive flow; idle review expiration and cancel release administrative lock; in-flight close/error keeps truthful incomplete state until reconciled. | Real browser, delayed-operation controls, OS process/lock checks |
| AC-008 | 008,010 / 010 | Current CLI/supervisor/current stored records retain behavior; no app/node references revived; no public assets or data changed. Repository checks and documentation/finalization/owned cleanup complete, with exact limitations. | Go race/vet/build, Python/Bash packaging, current-state fixtures, integration evidence and delivery receipt |

## Relevant scenarios and journeys
All ordinary journeys below are **Supported Normal Scenario** from the approved user direction or preserved CLI contract. Edges are explicitly identified; none is created solely by a callable method.
| SCN | Kind / actor, goal and trigger | Starting condition → product steps → expected outcome | Alternate/error and independent basis | Links |
|---|---|---|---|---|
| 001 | User launches selected role command | Installed program/local desktop → launch → local page → setup/status | Browser missing: local URL/manual open; unsupported OS/root: useful refusal. User command decision/E02 | 001,009 / AC001,007 |
| 002 | User shares project on server | Unconfigured host → choose folder/network/backend → OS approval → exact review → confirm → share details | Source/port/allowlist/permissions/consent refusal; same supported create journey E04–05 | 002,006 / AC002 |
| 003 | User connects other computer | Receives JSON → launch client → paste/choose target → review/approve → ordinary mount directory | Malformed JSON, unreachable service, wrong/occupied target remain errors; E03–05 | 003,006 / AC003 |
| 004 | Operator checks or reconnects | Configured host → open matching role → request check/reconnect → factual result/path | Wrong-role guide; unavailable storage remains checking/error, not READY. E06 | 004,007 / AC004 |
| 005 | Operator resumes interrupted setup | Pending intent after real interrupted setup → reopen matching role → inspect/review same source → consent/resume | Bound source mismatch refuses; no repair/reselection. **Supported Explicit Edge Scenario**, pending recovery contract E07 | 004,008 / AC004 |
| 006 | Operator stops sharing/connection | Active or supported partial state → stop users → acknowledge drain/review → disconnect | Busy/mismatched mount refuses; partial evidence/data retained. E08 | 005 / AC005 |
| 007 | Browser/OS authorization contract | Untrusted website or unauthorized local request reaches management, or operator denies sudo → refusal before host operation | **Supported Explicit Edge Scenario**, explicit task local-management security; no threat claim against compromised OS/root/browser extensions/same-user malicious code | 006 / AC006 |
| 008 | Operation safety contract | Ordinary repeated click, review abandoned, CLI/supervisor lock busy, interrupted UI connection → one operation or clear refusal; reconcile actual state | **Supported Explicit Edge Scenario**, task safety plus existing lock/pending contract. No invented distributed admin collaboration feature | 005–007 / AC004–007 |
| 009 | Operator ends/reopens management | Close tab or stop terminal UI → storage stays independently managed → later relaunch/status | In-flight work may continue/wait; cannot promise hard cancellation. E10 | 001,007 / AC001,007 |
| 010 | Maintainer/operator uses existing program | Build in standalone checkout / use existing CLI and saved records → unchanged contracts plus embedded UI | No public release or qualification inference. E01/E11 | 008,010 / AC008 |

## Experience and decisions
Product repository/spec/runnable visual reference/final screenshot approval: N/A — no separate Product request. Required interaction is here, not an implied approved mockup.
Initial screen: role/title, local-only and field-validation notice, one setup form or factual existing-state panel. Server uses labelled source chooser + path field, private network details and advanced backend/mount options. Client uses connection JSON + mount location. Then administrative authorization, exact review, operation progress, and result/status. Keep OS authentication instruction visible while terminal approval waits. Status includes time of last completed check, not a permanent green badge. Disconnect is distinct from “Stop dashboard”. Focus and screen-reader announcements follow validation and completion; long JSON/errors wrap or scroll without page-wide overflow at 390px. No file-content explorer.

| DEC | Question / evidence and reasoning | Decision / owner / state |
|---|---|---|
| 001 | Separate application or embedded UI? One-executable request, no existing web framework, Go standalone distribution. Browser with bundled assets minimizes installation. | Local browser UI, automatic attempt + manual fallback; foreground terminal owns management lifetime. Solution Designer / Decided |
| 002 | Administrator approval? Existing CLI already uses sudo and root-owned installation. Browser passwords or silent permanent admin service add unnecessary authority. | Start ordinary-user UI; explicit authorize action requests OS sudo approval in launching terminal; show exact plan separately before changes. No new credential policy or password capture. Solution Designer / Decided within delegated privilege-handling direction |
| 003 | Connection discovery/details? Current Connection UUID/protocol/export validators cannot safely infer identity from only an IP. | Copy/paste existing JSON with readable summary and local path override; no discovery. Solution Designer / Decided |
| 004 | Folder selection? Browser handles expose names, not a usable native absolute source contract; arbitrary file upload is wrong operation. | In-page directory-only local chooser at ordinary-user permissions plus path entry; real setup safety still authoritative. No native dialog requirement. Solution Designer / Decided |
| 005 | Multiple roles/backends/lifetime? Current store represents one attachment, server also self-mounts, Docker Linux is already supported. | Preserve one configuration; default native, Linux Docker advanced; opposite-role launch cannot replace it. Closing management leaves installed storage running. Solution Designer / Decided |
| 006 | Release and proof? Source changes cannot retrofit published v0.1.0; physical campaign is separate. | Docs distinguish source-built dashboard from old release; owned isolated host evidence required for new interaction, field task remains separate. Solution Designer / Decided |

## Quality, data and external contracts
- QR001→REQ006/AC006: remote and unauthorized/cross-origin requests produce no administrative effects; private keys/passwords never enter HTTP, logs or persisted dashboard data.
- QR002→REQ007/AC004,007: one outstanding host operation; process/HTTP UI state queries do not await filesystem check; visible review expiry, no guessed timeout success.
- QR003→REQ009/AC007: keyboard and accessible status/error labels; verified 1280px and 390px layout. No new localization system.
- QR004→REQ010/AC008: embedded assets included in existing source identity; no runtime Node/toolchain/CDN requirement.
- Persisted data affected through existing supported operations, but **no record/schema migration intended**. Preserve attachment, hosted identity, source data/marker and root-private pending/recovery files; ordinary operations only. Losing unsubmitted forms/session tokens on management exit is acceptable, not losing committed intent or user data. No storage contents copied into browser or ticket evidence.
- External contracts: supported macOS26+/Ubuntu24.04 hosts, native Apple/Ganesha and existing Linux Docker, private IPv4/AUTH_SYS; OS administrator authorization; current browser localhost behavior. Evidence E01–11. Native privilege/host/browser integration must be verified downstream rather than asserted from docs.
- Assumptions: a local browser and interactive launching terminal available; failure must explain manual open or terminal requirement. Real isolated guests/test toolchain availability is unproven, owned by implementation/API preparation. Block and report missing resources rather than weaken ACs or use live state.
- Supplements: None beyond own evidence/handoff docs. No open material user decision or product prerequisite.

## Traceability / architecture input / readiness
REQ001→UC001/BEH001/SCN001,009/AC001; REQ002→UC002/BEH002/SCN002/AC002; REQ003→UC003/BEH003/SCN003/AC003; REQ004→UC004/BEH004/SCN004–005/AC004; REQ005→UC004/BEH004–005/SCN006/AC005; REQ006→UC001–004/BEH005/SCN007/AC006; REQ007→UC001,004/BEH004–006/SCN008–009/AC004–007; REQ008→UC005/BEH002–007/SCN010/AC008; REQ009→UC001–004/BEH001–005/SCN001–004/AC001–003,007; REQ010→UC005/BEH007/SCN010/AC008.
Architecture must map all these entry forms and preserve the current setup boundary. Investigate IPC/OS authentication, exact-plan lifetime/lock, current records, browser authorization/asset inclusion and installed helper identity. Mechanisms belong in design, not unapproved requirements.
Readiness: evidence/current and desired/preserved behavior, scope, linked measurable ACs/scenarios, decisions and data continuity **Yes**. Product visual approval **N/A**. R1 approval recorded/user informed **Yes**. Approved basis ready for design **Yes**. No remaining content blocker; executable proof remains downstream work.
