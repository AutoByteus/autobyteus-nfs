# Local NFS setup dashboard (v0.2.0+)

The dashboard is embedded in the **published v0.2.0 executable**; no separate web
installation is required. Published v0.1.0 does not have these commands. See the
[versioned download instructions](../README.md#versioned-download). Publication is
not field/platform qualification. You still need a native macOS26+ or Ubuntu24.04 host,
an ordinary local user, an interactive terminal and OS administrator approval.
No application, Node runtime, separate web server or remote account is needed.

Run `autobyteus-nfs server` on the storage computer, or
`autobyteus-nfs client` on a computer that will mount the share. These role
launches accept no flags. Existing no-argument/create/connect/status/reconnect/
detach/version and installed `service` entry forms remain supported. Do not run
the dashboard command under sudo: only its administrative child is privileged.

## Open and authorize

The program listens on an ephemeral **127.0.0.1** port. It opens a private local
HTML launch file with your OS association. If this opens an editor, fails, or no
browser is available, use the PRIVATE one-time local URL printed in your terminal
in a browser. Keep the URL private; it is a capability, not a share invitation.
The fragment is removed as the page opens. Authorization stays in this tab's
session storage for reload and disappears when this process stops. No cookies,
remote scripts, analytics or public/LAN management listener are used.

Choose **Authorize administration**. Switch to the launching terminal for sudo's
OS approval prompt; never type a password into the page. This installs/uses the
same root-owned control executable and starts its pipe-only helper. It reads
private configuration but does not automatically mount, probe, reconnect or
export storage. Denied or expired approval requires a new explicit authorization;
no alternate root path is used. Idle administrative authorization expires after
15 minutes without work (an active review completes its own lifetime first).

### Terminal feedback in the current source

This feedback improvement is source-only; the published v0.2.0 binary does not
contain it. After explicit authorization, the terminal reports waiting for OS
approval/helper startup. **Administrator access confirmed** means the same-binary,
same-role helper handshake was admitted; it does not imply a password was entered
(cached approval may need none). **Preparing setup controls** means private saved
configuration is being read. **Dashboard ready—continue in your browser** follows
successful inspection, including empty, configured or pending state. Keep the
launching terminal open and use its private URL if necessary. This readiness is
for setup controls only: it has not created a share, connected storage or checked
storage health. Read the browser's configuration/role/pending guidance before
choosing any action.

After 10 seconds in either pending phase, one reminder explains what is still
awaited. It is not a timeout, a diagnosis or permission to start a second attempt.
OS approval retries/diagnostics remain in the terminal. If access was not
confirmed, approval may have been denied/cancelled or helper startup failed;
review those diagnostics rather than assuming a bad password. Confirmed access
followed by an inspection refusal is reported separately: read the browser error
and use **Inspect configuration** before retrying setup. Transport failure waits
for safe helper completion before suggesting reopening. Stop suppresses later
ready/reminder invitations but still drains already-admitted work.

## Server: share a folder

1. Choose an ordinary project folder, or type one new child below an existing
   parent. The directory chooser runs with your ordinary user's permissions and
   lists directories only. Symlink entries are omitted; a noncanonical path is
   reported, not silently selected. A slow filesystem listing may wait; you can
   close the chooser and enter a path manually. It never opens file contents or
   creates a folder merely by browsing.
   Typing in the path field is a draft: a background listing cannot replace it.
   Choose **List folders** to check that path; **Use this folder** becomes available
   only when the displayed listing matches it. Parent/child navigation deliberately
   changes the path. Listing errors leave the draft available for correction.
2. Enter this computer's private IPv4 and explicitly trusted client hosts/subnets.
   NFS is plaintext AUTH_SYS host trust, not per-user authentication. A subnet
   allows every host in that subnet. No firewall/router rules are changed.
3. Keep native macOS or native Linux storage, or select the existing advanced
   **Linux Docker storage engine** with its local daemon socket. Docker Desktop
   Mac storage is not supported. Select an unoccupied local mount root; occupied
   contents are never hidden. Server setup also mounts its own export.
4. **Prepare review**. Read the exact source, connection/protocol/storage ID,
   user mapping, network, service/package and storage effects. A review holds the
   administrative lock for up to **5 minutes**; other CLI/service attempts can be
   busy during that interval. Cancel releases it without applying storage changes.
5. Check consent and **Apply reviewed plan**. A new source, if requested, is only
   created through the existing setup boundary after consent. Existing source
   files stay in place. Copy the resulting nonsecret Connection JSON to a trusted
   client's operator. Clipboard denial selects the text for manual copying.

## Client: connect a computer

Paste the server's complete Connection JSON, optionally override the local mount
root, then prepare and approve the exact plan. Endpoint/export/protocol/storage
identity are validated by the same existing setup owner. Malformed JSON, wrong
source/identity or an occupied target is refused, never replaced with a local
fallback. There is no automatic discovery. Connection details describe
configuration, not a continuously monitored readiness guarantee.

## Inspect, check, recover and disconnect

- **Inspect configuration** reads metadata only. Existing setup is not overwritten
  by first-use forms. An opposite-role launch gives the correct command instead
  of offering mutation controls.
- **Check readiness** performs a fresh actual mount/source/nonroot check. Its
  timestamp is a past observation. Polling this page reads cached progress only;
  it does not start repeated NFS probes.
- **Review reconnect** deliberately reconnects saved active configuration. A
  pending setup instead offers review/resume of the exact saved intent, with
  fresh consent; no identity rebind or new source is inferred. A failed apply
  can leave saved intent/configuration. This is incomplete, not a data rollback.
- **Review disconnect** identifies the attachment/export. Stop every local and
  remote user first; the tool cannot discover/prove remote drain. Both plan
  consent and the drain acknowledgment are required. Busy/unrelated mounts are
  refused without force/lazy unmount. Source, marker and private recovery data
  remain. Supported partial-detach retries keep existing safety checks.

One host operation may run at a time. Duplicate submission cannot replay a
consumed plan. Hard NFS checks/changes may wait indefinitely for storage; restore
storage and wait rather than launch parallel retries. No synthetic percentage,
forced cancellation, source repair or timeout success is provided.

## End management, not storage

Closing a tab does not stop the foreground process. **Stop dashboard** or Ctrl-C
stops new requests and releases an uncommitted review. An admitted operation is
drained before its helper/lock is released; the terminal explains outstanding
work. An OS browser-association process is also waited for rather than killing a
user browser. Installed launchd/systemd supervision remains independent and
continues serial active-only reconciliation. It never resumes pending setup.
Restart the dashboard later to inspect current state; reload never replays a
mutation. Stopping management never detaches or deletes source data.

## Developer and validation boundary

See [TESTING.md](../TESTING.md) for real browser previews with a root-protocol
double and separate owned native proof. Go binaries contain all assets, no CDN
or runtime build tool. Local/virtual tests do not qualify physical deployments;
independent field/shared-filesystem/user validation remains deferred to its
separate task. No release/signing/installer policy is changed by this dashboard.

## Implementation ownership

The ordinary-user dashboard owns HTTP authorization, the chooser, browser launch
and cached operation views. The private helper delegates typed operations to
`admin.Session`; it does not run browser-provided commands. That administrative
owner keeps each exact plan, lock and Docker handle together through review,
commit/cancel and drain. `setup.Service` retains source/mount/backend invariants.

Installed supervision also belongs to `admin.Session`: one serial attempt owns
acquire, admission, reconnect and cleanup, followed by the completion-relative
30-second retry wait. CLI/service entry points are adapters, not callback owners
around a second lock acquisition. When adding another entry form, move the entire
operation lifecycle into its governing owner rather than duplicating only the
inner action. Existing stored configuration is directly usable; no migration or
persistent dashboard readiness flag is introduced.
