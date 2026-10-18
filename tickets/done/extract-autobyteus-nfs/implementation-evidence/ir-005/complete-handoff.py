from pathlib import Path
import json,hashlib
E=Path(__file__).resolve().parent;T=E.parent.parent
source=json.loads((E/'candidate-inputs.json').read_text())['commit']
assert json.loads((E/'cleanup.json').read_text())['scratch_removed']
(E/'checks-and-limits.md').write_text("""# IR005 — DR002 native Linux fixture correction

Source candidate: """+source+"""; baseline56c0c59 / published22e934b.
Only internal/setup/hosted_config_test.go changes. Large/High remains.

## Failure origin and bounded correction
Darwin platform.Mounts invokes the runner; Linux reads /proc/self/mountinfo.
The old fixture assumed the runner error on both hosts. On Linux its absent
default mount correctly reported not-mounted during Status and let Detach
advance to real later checks: the root-owned package-mask Store rejected the
nonroot private directory, and the deliberately unusable Docker client panicked.
These are fixture assumptions, not evidence that production trust checks fail.

Linux fixture now verifies its existing unrelated /proc mount read-only and
uses that target. Status stops at normal source/protocol mismatch; Detach stops
at the existing unrelated-source refusal before job/package/engine effects.
Darwin keeps the injected mount-command failure. No proc/mount writes, root
fixture, production seam, skip or runtime-policy change. Exact error and command
counts are asserted per OS. Invalid/missing Status config must specifically
fail configuration preflight, not merely return any error. Current/missing
Detach retries and Apple/connect-only controls preserve private record/config
bytes and absent files. Existing intentional unusable Docker sentinel remains
unreached; no fake live daemon or nil-client production fallback was added.

## Fresh execution
- Native Linux arm64, Ubuntu24.04 user1001 in owned Docker development container
  (LinuxKit kernel, native architecture, NOT amd64 emulation or hosted Actions).
  Go1.27.2 and GCC13.3, Python3.12.3. Independent baseline reproduces hosted
  Status/current, native Detach/private-owner failures and Docker nil-client panic.
  Baseline expected exit1 retained, not reclassified as green.
- Corrected Linux focused hosted-config tests pass; full go test -race ./...
  passes7 packages, go vet/build/version/Bash pass. Python20 collected,
  **17 executed /3 skips**: two installer cases deliberately refuse container
  hosts; one child-only installer fixture. Go's BootstrapDirectoryModes is also
  explicitly container-skipped and direct InstallerDirectoryModeChild skips
  without its parent. No container-installer coverage claim.
- Native Darwin arm64 Go1.27.2: focused hosted-config plus
  TestDetachDoesNotRequireLiveSource pass; full Go race7 packages and vet pass.
  Existing bootstrap parent exercises its child; direct child-only skip is
  intentional. This round does not claim fresh full macOS Developer Checks
  workflow/Python matrix completion.
- Three Linux mutation controls fail intended assertions (not compilation):
  ignored Status verification, ignored Detach verification, and rejection of a
  missing configuration during partial detach. Originals retained unchanged.
- Both source hashes remain348046594b470f7b294aa2162f78ec349eb57c4edf74aa2db32112a9dc9da90e;
  expected publish refusal exit1 (empty qualification). No engine artifacts used,
  rebuilt or qualified.
- Current independent copy inputs match canonical source; only test file differs
  from intake. Production/config safety/workflow all unchanged.
- Initial preparation selected tickets as source root (off-by-one path); failed
  before container/test creation. Corrected root, reused verified official Go
  downloads; attempt-1 preserved. No candidate test failure. Baseline and mutation
  failures are deliberate controls, separately identified.

## Carry / limits / cleanup
S runtime/docs finalization has no new impact; API002 S results carry with their
exact-input limits. No S worktree recreation or blanket S repeat. Current N
fixture correction still needs independent targeted source/test review and
affected validation. Hosted runs39097778705/39097779223 remain failures; local
arm64 fixtures do not clear hosted Ubuntu amd64 or cancelled macOS job receipts.
Delivery owns fresh checked-candidate publication/CI and final verification.

Only exact owned development container/source copies/toolchains/homes/temp removed,
no matching host process/cwd remained. Pulled immutable Ubuntu base is shared cache,
not a live resource or published image. D0/PM, ignored source cache, canonical app,
old retained engines and histories untouched. No target action/release/tag/deploy
or TaskDone/user-verification claim. Prior successful paired pushes stand.
""")
(E/'attempts.md').write_text("""# IR005 attempts
1. Initial preparation script used E.parents[3] instead of E.parents[4] for N,
   copied ticket files to owned baseline, and failed on missing
   tickets/packaging/release-lock.json before container or tests. Preserved script
   and result in attempt-1. Corrected root; discarded only that wrong owned copy;
   official SHA-verified Go downloads reused.
2. Native Linux baseline hosted-config run expected exit1 and reproduced the
   actual CI errors/panic. This is failure reproduction, not a candidate pass.
3. Corrected native Linux and Darwin checks passed first run. Three mutation
   copies deliberately fail named assertions; no mutation entered source.
""")
old=(E/'prior-implementation-handoff.md').read_text()
trace=old.split('## Reviewed behavior implementation trace\n',1)[1].split('## Key implementation boundaries',1)[0]
trace=trace.replace('Delivery finalization remains pending; no false full Task completion','Delivery completed paired source pushes; terminal CI/verification remains blocked, not full Task completion')
handoff="""# Implementation Handoff — Extract AutoByteus NFS

## Current result
**IR-005 — DR-002 implementation-owned Local Fix complete; Ready for targeted independent source review and affected validation.**
Task project_task_fdb2c737-fb08-48cf-8aca-e04df2d02ae8.
Personal execution only; no delegation. Not Delivery Completed/TaskDone.

## Authoritative paths and completed operations
- **N** /Users/normy/autobyteus_org/autobyteus-nfs-worktrees/extract-autobyteus-nfs,
  recovery branch codex/extract-autobyteus-nfs, target origin/main.
  Current test correction **"""+source+"""**, based on blocker checkpoint
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
"""+trace+"""
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
"""
(T/'implementation-handoff.md').write_text(handoff)
history=T/'implementation-revision-record.md'
assert history.read_bytes()==(E/'prior-implementation-revision-record.md').read_bytes()
with history.open('a') as f:f.write("""
## IR-005 — DR-002 hosted Linux configuration-fixture correction
- Trigger: delivery_engineer DR-002 Blocked / Local Fix, archived handoff-summary.md / delivery-revision-record.md / delivery-evidence/dr-002/ci. No new numbered CR finding.
- Prior result: IR004 Ready, then CRR005 source Pass100, API002 Pass95, CRR006 no-test-delta satisfied. Delivery completed ordered N/S pushes but newly executed Ubuntu CI failed; those earlier local results remain exact-input history.
- Current result: bounded fixture correction with fresh native Linux/Darwin implementation checks complete; Ready for targeted source review/affected validation, not hosted matrix or Delivery completion.
- Authority/classification: R2 Approved/SR003, SR004 Ready, ARCH002; Large/High/Reviewed unchanged. No new approval, Design Impact or Requirement Gap.
- Behavior: BEH005 host readiness/drained-detach preflight and configuration retention preserved; BEH004 source operations completed but terminal verification still open. No production behavior change.
- Cause/delta: hosted_config_test.go assumed both platforms observed mounts through Runner. Linux reads proc directly. Missing default mount bypassed that test trap and reached real root-owned package-mask refusal / unusable Docker test client. Linux fixture now verifies existing unrelated /proc mount read-only, expects ordinary not-mounted/unrelated-source refusal with0 commands; Darwin retains fake mount failure with1 command. Specific config-error assertions and exact record/config retention cover current/missing retries and Apple/connect controls. No root bypass/skip/new production seam.
- Identity: N"""+source+""" atop56c0c59. Runtime83726b and production source hash348046594b470f7b294aa2162f78ec349eb57c4edf74aa2db32112a9dc9da90e unchanged. Published N22e934b / S ticket9b72c8d1→personal55bff1f5 remain intact; S worktree retired, not recreated. D0 is populated main, not an authoring workspace.
- Fresh validation: native nonroot Linux arm64 Ubuntu24.04 Go1.27.2 baseline reproduces hosted failures; corrected focused tests/full Go race7packages/vet/build/version/Bash pass; Python20collected17executed3skips (container/child policy). Native Darwin focused/full Go race7packages/vet pass. Three Linux preflight/partial-detach mutations fail intended assertions. Source/copy integrity and expected unqualified publication refusal pass. No amd64-hosted matrix pass claimed.
- Attempts: initial harness path calculation failed before container/tests; corrected and retained. Baseline/mutation failures deliberate, not hidden candidate failures. No engine/provider/live-storage campaign or S rerun.
- Cleanup: owned development container/toolchains/copies/home/temp removed; immutable pulled Ubuntu image is shared cache only. D0/PM/ignored cache/canonical app/old engines unchanged. Frontend loop N/A.
- Evidence: archived implementation-evidence/ir-005, validation-plan.md, checks-and-limits.md, baseline/candidate/mutation logs, source-audit.json and cleanup.json. Prior IR001–004 byte prefix preserved; current handoff authoritative.
- Next/limits: fresh most-specific source Local Fix route then affected validation; Delivery owns refreshed reviewed candidate/hosted checks and remaining terminal receipt. No target action, undo/replay of completed pushes, tag/release/deploy/TaskDone/Terminal/user verification.
""")
assert history.read_bytes().startswith((E/'prior-implementation-revision-record.md').read_bytes())
(E/'final-checks.json').write_text(json.dumps(dict(revision='IR-005',trigger='DR-002',classification='Large/High/Reviewed',candidate=source,history_prefix_preserved=True,production_unchanged=True,native_linux='arm64 Ubuntu24.04 development container, UID1001, Go1.27.2',linux_packages_race_passed=7,linux_python_collected=20,linux_python_executed=17,linux_python_skipped=3,darwin_packages_race_passed=7,mutations_caught=3,hosted_CI='Not rerun; prior runs remain failed/cancelled',S_impact='None',completed_paired_pushes='Preserved, not repeated',release='None authorized',cleanup='Complete for exact owned live resources and scratch'),indent=2)+'\n')
print(source)
