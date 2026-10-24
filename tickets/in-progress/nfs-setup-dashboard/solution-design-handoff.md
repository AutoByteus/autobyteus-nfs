# Architecture Design Complete — nfs-setup-dashboard

2026-10-24; **R1/SR-001 Approved, SR-002 design Ready; Large / High**. Not yet independently reviewed or implementation-dispatched.

## Original request and approval
Task **autobyteus-nfs-2 / project_task_f1264eb8-5a99-4a19-949f-09d141c955a1**, requested by **/project_task_manager**, run **project_task_manager_a5f6d9d306e54970bafdad895bdf731d**. User selected `autobyteus-nfs server` and `autobyteus-nfs client`, each opening a local setup/status/reconnect/disconnect UI from the same standalone program, then explicitly dispatched this team. Exact Task direction is captured in requirements-doc.md. R1 approved by Solution Designer within that direction, user informed in conversation: local role UI, terminal OS approval (no browser password), exact-plan consent, closing management does not detach, standalone/no release. No outstanding product approval question or separate Product Team request.

## Workspace / base / next output
Worktree **/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/nfs-setup-dashboard**; branch **codex/nfs-setup-dashboard**; fresh base **origin/main52c17fb5480d23b89752a8ae201419e356b4c3fc**; finalization target **origin/main**, source-only. Canonical repo remains local main7e37598 with untracked PM task-plans; old extraction/release detached worktrees/candidates preserved. Do not author in those locations. Current changed files are only Solution Designer's ticket docs. No product implementation/tests, persistent runtime, VM or privileged work launched; only the disposable nonroot premise probe described in investigation. No push or release.

Canonical ticket: **/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/nfs-setup-dashboard/tickets/in-progress/nfs-setup-dashboard**.
Read own five files here:
- `solution-design-handoff.md` (this context)
- `requirements-doc.md` (approved R1, SCN001–010 / REQ001–010 / AC001–008)
- `investigation-notes.md` (E01–12, primary dependencies, measured narrow nonroot pipe/flock probe, limitations)
- `design-spec.md` (SR002, concrete security/IPC/lifecycle/owner/file/test design)
- `solution-revision-record.md` (SR001 requirements and SR002 design history)
No supplements, old forwarding manifest or Product package.

## Design and review focus
Embed plain web assets in Go; ordinary-user loopback-only dashboard; explicit sudo terminal approval starts same root-installed executable over stdin/stdout pipes, never root HTTP or password JSON. Introduce one admin.Session owner for existing CLI+helper+supervisor lifecycle instead of duplicating lock/Docker/plan/reconnect/job order. Keep setup/config/platform/backend invariants authoritative. Browser receives a display-only plan and opaque lease; root keeps exact Plan and existing nonblocking lock until commit/cancel/5min review expiry. Operation can remain pending on hard NFS; asynchronous UI state must not imply cancellation/rollback. No schema migration. Verify all current entry forms including service with no SUDO_UID and pending saved-user identity, not only UI happy paths.

Focus: browser Host/origin/token security and private bootstrap/fallback; real sudo/TTY/pipe/EOF/identity semantics; exact plan admission and lock lifetime; root versus UI versus storage-service shutdown; configured vs observed ready; all three existing host backends; preservation of terminal contracts and source hash/embedded assets. Full design lists native isolated and real browser proof obligations. Existing public v0.1.0 does not contain these future commands; documentation must not imply it does.

## Scope and evidence boundaries
NFS-only. No AutoByteus app/Guide/workspace skills/nodes/launcher coupling, new protocol/platform/discovery, public management, release/version/tag/signing/installer publication, live-user mount/export/Docker/config mutations, or reopening older campaigns. Existing autobyteus-nfs-4 field validation remains separately deferred; bounded owned VM UI/host tests do not close it. Task permits owned isolated resources, not operator host mutations. No credentials need to be obtained during design.

Evidence is read source/primary docs plus a disposable nonroot OS lock/pipe premise probe, NOT executed UI/Go/sudo/NFS acceptance. Go is absent from this shell's PATH; local toolchain/guest availability not established. Native Linux build must carry measured engine/package inputs in a development-only disposable build, not old signed bytes or a weakened admission. Missing external resources must be reported as precise blocker, not silently fake-passed or turned into a broad field questionnaire. Historical intake extraction DR002 blocker was resolved; do not resurrect it.

No prerequisite or new follow-up currently identified. No retained task-owned scratch: narrow probe scratch removed. Reviewer should return independent design findings or route reviewed design onward per its rules; Solution Designer does not perform implementation or duplicate a review-pass forwarding.

## Routing
Fresh get_handoff_rules, 2026-10-24: selected the most-specific Architecture Design Complete with Large or High rule; current approval within direction/user informed is satisfied. Exact recipient **/software_engineering_team/architecture_reviewer**. Expected output: independent architecture review of R1/SR002, followed by its configured route. The Low-risk implementation and Delivery Receipt Gap rules do not match. Send own five files only; no duplicate PM/implementation/API notification.
