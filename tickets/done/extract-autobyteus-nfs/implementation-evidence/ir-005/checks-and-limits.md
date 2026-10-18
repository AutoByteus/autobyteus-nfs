# IR005 — DR002 native Linux fixture correction

Source candidate: 09cac96225fe4f36fb0dcbe6ddec01248992874f; baseline56c0c59 / published22e934b.
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

Artifact hygiene: initial staged whitespace check reports raw command output /
unified-diff context. Exact bytes are retained; artifact-whitespace.json lists
exceptions. The staged check excluding only those raw artifacts passes.
