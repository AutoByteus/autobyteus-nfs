# IMP-06-18 — Existing-project signing reference

- Step: read-only `git show 5096011674c7db6ec0e92e522ea37f32f8f4ea40:.github/workflows/release-desktop.yml` and `autobyteus-web/build/scripts/macCodeSign.ts` in the superrepo; read exact upstream action source below.
- NFS commit: 2c12ec61f6339d0d264280b7117787ec821425af.
- Environment/date: local source inspection + public primary source; 2026-10-19. No superrepo write, credential or keychain call.
- Trigger: Delivery supplemental comparison relaying user's request to learn from the superrepo; no new delivery/review round.

The historical superrepo workflow uses apple-actions/import-codesign-certs@v3
before its custom Electron signer. Exact referenced
[action source](https://github.com/Apple-Actions/import-codesign-certs/blob/63fff01cd422d4b7b855d40ca1e9d34d2de9427d/src/security.ts)
adds the temporary keychain and login keychain to the user search list, sets a
six-hour timeout, imports PKCS12 with broad application access and grants Apple
partition access. NFS currently uses narrower codesign access, imports/partitions
successfully on the observed run, and saves/restores the existing list without an
explicit temporary-list update. This is a concrete comparison lead, not proof of
missing chain visibility or a lock/ACL cause. NFS should preserve the complete
prior list and least privilege if later actual evidence warrants such a change.

The superrepo workflow sets NO_TIMESTAMP and its adapter can suppress timestamps;
it also includes raw stderr/argv in errors. Neither is portable to this NFS
release's mandatory timestamp/privacy contract. Electron bundle entitlements and
DMG/deep-sign details are not requirements of this standalone CLI.

IR006 does not blindly copy those differences. The newly retained fixed
codesign observation can distinguish a chain warning, internal-component,
interaction or other supported diagnostic before an actual cause-specific change.
A chain warning would justify investigating actual temporary-keychain search-list
membership and issuer availability, not assuming this historical source difference
alone explains DR009. No current superrepo hosted success, credential equality or
runtime equivalence was independently proved; DR009 remains Blocked.
