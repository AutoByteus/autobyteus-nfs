# NFS release control

Normal versions only, first **v0.1.0**. No desktop version coupling, pre-created tag,
public beta or automatic publication on push/tag. Follow root [RELEASE.md](../RELEASE.md).
The current lock remains **unqualified**. These instructions describe the release
path, not a claim that a candidate, notarization or public release has succeeded.

## 1. Build-only candidate

Dispatch `.github/workflows/release-nfs.yml` on a reviewed source ref, specifying
`release_tag`, `publish=false`, and optionally its full `source_sha` (otherwise the
dispatch SHA). `sourceCommit` and `workflowCommit` are recorded separately. Candidate
jobs have only contents/actions read, no signing secrets and no registry login or
push. Two native Ubuntu builders produce the exact corrected main/VFS package
pairs; the existing recipe, pins and corresponding-source owner are unchanged.
Docker builds **once**, with complete OCI multiarch index, child manifests, configs
and layers retained. Native race/vet/build/version checks run on all four runners;
fail-fast is disabled. Hosted macOS15 is not macOS26 filesystem qualification.

The final `nfs-release-candidate` artifact contains `candidate.json`, `engine/`
(two measured package pairs, source archives, inventories/notices/checksums),
`engine.oci.tar`, and `native/` (four archives). Each native archive is exactly four
regular files: LICENSE, THIRD_PARTY_NOTICES, autobyteus-nfs, release.json. Binary
limit100MiB; engine members40MiB. Retention is requested90days, subject to repository
limits; the actual expiry is authoritative. Preserve the candidate through release.

`candidate.json` binds repository/workflow/run/attempt, source/workflow commits,
normal version, production source hash, measured engine-manifest hash, OCI root
and both platform-child digests, toolchain/base inputs and all member sizes/hashes.
The post-upload Actions envelope is external (artifact ID, wrapper SHA, expiry,
run/attempt/workflow commit); it cannot be embedded into its own hashed ZIP.

API/Delivery can resolve the *actual* candidate artifact ID from the selected
run's Actions inventory (no latest-run guessing), then use the read-only facade:

```sh
python3 packaging/release.py --operation candidate-envelope \
  --artifact-id "$ARTIFACT_ID" --run-id "$RUN_ID" --attempt "$ATTEMPT" \
  --workflow-commit "$WORKFLOW_SHA" --output envelope.json
python3 packaging/release.py --operation fetch-candidate --envelope envelope.json \
  --directory retained-candidate --output candidate-reference.json
python3 packaging/release.py --operation verify-candidate --directory retained-candidate
```

Use a current reviewed source checkout and `GH_TOKEN` with Actions read. These
commands verify actual API run event/conclusion/source and immutable wrapper,
then bounded member/engine/OCI/native contents. The output candidate reference is
not qualification. Missing/expired/changed data means a new candidate and affected
qualification, never a silent rebuild or fabricated amd64 package.

## 2. Current qualification (API evidence, Delivery acceptance)

Keep recipe/package pins. The lock's `engine` must exactly equal the measured
candidate engine manifest. `qualifiedTargets` must be exactly, in canonical order:
`darwin-amd64`, `darwin-arm64`, `linux-amd64`, `linux-arm64`.
`qualifiedSourceHash`, `physicalEvidence`, `userVerified`, and the new `qualification`
reference must come from reviewed **actual** evidence. Default `qualification:null`
and empty targets refuse publication. The engine `lock` command clears the old
qualification fields; an old leftover reference never suffices for the new gate.

A reference is `{path, sha256}`, a bounded regular in-repository file without links
or traversal. The referenced JSON record has these exact fields (see
`release_support/qualification.py` for the executable contract):

- `schema:1`, `candidate` = actual candidate-reference output above, `sourceHash`,
  `engineManifestSha256`, `oci` = measured candidate identities.
- `rows`: exactly six distinct `(target,mode)` rows: both Mac arches `mac-native`,
  both Linux arches `linux-native` **and** `linux-docker`. A row contains target,
  mode, actual osVersion (Mac>=26, Linux24.04), filesystem (APFS/ext4), backend
  (apple-nfs3/ganesha-native/ganesha-docker), topology, cases, evidence reference,
  actual binarySha256/manifestSha256 and engineImage used.
- Topology names `kind` (physical/virtual), `serverHost`, `clientHost`, `serverKernel`,
  `clientKernel`; hosts and boot/kernel-instance identities must be independent.
  A Docker container is not another kernel. Physical rows must cover all three
  modes; lock physicalEvidence matches their distinct raw evidence paths.
- `cases` records actual pass outcomes for create-connect, reciprocal-bytes,
  directory-visibility, permissions-locks-git, safe-detach-refusal,
  restart-reconnect, private-state. Missing/failed/inapplicable rows refuse.
- `userVerification`: kind `executed-user-check`, exact candidateRecordSha256,
  genuine user statement, per-target checks, hashed evidence. Publication/secret
  consent is not this check. Schema validation cannot establish truth; human
  evidence judgement remains mandatory. Never copy synthetic unit fixtures here.
- `review`: candidateCommit, sourceHash and a hashed source-review receipt covering
  the intervening change. Candidate must be an ancestor of final HEAD. Final HEAD
  is not put in a self-referential committed qualification record.
- `releaseNotes`: hashed reviewed Markdown, without credentials or fabricated claims.

For first-use Docker qualification, serve the exact retained OCI digest from an
isolated test-owned registry. A generated qualification-only runtime manifest may
change **only** the registry reference, keeping digest/version/source/package bytes
and empty qualifiedTargets. Record that metadata difference and actual binary
hashes. No runtime override or live-user daemon/DNS workaround. This is not a
canonical public download check. Generate from the retained candidate with
`--tag "$TAG" --engine-image "$OWNED_REGISTRY_DIGEST" --engine-manifest
retained-candidate/engine/engine-manifest.json --candidate retained-candidate
--output cmd/autobyteus-nfs/release.json` (plus the matching Linux `--target` and
`--engine-artifacts` when embedding); do not pass `--qualified`. The facade binds
version/source/engine/digest to the candidate while permitting this unqualified
registry alias. Final metadata uses
`ghcr.io/autobyteus/autobyteus-nfs@sha256:...` and the audited four targets.

The production hash covers runtime sources, main/go.mod, installer, Dockerfile,
engine recipe, release facade/all release_support code/signing script/workflow,
filesystem contract, testdata connection contract and license/notices, plus pinned
package/base/engine identities. Tests, generated release.json/embedded deb bytes,
qualification/evidence, caches and output are excluded. OCI identity is separately
mandatory (no hash cycle). Qualification/docs/test-only commits can follow a
candidate only with unchanged production hash/engine/OCI, ancestry and reviewed
diff. Any production change invalidates affected evidence.

## 3. Final payload and signing

Dispatch `publish=true` only on reviewed **main**, with its exact SHA and qualified
`candidate_run_id`. Preflight downloads that candidate and validates evidence
before public effects. If an owned version tag exists, it resolves the original
payload first; native rebuild/signing jobs are skipped on resume.

On a fresh publication, all four native jobs use the same production source hash
and exact engine bytes. Final qualified metadata and Mac signature change binary
bytes; do not claim equality to the unsigned candidate. Native checks cover these
deltas, not independent filesystem qualification.

Only fresh-publication Mac jobs receive NFS_MAC_CERTIFICATE_P12_BASE64,
NFS_MAC_CERTIFICATE_PASSWORD, NFS_MAC_SIGNING_IDENTITY, APPLE_ID,
APPLE_APP_SPECIFIC_PASSWORD, APPLE_TEAM_ID. All six are provisioned for the first
release; do not re-request export merely because old placeholder receipts exist.
Actual import/password pairing/account validation remains necessary. The script
rejects empty/placeholders, imports into an owned ephemeral keychain with random
keychain password, validates Developer ID/team, signs with runtime/timestamp,
verifies, and requires notarytool JSON **Accepted**. It restores the search list and
removes its certificate/keychain/scratch on every exit. Known notary status and
submission ID are retained as sanitized receipts even for a rejected submission;
failed signing never reaches archive publication. No secret log/base64 upload,
unsigned fallback, or fictitious stapling: standalone CLI tickets cannot be stapled.
Downloaded signature/online Gatekeeper behavior still needs supported Mac evidence.

Before any tag/image/release mutation, `nfs-release-payload` retains four native
archives, versioned installer, runtime/engine manifests, complete modified engine
sources/build inventories/notices, LICENSE/THIRD_PARTY_NOTICES, reviewed notes,
release-provenance.json and SHA256SUMS-nfs. Every public file except SHA256SUMS-nfs
is checksummed. Provenance lists product members; the external publication receipt
adds provenance/checksum hashes, avoiding self-hash cycles.

## 4. Publication and same-payload recovery

Only the publisher has contents/packages write. It re-verifies retained wrapper,
current candidate/evidence/payload, observes remote conflicts and checks fresh main
immediately before its first write. Repo-wide publication concurrency never cancels
another publish. Native/signing failures or unexpected skipped/cancelled ancestors
cannot reach this job. Candidate jobs never rebuild on publication.

1. Annotated version tag at exact main, with retained payload run/attempt/artifact
   ID/digest and publication receipt SHA in its annotation. No force/ref move.
2. Exact draft release (`--verify-tag`, non-prerelease), bound notes/identity.
3. Verify existing asset bytes, upload **only missing** assets, then re-download
   the complete set. Unexpected or conflicting bytes refuse; no `--clobber`.
4. Materialize the validated OCI archive into an owned layout (copy exact bytes,
   not tar ownership; no root chown). Promote it with
   `skopeo copy --all --preserve-digests oci:<owned-layout> docker://...`, no rebuild,
   recompression or format conversion. Refuse an existing different version tag;
   verify package repository association and root/platform identities.
5. Anonymous re-download of all OCI children/layers must succeed. A new GHCR package
   may be private; Delivery may make **this specific package** public under the
   release authorization. Missing permission is a named blocker, not authorization
   for an org-wide change. Keep the GitHub release draft meanwhile.
6. Publish normal/latest, verify exact tag/assets, anonymous versioned HTTPS downloads
   and owned-HOME explicit `version` installer smoke on the Ubuntu publisher. This
   does not replace the other native/signature/physical receipts.

`nfs-publication-receipt` records progress even on a later failure; an attempted
write may have completed. Remote state is authoritative, not that local log. Retry
must use the annotation-bound original artifact/attempt and identical signed bytes.
Retry with a **new manual dispatch** on the same exact main/version/candidate run,
so preflight observes current remote state again; do not rerun only the failed
publisher with stale job outputs. A failed overall run can have a successful retained-payload job; the resume reader
checks that exact job. A tag-only interruption is recoverable. An expired artifact,
ambiguous run, unrelated draft or changed asset/image is not automatically repairable.
Never delete a tag, overwrite assets, re-sign/repack or pick the newest artifact.
An already complete identical release is verified read-only; a different output
requires a newly authorized version. No live user data/configuration is touched.

Relevant primary contracts: [Actions artifacts](https://docs.github.com/en/rest/actions/artifacts),
[workflow attempts](https://docs.github.com/en/rest/actions/workflow-runs),
[release creation](https://cli.github.com/manual/gh_release_create),
[OCI copy](https://github.com/containers/skopeo/blob/main/docs/skopeo-copy.1.md).
Actual hosted execution, package visibility, signing, supported-platform downloads
and genuine user verification remain release gates, not claims made by these docs.
