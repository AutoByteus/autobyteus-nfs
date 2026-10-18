# AutoByteus NFS

A standalone, app-independent service for sharing **one chosen project folder**
between trusted computers. It does not sync, copy or back up projects.

**Release status:** first normal **v0.1.0** release preparation is in progress;
no successful public release is claimed yet. Current native/build, release-control,
source-review and release-first authorization evidence has been accepted in
[the stable v0.1.0 readiness record](packaging/releases/v0.1.0/readiness.json).
Actual signing/notarization and public download receipts remain pending. Shared-filesystem/physical and user testing
is **deferred until after publication**, not passed or a release prerequisite.
Distribution/signature checks are not field qualification.
The application Guide stays disabled; internal CI candidates are not public
installers. See [release procedure](packaging/RELEASE.md).

## Validation boundary

This is the independently maintained source repository. Extraction checks prove
standalone development/packaging and the host-only boundary, not physical
platform qualification. See [EXTRACTION.md](EXTRACTION.md) for exact original
source and attribution, [TESTING.md](TESTING.md) for local checks and
[filesystem usage](docs/filesystem-usage.md) for ordinary directory consumption.

Historical command-only filesystem evidence used two generic containers sharing
one Ubuntu VM's real NFS mount/kernel/cache, with native-Linux and Docker-Linux
storage sequentially. It is not independent-client, physical, Mac/cross-OS or
publication qualification. Its results remain historical, not promoted by this
move. The [archived original delivery](https://github.com/AutoByteus/autobyteus-workspace/blob/3712cd9bf0db998501d162db7f8655f169e3def6/tickets/done/shared-network-workspaces/handoff-summary.md)
records that bounded evidence. No old application/editor campaign is a gate for
this repository extraction. Distribution readiness remains separate under
[packaging/RELEASE.md](packaging/RELEASE.md); the app Guide stays unavailable.

## Intended host modes and downloadable build targets

| Storage computer | Export engine | Source | Protocol |
| --- | --- | --- | --- |
| Native macOS 26+ | Apple system nfsd | local APFS | NFSv3/TCP |
| Native Ubuntu 24.04 | corrected Ganesha 4.3/VFS | local ext4 | NFSv4.1/TCP |
| Docker on a Linux computer | same Ganesha/VFS image, host networking | explicitly selected ext4 bind | NFSv4.1/TCP |

Native Mac/Linux host clients are included. Consumers use ordinary directories;
container bind mappings are configured separately by their operator. Docker Desktop on Mac is not a storage-server option; use
native Mac hosting instead. Windows, public/multi-tenant service, offline sync,
HA, automatic remote notifications and application-node management are not
included. Release metadata advertises four distribution targets (darwin-amd64,
darwin-arm64, linux-amd64, linux-arm64), not independently field-qualified support.
Intended host floors above remain unchanged; compilation is not field validation.

Linux engine delivery uses the reviewed Noble backport `4.3-8ubuntu1+autobyteus1`,
not unpatched stock4.3. The matching packages are embedded in Linux release
binaries and shared with the Docker image; users need no compiler/PPA or extra
package command. This distribution path is still under validation.

## Versioned download (after publication is confirmed)

Advertised CPU targets are ARM64 and x64 for native macOS26+ and Ubuntu24.04.
The first release is normal v0.1.0, not beta. These are the exact intended versioned
commands; **do not treat a missing/draft release as a working download**:

```sh
curl --fail --location --proto '=https' --tlsv1.2 \
  https://github.com/AutoByteus/autobyteus-nfs/releases/download/v0.1.0/autobyteus-nfs-install.sh \
  -o autobyteus-nfs-install.sh
less autobyteus-nfs-install.sh
bash autobyteus-nfs-install.sh version
~/.local/bin/autobyteus-nfs version
```

Inspect the script before executing it. SHA256SUMS-nfs covers every distributed
file except itself; compare the installer hash as well as the archive/manifest
checks that the installer performs. Checksums do not protect against a compromised
publisher. Mac native payloads require Developer ID and Accepted notarization;
do not disable Gatekeeper or promise offline first-use validation. Standalone
binaries cannot have tickets stapled. No Go/Node/Python/Homebrew is required.
Use an owned HOME for a download smoke and pass **version**, not an implicit setup.
After installation choose create/connect explicitly with normal displayed consent;
no installation smoke authorizes storage changes on the user's computer. The
installer emits a deferred-field/user-testing notice on stderr after successful
manifest admission; `version` stdout remains the exact version.

## Intended first-use journey

A published, versioned bootstrap will download a checksum-verified archive and
manifest, validate archive members and the binary's embedded release metadata,
then execute the installed binary immediately. It needs no Go, Node or Python on
the participant. It reads prompts from `/dev/tty` even when piped to Bash. The
bootstrap does not change the invoking shell's PATH; it installs the user CLI at
`~/.local/bin/autobyteus-nfs` and invokes its absolute versioned path.

The command offers **Create** or **Connect**. Create asks for the ordinary source
folder, deployment and selected private hosts/subnet. Existing files remain in
place. Connect consumes bounded JSON printed by the storage computer, not shell
commands or an access token. Both flows display the host storage/mount plan
before applying it. They never discover or recreate application containers.
Necessary administrator and drain approvals are part of that invocation.

The default project root is `/Volumes/autobyteus-shared` on both operating systems.
A nonempty or writable unmounted target is refused, not hidden or emptied; choose
an explicit empty alternative. Setup prints the actual root. Select a project
beneath it as an ordinary AutoByteus workspace. Each other computer still runs its
own connection flow. Closing AutoByteus does not stop this service.

Installed commands: `create`, `connect`, `status`, `reconnect`, `detach`, `version`.
No arguments selects first-use setup or configured status/actions. Noninteractive
setup requires explicit inputs and administration consent (`--yes`). Detach
requires drained export/mount users (`--drained` with `--yes`). Connection input is never evaluated as shell.

## Data, trust and limitations

- The source contains a persistent `.autobyteus-nfs/storage.json` UUID and an owned
  health directory. Mac APFS volume UUID + directory inode (Linux device + inode),
  actual mount source/protocol, marker and
  nonroot synced-write/read/remove checks distinguish an attachment from a same-
  named local directory. No Git repository is created as a health check.
- NFS uses **unencrypted AUTH_SYS, coarse host trust**. An allowed subnet trusts
  every computer in it; a host allowlist is narrower. NAT identifies the computer,
  not individual containers. All writes, including client-root writes, map to the
  selected nonroot source identity. No root export or recursive chmod/chown is
  used. Do not expose these ports to the public internet.
- No firewall/router/UPnP rules are changed automatically. An existing network
  policy must permit the displayed private participants. Ganesha uses TCP2049;
  Apple also needs RPC111/mountd20048. Conflicting existing Apple/global engine
  settings are refused rather than disabling another export.
- Hard mounts protect normal write semantics but can **stall file operations,
  previews, agent startup/terminal work and unrelated application work** during
  storage loss. Status itself can wait. Restore storage/network connectivity
  before retrying. There is no local mirror, soft mount, forced unmount, guaranteed
  cancellation deadline or v1 outage-isolation guarantee.
- Deliberately reload/reopen to observe remote changes. Do not rely on remote
  filesystem watcher events. Healthy media, HTML/relative assets and completed
  artifact previews keep the existing streaming endpoints and policies.
- Coordinate same-file edits and Git index/branch operations. Different-file
  work is supported, not merged by the service. NFSv4 uses server locking; the
  selected Apple NFSv3 path uses local-only advisory locks, not distributed lock
  coordination. APFS case/Unicode behavior remains the source's behavior.
- Back up the source independently. Configuration rollback is never data rollback.

## Private state and lifecycle

Private configuration/receipts are root-owned under
`/Library/Application Support/AutoByteusNFS` or `/var/lib/autobyteus-nfs`.
The separately traversable root-owned executable is at
`/Library/AutoByteusNFS/libexec/autobyteus-nfs` or
`/usr/libexec/autobyteus-nfs/autobyteus-nfs`; nonroot probe children must be able to
execute it without opening private configuration. Fixed launchd/systemd jobs do
not read user-writable shell state or depend on the desktop application.

Private `attachment.json` describes only the host mount. No public application
attachment descriptor is produced, read or repaired. The Docker API is used only
for this service's owned Ganesha storage engine, never for application nodes.

Pending setup is explicit, not a persisted READY flag. Resume requires a fresh
plan and consent; the supervisor does not resume an incomplete setup. Healthy
repeat/reconnect preserves source UUID. Safe drained detach retains source/marker
and private recovery evidence; a busy unmount fails without force/lazy unmount.

Existing active or pending predecessor node-management obligations refuse before
root binary replacement and administrative/supervisor resource effects, under the
administrative lock. Empty/null old node lists are harmless; nonempty or malformed
ones are not silently discarded. Use the matching predecessor tool for explicit
operator drain/recovery before installing this host-only tool. This task neither
migrates live installations nor deletes old descriptors or node receipts.

Owned native Linux and Linux Docker Ganesha exports set
`Attr_Expiration_Time = 0` at EXPORT level so fresh source attributes are not
hidden behind the server's default cache window. Client hard NFSv4.1 mounts keep
`actimeo=1`; Apple exports are unchanged. The healthy acceptance target is a
fresh open seeing a synced/closed source write of up to 1 MiB within 5 seconds,
not instant watcher notification or visibility through an already-open handle.

Status verifies the hosted Ganesha configuration before reporting host readiness;
it does not rewrite configuration or restart an engine. Detach checks an existing
configuration before touching mounts, jobs or engines. Different or
unreadable bytes are retained and refused. Missing configuration permits retry
of an already-partial owned detach, but never readiness. Exact unit/container
ownership checks and source/marker/recovery preservation still apply.

There is no live configuration migration or hot-reload promise. For disposable
older test setups, drain and detach with their matching candidate **before**
installing the corrected candidate, then set up again against the preserved
source and marker. Do not overwrite a different config or delete the source to
get past refusal. Matching disk bytes alone do not prove a running daemon loaded
a changed policy. Reuse of retained supported deployments would require a
separately established transition, not this test-fixture procedure.

Consumers, including AutoByteus, use ordinary filesystem APIs. This service does
not inspect their workspaces, skills, credentials, processes, APIs or runtime
modules. Consumers do not use NFS metadata to admit workspaces. Provision paths
outside the app: an ordinary directory that remains after mount loss is still a
directory to the app, and OS I/O can block or fail. No app wrong-mount safeguard
is promised by this repository.

### Mac source identity and interrupted setup

Native Mac captures the actual open source directory's APFS volume UUID with the
trusted system `diskutil info -plist` command. Raw device numbers can change at
boot and are not saved as Mac identity. A different volume or directory is
refused even if its marker and project bytes were copied; there is no identity
refresh, marker fallback or automatic repair. APFS UUIDs are not cryptographic
proof against a privileged clone/spoof of a volume.

A newly created source is bound and saved to the existing pending intent before
marker/handle/export work. An interrupted setup needs a fresh displayed plan and
consent; a complete binding is reused, never reselected from the current path.
Status does not repair identity, and detach does not require a live source.

No supported released device-only Mac predecessor has been established for this
unqualified package. Known owned test setups using that old binding must be
**drained/detached with their matching old CLI before replacing it**, then freshly
created on the preserved source/marker/storage UUID. The current CLI refuses an
old or incomplete Apple binding; never hand-edit it or infer its original UUID
from today's path. Evidence of an actual supported retained installation requires
a concrete transition assessment, not this disposable-fixture procedure.

## Developer checks (not live-resource authorization)

From this repository root, with Go (CI pins 1.27.2), Python3 and Bash:

```sh
go test -race ./...
go vet ./...
go build -o out/autobyteus-nfs ./cmd/autobyteus-nfs
```

Source identity tests cover strict plist/variant parsing, descriptor correlation
and closure, bind-before-failure, bound retry/refusal and unchanged Linux identity
shape. One Mac test reads installed diskutil metadata for its own directory; this
is not whole-host reboot or mounted NFS qualification.

Unit tests use temporary owned files and fake Docker HTTP responses; they do not
mount/export storage or alter real containers. Cross-compilation and `version` smoke do not
prove native NFS or installer behavior. Root [TESTING.md](TESTING.md) applies. The historical command-only
increment and local extraction checks do not establish field qualification.
Current build/release-control, signing, integrity and public install/version checks
remain publication gates. Independent physical Mac/Linux/Docker filesystem and
genuine user tests follow publication, with findings fixed in a new release.
Delivery carries the scoped follow-up to Solution Designer and the requesting PM;
those deferred tests are not this first release task's closure prerequisite. This release does not reopen old application/editor or
provider campaigns; the publication guide defines its current NFS-only gates. Do not run privileged setup
or provider calls merely because a design review passed.

See [packaging/RELEASE.md](packaging/RELEASE.md) for distribution gates and
[THIRD_PARTY_NOTICES](THIRD_PARTY_NOTICES) for backend/runtime notices.
