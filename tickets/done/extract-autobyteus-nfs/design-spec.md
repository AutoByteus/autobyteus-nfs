# Design Spec — Extract AutoByteus NFS

## Solution And Approval Basis
- **SR-004 — Ready / Architecture Design Complete**, requirements **R2 / SR-003 Approved** by Solution Designer within the user's explicit corrected direction. Approval reference and user notification in requirements-doc.md. Behavior-defining input: user-filesystem-boundary-correction.md; no separate Product spec.
- Package `extract-autobyteus-nfs`; Task `project_task_fdb2c737-fb08-48cf-8aca-e04df2d02ae8`. This replaces SR002, not an addendum retaining its contradictory integration contract.
- Evidence: canonical investigation-notes.md E01–E20, especially recovery E12–20. ARCH-REV-001 reviewed only R1/SR002. Current implementation checkpoint is held, not forward-ready.
- Authorities read: solution-designer SKILL; full architecture-design.md, design-principles.md, design template and handoff-references; S root DESIGN/TESTING/RELEASE/AGENTS and server/web AGENTS; N root AGENTS/DESIGN/TESTING/RELEASE; S/autobyteus-server-ts/docs/design/data_migration_guideline.md. Read in this conversation, 2026-10-16. Design-examples not used.
- Policy discrepancy: newly extracted N policies still say preserve deployed app descriptors/probes. Update those R1-derived clauses to this R2 basis; they do not override newer user direction. General design principles remain aligned.
- **N** `/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/extract-autobyteus-nfs`; **S** `/Users/normy/autobyteus_org/autobyteus-worktrees/extract-autobyteus-nfs`; both `codex/extract-autobyteus-nfs`. N checkpoint0c9fd27a77d65504b8eef41ece8972badb31778c; S390e0c76dda56c206ed8cabd65fc3564caaf1804; extraction source base3712cd9bf0db998501d162db7f8655f169e3def6. N finalizes origin/main; S origin/personal. **D0** canonical `/Users/normy/autobyteus_org/autobyteus-nfs` remains protected alongside PM task-plans.

## Current-State Read / Intended Change
The R1 implementation moved the service and distribution but left two-way runtime coupling: AutoByteus asks NFS whether a workspace is admitted; NFS probes app modules/APIs and recreates selected app nodes. Private skill behavior and Git trust are also selected by filesystem metadata. Merely moving directories or removing a fixture does not meet the user's boundary.
Retain the useful extraction commits; replace the coupled paths. NFS ends at a ready host filesystem path. AutoByteus begins with a supplied path and normal filesystem APIs. Docker deployment mapping remains generic; no runtime protocol connects the products. Service identity/source checks stay inside the service, not in application admission.

## Task Size And Architectural Risk
- **task_size: Large**: Go service lifecycle/interface reduction, app run/terminal/private-skill path correction, launcher removal, independent build/distribution and two-repo finalization.
- **architectural_risk: High**: privileged host lifecycle shares modules with removed node control; active predecessor obligations cannot be dropped; asynchronous profile/client cleanup and app security behavior change. Evidence E14–20, not artifact volume.
- Escalation: new persisted-data conversion, need to mutate a live deployment, unavailable native skill capability requiring new provider behavior, altered backend/source correctness or broadened Git trust returns here before implementation invents a workaround. Ordinary local implementation defects remain implementer's work.

## Architecture Evidence And Supplemental Artifacts
| Evidence | Supports | Limit |
| --- | --- | --- |
| E02–07,10–11 | Standalone module/build/installer/workflow/license boundaries | Not executable qualification |
| E12–13, user-filesystem-boundary-correction.md, implementation-evidence/ir-001/hold-checkpoint.json | Corrected intent and race-free recovery; preserve committed partial work and owned scratch | Prep failed before tests; no readiness claim |
| E14–17,20 | Complete app/launcher/private-profile call sites and existing generic mapping | No new paid/provider execution |
| E18–19 | Host-vs-node ownership and source/pending/installer ordering | No live installed-state inventory; unqualified predecessor fixtures/source only |
| design-review-report.md, architecture-review-revision-record.md | ARCH-REV-001 rationale retained | Historical R1 only, no current pass |
Complete inventory belongs to investigation. Old filesystem/editor archives remain read-only provenance, not new acceptance gates. Product artifacts N/A.

## Change Scope
UC001–006; N Go/CLI/config/setup/Docker app-control removal, local tooling/docs/tests/policies; S app NFS admission/private-profile selection/Git injection/launcher adapter and corresponding tests/docs. Retain extraction work, do not reset it.
Leave alone: NFS wire protocol/backends/engine recipe/pins/source identity/cache settings, generic app file APIs/editor/search/notifications, skill source registry and ownership, runtime credentials/history, provider authentication, unrelated launcher ports/security settings, other projects/history/PM boards.
Follow-ups: none newly discovered beyond existing excluded outage/platform/auth/notification issues. Do not reopen prior Tasks or duplicate existing follow-ups. A claim that all underlying filesystems are equivalent, or that app will detect an absent mount, is explicitly outside this design.

## Behavior And Production-Path Map
| Behavior | REQ / AC | Trigger and target path | Preservation / intended change |
| --- | --- | --- | --- |
| BEH001 | 001,002 / 001,002 | Contributor → N root module/local checks (DS1) | Independent build/check, declared tools |
| BEH002 | 002,004,005 / 002,004,005 | Maintainer → N packaging/workflow (DS2) | Own source hash, unchanged closed publication gates |
| BEH003 | 003,006,010 / 003,006,010 | Workspace/run/terminal request → app workspace/path owner → normal file/process APIs (DS3) | No NFS admission/CLI/descriptor/mount type; registered selection retained; normal errors |
| BEH004 | 007,008 / 007,008 | Delivery → validated two-repo candidates → exact target commits (DS6) | Fresh refs, safe cleanup, no release |
| BEH005 | 009 / 009 | NFS command/job → trusted host configuration → backend/mount/probe (DS4) | Same host correctness, no app node control; incompatible active installation refused |
| BEH006 | 010 / 010 | Runtime preparation → configured-skill private profile → provider → exact cleanup (DS5) | Filesystem-independent private app policy, existing owner/source/collision rules |

## Task Design Health Assessment
Posture: Behavior Change + ownership refactor. Design issue: Yes. Root cause: Boundary Or Ownership Issue and Duplicated Policy Or Coordination. Structural triggers: app execution imports infrastructure-specific admission; NFS service probes app internals; filesystem condition selects unrelated skill privacy/Git policy; Docker engine and app recreation mixed. E14–20 demonstrate production reachability.
**Refactor needed now: Yes**, restricted to these boundaries. Response: remove cross-product protocol and selectors; reuse ordinary workspace, profile and NFS host owners. Do not invent a generic storage adapter/driver registry, orchestration service or a renamed NFS bridge. Retain stable platform/backend internals. Deferred risks: operational mount availability and real external provider/platform qualification are not solved by this refactor.

## Data-Flow Spine Inventory, Narratives And Ownership
| Spine / scope | Flow and narrative | Governing owner / subject | Off-spine concerns |
| --- | --- | --- | --- |
| DS1 primary | Clone N → declared tools → Go/Python/build. Contributor checks never traverse S | N module/developer tooling | Toolchain availability, license/provenance |
| DS2 primary | Explicit candidate request → exact engine/source metadata → target artifacts → closed publish gate | N packaging/release owner | Signing, physical qualification, supply integrity |
| DS3 primary | Selected workspace → WorkspaceManager registered path → normal file operation or process cwd. Terminal/run errors remain operation-scoped | App workspace/runtime/terminal owners | Generic path containment and private config, not NFS |
| DS4 primary + bounded job | CLI → consent/lock/current-installation admission → setup.Service → backend + platform mount → nonroot probe → saved host state. Supervisor reconnects that host state only | N setup.Service; hosted filesystem/host attachment | Exact source identity, permissions, old incompatible obligation refusal |
| DS5 bounded runtime | Preparation owner → private profile → native runtime exposure/client lease → operation → proven process close → profile release | Existing backend preparation/client/profile owners | Source skill resolution/collision, cancellation, app-private paths |
| DS6 operational | Paired reviewed candidates → fresh refs/integration → N main then S personal → receipts/owned cleanup | Delivery | Concurrent work and partial completion |
Public CLI is a thin command/privilege/consent entry; setup.Service owns host lifecycle. WorkspaceManager owns workspace identity, not mount readiness. RuntimeSkillProfile owns only its generated per-execution links/wrappers, not source skills, credentials or network storage. Return/errors follow existing CLI JSON/diagnostic and app error/event surfaces; no new event protocol or queue.

## Interfaces / Dependency Rules / Encapsulation
| Boundary | Accepted subject | Allowed responsibility | Forbidden bypass |
| --- | --- | --- | --- |
| App filesystem workspace | Registered workspace ID → ordinary absolute path | Resolve path, normal filesystem operations/containment | /etc NFS reads, storage UUID, mount table/type inspection, NFS CLI call |
| Generic Docker workspace mapping | Existing configured host root and node name | Ordinary bind directory arguments/private volumes | NFS labels/volume driver interpretation, descriptor injection, mount-presence policy |
| NFS CLI/setup | Connection endpoint/export/protocol/storage UUID + host source/mount options | Sharing/backend/mount configuration, status/reconnect/drained detach | AutoByteus node discovery/recreation/health check or server JS imports |
| Runtime skill profile | Exact execution owner, app-private parent, working directory, configured bindings | Native configured-skill exposure and exact cleanup | Inferring privacy from filesystem type; copying credentials into workspace; broad Git trust |
| Build/distribution | Service-owned inputs | Independent archive/metadata/refusal tests | Hashing app source or paired consumer fixture protocol |
Responsibilities and identities are singular; ambiguity risk low after removal. NFS still knows NFS (its purpose); its own private connection metadata and source marker are not an application contract. No Go shared module, symlink, sibling replace, submodule, runtime HTTP connection or new package is introduced between products.

## Persisted Data / Migration Decision
Decision: **No automatic migration.** App persistent data is Not Affected; node-free NFS host state is Directly Usable — No Migration. Active old node-managed installations are explicitly unsupported for automatic adoption and refused, not discarded/rebuilt. This is a capability-scoped safety admission, not an app startup gate.

Governing convention: source data_migration_guideline.md plus current N config.Store/pending intent mechanisms (E18–19). N has no released migration runner/public version to reuse; do not invent one. Update N DESIGN with the limited policy: exact current writers, tolerant irrelevant fields, preserved unsupported obligations, no speculative transformation/history scan.

Checklist:
1. Need: no user data/identity relocation or new fact derived from history. Removed public app descriptor needs no replacement. Removing an active node obligation cannot be treated as a harmless ignored field.
2. Availability: AutoByteus never consults NFS installation state, including malformed/old state. NFS version/verify-release/help remain usable; only administrative installation/host operations on incompatible owned config refuse.
3. Sources/targets: private attachment.json Nodes; pending-setup.json Attachment.Nodes; host/source/Apple/engine state and partially bound source intents. Source structs/tests and write ordering inspected; no released public dataset or live-inventory claim. Prior source-unbound validation remains unchanged.
4. Dispositions: node-free existing config directly usable; empty/null retired nodes accepted as no obligation, current writers omit it; nonempty/malformed obligation refuses; old public descriptor and detached/completed receipts inert and preserved. No success label inferred from residue.
5. Commit/retry: use existing locks and atomic writers. Read only bounded active/pending records for safety; no migration journal/backups/ledger or automatic field rewrite. Refusal changes nothing.
6. Current-only boundary: a small read-only `config.CheckStandaloneState(Store)` (proposed `internal/config/installation_state.go`) recognizes only incompatible active obligation presence. It neither interprets node identities nor runs legacy behavior. Current Attachment/Plan carry no Nodes; their normal readers/writers use current host model. No legacy execution branch or fallback.
7. Cost: at most the two existing bounded active/pending records per administrative admission, no scan of nodes/receipts/workspaces/history. No installed-data measurements needed for this bounded check.
8. References: current source UUID/installation/source binding still validated by N owners. Old public node descriptors are never used by current app/NFS; active obligations require matching old tool/operator recovery before a later new setup. No automatic mutation of containers/volumes/paths.
9. Evidence: fixture tests for empty/node-free/nonempty/malformed active and pending shapes, preserving bytes and recording zero resource/config/binary mutations on refusal. Existing partial source-binding tests stay.
10. Review: independent architecture/code review of this revised basis. No unrelated app-data migration is modified/replayed; N's actual predecessor recovery is pending setup, inspected directly. If real migration becomes necessary, return a Requirement Gap before inventing it.

Enforcement details: check trusted private store before `internal-install` replaces the root binary (under the existing administrative lock) and before CLI administrative dispatch or supervisor tick opens/changes backend resources. New installation with absent active files proceeds. Malformed active files are errors, not empty state. Pass current state to existing setup flow; do not add a separate ongoing compatibility subsystem. Never delete node receipts/public files to pass the check. This task does not execute upgrade/recovery on live installations.

## App Workspace / Terminal / Git Paths (DS3)
Remove shared-run-workspace-admission and its AgentRunManager prepare wrapper; normal preparation ownership remains. Remove `shared-workspace-binding.ts` and mount-observation module after all imports/test hooks are gone.
Claude/Codex resolver error path retains failure for an explicitly registered workspace regardless of storage type, using WorkspaceManager's registration fact rather than a descriptor. Native factory resolves registered workspace through getOrCreateWorkspace uniformly. Preserve existing no-selection and unknown-ID fallback semantics; do not redesign general workspace registration. No mount preflight or eager filesystem scan is added. Actual cwd/file operations surface ordinary errors.
PTY session uses original cwd/start lifecycle without binding admission. Remove `native-shared-workspace.ts`; native custom data no longer adds NFS terminal environment. Remove all automatic scopedProjectGitEnvironment calls (PTY, native, AGY, ACP, Claude query, Codex client manager) and delete its helper/tests once unreachable. Keep operator-supplied normal environment/Git configuration; do not replace with safe.directory=* or automatically trust all workspace paths. Git ownership errors are ordinary results.
Do not change File Explorer REST/GraphQL/editor semantics; its normal filesystem interfaces are the desired integration surface. A path that exists without its former mount is not distinguishable to the app by design. Storage provisioning must be correct outside the app; do not rebuild the removed check elsewhere in application code.

## Private Runtime Skills (DS5)
Use existing RuntimeSkillProfile for configured skills of already-capable Claude/Codex/Grok, independent of filesystem. `prepare-private-runtime-skills.ts` loses binding imports and mount-root test. Its inputs remain execution memoryDir, workingDirectory, bindings, skills, collision policy and exact guard.
With configured bindings, require the existing app-owned absolute execution directory; preserve per-profile random subdirectory/0700/0600 and register owner before prepare. Validate the private target is not the project directory or inside it using ordinary resolved path relationships (including symlink alias), not mount tables/source IDs. Do not assert that a path outside the project is physically on a different filesystem; operator config owns that fact. Missing/invalid private execution storage fails only that run; no fallback to writing configured exposure into the project.
No configured bindings means no configured-skill profile acquisition and empty generated exposure—not invocation of the removed workspace materializer fallback. Existing project-owned native skills remain discoverable, and collision policy/source manager behavior remains. Keep capability checks/native adapters and profile-aware Codex client lifetime; do not silently fallback to shared project links when capability fails.
Update Claude/Codex bootstrap and Grok-bound ACP path to one private exposure path; remove unreachable conditional materializer calls/imports/helpers in these touched owners. ACP adapters without privateSkills retain their existing filesystem-independent behavior; do not redesign other providers. Existing generic materializers that still have real callers remain. AGY private capsule and native runtime existing skill ownership remain, except removed Git/binding imports. Cleanup must still await child/client close and release only the exact owned profile; do not sweep old source/project links or peer profiles.

## NFS Host-Only Lifecycle (DS4)
Keep create/connect/status/reconnect/drained detach and internal root/nonroot service actions. Remove `--nodes`, launcher-attachment and node selection prompts/output; removed options fail normal parsing rather than accept/no-op. Keep --drained for export/mount users, with node-independent wording. Connection values and default paths remain NFS-owned; update purpose text, not broad rename.
`setup.Request`, Plan, Attachment and Status lose node fields; Service loses Public store. Delete selected-node plan/discovery/image qualification, volume creation/probe/recreate/publish, failed-start recovery and node detach. Reconnect no longer takes retryConsumed node flag; it validates host config/source/backend, ensures mount and nonroot probe. Detach retains consent, source/config checks, non-forced unmount before stopping/removing owned export/engine, no source/marker/user-byte deletion. Busy refusal keeps service/config available. Preserve source binding persistence order and pending setup recovery for host resources.
Stop creating/reading/updating/removing /etc/autobyteus-nfs descriptors and remove public-store-only plumbing. Keep private attachment.json as host mount state and source marker .autobyteus-nfs/storage.json: those are internal NFS safety inputs, not app APIs. A generic Connection JSON can still be printed/read for NFS clients; rename fixture to testdata/connection.json for its actual subject, update producer tests/hash list, no S copy.
Docker remains solely for the service's own ganesha-docker backend. Keep local socket client, minimal Inspect/Create/Start/Stop/Remove, engine payload/identity/config/capability validation and pinned-image rules. Remove app discovery, launcher/node labels, exec/probe/recreate/volume/start-recovery/ownership operations and their tests only after moving shared engine-used Snapshot/Object/label helpers into the retained Docker owner. Do not delete `internal/docker` wholesale, change engine identity/security checks, or move app logic to a plugin/bridge repository.

## Generic Launcher And Documentation
Remove nfs-attachment.sh, its entry module/download list slot, resolver/hash/run/start calls and appended NFS args. Keep generic core shared-root config, normal node/shared bind mounts, private named volumes, normal node start/stop/update/workspace apply. Generic stop/no-op/restart=no instructions/tests survive in a generic launcher suite.
Document current mapping precisely: AUTOBYTEUS_DOCKER_SHARED_WORKSPACE_DIR is a host root whose shared/ and nodes/<name>/ children are mapped; it is not automatically an arbitrary NFS mount root. Operator can provision those directories externally; app sees container paths. No new mapping option or live mount propagation guarantee is introduced. No automatic upgrade of old specially attached containers is attempted; deployment transition requires explicit operator drain/reconfiguration outside this task.
N docs/filesystem-usage.md replaces docs/integration-contract.md with ordinary host/client setup and generic consumer use/limitations, not an app protocol. S docs link canonical independent repository and explain ordinary paths; no pinned fixture, CLI prerequisite or server readiness promise. Existing Guide is display-only: preserve disabled commands/release=null and correct any node-attachment promises in localized copy, without visual redesign or enabling release.

## Subsystem / File Responsibility And Removal Map
Final mapping refines the existing owners; no new architectural layer. Folder depth remains CLI/coordination/config/backend/platform/Docker adapter on N, and existing app workspace/runtime/launcher areas on S.
| Path/group | Change / owner | Reason and scope |
| --- | --- | --- |
| N go.mod, cmd, internal imports | Retain extraction to github.com/AutoByteus/autobyteus-nfs | No sibling module/replace |
| N internal/cli/{inputs,interactive-setup,run,install}.go; launcher.go | Remove app-node CLI; install/admission safety; delete launcher.go | Thin CLI, no app control |
| N internal/config/{state,connection,store}.go; installation_state.go | Current host structs/private store; bounded incompatible-state refusal | No public NodeAttachment or generic app schema |
| N internal/setup/{service,plan,apply,pending,lifecycle,status}.go | Host-only owner, preserve pending/source invariants | No Nodes/Public/retryConsumed; remove app branch methods |
| N internal/setup/{detach_nodes,reconnect_nodes}.go + node tests | Delete | Dead after node capability removal |
| N internal/docker/{client,engine,snapshot}.go + engine tests | Retain/reduce to storage-engine needs | Do not remove shared engine types with app functions |
| N internal/docker/{attachment,exec,ownership,probe_cleanup,recovery,recreate,start_observation,start_recovery,volume}.go + corresponding app-only tests | Delete after retained helper extraction/caller audit | Dead app orchestration, not moved to another coupled adapter |
| N backend/platform/service, source-binding helpers/tests | Preserve except obsolete Public fixtures/imports | Actual NFS behavior remains owned here |
| N testdata/attachment.json → connection.json; docs/integration-contract.md → filesystem-usage.md | Replace naming/contract ownership; update source hash/tests | No paired app schema |
| S server workspaces/shared-workspace-{binding,mount-observation}.ts; services/shared-run-workspace-admission.ts; native-shared-workspace.ts | Delete after callers corrected | Dead infrastructure-specific app policy |
| S AgentRunManager, PTY, native/Claude/Codex resolvers/factories | Use ordinary path lifecycle | No mount or descriptor access |
| S private-skill preparation/profile callers; Claude query; Codex client manager; ACP/AGY factories | Generic private exposure, remove Git trust injection | Existing per-run ownership reused |
| S runtime-management/shared/scoped-project-git-environment.ts + obsolete tests | Delete after all callers removed | Dead implicit trust policy |
| S Docker Bash entry/config/runtime/NFS module and launcher tests | Remove NFS adapter; retain/add generic mapping and stop regressions | No new launcher framework |
| S tests/fixtures/shared-network-workspaces/{attachment,provenance}.json and obsolete binding tests | Delete | Dead cross-product contract, no new pin/equality suite |
| N packaging/installer/workflows/Python suites/licenses/policies/provenance | Keep R1 extraction and correct R2 scope/hash/docs | One maintained service home |
| S active README/runtime/launcher/Guide docs and relevant translations/tests | Correct ownership/behavior claims | Historic tickets untouched; no editor implementation |
Names: HostedFilesystem/Connection/host Attachment retain concrete NFS meaning; RuntimeSkillProfile remains app-owned. Generic Snapshot contains only Docker engine inspection fields used by engine validator. No universal DTO combining application workspace and NFS connection. Draft/final allocation is the same existing ownership map after mixed node functionality is removed. Reuse: Store/atomic writer, source/platform/backend, WorkspaceManager, private profile/guard and launcher bind mapping; create only the small installation-state admission file where the current config owner belongs.

## Independent Build / Distribution / Licensing (DS1–2)
Retain root module, scripts/public/nfs/install.sh and service Python suites moved under N; Go directory_modes_test.go uses ../.. to invoke its local Python fixture. Remove only obsolete public-directory fixture expectations; keep umask/owner/nonroot installer assertions. Installer download repository AutoByteus/autobyteus-nfs. No app/launcher source copied into N.
packaging/release.py ROOT parents[1]; SOURCES includes internal, cmd main, go.mod, scripts/public/nfs, packaging/Dockerfile, packaging/engine, packaging/release.py, release workflow, testdata/connection.json, docs/filesystem-usage.md, LICENSE and THIRD_PARTY_NOTICES. Hash deterministic relative paths/bytes and exact engine/base/package identities; exclude generated metadata/output/qualified receipt/hash and existing test/cache/deb exclusions. Missing declared file fails. No source checkout outside N, no consumer fixture pin. Mutation invalidation tests required.
Keep engine source-lock/patch/build recipe byte-identical where relocation already worked. Preserve four-target compilation, Linux corrected-engine asset requirements and source notices. Retained old arm64 engine may be read/copied into owned scratch and freshly verified; not rebuilt or requalified merely because extraction occurred. Missing amd64/native/physical/signing coverage remains explicit.
Release workflow stays manual-only existing release_tag/candidate_run_id/publish=false, no desktop version assertion or automatic tag/main publication. Preserve six-job dependency/failure/cancellation/reuse/engine equality/native/signing/size/existing-release gates. No release/tag/version request here. Lock remains qualifiedTargets=[], qualifiedSourceHash="", physicalEvidence=[], userVerified=false, engine=null; never fill from old proof. Service-only physical qualification no longer implies AutoByteus app acceptance; do not weaken the publication gate or claim generic fixture checks qualify it.
Preserve LICENSE and CLA exact bytes, applicable root section7 permission, AGPL3-only/commercial terms, notices/source pins/author attribution. EXTRACTION.md records source3712cd9b and old paths, moved/split files, retained R1 extraction commits plus explicit R2 semantic changes; do not call the final runtime a byte-identical relocation. Historical source provenance is linked, not rewritten/imported wholesale.

## Verification Guidance (intent, not results)
Respect N/S TESTING. Implementation self-checks, Code Reviewer, API/E2E and Delivery retain ownership. No live-resource/user acceptance gate is invented. Current design changes real runtime control, so R1 mechanical comparison alone is insufficient.
| AC | Required evidence |
| --- | --- |
| 001,002 | Fresh standalone archive without S: full Go race/vet/native build/version, four-target compile, Python fixtures, shell/actionlint, current source hash/invalidation, installer/archive/embed/refusal controls. Resolve bootstrap Python compatibility only in owned test setup; preserve failed attempt |
| 003,006 | Source/import/call audit for removal PLUS executable ordinary-directory workspace/file route/run preparation/PTY and generic launcher fixtures. Test registered-resolution error without filesystem discriminator; absent/stale NFS metadata has no effect. Do not write /etc or mount real storage to prove absence of dependency |
| 009 | Go host-only lifecycle/source/pending/mount/config/permission/busy-detach tests; fake Docker engine API proves only owned engine calls. Incompatible active/pending envelope refusal before install replacement/resource mutation; node-free old fields direct-read and exact current writes; removed CLI options reject |
| 010 | Existing real private profile filesystem tests with local temp directories plus provider/client process fixtures: configured source/collision, no bindings, missing private dir, path alias rejection, per-run concurrency, cancellation/failed prepare, close-before-release, no source/project deletion, no implicit Git trust. Update actual production call-site tests, not only mocks of removed module |
| 003,010 | Affected server prerequisite build/typecheck and existing backend/activation/terminal/API suites per TESTING; real local socket file-content path as affected integration. Use protocol/process fakes at external-provider boundary, no credential/paid request needed; do not claim authenticated native provider qualification |
| 004,005,006 | License/source-pin equality, provenance and active-reference audit; preserved generic launcher stop control; disabled Guide component/utility/copy regressions. Historic tickets excluded from stale ownership removal |
| 007,008 | Final integrated candidate hashes, fresh refs, evidence mapping/limits and owned cleanup, no tags/releases/live deployment; old retained assets and PM work preserved |
Required functionality failing is a failure, not silently skipped. Report unavailable prerequisites and split compile/fixture/native evidence. Unchanged NFS engine behavior is protected by preserved code/tests, not a fabricated new cross-kernel/physical campaign. No special mount-loss test can establish a guarantee the app no longer makes.

## Backward-Compatibility Rejection Log
| Candidate | Rejection / replacement |
| --- | --- |
| Keep descriptor reader under generic name or optional NFS adapter | Rejected; direct ordinary path semantics, no storage classifier |
| Move attachment bridge into NFS while it still probes app internals | Rejected; service host lifecycle only, generic external directory mapping |
| Preserve app-node execution for old config or silently ignore active Nodes | Rejected; no legacy runtime; bounded refusal preserves outstanding obligations |
| Keep sibling module/submodule/wrapper installer or paired fixture pin | Rejected; independent source/tools, docs-only reference |
| Make all workspaces auto Git-safe or fallback to project-generated skill links | Rejected; ordinary Git policy and app-private configured exposure |
| Import old qualified hashes/targets | Rejected; changed source/current evidence, lock stays unqualified |

## Change / Refactor / Finalization Sequence
1. Continue from held N0c9fd27/S390e0c76, preserve both commits and failed prep evidence. Replacement architecture review precedes new affected implementation. Do not touch ir-001 scratch except by its owner.
2. N: installation safety boundary first; current host structs and host-only lifecycle; remove app Docker/CLI/public writers after retaining engine-used helpers. Keep source/pending/refusal invariants. S: remove admission/Git selectors, normalize registered path handling and private profiles, remove NFS launcher module/callers/fixtures. Delete newly dead touched code/tests; retain generic controls.
3. Correct policies/docs/provenance/source hash/test naming; self-check each independent archive and affected S integration. No temporary bridge or dual path remains. Independent review/executable validation through normal rules.
4. Delivery refreshes both remotes and integrates any newer affected source rather than blindly deleting it. N main established from reviewed initial history only if remote still empty, otherwise safely reconcile or report conflict; no fake unrelated-history merge or force. Finalize N first, then S personal with required --no-ff. No paired fixture pin remains; delivery records both exact revisions and documentation links. Partial finalization must be reported, not rolled back destructively.
5. Safely populate D0 only if still unborn/unconflicted, ordinary non-force checkout preserving PM metadata. Canonical source checkout remains untouched. Archive ticket/evidence under N delivery lifecycle; clean only task-owned scratch/worktrees/branches after durable receipts, retain any unowned assets. Never force clean/prune the old filesystem checkout. No release/tag/deploy.

## Tradeoffs / Risks / Implementation Guidance
True decoupling removes app-side wrong-mount/UUID prevention and app-node lifecycle automation intentionally; do not advertise them as preserved. Operators manage paths/readiness outside the app. Private profile standardization changes configured-skill exposure on ordinary paths but reuses existing runtime support and cleanup rather than inventing filesystem detection. Ordinary Git ownership can reject repositories previously implicitly trusted; no automatic bypass is authorized.
Bounded refusal avoids abandoning old node obligations, but is not a migration solution or release upgrade promise. No live migration is requested. Two-repo delivery is ordered, not atomic. Preserve snapshots and truthful failures; exact semantic changes must appear in implementation/test evidence. No decision outstanding for this design; new facts requiring changed behavior return to Solution Designer.
