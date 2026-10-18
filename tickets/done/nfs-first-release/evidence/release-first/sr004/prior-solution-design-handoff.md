# Architecture Design Complete — nfs-first-release

## Identity / workspace
- Task **autobyteus-nfs-3** / `project_task_97c6ab09-83cb-46df-bf28-d07b39259dd5`; Project `project_6416db5b-926a-4865-8705-d8ebb2425780`.
- Requested by `/project_task_manager`, run `project_task_manager_a5f6d9d306e54970bafdad895bdf731d`. Closed extraction/previous filesystem tasks remain closed; dashboard nfs-2 is not dispatched.
- **Requirements R2/SR-002 Approved; design SR-003 Ready; task_size Large; architectural_risk High.** Result is Architecture Design Complete, not implementation-ready without applicable review, not a release or TaskDone result.
- Repository https://github.com/AutoByteus/autobyteus-nfs . Isolated task worktree `/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/nfs-first-release`, branch `codex/nfs-first-release`.
- Fresh bootstrap base and finalization target `origin/main`7e375984be2bea7a4d536e43cc59d6bc2b116870; same remote SHA observed2026-10-18. Initial requirements commit5e30a45a988cdc83f0c5c7ccab03aafc6a87c054; final design document commit supplied with handoff message. No production/source changes or remote pushes by SD.
- Ticket `/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/nfs-first-release/tickets/in-progress/nfs-first-release`.

## Original request, scope and approval
User asked via PM to enable CI-driven releases analogous in usability to the superrepo and **actually publish the first downloadable NFS release**, not just an unexercised workflow. User explicitly rejected beta: “I will directly drop the beta release approach. I will just use the normal release.” SD approved initial normal v0.1.0 and retained current four-target scope within direction, user informed; no Needs-user requirement decision remains.

Standalone NFS releases are independent of desktop versions/app nodes. Existing targets remain native macOS26+/Ubuntu24.04, ARM64/amd64, with Docker-Linux engine mode. Internal build-only candidates are not beta/public releases. Do not infer permission to qualify unsupported targets, weaken physical/explicit-user/signing gates, or operate live user storage from publication authorization. Actual current-source qualification is absent at this solution stage.

Authorized change includes release workflow/tooling/tests/docs and actual evidence-backed publication, not dashboard, superrepo edits, Homebrew tap, new runtime/filesystem features/backends, paid infrastructure, live mounts/data/node upgrade, Guide activation, editor/updater repair or historical archive reopening. Keep PM task-plans/unowned caches/canonical checkouts untouched. Root RELEASE and packaging RELEASE must be reconciled from extraction-era prohibitions to this new explicitly authorized independent-release scope.

## Completed design / what review should examine
1. Manual candidate/publication workflow, strict normal versions and exact SHA; no pre-created tag/release requirement and no automatic main/PR publication.
2. Build one measured two-architecture engine pair and complete multi-arch OCI candidate; bind run/attempt/repo/workflow/source/engine/OCI/payload identities. No rebuilt image under old qualification.
3. Actual per-target/mode physical/independent-host and explicit-user receipts remain mandatory; structured reference validation supplements human evidence judgement. Test registry serves identical candidate digest because Docker first-use always pulls; metadata-only qualification alias is disclosed, not a runtime override/backdoor.
4. Same production source/exact engine packages create final metadata/native payload; Mac Developer ID + explicit Accepted notarization before public writes; final candidate versus signed binary byte differences disclosed.
5. Retain final payload; annotated exact tag binds recovery identity; complete draft asset verification; digest-preserving OCI promotion and anonymous package availability; only then normal public release. No clobber/force/implicit-tip/hidden partial-success path. Reuse same retained payload on retry; refuse conflict/expiry.
6. Preserve exact bounded installer/runtime-manifest admission and host-only runtime; versioned download instructions and no-setup owned-HOME smoke. Current immutable image/candidate/signing/evidence boundaries drive Large/High classification.

No runtime Go/source-state redesign. Packaging release-support owners replace duplicated workflow policy; existing engine validator and CLI admission are reused. Root design and migration-convention check passed: no installed host-data migration; unqualified generated records can be rebuilt as a new candidate, never as old proof. See design file for concrete ownership/file map, removals, recovery and AC proof intent.

## Current credential prerequisite — provisioned, not validated
User explicitly authorized selected Developer ID export/upload, entered account/app-specific/export passwords directly, and confirmed filename/folder. All six NFS repository secret entries are now populated. SD exported only the selected identity via UI, with human handling protected password steps; uploaded Base64 through gh stdin without logging it. Original Keychain certificate/private key untouched. The task-owned temporary .p12 and empty private directory were removed. No source GitHub secret extraction, unrelated private-file scan, secret value readback or secret content in artifacts.

The latest receipt is evidence/intake/signing-certificate-upload-receipt.json. Earlier placeholder receipts are historical; **do not ask the user to fill the same fields again solely from their existence**. Password/P12 pairing, actual import/signing and notarization still require the intended workflow. Any real failure should name the failing credential/gate without exposing values. No signing run has been dispatched by SD.

## Evidence and remaining prerequisites
Canonical investigation E01–18 separates observations from design decisions. Source files and primary GitHub/Apple/skopeo contracts were inspected. Local artifact audit checks only SD document consistency, parseability, whitespace and unchanged production tree; it is not a product/test/signing/physical/CI verdict.

Remaining execution work: implement/review; actual hosted candidate; inventory and authorize scoped test-owned physical hosts/registry; applicable candidate/host-mode/user verification; signing/notary; GHCR public visibility; authorized publish run and actual public downloads. Native CI/VM/historical extraction results must not be promoted to those gates. If a real external prerequisite prevents publication, keep Task open with that precise blocker; workflow enablement alone is not done.

No live service/container/mount/provider action, tag/release/image publication, deployment or source finalization by SD. No owned background process/runtime resource remains. Credential temp cleanup complete; task worktree retained for normal downstream work.

## Canonical artifacts to read
Own documents (all attached):
- `/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/nfs-first-release/tickets/in-progress/nfs-first-release/solution-design-handoff.md`
- `/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/nfs-first-release/tickets/in-progress/nfs-first-release/requirements-doc.md`
- `/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/nfs-first-release/tickets/in-progress/nfs-first-release/investigation-notes.md`
- `/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/nfs-first-release/tickets/in-progress/nfs-first-release/solution-revision-record.md`
- `/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/nfs-first-release/tickets/in-progress/nfs-first-release/design-spec.md`
Selected supporting files: evidence/intake/repository-release-preflight.json and evidence/intake/signing-certificate-upload-receipt.json. Older receipts remain linked by investigation inventory; no cumulative forwarding manifest.

Independent architecture/code/API/delivery reports for this new task: **N/A — not yet applicable**. Closed extraction reports are provenance only.

## Expected next output
Independent architecture review of SR003 against R2 and NFS design/testing/release authorities, focusing identity/qualification/signing/promotion/recovery. Any scope-changing finding returns to SD; no automatic questionnaire or platform reduction. On Pass follow configured reviewer downstream route; informational Pass to SD must not cause duplicate implementation dispatch. API/Delivery retain executable/release ownership.

## Routing
Fresh get_handoff_rules returned the Large/High Architecture Design Complete rule. Only that rule matches; exact recipient **/software_engineering_team/architecture_reviewer**. Requirements R2 are approved, design SR003 is complete and the package is ready for independent architecture review. Raw rules and selection are persisted in evidence/design-routing.json. Send this handoff plus the four own canonical documents and two selected intake receipts; no implementation/API/PM duplicate dispatch. The send_message_to tool receipt is the delivery record. Stop after successful handoff.


## User-requested resume after power interruption
Observed 2026-10-18T07:16:50.146034+00:00. User: “continue sorry there was a poweroff”. Saved design commit cbf7b35edc3fae86d90800003a1720528666d67e is intact; worktree was clean. No local review/implementation report was present at this checkpoint; this is not proof of the reviewer’s in-memory state. All six GitHub secret names/timestamps still exactly match the successful provisioning receipt; no secret reset/export/re-entry needed. Temporary private export directory remains absent.

Resume the **existing SR003 review** from its durable checkpoint; this is not a new design round or a request to repeat completed work. If review/forwarding already finished, reconcile/report that existing outcome rather than duplicate dispatch. Requirements/design/classification unchanged. Fresh routing will be recorded in evidence/poweroff-routing.json; evidence/poweroff-resume.json records the narrow restart checks. All original scope/approval/workspace/evidence/next-output context above remains controlling.

Fresh routing selected only `/software_engineering_team/architecture_reviewer` under the unchanged Large/High Architecture Design Complete rule. Resume request is directed to that existing owner; no other specialist or PM notification.
