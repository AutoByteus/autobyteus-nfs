# NFS distribution and qualification

NFS owns its independent `vX.Y.Z` / `vX.Y.Z-beta.N` tags; follow root [RELEASE.md](../RELEASE.md).
There is no desktop package-version coupling or automatic tag/main publication.
Do not tag, publish an engine/installer, or change the Guide's unavailable state
without the selected release decision and completed delivery gates.

`release-nfs.yml` supports manual **build-only** execution (`publish=false`), which
uploads candidate binaries and an OCI engine artifact but does not push an image,
create a release or upload public release assets. NFS tag validation, native
architecture unit/vet/binary smoke checks and immutable engine inputs are explicit.
Mac runtime hosting/physical tests are not claimed by the CI binary smoke.

`release-lock.json` starts with **no qualified targets**. Its Ubuntu package/base
pins are the selected architecture-reference versions only. The release gate
requires current production-source hash, committed independent physical evidence
and explicit user verification before publishing. Delivery owns replacing these
fields from actual evidence and syncing related docs/Guide. To calculate the source
hash: `python3 packaging/release.py --source-hash` from the root.
The local digest covers NFS-owned inputs and the declared filesystem usage boundary,
not application source. Future service qualification names exact service source,
engine identities and independently tested host platforms; it is not application
acceptance or an authorization to publish.
Evidence paths alone do not establish those receipts' semantic sufficiency.
The extraction retains empty qualifiedTargets/qualifiedSourceHash/physicalEvidence,
userVerified=false and engine=null; old qualification cannot be imported.
Changing engine family/package/base pins requires renewed full mode evidence; no
unbounded apt upgrade occurs on normal reconnect.

Publication uses the same repository tag, an immutable Linux engine digest,
versioned `autobyteus-nfs-<version>-<os>-<arch>.tar.gz`,
`autobyteus-nfs-manifest.json`, `SHA256SUMS-nfs` and
`autobyteus-nfs-install.sh`. Only qualified target archives are published. The
installer script has a replaced **versioned tag**, never `latest`; source with its
unreplaced placeholder fails without downloading anything. Archive and embedded
manifest must agree. Checksums do not protect against a compromised publisher.

Publishing Mac binaries requires Developer ID signing and notarization. The job
requires `NFS_MAC_CERTIFICATE_P12_BASE64`, `NFS_MAC_CERTIFICATE_PASSWORD`,
`NFS_MAC_SIGNING_IDENTITY`, `APPLE_ID`, `APPLE_APP_SPECIFIC_PASSWORD`,
`APPLE_TEAM_ID`. It uses an ephemeral runner keychain and cleans it. Signing and
notarization must pass before archive upload. The target GitHub release must already
exist; the NFS workflow never creates a release or tag.

The Linux engine has no host-wide/private-data/Docker-socket bind and no privileged
mode. It receives only the exact source, generated config, private recovery state,
host networking and the specified Ganesha capability set. Distribution retains
package inventory and license notices. Review Docker/OS package lifecycle on each
qualified reference rather than treating unit fakes as proof.

No release has been published or authorized by the implementation work.

## Corrected engine candidate lifecycle

The build-only workflow builds the exact source recipe in `engine/` on native
arm64/amd64 Ubuntu builders. It assembles one `nfs-engine-candidate` artifact with
both measured pairs, manifest, corresponding modified source and build inventory.
Native Linux CLIs embed only their matching pair; Docker uses these SAME artifacts.
Mac CLIs carry metadata, not engine bytes. Installed binary limit remains100MiB;
package members are bounded at40MiB each. Existing four-member archives stay.

Candidate qualification must use those exact artifacts, not freshly rebuilt
packages. Download the candidate, verify with `engine/manifest.py verify`, then
use its `lock` operation to record actual identities in release-lock.json; that
operation clears prior qualification. It never creates a release or approval.
A different recipe, source, package SHA/size, inventory or source archive changes
the production hash and invalidates qualification. Do not copy prototype hashes.
No candidate identities are invented for an architecture not actually built.

Publication requires an explicit manual workflow dispatch with `candidate_run_id`
pointing to the retained build-only run, plus all existing source/physical/user/
release gates. Publication downloads and verifies that exact candidate against
the reviewed lock; it does NOT rebuild the package pair. A tag push never triggers this workflow; only explicit manual dispatch can
request publication. Artifact expiration is a missing-input failure,
not permission to rebuild under an old Pass. Preserve candidate artifacts through
qualification and authorized publication. Current default lock remains unqualified.

Published source archives include complete modified source, exact Ubuntu origin,
backport provenance/build instructions and notices, rather than only a URL. The
image/native package inventory identifies distro runtime dependencies. Users do
not need a compiler, PPA, package download URL or additional shell command. Setup
validates embedded bytes before staging, uses private0700/0600 scratch under the
existing consent/admin lock and distribution-unit mask, requeries actual installed
versions/status and removes only its own scratch. No stock hosting fallback or
package upgrade during ordinary reconnect; a missing bundle fails incomplete.
