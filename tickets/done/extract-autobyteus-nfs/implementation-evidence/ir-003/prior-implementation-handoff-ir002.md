# Implementation Handoff — Extract AutoByteus NFS

## Current result and identities
**IR-002 — CR-001 bounded import cleanup complete; Ready for targeted independent source re-review.**
Task project_task_fdb2c737-fb08-48cf-8aca-e04df2d02ae8. Personal execution only; no delegation.

- **N**: /Users/normy/autobyteus_org/autobyteus-nfs-worktrees/extract-autobyteus-nfs, branch codex/extract-autobyteus-nfs, target origin/main. Current service source **83726b27400b405a7a6a79bd962d8e2419daa561**; later ticket-only handoff commit does not change tested service inputs.
- **S**: /Users/normy/autobyteus_org/autobyteus-worktrees/extract-autobyteus-nfs, same branch, target origin/personal under --no-ff policy. Current source/tests **a2023feff3d498fb6c51cebf1c93360da3679a45**; this round removes only five unused local import bindings atop reviewed d3f7f67015587b4c8aa26824786be807793485d1. Production decoupling commit2448e166bd6fe17c83d70a55d1370db001a4989b remains.
- Original extraction source S3712cd9bf0db998501d162db7f8655f169e3def6. Preserved held extraction commits N353dd2c/0c9fd27 and S390e0c76. No reset/rewrite.
- Canonical ticket: N/tickets/in-progress/extract-autobyteus-nfs. Initial implementation evidence is implementation-evidence/ir-001 (**E** below); current bounded-fix evidence is implementation-evidence/ir-002 (**E2**).
- D0 /Users/normy/autobyteus_org/autobyteus-nfs stays unborn main with PM task-plans. It is not the implementation worktree.
- Historical IR-001 fetch observations: N remote had no refs; S origin/personal was3712cd9b. IR-002 did not fetch; finalization still requires fresh checks. Neither target has been merged/pushed; no release/tag/deployment/TaskDone/user-verification claim.

## Upstream authority and revision links
Approved **R2/SR-003**, Ready **SR-004**, **ARCH-REV-002 Pass**, review commitfc5d2ff3f404de3a683994766dfd47c258efb374 atop designer983812e8b4fe3363909e44cc905285fc800ca19a.
Canonical requirements-doc.md, investigation-notes.md, solution-revision-record.md, design-spec.md, solution-design-handoff.md, design-review-report.md and architecture-review-revision-record.md in this ticket remain unchanged by implementation. user-filesystem-boundary-correction.md is the governing supplemental direction.
ARCH-REV-001/R1/SR002 are historical, not the current implementation basis. The held preparation was not a completed handoff. implementation-revision-record.md retains IR001 with prior result N/A and appends IR002.
Related review: **CRR-001 Fail / Local Fix /98.8%**, canonical code-review-report.md and code-review-revision-record.md; review fedefa52583cf8f404b11f6080d87ed36ba0ae1e, receipt a77048efc905f1996d6481963625d3940a2c542a. Triggering finding **CR-001** is the sole mandatory cleanup item, not a behavioral defect. API-REV/DR: **N/A for this new Task**. Older filesystem/editor Tasks and their verdicts are not inherited or reopened.

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

## IR-002 bounded change and fresh checks
- Removed AgentRunConfig and RuntimeAgentRunContext local bindings from the Claude and Codex backend factories, and the local ClaudeSessionEvent type import from claude-session-manager.ts. Actual AgentRunContext imports and the independent ClaudeSessionEvent public re-export remain. Exact three-file delta: E2/source.diff.
- No runtime logic, tests, schemas, N service inputs, requirements/design, Guide or launcher changed. BEH006 / REQ010 / AC010 ownership and cleanup behavior is preserved; no new behavior. Classification remains Large/High for the completed package, not downgraded for this small fix.
- TypeScript5.9.3 unused-local audit of all25 extraction-touched production TS files: zero6133/6192/6196 diagnostics. Separate production typecheck via documented `pnpm -C autobyteus-server-ts typecheck`, including pretypecheck shared builds: exit0 in owned current-source copy with clean HOME/TMPDIR.
- Transpile comparison under production options: identical JavaScript for all three changed files, public re-export retained; 2insertions/7deletions and all files shrink. This comparison is not a runtime test or substitute for the separate semantic typecheck.
- Frozen filtered installation and Prisma generation are setup only. Initial typecheck setup omitted a script-only backend SDK prerequisite; corrected install and unchanged-source rerun passed. Optional audit initially used a relative fileName outside absolute rootDir; corrected the harness. Raw attempts preserved in E2/attempts.md, attempt-1 and attempt-2.
- E2/checks-and-limits.md, checks-result.json, unused-imports.json, delta-audit.json and cleanup.json hold fresh results. No new tests or broader campaign were needed for import-only identical-emission cleanup; IR001 and CRR001 evidence carries with explicit attribution. Owned scratch removed, no live resources started.
- Frontend loop **Not Applicable for IR002**: no rendered/user-interaction change. Initial Guide inspection remains historical IR001 evidence below.
- CRR001 remains the current reviewer verdict until targeted re-review. This implementation does not assign a reviewer/API Pass.

## IR-001 carried local implementation checks
The following are the initial implementation checks, **not newly executed in IR002**. All are local self-checks, **not API/E2E signoff**. See E/checks-and-limits.md, E/attempts.md and raw logs.

- Independent committed N archive, no sibling S: Go race across seven packages and vet exit0; Python20 collected/19 executed successfully, one child-only skip also exercised through Go's bootstrap fixture; actionlint and Bash syntax exit0.
- Darwin/Linux ×arm64/amd64 compile, native Darwin arm64 version. Fresh exact retained IR005 arm64 engine hash/manifest/file verification and embedded Linux arm64 compile only. No engine rebuild/execution/new qualification.
- Source hash **348046594b470f7b294aa2162f78ec349eb57c4edf74aa2db32112a9dc9da90e**, invalidation/missing-input/installer/archive/engine/workflow controls. Publication check expected exit1. Lock unchanged.
- Independent S copy with clean HOME/TMPDIR: documented prerequisite build (including sanitized built bootstrap), production typecheck exit0. Focused unit command1158 successful checks, six explicitly gated AGY-live skips. Additional final activation/PTY units40 checks.
- Existing local route/profile fixture commands39 checks; real local run composition/dummy-LLM memory lifecycle/native PTY command17 checks. Requested ordinary cwd, home, unavailable cwd and close/churn exercised. External provider process boundaries are scripted fixtures, not credential-backed models.
- Guide/component/command utilities24 checks; localization guard; generic launcher36 collected/34 executed, pwsh unavailable and occupied8001 collision setup skips; Bash syntax. No real Docker nodes.
- Final source input hashes unchanged;58 changed TS files parse clean. This is not a semantic typecheck of every test in the whole repository.

Failed attempts retained: unsupported Python bootstrap, protected ephemeral source location, workflow glob lint, dependency filters, stale test/mock inputs, alias-path expectations, nested test constructor rewrite and wrong runner selectors. Corrections never weaken source/mount/privacy/publication policy. Current final runs green within stated scope.

## IR-001 carried frontend rendered-result check
Factual EN/zh NFS Guide copy only, using existing NfsGuideCard/NodeManager visual language; no new UI design. Owned Nuxt route rendered actual current component/catalogs and null release, clicked locale controls at1440 and390 widths. Disabled copy/no download, readable wrapping, spacing/alignment and no horizontal overflow/runtime errors observed. E/guide-render/result.json plus four screenshots; browser/Nuxt stopped and temporary route removed. No installed desktop, available-release clipboard success, storage/UI acceptance or old editor campaign claimed.

## Environment, assumptions and known limits
Darwin arm64; exact tool versions E/final-toolchain.json. Clean isolated homes, no credentials or live provider usage. Scratch copies used installed workspace dependencies, never a sibling service module.
App intentionally cannot distinguish a directory after its mount disappears; ordinary path/I/O behavior is the new contract. Operators own storage availability and generic container mapping. NFS refuses predecessor obligations rather than silently abandoning them; no live installation was upgraded.
Four-target compilation is not Linux/amd64/physical runtime qualification. No real privileged install, mounts/exports, VM campaign, Mac/Linux cross-host or paid provider campaign, hosted Actions/signing/public bootstrap qualification. Source/engine/app identities remain separate. Empty qualification/disabled Guide are required, not a release blocker to be bypassed.
Original retained engine/canonical source and unrelated scratch/dist assets were not modified or deleted. D0 PM board hash preserved. Cleanup covers enumerated owned resources only, E/cleanup.json.

## Downstream coverage hints / remaining gates
1. Targeted source re-review of CRR001/CR001 five-binding cleanup and fresh E2 checks. Full R2 review is already recorded in CRR001; no wider or renewed architecture review requested. Unchanged source/behavior evidence carries, not a new runtime Pass.
2. Selected API/E2E engineer investigates/executes proportionate current standalone and local app path/profile/launcher coverage, owns verdict and confidence. No old completed filesystem/editor/VM/provider campaign or new user-approval loop is implied.
3. Delivery refreshes both targets, integrates concurrent changes safely, syncs docs and finalizes N first then S (--no-ff), safely populates D0 only if still unborn/unconflicted, and reports exact two-repo receipts. **AC007 not yet achieved.** No release authorized.
