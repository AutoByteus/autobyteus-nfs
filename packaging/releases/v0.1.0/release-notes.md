# AutoByteus NFS v0.1.0

First standalone AutoByteus NFS distribution; no AutoByteus application required.

Native archives: macOS ARM64/x64 and Linux ARM64/x64. Assets include checksums, release provenance, runtime/engine manifests and corresponding-source/license notices. Mac public assets require Developer ID signing and Accepted notarization before publication. Linux artifacts preserve the exact measured candidate engine packages and OCI identity.

Reference operating systems: macOS26+ and Ubuntu24.04. Hosted native build checks use macOS15 and Ubuntu24.04; build availability is not independent-host filesystem qualification.

## Install without storage setup

Download and review this release's autobyteus-nfs-install.sh, then run:

```sh
bash autobyteus-nfs-install.sh version
```

This verifies archive/manifest integrity, installs beneath HOME/.local, shows the deferred-field-validation notice and prints v0.1.0. It does not create an NFS export or mount. Storage create/connect are separate explicit host actions; use expendable test data first.

## Evidence and follow-up

Current four-target native and release-control checks plus exact candidate integrity were verified. Actual signature/notarization identities are recorded in release-provenance.json; public download outcomes are recorded in Delivery receipts. Shared-filesystem/physical and genuine user tests are deferred by explicit release-first direction. The approved follow-up transfers through Delivery and Solution Designer to Project Task Manager for separately scoped testing and fix-forward. Do not overwrite v0.1.0 tags/assets/images for subsequent fixes.
