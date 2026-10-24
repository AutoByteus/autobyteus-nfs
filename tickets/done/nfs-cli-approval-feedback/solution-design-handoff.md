# Architecture Design Complete — NFS CLI approval feedback

Package `nfs-cli-approval-feedback`; assigned Task **autobyteus-nfs-7** (no Task UUID was supplied). Requested by `/project_task_manager`, run `project_task_manager_a5f6d9d306e54970bafdad895bdf731d`. Solution Designer2026-10-24. Current solution **SR-002 Ready**, requirements **R1/SR-001 Approved** within user direction; **Small / Low**. No material decision/blocker or new follow-up.

## Request and intended result
The user, on installed publicv0.2.0/macOS26.5.2ARM64, reports no terminal feedback after administrator password for `~/.local/bin/autobyteus-nfs server`. PM explicitly approved a focused same-team change for both roles: truthful confirmed administrator access, preparation/waiting, browser next action, distinguish setup controls from storage, actionable unsuccessful outcome and preserve Ctrl+C safe drain. This is not established authentication/storage failure. Private screenshot URL/token was deliberately excluded; screenshot described by PM, not directly inspected.

Solution Designer approved R1 in conversation after evidence: actual lifecycle confirmation and readiness, bounded waiting reminder, phase-accurate failure with uncertainty. Exact wording engineering-owned. No new approval questionnaire or Product task needed. This design changes ordinary-user presentation only, not NFS behavior/auth model.

## Workspace and current authority
- Worktree: `/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/nfs-cli-approval-feedback`.
- Branch: `codex/nfs-cli-approval-feedback`.
- Refreshed source base: `origin/main` **456e5808e828d224804f9d4ce65c4cf740816eca**; final target `origin/main` under current RELEASE.md.
- Canonical ticket: `/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/nfs-cli-approval-feedback/tickets/in-progress/nfs-cli-approval-feedback`.
- Current production unchanged from that base, including admin/CLI paths equal published source448cef83. Only own ticket docs/evidence authored. No code/build/qualification or release claim.
- Canonical NFS checkout main7e375984 + untracked PM task-plans preserved. Older detached task archives/assets, application/superrepo/skills and user root state untouched.

## Evidence and technical direction
Read investigation E02–E04/E06 for actual command→private browser→explicit authorize→OS sudo→root install/admit→validated same-role/digest hello→locked metadata inspect→operation result→drain path. Browser already listens before sudo. Validated hello supplies confirmation; correlated successful inspect supplies setup-controls readiness, never mounted-storage health.

E05 is a safe independent ordinary-user diagnostic against actual Session/pipe code with child protocol doubles:12 cases across both roles have the expected existing result but no terminal result beyond PID. Baseline red reproduced, not an implementation Pass. No actual password/sudo/root/storage exercised. Official Go1.27.2 verified from go.dev; all owned diagnostic scratch/processes removed, durable raw log/probe/cleanup retained.

Implement the design's small private terminal-feedback presenter in dashboard, observe actual Session phases, serialize terminal lines, one10s reminder per still-pending phase and suppress obsolete output after transition/Stop. Remove obsolete PID-only logger/argument from transport, use narrow safe error categories rather than raw output parsing. No changed root/wire/browser state/operation concurrency. Preserve helper drains and original OS retry channel. No success from elapsed time, child PID or a mere metadata record. Design table gives message meanings, exact owners, removal and file list.

## Required next output / scope controls
Implementation Engineer owns production/tests and own checks; then use configured API/delivery routes. Required focused phase/order/error/race/privacy/dedup/Stop tests plus realistic current PTY/HTTP flow using isolated controlled helper. Doubles are not native sudo proof. No new VM/field campaign is mandated for unchanged privileged behavior; any optional native check must use already-owned disposable guests, never user's sudo/mount state. Current repository regression checks remain, with every skip/failed attempt/coverage limit truthful.

No release/tag/publication, installer upgrade, live-user create/connect/reconnect/detach, credential/OS policy change, application Guide/superrepo or skills. Publishedv0.2.0 is not changed by source completion. Existing field Task autobyteus-nfs-4 remains separate, not dispatched. Return Design Impact if new auth/protocol/security/cancellation/root/storage/HTTP behavior is actually needed; do not broaden Low-risk work.

Own authoritative files: requirements-doc.md, investigation-notes.md, design-spec.md, solution-revision-record.md and this handoff. Selected supplements: evidence/approval-feedback-probe.go.txt, approval-feedback-probe.log, approval-feedback-probe-result.json, probe-cleanup.json; other preparation evidence indexed in investigation, not forwarded wholesale. No prior review/implementation/API reports exist for this task; N/A rather than invented pass. Cleanup already complete for designer diagnostics; task worktree deliberately remains for implementation.

## Routing
Fresh get_handoff_rules on2026-10-24 returned Small/Medium+Low Architecture Design Complete → `/software_engineering_team/implementation_engineer`. This is the single matching rule; selected **Direct Low-Risk implementation**. Large/High architecture review and Delivery-receipt-gap rules do not apply. Requirements R1/SR-001 Approved, design SR-002 Ready; all five owned docs plus the focused reproduction/log/result/cleanup are attached. No separate architecture/source review is selected by this classification; implementation self-checks and executable API validation remain required. No duplicate PM/reviewer/API dispatch. Stop after required message succeeds.
