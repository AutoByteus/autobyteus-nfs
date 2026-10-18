# Implementation Handoff — Extract AutoByteus NFS

## Current result
**IR-005 — DR-002 implementation-owned Local Fix complete; Ready for targeted independent source review and affected validation.**
Task project_task_fdb2c737-fb08-48cf-8aca-e04df2d02ae8.
Personal execution only; no delegation. Not Delivery Completed/TaskDone.

## Authoritative paths and completed operations
- **N** /Users/normy/autobyteus_org/autobyteus-nfs-worktrees/extract-autobyteus-nfs,
  recovery branch codex/extract-autobyteus-nfs, target origin/main.
  Current test correction **09cac96225fe4f36fb0dcbe6ddec01248992874f**, based on blocker checkpoint
  56c0c59efdd3b963b2fc11ba07bda7410b4067b2. Runtime remains83726b27400b405a7a6a79bd962d8e2419daa561;
  later delivery policy/docs are preserved. Production source hash unchanged.
- **Canonical ticket is already archived:** N/tickets/done/extract-autobyteus-nfs.
  Continue here; archive location is not TaskDone. E5 below means
  implementation-evidence/ir-005; prior E/E2/E3/E4 evidence remains in this archive.
- Delivery already pushed N main/ticket **22e934b9f2b95daf3c72a840788ee155cbd4ff6d**
  first; then S ticket **9b72c8d1c8d6f7e294af2c23fb497211c67f930c** merged --no-ff
  to personal **55bff1f5eea1f140bab6e372e3faadeb7ea33465**, exact tree equality.
  Source operations must not be replayed, reset or undone. Their authority is
  delivery-evidence/dr-002/finalization.json, not a new implementation fetch.
- **S** task worktree was safely removed by Delivery after merge; no S change
  or worktree recreation this round. Canonical app checkout untouched.
- **D0** /Users/normy/autobyteus_org/autobyteus-nfs now populated main22e934b
  tracking origin/main by Delivery, PM board preserved; no authorship here.
- IR005 made no target fetch/merge/push/default-branch/tag/release/deployment action.
  User wants no release. Delivery must refresh targets for the reviewed fix-forward.

## Authority / trigger / classification
Approved **R2/SR003**, Ready **SR004**, **ARCH-REV-002 Pass** remain unchanged.
Requirements, investigation, design, solution history and filesystem-boundary
correction remain separate authorities in the archived ticket.
**Large / High / Reviewed** retained: two-product boundary, trusted host install/
state, asynchronous private-profile cleanup and two-repo distribution ownership.
No Design Impact/Requirement Gap or changed intended behavior established.
Current trigger **DR-002 Blocked / Local Fix**: actual hosted Ubuntu Developer
Checks39097778705 and39097779223 failed at22e934b. CRR005 source Pass100,
API002 current integrated/local Pass95 and CRR006 no-test-delta satisfied remain
historical exact-input authorities, not Linux hosted qualification. CR001/002
import findings are resolved; no old filesystem/editor Task is reopened.
Selected next stage is Code Review via fresh most-specific Local Fix rule;
direct-route self-review N/A.

## Current correction and behavior trace
Only N/internal/setup/hosted_config_test.go changes (test fixture/assertions).
Production platform.Mounts on Linux reads /proc/self/mountinfo, so the original
runner-only mount trap was never called. The absent default mount let detach
reach root Store ownership enforcement and an intentionally unusable Docker client.
Production safely retains these checks; no product runtime failure is inferred.

The corrected Linux fixture first verifies the already-present unrelated /proc
mount read-only. Valid hosted-config preflight then reaches the ordinary Status
source/protocol mismatch or Detach unrelated-source refusal before teardown.
Darwin still reaches its fake mount-command error. Specific error/call assertions
distinguish platform paths. Missing/changed/malformed configs still fail before
readiness/effects; current or partially missing config still reaches existing
checks on retry. Config/receipt bytes and file absence remain unchanged.
No proc write, mount operation, root bypass, new runtime seam, skip, migration or
fallback added. BEH005 host status/drained-detach invariants are preserved.

## Preserved reviewed implementation
| Behavior / AC | Actual path and outcome |
| --- | --- |
| BEH001 / AC001,002,006 | N root go.mod/cmd/internal imports use github.com/AutoByteus/autobyteus-nfs. Installer, packaging, five service Python suites and workflow are local. Go-to-Python fixture root resolves two levels up to N. S removes embedded service/workflow/installer/service suites; no sibling replace, app-source vendor or second maintained implementation |
| BEH002 / AC002,004,005 | N packaging/release.py hashes service-local inputs plus docs/filesystem-usage.md and testdata/connection.json, not arbitrary app bytes. Workflow is manual-only with publish=false, no desktop version assertion/automatic tag trigger. Candidate reuse/equality, cancellation/failure/current-source/native/signing/physical/user/existing-release gates remain. Empty qualification lock and disabled S Guide remain. License/CLA/notices/pins and section7 permission preserved |
| BEH003 / AC003,006 | S AgentRunManager prepares directly; native/Claude/Codex workspace resolvers preserve registered failure and prior unknown/no-selection policy. PtySessionManager uses ordinary cwd and normal lifecycle. Shared mount/binding/admission modules, all automatic scoped Git trust calls, launcher NFS module/hooks/download/hash and paired fixture/pin removed. No replacement mount detector. Generic launcher root/shared plus root/nodes/name and private volumes retained |
| BEH004 / AC007,008 | Both development histories preserved and source/evidence identities recorded. Owned isolated check resources cleaned; protected PM/retained engine hashes checked. Delivery completed paired source pushes; terminal CI/verification remains blocked, not full Task completion |
| BEH005 / AC009 | N CLI/setup/config become host-only create/connect/status/reconnect/drained detach. Removed app node discovery/control/HTTP probes/public descriptors and retired CLI options. Retained storage-engine Docker client/types/config/identity/capability checks. Source/marker/pending/permission/mount/busy-detach behavior preserved; 28 backend/platform/service production files normalized-equal after import change |
| BEH006 / AC010 | S prepare-private-runtime-skills and RuntimeSkillProfile acquire existing per-execution profiles uniformly for Claude/Codex/Grok. Exact owner registered before await; no bindings means no acquisition, not materializer fallback. Absolute private execution directory must resolve outside project including aliases. Existing managed-source/collision semantics and native capability errors retained. Process/client close precedes exact profile release; peers/project/source bytes preserved. Other ACP adapters retain filesystem-independent materializer behavior; Grok's now-dead materializer wrapper is removed |

N and S are path abbreviations defined above, not extra directories. Detailed changed paths: E/change-inventory.json. No editor implementation change.


The table records preserved implementation, not freshly repeated qualification.
The original extraction delta, source/pending identity, trusted incompatible
active/pending node refusal, exact private-profile process/client cleanup,
removed NFS/UUID/Git-trust admission and generic launcher ownership remain unchanged.
License/CLA/section7/notices/engine pins, manual-only nonpublishing-default workflow,
empty qualification and Guide instructions/disabled downloads are retained.
Runtime source sizes are unchanged; only a test changes, outside the hard source
size threshold. No newly discovered unrelated dead-code follow-up.

## Current implementation-scoped evidence
- E5/validation-plan.md precedes checks; E5/checks-and-limits.md and raw logs
  record exact scope, baseline failures, limits and skipped cases.
- Independent native Linux arm64 Ubuntu24.04 nonroot development container:
  baseline reproduces all hosted failure classes; corrected focused setup tests,
  full race7 packages, vet, build/version, Bash pass. Python20 collected,
  **17 executed/3 explicit installer/child skips**. Container-host bootstrap is
  intentionally skipped by the unchanged suite; not counted as passed.
- Independent native Darwin arm64: focused hosted-config/no-live-source-detach
  and full race7 packages/vet pass. Direct child skip remains covered by bootstrap
  parent. No hosted matrix completion claim.
- Three independent Linux mutation copies fail the intended assertions:
  ignored Status preflight, ignored Detach preflight, reject missing partial
  detach config. No compilation-only failures or changes to canonical code.
- Official Go1.27.2 downloads SHA-verified; native Linux GCC13.3/Python3.12.3,
  Darwin Apple clang17/Python3.14.2. E5 toolchain/command logs retain environment.
- Source hash on both OSes remains
  **348046594b470f7b294aa2162f78ec349eb57c4edf74aa2db32112a9dc9da90e**.
  Empty-qualification publish refusal still exit1 as expected. No engine rebuild/
  candidate qualification or new release metadata.
- Initial preparation root-path error failed before container/tests; corrected
  without product edits. Baseline/mutation failures explicitly retained.
- E5/source-audit.json proves only this test differs from intake, all copied inputs
  match and preexisting ignored cache is unchanged. S has no new impact.
- Frontend loop **Not Applicable**: test-only N change; no rendered behavior.

## Cleanup and remaining gates
Owned development container, source/toolchain copies and private home/temp removed;
no matching host process/cwd left. Only immutable Ubuntu image shared cache remains.
D0/PM/canonical app/source ignored cache/old engine assets and completed pushes
were not modified or removed. E5/cleanup.json scopes the receipt.

1. Targeted source/test review of IR005, then proportionate affected N validation.
   S API002 results carry with exact-input limits; no blanket S repeat or worktree
   recreation is needed for this test-only correction.
2. Native Linux arm64 fixture success is not GitHub Ubuntu amd64 job completion.
   Hosted failures and cancelled macOS job conclusions remain historical failures/
   limits until a reviewed current candidate passes new Developer Checks.
3. Delivery resumes fix-forward target freshness/receipts and terminal verification.
   **Paired repository source operations completed; terminal/AC007 receipt gate
   remains open.** R1 RELEASE prose was already synchronized by Delivery; do not
   create a duplicate docs task or replay ordered initial finalization.
4. No old editor/filesystem/VM/authenticated-provider campaign, new topology approval,
   live mount/node mutation, release, TaskDone, Terminal or user-verification claim.
