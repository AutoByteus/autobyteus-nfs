# Implementation Handoff — Extract AutoByteus NFS

## Current result and identities
**IR-001 initial implementation baseline — Ready for independent source review.**
Task project_task_fdb2c737-fb08-48cf-8aca-e04df2d02ae8. Personal execution only; no delegation.

- **N**: /Users/normy/autobyteus_org/autobyteus-nfs-worktrees/extract-autobyteus-nfs, branch codex/extract-autobyteus-nfs, target origin/main. Current service source **83726b27400b405a7a6a79bd962d8e2419daa561**; later ticket-only handoff commit does not change tested service inputs.
- **S**: /Users/normy/autobyteus_org/autobyteus-worktrees/extract-autobyteus-nfs, same branch, target origin/personal under --no-ff policy. Current source/tests **d3f7f67015587b4c8aa26824786be807793485d1**, production decoupling commit2448e166bd6fe17c83d70a55d1370db001a4989b.
- Original extraction source S3712cd9bf0db998501d162db7f8655f169e3def6. Preserved held extraction commits N353dd2c/0c9fd27 and S390e0c76. No reset/rewrite.
- Canonical ticket: N/tickets/in-progress/extract-autobyteus-nfs. All implementation evidence is its implementation-evidence/ir-001 directory (**E** below).
- D0 /Users/normy/autobyteus_org/autobyteus-nfs stays unborn main with PM task-plans. It is not the implementation worktree.
- Fresh fetches: N remote has no refs; S origin/personal remains3712cd9b. Finalization still requires another freshness check. Neither target has been merged/pushed; no release/tag/deployment/TaskDone/user-verification claim.

## Upstream authority and revision links
Approved **R2/SR-003**, Ready **SR-004**, **ARCH-REV-002 Pass**, review commitfc5d2ff3f404de3a683994766dfd47c258efb374 atop designer983812e8b4fe3363909e44cc905285fc800ca19a.
Canonical requirements-doc.md, investigation-notes.md, solution-revision-record.md, design-spec.md, solution-design-handoff.md, design-review-report.md and architecture-review-revision-record.md in this ticket remain unchanged by implementation. user-filesystem-boundary-correction.md is the governing supplemental direction.
ARCH-REV-001/R1/SR002 are historical, not the current implementation basis. The held preparation was not a completed handoff. Current implementation-revision-record.md begins IR001 with prior result N/A.
Related CRR/API-REV/DR: **N/A for this new Task**. Triggering finding IDs: N/A. Older filesystem/editor Tasks and their verdicts are not inherited or reopened.

## Routing classification
- Task size: **Large**, architectural risk: **High**, confirmed unchanged.
- Design health: Behavior Change + ownership refactor; Boundary Or Ownership Issue / Duplicated Policy Or Coordination; Refactor Needed Now. Implementation matches reviewed scope.
- Evidence: two products' runtime boundary, trusted installation admission, exact asynchronous private-profile ownership, source/distribution ownership and two-repo finalization. This is not mechanical relocation alone.
- Selected next stage: **Code Review**, confirmed through fresh handoff rules before dispatch.
- Direct-route self-review: N/A. New Design Impact / Requirement Gap: None demonstrated. Approved scope guardrail respected.

## Reviewed behavior implementation trace
| Behavior / AC | Actual path and outcome |
| --- | --- |
| BEH001 / AC001,002,006 | N root go.mod/cmd/internal imports use github.com/AutoByteus/autobyteus-nfs. Installer, packaging, five service Python suites and workflow are local. Go-to-Python fixture root resolves two levels up to N. S removes embedded service/workflow/installer/service suites; no sibling replace, app-source vendor or second maintained implementation |
| BEH002 / AC002,004,005 | N packaging/release.py hashes service-local inputs plus docs/filesystem-usage.md and testdata/connection.json, not arbitrary app bytes. Workflow is manual-only with publish=false, no desktop version assertion/automatic tag trigger. Candidate reuse/equality, cancellation/failure/current-source/native/signing/physical/user/existing-release gates remain. Empty qualification lock and disabled S Guide remain. License/CLA/notices/pins and section7 permission preserved |
| BEH003 / AC003,006 | S AgentRunManager prepares directly; native/Claude/Codex workspace resolvers preserve registered failure and prior unknown/no-selection policy. PtySessionManager uses ordinary cwd and normal lifecycle. Shared mount/binding/admission modules, all automatic scoped Git trust calls, launcher NFS module/hooks/download/hash and paired fixture/pin removed. No replacement mount detector. Generic launcher root/shared plus root/nodes/name and private volumes retained |
| BEH004 / AC007,008 | Both development histories preserved and source/evidence identities recorded. Owned isolated check resources cleaned; protected PM/retained engine hashes checked. Delivery finalization remains pending; no false full Task completion |
| BEH005 / AC009 | N CLI/setup/config become host-only create/connect/status/reconnect/drained detach. Removed app node discovery/control/HTTP probes/public descriptors and retired CLI options. Retained storage-engine Docker client/types/config/identity/capability checks. Source/marker/pending/permission/mount/busy-detach behavior preserved; 28 backend/platform/service production files normalized-equal after import change |
| BEH006 / AC010 | S prepare-private-runtime-skills and RuntimeSkillProfile acquire existing per-execution profiles uniformly for Claude/Codex/Grok. Exact owner registered before await; no bindings means no acquisition, not materializer fallback. Absolute private execution directory must resolve outside project including aliases. Existing managed-source/collision semantics and native capability errors retained. Process/client close precedes exact profile release; peers/project/source bytes preserved. Other ACP adapters retain filesystem-independent materializer behavior; Grok's now-dead materializer wrapper is removed |

N and S are path abbreviations defined above, not extra directories. Detailed changed paths: E/change-inventory.json. No editor implementation change.

## Key implementation boundaries
- N internal/config/installation_state.go reads only active attachment.json and pending-setup.json's Attachment under existing trusted bounded Store semantics. Absent/null/empty Nodes are directly usable if current host metadata validates; nonempty/malformed/ambiguous envelopes refuse. Unknown harmless fields remain tolerated. No receipt/history scan, automatic migration, deletion or legacy execution path.
- N internal/cli/install.go locks admission and root binary replacement together; refusal precedes target parent/replacement effects. Dispatch and supervisor recheck under the same administrative lock before resource effects. setup entry points also refuse incompatible state. Internal helper is not a new public configurable installer path.
- Host pending source bind-once/persist-before-effects ordering remains; status does not repair, detach does not gain a live-source requirement or forced unmount.
- S private configured-skill profile selection no longer depends on any filesystem classifier. ACP dependencies specialize private-profile versus generic-materializer inputs; the Grok owner does not construct a dead project materializer.
- S native runtime and AGY keep their genuine private/tool owners; only removed binding/Git policy leaves their paths.

## Legacy / compatibility / state check
No compatibility bridge, old/new runtime mode, schema version, implicit safe.directory wildcard, application mount classifier or automatic installed-data migration added.
Retired app-node/NFS coupling and touched dead wrappers/cleanup imports/tests are deleted. Generic ACP materializers remain per the explicit design; no provider framework redesign.
Persisted-state decision follows design MP001/002: host-only NFS state directly usable; active/pending node obligations refuse safely and require the matching predecessor tool for explicit operator recovery outside this task. Workspace registry/history/credentials and sources/markers are not migrated. Generated runtime profiles use existing exact ownership; no scan/sweep of prior project links or old profiles.
Shared design principles reapplied; no changed implementation file exceeds500 effective nonempty lines or grows an already-over-limit file; no >220 changed-line source signal in the R2 delta (tests excluded). Full source audit recorded. No additional out-of-scope dead-code follow-up identified.

## Local implementation checks
All are local self-checks, **not API/E2E signoff**. See E/checks-and-limits.md, E/attempts.md and raw logs.

- Independent committed N archive, no sibling S: Go race across seven packages and vet exit0; Python20 collected/19 executed successfully, one child-only skip also exercised through Go's bootstrap fixture; actionlint and Bash syntax exit0.
- Darwin/Linux ×arm64/amd64 compile, native Darwin arm64 version. Fresh exact retained IR005 arm64 engine hash/manifest/file verification and embedded Linux arm64 compile only. No engine rebuild/execution/new qualification.
- Source hash **348046594b470f7b294aa2162f78ec349eb57c4edf74aa2db32112a9dc9da90e**, invalidation/missing-input/installer/archive/engine/workflow controls. Publication check expected exit1. Lock unchanged.
- Independent S copy with clean HOME/TMPDIR: documented prerequisite build (including sanitized built bootstrap), production typecheck exit0. Focused unit command1158 successful checks, six explicitly gated AGY-live skips. Additional final activation/PTY units40 checks.
- Existing local route/profile fixture commands39 checks; real local run composition/dummy-LLM memory lifecycle/native PTY command17 checks. Requested ordinary cwd, home, unavailable cwd and close/churn exercised. External provider process boundaries are scripted fixtures, not credential-backed models.
- Guide/component/command utilities24 checks; localization guard; generic launcher36 collected/34 executed, pwsh unavailable and occupied8001 collision setup skips; Bash syntax. No real Docker nodes.
- Final source input hashes unchanged;58 changed TS files parse clean. This is not a semantic typecheck of every test in the whole repository.

Failed attempts retained: unsupported Python bootstrap, protected ephemeral source location, workflow glob lint, dependency filters, stale test/mock inputs, alias-path expectations, nested test constructor rewrite and wrong runner selectors. Corrections never weaken source/mount/privacy/publication policy. Current final runs green within stated scope.

## Frontend rendered-result check
Factual EN/zh NFS Guide copy only, using existing NfsGuideCard/NodeManager visual language; no new UI design. Owned Nuxt route rendered actual current component/catalogs and null release, clicked locale controls at1440 and390 widths. Disabled copy/no download, readable wrapping, spacing/alignment and no horizontal overflow/runtime errors observed. E/guide-render/result.json plus four screenshots; browser/Nuxt stopped and temporary route removed. No installed desktop, available-release clipboard success, storage/UI acceptance or old editor campaign claimed.

## Environment, assumptions and known limits
Darwin arm64; exact tool versions E/final-toolchain.json. Clean isolated homes, no credentials or live provider usage. Scratch copies used installed workspace dependencies, never a sibling service module.
App intentionally cannot distinguish a directory after its mount disappears; ordinary path/I/O behavior is the new contract. Operators own storage availability and generic container mapping. NFS refuses predecessor obligations rather than silently abandoning them; no live installation was upgraded.
Four-target compilation is not Linux/amd64/physical runtime qualification. No real privileged install, mounts/exports, VM campaign, Mac/Linux cross-host or paid provider campaign, hosted Actions/signing/public bootstrap qualification. Source/engine/app identities remain separate. Empty qualification/disabled Guide are required, not a release blocker to be bypassed.
Original retained engine/canonical source and unrelated scratch/dist assets were not modified or deleted. D0 PM board hash preserved. Cleanup covers enumerated owned resources only, E/cleanup.json.

## Downstream coverage hints / remaining gates
1. Independent source review of R2 removal and trusted install admission, source hash/workflow/license ownership, ordinary path resolution and exact private-profile cleanup. Recheck test changes proportionately; R1 comparison alone is insufficient.
2. Selected API/E2E engineer investigates/executes proportionate current standalone and local app path/profile/launcher coverage, owns verdict and confidence. No old completed filesystem/editor/VM/provider campaign or new user-approval loop is implied.
3. Delivery refreshes both targets, integrates concurrent changes safely, syncs docs and finalizes N first then S (--no-ff), safely populates D0 only if still unborn/unconflicted, and reports exact two-repo receipts. **AC007 not yet achieved.** No release authorized.
