# Testing AutoByteus NFS

## Prerequisites and local checks

From this repository root, use Go (go.mod minimum 1.25.0; CI pins 1.27.2), Python3
stdlib and Bash on Linux or macOS. Go tests require Python3 for the bootstrap
permission fixture. No Node/pnpm, AutoByteus checkout, Go replace or sibling
module is needed. Install toolchains outside the source tree or in owned scratch.

```sh
go test -race ./...
go vet ./...
go build -o out/autobyteus-nfs ./cmd/autobyteus-nfs
out/autobyteus-nfs version
python3 -m unittest discover -s scripts/tests -p 'test_nfs_*.py' -v
bash -n scripts/public/nfs/install.sh packaging/sign-macos.sh
python3 packaging/release.py --source-hash
```

With actionlint installed, run `actionlint .github/workflows/*.yml` for workflow
syntax. Python workflow fixtures check a deliberate boolean subset, not hosted
Actions. The placeholder installer and `python3 packaging/release.py
--check-publish` must refuse while releaseReadiness is null; refusal is expected,
not a working public install command.

Use `CGO_ENABLED=0 GOOS=<darwin|linux> GOARCH=<arm64|amd64> go build -o
<owned-output> ./cmd/autobyteus-nfs` for compilation. Cross-compiled tests/binaries
are not runtime qualification. `-race` needs a matching native compiler; do not
silently drop it and claim race coverage.

## Evidence layers and isolation

Unit/fixture checks exercise temporary files and doubled command/Docker
boundaries. The native Mac source test reads diskutil for its own test directory;
it does not reboot or qualify NFS. The installer Python suite's Go-child mode is
covered by TestBootstrapDirectoryModes, and explicitly skips without that child
when run alone; container-host skip is intentional. Record skips, not Pass.

Run extraction checks in an independent source archive/clone with a private
HOME/TMPDIR and no sibling checkout. Keep current candidate source/commit,
commands, logs, platform and tool versions in ticket evidence. Build outputs,
engine bundles, generated release metadata and caches belong to owned scratch;
never use old builds as proof of current source or commit these generated inputs.
Preserve unowned files and stop/remove only processes and scratch you created.

Ordinary development checks need no root, mounts/exports, live Docker nodes,
provider credentials, user app data, or published release. Do not invoke installed
create/connect/reconnect/detach as a test. A necessary live integration campaign
requires separately scoped, test-owned resources and authorization; neither a
passing fixture nor this repository extraction authorizes one.

Packaging checks may copy an exact retained engine candidate read-only into own
scratch and freshly verify it with packaging/engine/manifest.py. Distinguish actual
arm64 artifact checks from synthetic both-architecture controls; never invent an
amd64 artifact or reuse old source qualification. No engine rebuild is needed
when unchanged verified artifacts suffice. Distribution gates are in
[packaging/RELEASE.md](packaging/RELEASE.md).

Host-only fixtures cover incompatible active/pending records, refusal before
resource/binary effects, exact current writes, engine-only Docker operations,
source/pending/permission/mount/busy-detach preservation and removed CLI rejection.
Consumer checks live independently in their app repository: ordinary paths,
registered resolution/errors, process lifecycles and private execution profiles.
No public attachment fixture, consumer commit pin or paired equality check exists.

Fix demonstrated in-scope failures; disclose failed attempts and environmental
limits. New behavior/design needs return to its owner. Do not silently weaken
checks or reopen unrelated completed filesystem/editor work. No test result is
user verification, physical/platform qualification or release authorization.

## Release-control changes

Run all `test_nfs_*.py` suites. Record fixtures parse real candidate/OCI/native
archives, strict JSON and readiness references; engine bytes/check receipts/
authority statements in them are synthetic and must never enter the real lock.
Publication fixtures double GitHub/registry boundaries and check same-payload
retry, conflicting assets/images, stage order and main drift. Signing fixtures
execute the actual shell with fake commands/credentials, checking Accepted-only
behavior and cleanup, not Apple acceptance. They inject stage failures and TERM,
check sanitized stderr/failure receipts (including hostile private tool output),
preserve exact command exit status and existing receipts. Codesign failure fixtures
also check literal diagnostic categories, unrecognized/oversized/non-UTF8 output,
parser failure and successful-command precedence. These categories describe tool
observations, not a proven root cause; all raw output stays in private transient
scratch and is removed. Checks cover keychain-list
capture/configure/restore with multiple prior paths (including spaces and shell
metacharacters), configuration failure before signing, and cleanup failure refusal.
The codesign double requires owned-keychain search membership, matching the
controlled native synthetic-identity reproduction; this is not real Developer ID
or hosted signing proof. Workflow receipt glob checks exclude
private files; only actual hosted execution proves artifact upload and real signing.
Installer fixtures use actual tar/hash
tools and an inert binary. Workflow truth tables cover candidate/fresh/resume/recover modes
and failed/cancelled/legitimate skipped ancestors; actionlint checks YAML separately.
The workflow suite also executes the native metadata prefix with `/bin/bash`
(including the Mac system Bash3.2) and inert release-command boundaries: exact
candidate/fresh argv, command failure, missing input and pipeline failure. This
is shell invocation coverage, not native metadata/build or hosted-matrix proof.
No fixture is a hosted run, public download or qualified physical platform.

An independent source archive is sufficient for normal runtime checks; release
identity checks require an independent Git clone with the relevant commit ancestry.
Retain source identity/logs and tool versions. For release work, all four native hosted checks,
current complete engine/OCI candidate, actual release-control/source-review
evidence, real notarization and public downloads remain API/Delivery gates.
Shared-filesystem/physical and user tests are explicitly deferred until after the
first signed release, not inferred from builds or required for publication/closure.
The release schema is documented in packaging/RELEASE.md. Do not fabricate receipts
or automatically mark the readiness lock populated from test success.

On macOS, place the independent source checkout/copy in an owned local APFS
development directory, **outside** `/private` and `/tmp`. Source-binding fixtures
create their owned project below the package cwd and intentionally preserve the
production refusal of system/private/ephemeral sources. HOME/TMPDIR/cache may
still be private scratch. A bad fixture location is not a reason to weaken that
guard or skip native tests.

For a Linux container local-check harness, extract the independent source archive
and create HOME/TMPDIR/cache **inside the guest filesystem**, not on a Docker
Desktop host bind. Host-bridged file-lock behavior is not native Linux flock.
Use read-only input archives and copy only owned result files out. Container-host
installer refusals remain explicit skips, not host installer qualification.

Current runtime schema2 uses releaseTargets and fieldValidation (filesystem/user
both deferred). Native CLI tests exercise strict release-only decoding, legacy/
unknown/duplicate claim refusal, target/equality checks, stderr notice and exact
version stdout; installed host-state additive decoding stays unchanged. Payload
fixtures rehash tampered notes/provenance to prove semantic deferral enforcement,
and engine-lock fixtures execute the actual reset operation. These are local
release-boundary checks, not field testing. Readiness must use genuine current
records at stable paths, prepared by Delivery after affected API validation.


## Immutable-publication executor repairs

Run all Python suites, actionlint and Bash checks for release-control repairs.
Recovery fixtures create real separate C/P/H/E Git commits and synthetic artifacts
inside owned scratch, then execute the complete current verifiers. They cover
fixed repair scope, preserved original lock/evidence, H/E equality, admission and
read-only inspection, bounded source projection, original payload/native/signing
job proof and no-effect failures. Endpoint doubles model by-tag404 with publisher
list/direct-ID draft visibility, unique paginated inventories, ID uploads, ambiguous
POST outcomes, immutable drift and read-only completed reconciliation. They are
not actual Actions, Apple, public upload or release proof. Synthetic recovery
records must never be copied into packaging/recovery in the real repository.

Use inspect-bound from the corrected reviewed checkout for actual retained-input
verification before Delivery's genuine authorization exists. After admission,
prepare/publish independently repeat validation and never trust the inspection
report or downloaded preflight as authority. Exact old signed bytes and engine/OCI
checks can carry for this executor-only repair; do not rerun native signing or
build a new candidate solely to repair a bound publisher. New unbound product
payloads still require current-source candidate/native evidence. Delivery owns
actual hosted same-byte recovery and public download/install/signature receipts.

## Setup dashboard — source tests and published launch

Ordinary Go race/vet tests cover admin ownership, exact leases, same-binary pipes,
real local HTTP security, cached-operation responsiveness and directory-only
selection with owned temporary inputs. The subprocess broken-pipe tests close
real read ends and observe the held lock before/after drain. These do not invoke
sudo or mount/export storage. The private transport is not an application API.
Python `test_nfs_dashboard_packaging.py` checks JS/CSS hash inclusion and static
embedding; compilation does not retroactively add the UI to published v0.1.0.
The dashboard is distributed starting with v0.2.0. Release launch checks use an
actual downloaded installed binary, private HOME/TTY and an owned sandboxed
browser without authorizing administration; they do not replace native storage
or field testing.

For a rendered local feedback loop, use an **independent owned source copy** and
private HOME/TMPDIR/cache. A dev-only Playwright1.64.1 installation and its Chromium/
WebKit binaries can live in owned scratch; no Node dependency enters the Go build:

```sh
# In the independent source copy; outputs/dependencies are outside the checkout.
go test -c -tags=dashboardpreview -o "$SCRATCH/dashboard-preview" ./internal/dashboard
npm install --prefix "$SCRATCH/browser-tools" --no-audit --no-fund --ignore-scripts playwright@1.64.1
PLAYWRIGHT_BROWSERS_PATH="$SCRATCH/browsers" node "$SCRATCH/browser-tools/node_modules/playwright/cli.js" install chromium webkit
NFS_PLAYWRIGHT_MODULE="$SCRATCH/browser-tools/node_modules/playwright/index.js" \
NFS_PREVIEW_BINARY="$SCRATCH/dashboard-preview" NFS_PREVIEW_SCRATCH="$SCRATCH" \
NFS_PREVIEW_EVIDENCE="$SCRATCH/browser-evidence" PLAYWRIGHT_BROWSERS_PATH="$SCRATCH/browsers" \
node internal/dashboard/__tests__/browser.cjs
```

The explicit build-tagged preview serves actual embedded HTTP/assets and uses a
subprocess **root-protocol double**. It cannot install or mount. Both roles at
1280/390, bootstrap/reload, keyboard, chooser, exact review/consent, read-only
configuration, wrong-role/pending/errors, slow work, copy success/failure boundary
and drained disconnect are exercised. Clipboard is doubled to avoid changing the
operator's clipboard. Screenshots require actual inspection, not existence-only
claims. Preview contexts/processes and directory fixtures are cleaned by the
runner. No compiled fixture or dependency is committed.
The `chooser-poll` and `chooser-post` cases hold one **actual directory HTTP
response** until keyboard prefix entry, then release it before typing the suffix.
They check draft preservation, settled input, explicit List/parent/child/selection
and listing errors; scheduling is controlled, not native storage latency proof.
Run only those plus normal controls with
`NFS_PREVIEW_SCENARIOS=chooser-poll,chooser-post,normal` on the same command.

Native privilege/storage checks require task-owned disposable Mac26+ and
Ubuntu24.04 guests; never run tests against operator root state. Verify public
ordinary-user/TTY launches, actual sudo/identity/pipe/lock/EOF/signals, service
without SUDO/TTY, and control-originated server/client/status/reconnect/drained
detach using private guest-only sources and actual nonroot mounted bytes. Linux
Docker storage must use its owned guest daemon, not Docker Desktop on the host.
Record every resource, current executable/source identity, outcomes, failures and
cleanup. Preserve source/marker/recovery evidence during detach. Hard-NFS calls
are not force-cancelled to produce a cleanup claim.

Native Linux development builds need actual freshly verified pinned engine
packages and Ubuntu package metadata in a disposable build tree. Carry an actual
current source hash, `version: development-dashboard`, empty `releaseTargets`,
and deferred field statuses. Do not alter the repository lock or public
metadata/installer to make that build admitted as a release. Reuse matching
retained engine bytes read-only and distinguish cross-compilation from native
execution. These virtual journeys are not the separate physical field campaign.

### Terminal approval-feedback checks

The ordinary dashboard Go tests cover both roles, real child pipes with controlled
hello/inspection completion, fixed safe failure categories, duplicate/new attempt
feedback, helper drain, dead-helper refusal of ready text and Stop races. A
private scheduler exercises obsolete/one-shot reminders; one held-hello test
observes the actual 10-second reminder without treating it as authority. No test
reads a password, invokes sudo, or changes OS approval policy/storage. Writer
failures do not control host operations. These are not OS cached-consent proof.

A focused current-page/PTY journey may use the build-tagged feedback fixture recorded in implementation evidence, in
an owned preview binary, private HOME and browser profile. This serves actual
Session/HTTP/assets with an ordinary-user protocol child and signal/Stop driver;
it deliberately does not invoke the OS opener or the installed privileged CLI.
Keep the private launch URL/token out of durable transcripts. Browser visual
layout is unchanged; check authorize/progress/result/Stop alongside terminal
ordering. Native root/storage campaigns are not required solely for terminal
presentation changes; preserve their separate evidence boundaries.

## Downloaded standalone Mac CLI verification

For the exact public binary, require strict signature/DeveloperID/team/runtime/
timestamp and equality to its genuine Accepted notary receipt, then run:

```sh
codesign --verify --strict --verbose=4 --check-notarization -R=notarized /owned/path/autobyteus-nfs
```

This forces an online notarization requirement. Apple DTS distinguishes this
[other-code check from app assessment](https://developer.apple.com/forums/thread/130560).
App-style `spctl --assess --type execute` may report valid code that is not an app
for this standalone CLI; retain that observation, not a false Gatekeeper Pass.
Never disable security policy or clear quarantine to manufacture a pass. Online
code checks and the advertised curl/CLI install are not fresh quarantined-Finder,
offline, independent-host or physical/user qualification.
