# Design — First downloadable NFS release

## Solution And Approval Basis
- Package `nfs-first-release`; Task `autobyteus-nfs-3` / `project_task_97c6ab09-83cb-46df-bf28-d07b39259dd5`; current solution **SR-003**.
- **Design Ready — Architecture Design Complete**, not reviewed/implemented/qualified/published.
- Requirements **R2/SR-002 Approved**: user explicitly rejects beta; SD approved initial normal `v0.1.0` and retained four-target scope within the assigned direction and informed the user. Original PM-carried user direction authorizes actual publication after readiness. No behavior-defining supplement. Publication consent is not a user-verification receipt.
- Canonical investigation: `/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/nfs-first-release/tickets/in-progress/nfs-first-release/investigation-notes.md` (E01–E18).
- Workspace `/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/nfs-first-release`, branch `codex/nfs-first-release`; fresh base/finalization `origin/main`7e375984be2bea7a4d536e43cc59d6bc2b116870, still confirmed by ls-remote2026-10-18. Canonical checkout/PM/archive untouched.
- Authorities read2026-10-18: solution-designer SKILL; full references/requirements-engineering.md, architecture-design.md, design-principles.md, handoff-references.md and relevant artifact templates; NFS root AGENTS.md, DESIGN.md, TESTING.md, RELEASE.md and packaging/RELEASE.md. No closer design/agent instructions found. Design-examples: N/A. General/project design conflicts: none. Extraction-specific release prose is obsolete for this newly authorized task and is replaced, not silently ignored.

## Current-State Read And Intended Change
Current manual workflow checks out an already-existing tag, optionally rebuilds/pushes the image before all signing gates, and uploads with clobber to an already-existing release. Its engine-package reuse invariant is useful, but its distributed gate/side-effect ordering is incomplete. Source hashing, embedded metadata verification and bounded four-member archives are sound existing boundaries to retain. Current qualification is empty; historic native CI and shared-kernel filesystem results do not fill it. See E03–09/E15.

Replace the release orchestration with one manually initiated, identity-pinned candidate/publication workflow. Build and retain engine packages **and the OCI image once**; qualify those inputs; sign final Mac binaries; create the exact tag, stage a complete draft, promote the exact image and publish a normal release. Ordinary push/PR checks remain nonpublishing. Users obtain prebuilt binaries through a versioned installer; no Go/Homebrew prerequisite. No runtime filesystem change.

## Task Size And Architectural Risk
- **task_size: Large** — changes span Actions orchestration, candidate/qualification/promotion records and tooling, signing, installer asset assembly, durable tests and repository/distribution docs, followed by actual multi-platform qualification/publication.
- **architectural_risk: High** — external irreversible Git/release/registry effects, private signing credentials, trust in externally supplied evidence/artifacts, cross-run identity and failure/retry sequencing. Compilation cannot validate these boundaries.
- Escalate changed runtime/state/host behavior, target/channel/qualification policy, new paid infrastructure or a needed trust bypass to Solution Designer; do not patch around the gate. Concrete unavailable credentials/hosts are execution prerequisites, not permission to weaken R2.

## Architecture Investigation Evidence
| Evidence | Current owner / path | Finding / design consequence | Remaining uncertainty |
| --- | --- | --- | --- |
| E03/E15 | `.github/workflows/release-nfs.yml` | Existing-tag checkout and existing-release upload prevent end-to-end flow; image pushed too early and rebuilt with potentially different runtime apt dependencies | Real hosted replacement must be exercised |
| E04/E15 | `packaging/release.py`, engine/manifest.py, Dockerfile | Engine pair verified; source identity includes engine; physical evidence only counted as paths by code | Semantic evidence and real platforms remain mandatory |
| E05/E15 | install.sh → VerifyRelease → setup | Exact manifest equality and target admission before installer writes; direct candidate CLI can be exercised on isolated hosts without claiming installer qualification | Actual final download/signature/host runs pending |
| E15 | `internal/docker/engine.go:EnsureEngine` | New Docker engine always pulls digest; simply loading a local image will not exercise first-use correctly | Isolated qualification registry/host inventory required |
| E16 | GitHub/Apple/skopeo primary contracts in notes | Explicit tag pin, draft promotion, no token-trigger recursion, digest-preserving OCI copy, explicit notarization Accepted and anonymous GHCR access checks | Package visibility privilege and credential validity not assumed |
| E11–14/E18 | Sanitized signing receipts | All six entries now populated: user set app/export passwords, selected local identity exported and uploaded without disclosure | Key import/password pairing/notary account/team validation pending |

## Change Scope
- UC001–005 / BEH001–006: NFS-only release workflow, packaging release boundary/records, narrowly needed installer checks, tests, support/release/testing docs and actual release execution evidence.
- Leave Go runtime source/config/mount/backend/Docker semantics, engine recipe/backport/pins, installed state, application/desktop repos, Guide, dashboard, PM boards and old archives alone. Dockerfile may add source/license labels/inventory reporting only; no engine/dependency-policy change.
- No Homebrew tap/formula, new OS family, auto-updater, setup-on-user-host, provider/app acceptance, or rollout. No application coupling restored.
- Follow-ups found: **None newly requested**. Homebrew is optional future distribution, not part of this task; dashboard remains existing nfs-2. Previously deferred filesystem work stays deferred.

## Relevant Behavior And Production-Path Map
| Behavior | Kind / approved IDs | Existing evidence | Target path / preserved outcome |
| --- | --- | --- | --- |
| BEH001 | Operational; REQ001/002, AC001 | ci.yml and release prepare/build | DS1: explicit candidate request → fixed checkout → engine/OCI/binary builds → identified CI artifacts; no publication permission |
| BEH002 | Contract; REQ003/004/006, AC002/003/006 | release.py/lock + engine manifest + signing | DS2: verified candidate → actual host evidence/user receipt → qualified lock → publish preflight; fail closed |
| BEH003 | Operational; REQ001/005/006, AC004/006 | engine push + final upload | DS3: exact qualified inputs → final binary/signing checks → retained payload → tag/draft/image → normal release; safe resumable partial state |
| BEH004 | User; REQ005/007/008, AC005/007 | versioned installer → bounded tar → VerifyRelease | DS4: public download → checksum/archive/embedded metadata/target validation → user CLI installation/version; setup only by normal explicit consent |
| BEH005 | Contract; REQ003/007/010, AC002/005/008 | host admission/setup/source/private-state owners | DS2/4 preserve host-only modes and all safety/refusal semantics; tests on explicitly owned resources only |
| BEH006 | Operational; REQ009/010, AC008 | root and packaging policy/docs | DS3 delivery receipt records main/tag/run/asset/image identities, truthful platform limits and owned cleanup |

## Supplemental Task Artifacts
The investigation inventory is canonical. Seven intake receipts record bootstrap/secret-name/admin operations, not runtime qualification or approval. Only `signing-certificate-upload-receipt.json` and `repository-release-preflight.json` are selected handoff supplements; earlier metadata receipts remain linked. Prior extraction DR003 is read-only provenance. Architecture/source/API/delivery review artifacts for this task: **N/A — not yet applicable**.

## Task Design Health Assessment
- Posture: Larger Requirement / release behavior completion. Current design issue: **Yes**, missing promotion invariant and scattered coordination.
- Structural triggers: workflow mixes building, remote image mutation and later signing; final publish can see an image already exposed despite binary failure. Qualification gate counts evidence paths instead of binding supported target/mode receipts. Existing-release/clobber assumptions obscure ownership and recovery.
- Root cause: **Missing Invariant / Duplicated Policy Or Coordination** in distribution orchestration, not Go filesystem layering.
- Refactor needed now: **Yes, bounded to packaging/workflow**. A release-specific control owner validates candidate/qualification identity and remote reconciliation; workflow owns runner scheduling/permissions, not competing identity rules. Existing engine manifest and runtime installer verification are reused.
- No broad runtime refactor or generic workflow framework. Residual unavoidable risk: GitHub Release/Git/registry are not one atomic transaction; explicit stage receipts and non-clobber reconciliation handle partial completion.

## Legacy Removal Policy / Removal Plan
No compatibility wrappers, parallel old publisher, beta fallback or existing-tag-only route.
| Remove / replace | Why unnecessary | Replacement owner | Scope |
| --- | --- | --- | --- |
| Existing-tag and manually pre-created-release prerequisite | Contradicts UC001/003 | Fixed source input + controlled tag/draft creation | This change |
| Image rebuild/push during engine build in publish mode | Breaks exact OCI identity and early-effect ordering | Candidate image retention + late digest-preserving promotion | This change |
| `gh release upload --clobber`, implicit default-tip tag behavior | Can silently substitute assets/source | Exact-tag/draft identity reconciliation, missing-asset-only upload | This change |
| Permissive prerelease regex and beta prose | User rejected public beta | One strict normal-version parser | This change |
| Path-count-only physical gate as sufficient | Not semantic source/platform proof | Structured qualification validator plus API/Delivery evidence review | This change |
| Old workflow fixture assertions prohibiting all tag/release creation | Old no-publication extraction basis | Candidate-no-effects and gated-publication tests | This change |
| Extraction-specific paired/unborn-main/root release procedure | Extraction done, NFS independent | Current-main NFS finalization/release docs | This change |

## Persisted Data / State Transition Decision
Repository DESIGN.md current-record/admission convention was read before this decision; representative writers/readers are setup.Release/VerifyRelease and release.py/lock. No migration inference from field changes.

| Stored subject | Evidence / direct-use constraints | Decision |
| --- | --- | --- |
| Installed host state/binaries, source/mount identity | Existing paths/schema/consent unchanged; no active/pending transformation | **Not Affected**. No deployment/upgrade/migration in this ticket |
| Current release lock | One committed unqualified record, no published tag; engine null, targets/evidence empty | **Discard or Rebuild** for qualification fields from actual new candidate/evidence. Preserve recipe pins, historical raw evidence and original lock in Git; never reuse an old Pass. New validator accepts one current shape only |
| Candidate/generated release metadata/build products | Disposable derived outputs; exact source/recipe is authority but rebuilding invalidates candidate evidence | **Discard or Rebuild** only as a new identified candidate, never under prior qualification. Do not delete historical/unowned retained artifacts |
| Tags/releases/assets/registry | Initial inventory empty; later externally visible identity is append-only | **Directly Usable — No Migration**. Read exact new-state identity and reconcile; never rewrite a published tag/asset. No preexisting public formats require compatibility reader |
| GitHub secrets | Six named entries, private values unreadable through API | **Directly Usable — No Migration**; normal authorized secret provisioning. No repo persistence of private values |

No migration plan or startup migration gate is applicable. New release-control records live in packaging/ticket evidence, not runtime host state.

## Data-Flow Spines / Narratives
| Spine | Scope / trigger → outcome | Governing owner | Narrative |
| --- | --- | --- | --- |
| DS1 | Primary: explicit build-only dispatch → retained candidate | Workflow scheduling + candidate owner | Resolve source SHA once, validate normal version, build measured engine pair/OCI once and native CLI matrix, aggregate immutable identity/manifest/checksums and CI artifact references. No tag, release, registry push or qualification write |
| DS2 | Primary: candidate available → audited qualified inputs | API/E2E evidence; Delivery qualification acceptance; packaging validator | Verify actual artifacts, test supported modes on scoped hosts, record exact source/engine/OCI and genuine user verification. Commit the reviewed qualification-only record. The validator rejects missing/stale/unsupported records; it does not create evidence |
| DS3 | Primary: authorized publish dispatch → public receipt | Publication owner; Delivery execution | Pin reviewed main, download exact candidate, validate qualification; build/sign final payload before any public write. Retain the complete payload; reconcile exact tag/draft, promote OCI, verify anonymous availability, publish draft, confirm assets/downloads and report cleanup |
| DS4 | Primary: user downloads → installed CLI/version | Existing installer and CLI VerifyRelease | Download pinned version/checksums/manifest/archive, validate before installation, invoke explicit version for smoke. No automatic setup on a live user host. Actual storage use remains the existing explicit CLI consent path |
| DS5 | Bounded local within DS3: interrupted publication → same-input resume or refusal | Publication owner | Observe tag, draft/release, assets, image and bound payload identity on every retry; never use a local success flag alone. Fill only missing exact outputs, or stop on conflict/expiry. Preserve failed attempts |

Main-line subjects: **Candidate**, **Qualification**, **Publication**, **Release Manifest**. All names have distinct meanings; no generic context bag. Returned status/evidence is a workflow result/report, not a new callback/event subsystem. Public facade `packaging/release.py` remains a thin command entrypoint; release control modules govern their respective invariants.

## Workflow And Identity Decisions
### D1 — Trigger, source and version
Retain one `workflow_dispatch` release workflow with `release_tag`, `publish` (default false) and `candidate_run_id` (required only for publish). Add explicit `source_sha` full commit input, defaulting to the selected dispatch ref resolved once; show the resolved SHA in summary. Candidate may run on the reviewed task ref. Publish must execute the reviewed workflow on **main** and use its exact checked-out current main SHA; reject arbitrary branch publication. Never interpolate inputs directly into shell source; pass validated environment/arguments.

Normal-version grammar: `^v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$`. First release v0.1.0; no prerelease or build suffix. Version is NFS-owned, not a desktop package file. An internal candidate can carry v0.1.0 metadata while clearly unqualified and unpublished.

No tag-push or release-event recursion: the same authorized workflow creates its tag/draft and publishes. This avoids requiring a PAT just to trigger another workflow from GITHUB_TOKEN. Publication serialized under a single repository release concurrency group with cancellation disabled; candidates may run independently. Native matrix fail-fast false preserves useful failures but **all** required jobs must succeed. Explicit needs/result guards distinguish legitimate mode skips from failed/cancelled ancestors.

### D2 — Candidate identity and retention
Use an aggregated `nfs-release-candidate` CI artifact containing a small candidate record and all required engine packages/source/inventories, OCI layout/archive, native build artifacts and hashes. Native per-job artifacts may remain execution intermediates. Retention explicitly90days subject to repository limits; record actual expiry. Retain through qualification/publication. Missing artifact means new candidate + affected qualification, not silent rebuild.

Candidate identity binds repository, workflow path, run ID/attempt, source commit, normal version, production source hash, exact engine manifest digest, OCI index and platform child digests, toolchain/build inputs, named members' sizes/SHA256 in its immutable content record. After upload, Actions supplies an external envelope with artifact ID, wrapper digest and expiry; this is resolved by run/attempt and recorded in qualification, never embedded into the artifact that would have to hash itself. Artifact-service digest is recorded alongside payload hashes, not substituted for them. Reject missing/duplicate/unsafe paths, unexpected platforms, malformed sizes, hash mismatch or archive traversal. Verify workflow run event/conclusion/source and artifact identity with Actions API, not a user-written manifest alone. Rerun artifacts must not be mistaken for the qualified attempt.

Reuse engine/manifest.py verification, source inventory and main/VFS pair limits. Build the multi-arch image once from those pairs; runtime apt dependencies make a later rebuild non-equivalent even if .deb bytes match. Keep OCI index **and all children**, no recompression/manifest conversion. Candidate jobs have no contents/packages write permissions or Mac secrets.

Source digest includes all release-executing code under the new packaging/release_support folder and packaging/sign-macos.sh, current workflow, existing installer/engine/runtime/licensing inputs and measured engine identities. Exclude only generated metadata, qualification fields/evidence, tests, cache and built artifacts as documented. Tests ensure a change to any new release logic changes the digest. Image digest is a separate mandatory identity, avoiding a build/hash circular dependency.

### D3 — Qualification, current source and Docker first-use
Retain release-lock fields for package pins, engine, qualifiedSourceHash, qualifiedTargets, physicalEvidence and userVerified; add one `qualification` reference (relative regular file + SHA256) to a structured record. Empty default fails. Require **exactly the approved four-target set** for this release, no automatic subset filtering.

Qualification record binds candidate identity, source hash/engine/OCI and explicit target/mode rows. Each row names actual OS/version/architecture/filesystem/hosting backend, physical versus virtual topology, independently identified client/server kernels/hosts, executed case outcomes and bounded in-repo raw evidence paths/hashes. Mac-native, Linux-native and Linux-Docker modes must be covered on their advertised architecture/reference; Docker-Linux alone does not cover native Linux. At least the current three physical evidence categories remain, not merely any three files. Reject duplicate/missing/failed/inapplicable rows. User verification has a separately recorded actual user statement/check and exact candidate scope; consent to publish or configure credentials is not verification. Do not manufacture `userVerified=true`.

API owns executable coverage and semantic evidence; Delivery judges sufficiency and updates qualification from that evidence. A schema can check consistency, not prove a physical host exists. Sanitized public receipts retain meaningful identity without credentials/IP/account email. No full raw secret-bearing logs committed.

Docker first-use requires a registry pull (`EnsureEngine`), so `docker load` alone is insufficient. API's **test-owned isolated registry** serves the exact candidate multi-arch OCI digest over a reachable scoped transport. A qualification-only generated release.json may substitute only that registry hostname/reference while retaining the same digest, version, source hash and exact package bytes; qualifiedTargets remains empty. Record the metadata-only difference and generated binary hashes. Direct CLI invocation on test hosts exercises current product paths; it does not claim public-installer success. No runtime override flag, live daemon reconfiguration, host DNS/credential workaround or production-code patch. Prefer TLS; any necessary isolated test daemon trust configuration belongs only to owned resources and is disclosed. If no suitable owned registry/hosts exist, report that precise prerequisite.

Final release metadata uses canonical `ghcr.io/autobyteus/autobyteus-nfs@sha256:...` and audited qualifiedTargets. Final CLIs are built from **the same production-source hash and exact engine packages**; qualification metadata and Mac signature change executable bytes, so never claim candidate/final binary byte equality. Record both. Final native version/manifest/signature/download checks close those deltas; canonical anonymous image pull is also mandatory before release exposure.

Qualification-only commits and reviewed docs/tests can follow candidate commit without a rebuild if production digest and engine/OCI identities remain exact. Record candidate commit and final tag commit separately, prove ancestry and inspect the intervening diff. Any source/hash/input change requires a new candidate and affected qualification. Do not put the yet-unknown final tag commit inside a self-referential committed record.

### D4 — Final payload, signing and preflight
Publish preflight downloads the identified successful candidate and validates its full record and qualified lock **before any remote mutation**. Check required credentials for missing values and `REPLACE_ME_BEFORE_RELEASE`; do not log values. Repository-secret metadata names alone never qualify signing.

Build the final native matrix using pinned Go1.27.2 and unchanged per-architecture engine bundle. Run native race/vet/build/version and packaging boundary checks. Hosted macOS15 compiles/tests; it is **not** macOS26 runtime hosting proof. Installed binary limit100MiB and engine member40MiB remain. Each archive is exactly LICENSE, THIRD_PARTY_NOTICES, autobyteus-nfs and release.json. Names `autobyteus-nfs-0.1.0-<darwin|linux>-<arm64|amd64>.tar.gz` omit v as the current installer expects.

Only publication-mode Mac jobs receive the six named secrets. Decode .p12 to0600 owned runner scratch; import into a separate ephemeral keychain with a random ephemeral keychain password, not a persistent login keychain. Validate intended Developer ID identity/team, sign with hardened runtime + secure timestamp, verify signature, submit ZIP carrier with notarytool --wait and JSON output; require **status Accepted** and retain submission ID plus sanitized result/log. Restore any changed search-list state and delete only owned keychain/certificate/temporary credential files on every exit. No credential/base64/xtrace upload. No unsigned fallback. Standalone binaries cannot have tickets stapled; do not report a fictitious stapling success or promise offline first-use Gatekeeper validation. Verify the downloaded signature/notarization behavior on supported owned Mac hosts.

Aggregate final payload as retained CI artifact **before remote writes**: four archives, versioned installer, runtime manifest, engine manifest, corresponding complete modified source/build inventories/notices, release-provenance.json, reviewed release notes, SHA256SUMS-nfs. Checksum every distributed payload file except the checksum file itself (not only tar.gz). Provenance binds candidate/qualified/tag-source/OCI/signing inputs and payload members without self-hashing cycles: manifest lists product members, aggregate receipt adds provenance/checksum hashes. No credentials in public provenance.

### D5 — Publication, visibility and retries
One write-capable publication job starts only after preflight and every native/signing job succeeds. Default workflow permissions are contents/actions read; only this job gains contents/packages write. Pinned/reviewed action implementations, no PR secrets or pull_request_target execution. Validate repository identity and actual fresh remote main against the approved publication SHA immediately before first write; stale main fails for reintegration, not force push.

Normal ordering:
1. Retain final payload identity (run/attempt/artifact ID/SHA) and verify all inputs again.
2. Create an annotated version tag at exact SHA without force; its annotation binds the pre-write payload artifact ID, run/attempt and payload digest so a tag-only interrupted attempt remains recoverable. If it exists require exact peeled commit and annotation identity. Never rely on gh's default-tip implicit tag creation.
3. Create **draft** GitHub release using --verify-tag and explicit normal/non-prerelease metadata, with approved release notes and bound payload identity. Existing unrelated draft/tag is a conflict.
4. Upload complete final payload to draft, validating existing same-name assets by bytes/hash; only missing exact assets can be added, never --clobber. Re-download draft assets and verify full set/integrity.
5. Promote retained OCI using `skopeo copy --all --preserve-digests`; verify registry index and all child digests against the candidate, no rebuild. Refuse a conflicting version tag. Record Docker package version/digest and source repository association.
6. Confirm the package is public and canonical digest anonymously fetchable on both Linux architectures; a new GHCR package defaults private even for a public repo. Delivery may set this **specific package** public under authorized public release scope using available normal administration; unavailable permission is a named external blocker, not a broad org/token escalation. Keep release draft until resolved.
7. Publish the fully verified draft with prerelease=false, mark latest for this first release, verify tag/assets/image and perform public installer/download smoke. Record real release URL and result.

Non-atomicity is explicit. Once tag/image is visible a later failure cannot be described as no publication effects. Never delete/move a published tag/image to simulate rollback. Retry uses observed remote state plus the **retained same final payload**, not freshly re-signed/repacked bytes (timestamps differ). If any remote stage exists, resolve its bound publication artifact identity before building again; reuse that retained artifact for same-input resume. If tag alone exists after interruption, require exact tag SHA and locate the successful pre-write payload for the recorded attempt; no guessing by newest artifact. Missing/ambiguous payload or conflicting assets blocks automatic resume. Completed identical release is idempotent read/verify success; it is not overwritten. A genuinely different candidate/output needs a new authorized version, not deletion/clobber.

### D6 — Installer and human guidance
Keep versioned HTTPS URLs and current manifest equality. Do not switch to an unsigned Homebrew/source-build requirement or latest URL. Strict normal tag substitution is done by the same release identity owner. Verify checksums for downloaded manifest/archive before execution; verify archive membership, regular files, bounded size, target and embedded metadata before install. Preserve fail-without-setup behavior on corrupt/unsupported inputs. Shell installer is an inspectable downloader, not a new signed .pkg/app; only its separately signed/notarized native payload runs.

Release notes/README show supported OS floors and architectures, exact curl download + inspect + shell invocation, an explicit `version` smoke, normal create/connect consent instructions and checksum guidance. Distinguish installing the CLI in an owned HOME from creating a storage service under admin consent. Do not advertise success before actual publication or bypass Gatekeeper/quarantine. No compiler or Homebrew installation required; platform system/Docker prerequisites are still described truthfully.

## Ownership, Dependencies And Interfaces
| Boundary / owner | Owns / allowed callers | Forbidden bypass |
| --- | --- | --- |
| release.py facade → release_support | Typed CLI dispatch; compatibility of existing source-hash/metadata command spelling, not old publication behavior | Shell reimplements version/source/qualification rules |
| candidate owner | Candidate compound identity + file verification; workflow calls it after builds/downloads | Trust run ID alone, loose latest-artifact lookup or arbitrary artifact manifest |
| qualification owner | Lock/record validation and source-engine-target applicability; publisher calls before writes | Treat three files, secret presence or user publication consent as qualification |
| publication owner | Stage ordering/remote identity reconciliation; sole writer entrypoint | Image push during build, direct clobber upload, force tag, silent partial completion |
| engine/manifest.py | Exact pair/source/inventory validation/embedding; existing owner reused | Duplicated package decoder or unqualified rebuild on promotion |
| installer / CLI VerifyRelease | Public install admission / embedded runtime metadata | Packaging pipeline changes runtime host safety or grants app coupling |
| API / Delivery | Real checks, evidence judgement, approved finalization/publication/cleanup | SD/reviewer fabricates runtime or user-test receipts |

Dependencies: workflow → release facade → cohesive release_support modules; those reuse engine manifest and invoke subprocess/API adapters at their effect boundary. Go runtime never imports/queries release-control evidence or GitHub. No new external Python dependency/framework. Explicit subprocess argv, bounded inputs and structured JSON; no eval of artifact content.

| Interface | Identity / result | Boundary check |
| --- | --- | --- |
| candidate assemble/verify | Repo+workflow+run+attempt+commit+version+source+engine+OCI; named artifact hashes | Singular, explicit; no overloaded tag/run selector |
| release.py --source-hash / metadata | Current production inputs + optional measured engine; existing runtime Release shape | Singular; same common implementation, no second digest algorithm |
| --check-publish | Current lock + candidate + qualification record → typed readiness/error | Singular; no effect, does not mint approvals |
| publication plan/resume | Validated final SHA/version + candidate + final payload/run identity → stage observations | Singular; missing/conflict explicit, no arbitrary shell command input |
| installer/VerifyRelease | Versioned archive/downloaded runtime manifest == embedded Release | Existing exact target/hash admission retained |

## Off-Spine Concerns And Capability Reuse
| Concern | Owner / reuse decision | Why not a second main-line owner |
| --- | --- | --- |
| Hash/path/version/schema parsing | release_support identity; new narrowly shared value/validation module | Avoid duplicated meanings, not a generic shared-utils bag |
| Package/backport/source proof | Existing packaging/engine, **Reuse** | Release code coordinates, never reimplements engine family |
| Mac signing/keychain | Narrow signing script, **Extend** existing workflow responsibility | Secrets confined to Mac step; cannot decide qualification or publish |
| Retention/provenance/log hygiene | Candidate/publication owners, workflow uploads | Audit sidecar carries result, not authoritative fabricated Pass |
| OS/source/consent/mount lifecycle | Existing Go owners, **Reuse unchanged** | No packaging credential/evidence coupling into runtime |

## File Responsibilities And Folder Projection
Draft allocation put scheduling in YAML and all gate/effect logic in release.py. Re-tightening separates candidate/qualification/publication subjects to keep the facade readable; one cohesive release_support folder is sufficient, not one folder per job. Shared identity types remove parallel source/version/path parsing. Runtime Release stays a distinct exact existing schema; publication provenance is not stuffed into it.

| Path | Change / owner / concrete responsibility | Must not contain |
| --- | --- | --- |
| `.github/workflows/release-nfs.yml` | Replace orchestration; scheduling, mode/needs/concurrency, least privileges, pinned job tools, artifact plumbing | Independent policy parsers, early image publication, inline monolithic recovery logic |
| `.github/workflows/ci.yml` | Extend affected packaging/test checks only if needed; ordinary nonpublication retained | Signing secrets/write permissions/public release trigger |
| `packaging/release.py` | Thin existing CLI facade and metadata orchestration | Generic catch-all release engine or duplicated policy |
| `packaging/release_support/__init__.py` | Package boundary only | Side effects at import |
| `packaging/release_support/identity.py` | Version/source hash and bounded artifact/record identity structures | Github mutation/secret retrieval |
| `packaging/release_support/candidate.py` | Candidate assembly/verification and retained run/artifact reconciliation | Qualification creation or publication effects |
| `packaging/release_support/qualification.py` | Current lock/structured evidence validation, exact target/mode coverage | Invented receipts or test execution |
| `packaging/release_support/publication.py` | Final payload/stage planning, strict remote reconciliation and promotion | Filesystem service setup or engine rebuilding |
| `packaging/sign-macos.sh` | Narrow fail-closed credential/keychain/codesign/notary boundary with cleanup | Public upload or user data access |
| `packaging/release-lock.json` | Current pins/engine and evidence reference; keep unqualified until accepted real receipts | Placeholders masquerading as qualified evidence |
| `packaging/Dockerfile` | Optional source/license labels and inventory consistency only | New backend/caps/dependency policy |
| `scripts/public/nfs/install.sh` | Normal-version/integrity consistency, preserve current bounded installation flow | Live setup in smoke, unsigned fallback, app integration |
| `scripts/tests/test_nfs_release_workflow.py`, test_nfs_packaging.py; focused `test_nfs_release_*.py` | Durable release/installer semantic and failure controls | Claim that boolean/string fixtures are hosted/platform proof |
| `README.md`, `RELEASE.md`, `TESTING.md`, `packaging/RELEASE.md`, engine README if affected | Single-repo normal-release/candidate/qualification/recovery/download guidance | Old beta/manual-precreate/paired extraction requirements or premature published claims |
| Ticket-owned evidence and qualification record | API/Delivery actual receipts with relative hashed references | Private credentials or changes to finalized old archives |

Folder boundary: .github is transport/scheduling; release_support is cohesive release control with explicit effect boundary (mixed control/provider justified for small packaging-only area, no service/container framework); packaging/engine retains its independent build/provenance boundary; signing is off-spine Mac capability; scripts/public is user entry; internal remains untouched runtime. Low over-split risk: four release modules by lifecycle responsibility, not one module per field/job. Implementation may choose fewer files only if those singular boundaries remain evident and testable; no parallel old/new path.

Shared structure tightness: CandidateIdentity separates run attempt, source SHA, production hash and OCI digest (not interchangeable); Qualification references CandidateIdentity rather than duplicating unvalidated copies; PublicationIdentity binds final payload separately from candidate (signed bytes differ); Runtime Release retains its existing fields. One owner validates each, contradictory redundant assertions rejected. Pattern: explicit staged publication with reconciliation, not a general transaction/rollback framework.

## Concrete Shapes / Compatibility Rejection
Good: candidate index digest A → qualification A → copy --preserve-digests A → anonymous pull A → publish. Bad: same .deb pair → rebuild image B → call it qualified A.
Good: user explicitly confirms a scoped test → hashed receipt → userVerified. Bad: “go ahead with release” → true.
Good: draft asset exists with exact hash → reuse; different hash → conflict. Bad: upload --clobber because a retry is convenient.

| Considered compatibility | Decision / replacement |
| --- | --- |
| Retain old existing-release/tag publisher alongside new create flow | Rejected; single current candidate/publication route |
| Accept beta or infer a reduced target set for old workflow callers | Rejected; strict normal-only/four-target input |
| Old path-count gate as fallback when structured evidence absent | Rejected; current record required, default unqualified |
| Import old extraction qualification / use VM result for physical coverage | Rejected; historical evidence retained only as historical |
| Backward-compatible host-state transformation | N/A; no host-state schema/reader change, existing refusal intact |

Derived layering: scheduling → release identity/control → existing engine validator and bounded GitHub/registry/signing effects; public installer → Go runtime admission. No app or host-data migration layer.

## Change / Refactor Sequence
1. Implement singular identity/source hashing and candidate/qualification schemas/tests. Keep default lock empty; never fabricate record population.
2. Replace workflow candidate path and affected tests; create reproducible identified engine/OCI/binary artifacts on an actual hosted build-only run with no public side effects.
3. Implement final signing/payload + publication reconciliation and failure controls, remove legacy clobber/precreate/early-push/beta behavior; reconcile docs. Validate credentials only in intended signing context, with secret hygiene.
4. Independent source review and API testing under configured route. API establishes concrete owned physical host/registry inventory and executes qualified candidate scenarios or reports precise prerequisites. No live-user storage change.
5. Delivery judges real evidence, records qualification/current-source relationship, integrates fresh main under --no-ff policy, revalidates affected changes. Ordinary workflow main availability may require staged source finalization before candidate/publication; source merge alone is never Task completion.
6. Authorized publication workflow signs/prepares/reconciles/promotes/publishes; Delivery verifies actual public downloads, records URL/version/platform/commands and cleanup. If any external gate fails, preserve partial effects and keep Task open. No repeat duplicate source merge or force rollback.

## Validation Intent / Acceptance Coverage
Implementation owns focused checks; API owns executable coverage and ledger; Delivery owns final publication/download evidence. These are required boundary outcomes, not fabricated test results.
| AC | Required proof / negative controls |
| --- | --- |
| AC001 | Actual candidate without preexisting tag/release; exact identity/artifacts; remote inventory unchanged. Wrong repo/run/attempt/source/version/expired artifact refused |
| AC002 | Per-target/mode physical and explicit-user receipts verified against hashes/topology; reject stale/duplicate/missing/mismatched/inapplicable evidence, empty lock and publication consent used as test |
| AC003 | Real P12 import/identity/codesign/Accepted notary, final download signature; missing/placeholder/rejected notary and cleanup-on-failure controls; no secret logs |
| AC004 | Real normal release/tag exact SHA; no beta accepted; branch/main drift, cancelled/skipped/failed prerequisite, conflicting asset/tag/image refusal; resume at each partial stage without overwrite |
| AC005 | Public supported-target archive/manifest/checksum and owned-HOME version install; wrong digest/target/manifest/member/link/traversal refused before installation/setup |
| AC006 | Exact measured pair plus whole OCI index/children preserved; mutation/rebuild/expiry fails; source/inventory/notices available |
| AC007 | Actual authorized workflow and public downloads, not only unit/YAML. Native four-platform checks distinct from supported OS physical hosting and independent client proof |
| AC008 | NFS-only source/main identities, documentation/license review, no app coupling, preservation/owned-resource cleanup |

Required realistic storage validation derives existing supported behavior: create/connect and reciprocal exact bytes, directory operations/visibility, permissions/locks/Git, safe detach/refusal/preservation, restart/reconnect/private-state on actual candidate and supported mode/topology. API must define the complete applicable ledger from current source and existing requirements; no blanket carry of previous task's passes. Unit race/vet, Python/Bash, actionlint and mutation/adversarial controls support but do not replace runtime/hosted/publication evidence.

## Tradeoffs, Risks And Implementation Guidance
- Manual candidate/publish dispatch is deliberate: infrequent normal releases, explicit authorization, no accidental main/tag publish. No public beta does not remove internal candidates.
- Exact image promotion costs artifact storage but prevents apt drift. Retention/registry digest support must be proved; fallback rebuild is forbidden.
- Current four-target physical/host requirements are materially stronger than hosted build availability. Test resources remain unknown; report exact missing target/mode, not a generic “needs testing” or silent subset.
- As of E18 all six signing entries are populated. User entered app/export passwords; the selected Developer ID identity was exported into an owned private folder, encoded in memory and uploaded via encrypted GitHub secret administration. The temporary export was removed; original Keychain identity untouched. Actual P12/password pairing, import, signing and notarization remain unvalidated. No further private input is currently requested; no credential validity assumed.
- GHCR visibility may need normal package-admin action after first push. Report partial image stage and keep release draft if anonymous availability fails.
- Checksums prove payload consistency, not resistance to a compromised publisher. Notary acceptance is not filesystem qualification. No new security promise, sandbox/service or paid dependency is introduced.
- Classification remains Large/High even if runtime Go files remain unchanged. Architecture review is requested on this completed design under fresh routing rules. Review must not reopen settled normal-only scope or turn execution prerequisites into a new product questionnaire.
