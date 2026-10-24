# AutoByteus NFS v0.2.1

## Clearer terminal feedback for server and client
- Reports waiting for administrator approval/helper startup, confirmed helper access,
  preparation of setup controls and the next browser action.
- Adds one reminder after10seconds in each sustained waiting phase, without a
  timeout, automatic retry or invented progress.
- Distinguishes helper startup/uncertain approval and configuration-inspection
  failures. Stops obsolete guidance after Stop while admitted work drains.
- Setup-control readiness is not storage readiness. This patch does not diagnose
  the original password outcome or change OS approval, NFS or storage operations.

The standalone dashboard remains embedded; no AutoByteus app or Node runtime is
needed. Download targets remain macOS/Linux ARM64 and x64. Mac distribution uses
Developer ID signing and Apple Accepted notarization; release receipts govern
actual checks. Existing immutablev0.1.0/v0.2.0 distributions are not replaced.
Install this version explicitly; existing user installations are not upgraded by
publication. Use the versioned installer with the explicit `version` command for
an install-only check, then launch `server` or `client` as an ordinary user.

Filesystem/physical and user testing remains deferred, not passed. Source protocol
and PTY controls do not establish real sudo/password/cache behavior. This release
is not authorization to modify a live user's configuration, mounts, exports or data.
