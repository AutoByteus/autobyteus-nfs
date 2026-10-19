# NFS release control

Normal versions only, first **v0.1.0**. No desktop version coupling, pre-created tag,
public beta or automatic publication on push/tag. Follow root [RELEASE.md](../RELEASE.md).
The current lock binds the [audited v0.1.0 readiness record](releases/v0.1.0/readiness.json)
and exact current candidate. This accepts prepublication checks only; actual
signing/notarization and public release/download receipts remain separate gates.
The user requests signed normal v0.1.0 first, then field/user testing and fixes.
Shared-filesystem/physical and user tests are deferred, not publication or closure
prerequisites; build availability is not field-qualified support.

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
not release readiness. Missing/expired/changed data means a new candidate and affected
release-boundary validation, never a silent rebuild or fabricated amd64 package.

## 2. Current release readiness (API evidence, Delivery acceptance)

Keep recipe/package pins. The exact lock fields are ubuntuBaseImage,
ubuntuPackages, engine, releaseReadiness and note. `engine` equals the measured
candidate manifest. `releaseReadiness` defaults null and refuses publication;
engine `manifest.py lock` clears it. No qualifiedTargets, qualifiedSourceHash,
physicalEvidence, userVerified or qualification compatibility path exists.

Delivery prepares **actual**, reviewed and sanitized records in stable
`packaging/releases/v0.1.0/` after new API checks, not synthetic fixture copies or
moving tickets/in-progress paths. A reference is `{path,sha256}` to a nonempty
bounded regular in-repo file, without links/traversal. Human review establishes
meaning/truth; parser checks only integrity/applicability. See singular owner
`release_support/readiness.py`. Exact readiness fields:

- `schema:1`, `kind:"release-first"`, `version`, `targets`: exactly darwin-amd64,
  darwin-arm64, linux-amd64, linux-arm64 in that order.
- `candidate`: actual candidate-reference output above; `sourceHash`,
  `engineManifestSha256`, `oci`: exact measured candidate identities.
- `authorization`: kind `publish-before-field-testing`, requirementsRevision
  `R3/SR004`, matching version, evidence reference to genuine user direction.
  Permission to publish does not claim a user test was executed.
- `checks`: exactly native and releaseControls, each `{status:"passed",evidence}`
  referencing actual current CI/API records. Skipped/failed checks do not pass.
- `fieldValidation`: exactly `{filesystem:"deferred",user:"deferred"}`. No
  physical topology rows or executed-user placeholders, no passed shortcut.
- `postpublicationPlan`: hashed approved scoped plan with Delivery → terminal
  Solution Designer → requesting PM custody for assigned field/user tests and
  fix-forward. This is not a prepublication campaign or authorization for live data.
- `review`: candidateCommit, sourceHash and evidence reference covering actual
  source review and intervening changes; candidate is an ancestor of final HEAD.
- `releaseNotes`: hashed reviewed Markdown without private access/credentials or
  false qualification claims. A deterministic deferral paragraph is appended to
  public notes/body and verified again during payload/resume validation.

Runtime manifest schema2 has schema, version, sourceHash, ubuntuPackages,
engineImage, optional engine (development only), releaseTargets, fieldValidation.
Candidates have empty releaseTargets and both statuses deferred; they run version
but cannot pass public installer admission. Final metadata uses all four targets
only after validated readiness and retains both deferred statuses. Generate it
with `--release --candidate <retained-directory>` plus --tag, canonical immutable
--engine-image and measured --engine-manifest (Linux also --target and
--engine-artifacts). `--qualified` is removed, not an alias.

Candidate-only metadata can still use an isolated registry alias with the exact
OCI digest/source/engine and empty targets; omit --release. This is not a runtime
override, canonical public download or prepublication physical-test requirement.
The installer verifies bounded exact archive/checksums and typed embedded/loose
metadata equality before writing. Current-schema release target admission is not
field qualification: unknown/legacy/false statuses, candidate or wrong targets
refuse. Successful verify-release prints the deferral notice on stderr; explicit
version stdout remains exact, with no new prompt or flag. Host consent and private
state/source/busy-detach protections are unchanged; no live setup is part of smoke.

The production hash covers runtime sources, main/go.mod, installer, Dockerfile,
engine recipe, release facade/all release_support code/signing script/workflow,
filesystem contract, testdata connection contract and license/notices, plus pinned
package/base/engine identities. Tests, generated release.json/embedded deb bytes,
readiness/evidence, caches and output are excluded. OCI identity is separately
mandatory (no hash cycle). Readiness/docs/test-only commits can follow a
candidate only with unchanged production hash/engine/OCI, ancestry and reviewed
diff. Any production change invalidates affected evidence.

## 3. Final payload and signing

Dispatch `publish=true` only on reviewed **main**, with its exact SHA and current
`candidate_run_id`. Preflight downloads that candidate and validates evidence
before public effects. If an owned version tag exists, it resolves the original
payload first; native rebuild/signing jobs are skipped on resume.

On a fresh publication, all four native jobs use the same production source hash
and exact engine bytes. Final release metadata and Mac signature change binary
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
submission ID are retained as sanitized receipts even for a rejected submission.
On any caught failure, a fixed stage label, numeric exit code and cleanup result
are written to stderr and a separate `*-notary-failure.json` receipt, without
command arguments, identities, account details or raw private tool output. The
always-run artifact step retains only these failure receipts and sanitized notary
receipts. Existing receipts are never overwritten. A failed keychain-list capture
is not used to restore the search list; cleanup failures cannot turn success into
a passing signing job or hide the primary failure. A failure stage localizes the
boundary, not its cause: credential validity or Apple rejection requires actual
specific evidence, not speculation/re-provisioning. For codesign failures only,
`diagnostic` adds a fixed observation category to the same failure receipt/stderr.
The parser reads at most64KiB plus one overflow byte of private transient output;
only exact known messages tied to the requested binary/identity are recognized.
Unknown/ambiguous output is `unclassified`, oversized output `output-too-large`,
and unavailable/undecodable output `unavailable`; other stages are `not-collected`.
Known categories are chain-build-warning, internal-component,
interaction-not-allowed, authentication-failed, keychain-item-not-found,
certificate-expired, certificate-revoked and timestamp-unavailable. None alone
proves a credential, chain or ACL cause. Parsing cannot replace codesign's original
nonzero exit, and successful codesign output does not create a failure. This does
not change signing/keychain/trust settings or create a retry/fallback. Private
capture is mode0600 inside the existing owned scratch, never an artifact, removed
on cleanup with all other private inputs. Failed signing never reaches
archive publication. No secret log/base64 upload,
unsigned fallback, or fictitious stapling: standalone CLI tickets cannot be stapled.
Downloaded signature/online Gatekeeper behavior still needs supported Mac evidence.

Before any tag/image/release mutation, `nfs-release-payload` retains four native
archives, versioned installer, runtime/engine manifests, complete modified engine
sources/build inventories/notices, LICENSE/THIRD_PARTY_NOTICES, reviewed notes,
release-provenance.json and SHA256SUMS-nfs. Every public file except SHA256SUMS-nfs
is checksummed. Provenance lists product members; the external publication receipt
adds provenance/checksum hashes, avoiding self-hash cycles. Provenance schema2
binds releaseReadiness and explicit fieldValidation to the same validated record;
notes and provenance cannot hide deferral on a same-byte retry.

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
   does not replace the other native/signature download receipts.

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
remain release gates, not claims made by these docs. Field/user tests remain
explicitly deferred with postpublication custody. Preserve historical Blocked/Fail
results; changed production requires a new complete candidate, not relabeling an
old run. Fixes discovered after publication use a new approved version.
