# Design — First downloadable NFS release

## Solution And Approval Basis
- **SR-004 / Design Ready — Architecture Design Complete**. This is release-first requirement/design recovery, not a code defect or Delivery Completed. Large/High; review of this delta is pending. Prior ARCH001 covered SR003 only.
- Requirements **R3/SR004 Approved**, user direct publication-first instructions in `delivery-evidence/dr-003/user-publish-first-direction.json`; exact scope/approval in `approval-record-sr004.md`. Normal v0.1.0/four targets retained. `postpublication-testing-plan.md` is the approved deferral/custody supplement. No renewed user question.
- Package nfs-first-release / autobyteus-nfs-3 / project_task_97c6ab09-83cb-46df-bf28-d07b39259dd5. Canonical investigation: `/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/nfs-first-release/tickets/in-progress/nfs-first-release/investigation-notes.md`, E19–22 for this recovery; E01–18 historical.
- Workspace `/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/nfs-first-release`, `codex/nfs-first-release`; intake HEAD a5f57097578f9503eff0beb120dbc9e33e194eef, product8436d0cf6048cd3b4cadbf28815e3d9f82ba6b34. Last Delivery-refreshed origin/main/base7e375984be2bea7a4d536e43cc59d6bc2b116870; finalization origin/main with fresh fetch by Delivery.
- Authorities read: solution-designer SKILL; full requirements-engineering, architecture-design, design-principles, handoff-references and required templates; NFS AGENTS/DESIGN/TESTING/RELEASE and packaging/RELEASE (2026-10-18). No closer AGENTS. Project design conflicts: none. R3 explicitly supersedes the old release policy's physical/user sequencing; implementation must update the guides and code together. Design-examples N/A.

## Current-State Read / Intended Change
IR002 already implemented the cohesive candidate → qualification → payload → publication flow; CRR003 reviewed it. API002 actually built/downloaded the complete candidate but could not run assigned physical tests. Old qualification.py deliberately requires independent physical rows and an executed-user receipt. Final metadata fills QualifiedTargets and VerifyRelease requires that field before installation. Changing only publication would either leave downloads unusable or falsely label targets qualified.

**Replace the old qualification-as-admission contract with explicit release readiness and separate deferred field-validation status.** Preserve the existing candidate/engine/signing/payload/immutable-publication implementation, not a new release system. No runtime NFS/backend/consent behavior change. Official normal release availability and actual filesystem qualification are different claims.

## Task Size And Architectural Risk
- **task_size: Large**: release-control record/lock, Python metadata/payload/publisher contracts, Go release metadata/admission, workflow/tests/docs and actual four-platform signed publication are affected. The recovery is narrower than the original release implementation but crosses multiple distribution boundaries.
- **architectural_risk: High**: authorized publication of explicitly field-untested privileged tooling; private signing keys, immutable external effects and identity/claim coupling. Native green tests cannot prove field behavior.
- Escalate any newly needed host-state/backend/source protection change, unsigned fallback, target/channel omission, paid hosts or new product scope. Missing physical hosts are now deferred, not escalation for prepublication permission; concrete signing/integrity/access failures still block.

## Architecture Investigation Evidence
| Evidence / source | Observed current path | Decision supported / remaining uncertainty |
| --- | --- | --- |
| E19 / DR003 exact user direction, API002 report | Actual candidate success, missing field hosts, no release/tag | Change intent explicitly; preserve old verdict, no new physical campaign before release |
| E20 / release.py, qualification.py, payload.py, publication.py | Physical/user record demanded at every preflight/assembly/verify/write boundary | Replace singular owner, no bypass flag or only one call-site deletion |
| E20/E22 / candidate.runtime_metadata → setup.Release → VerifyRelease → install.sh | Generated QualifiedTargets gate; other Release uses supply existing engine pins/image | Separate releaseTargets from field status, current-schema-only bounded installer admission |
| E20/E22 / identity.source_hash, candidate.verify, engine manifest lock | Every changed production path hashed; workflow bytes and native manifests verified | API002 candidate cannot be promoted after this change; new exact candidate required |
| E21 / DESIGN.md and read-only remote0 releases/0tags | One empty lock, no published manifest/release obligations | Clean-cut derived metadata/control replacement, no live-host migration |
| E16/E18 / signing and external contracts | Credentials provisioned; immutable promotion and Accepted notarization required | Reuse unchanged, actual signing/public accessibility still unproven |

## Change Scope
UC001–005, BEH001–006: replace qualification/readiness coupling; narrowly change release metadata/install admission, pipeline wording/plumbing, evidence provenance/notes and affected tests/docs. Source hash remains complete. Preserve candidate retrieval, engine recipe/pins/packages/OCI verification, signing, tag/draft/asset/image recovery and ordinary CI nonpublication.

Leave backend/platform/source/mount/private-state/lifecycle semantics, installed host records, application/superrepo, dashboard nfs-2, updater/editor, PM boards, original archives and unowned caches alone. No live setup/deployment/upgrade or credential reprovisioning. No Homebrew or new platform.

**Follow-up:** postpublication shared-filesystem/physical/user validation and fix-forward, carried explicitly by Delivery to terminal Solution Designer → requesting PM per `postpublication-testing-plan.md`. No new Task/dispatch or test completion invented. No other new follow-up.

## Relevant Behavior And Production-Path Map
| Behavior / kind | Approved trigger / REQ / AC | Existing evidence → target production path |
| --- | --- | --- |
| BEH001 Operational | SCN001; REQ001/002; AC001 | Existing candidate orchestration retained; DS1 builds NEW reviewed current-source metadata/code, no publication |
| BEH002 Contract | SCN002/005; REQ003/004/006; AC002/003/006 | Old qualification → DS2 readiness owner validates exact candidate, real prepublication evidence, explicit release-first authority and deferred status |
| BEH003 Operational | SCN003/006; REQ001/005/006; AC004/006 | DS3 payload/publisher consumes readiness not physical receipts; signing and immutable external sequence unchanged |
| BEH004 User | SCN004/005; REQ005/007/008; AC005/007 | DS4 checksum/archive/current release schema + distribution target → install/version with deferred notice; no false qualified flag |
| BEH005 Contract | SCN002/004/007; REQ007/010; AC005/008 | Existing host/source/state guards unchanged; DS2/4 exercise owned no-setup checks only |
| BEH006 Operational | SCN007/008; REQ009/010; AC007/008 | DS3 receipt + explicit off-spine follow-up custody; docs separate build/distribution from field qualification |

## Supplemental Artifacts
Canonical inventory in investigation notes. Current: `approval-record-sr004.md` (R3 authority), `postpublication-testing-plan.md` (approved deferred scope), Delivery exact direction/handoff (read-only), API002 report (actual candidate/history, not new Pass), E18 credential upload receipt (provisioning only). Prior design/requirements snapshots and all review/implementation/API histories remain linked. ARCH001/IR002/CRR003/API002 do not cover this new delta. Independent review of SR004: pending; omitted new review artifact **N/A — not yet applicable**.

## Task Design Health Assessment
- Posture **Behavior Change**; design issue **Yes under R3**, not a retroactive source defect under R2.
- Structural trigger: **Shared Structure Looseness / Boundary Or Ownership Issue**: one QualifiedTargets concept controls distribution admission and asserts physical/user qualification; removing only the publisher gate leaves installer behavior contradictory.
- **Refactor needed now: Yes, bounded**: replace qualification.py with a release-readiness owner and replace generated metadata semantics at the existing runtime admission owner. Existing candidate/payload/publication decomposition is healthy; no extra coordinator, provider layer, framework or broad runtime refactor.
- Root cause: changed authority plus conflated claim/admission structure. Response: one current schema, one policy path, explicit immutable deferral state. No skip-qualification switches, legacy fallback or test-success-to-userVerified conversion.
- Residual risk: actual filesystem behavior remains unqualified; mitigated by honest notices, preserved safety guards and specific later test/fix custody, not falsely claimed eliminated.

## Terminology
**Build target**: native binary exists and checks run on that CPU/OS runner. **Release target**: approved distribution asset may pass installer admission. Neither is a field-qualified platform. **Readiness**: exact authorized candidate plus observed prepublication release checks and disclosure. **Field validation**: actual independent shared-filesystem/physical and user testing, deferred for this release. Signed/notarized does not mean field tested.

## Legacy Removal / Decommission Plan
| Remove / replace in this change | Why unnecessary | Single replacement |
| --- | --- | --- |
| qualification.py physical/user admission owner and all live imports | R3 supersedes that prepublication policy | readiness.py; do not retain old module as fallback |
| Lock qualifiedTargets/qualifiedSourceHash/physicalEvidence/userVerified/qualification fields | They mix an install/release permission with an unperformed test assertion | Pins + measured engine + releaseReadiness ref; field status in readiness record |
| --qualified flag and runtime QualifiedTargets/qualifiedTargets field | Cannot truthfully fill them to install untested official release | --release flag, releaseTargets + explicit fieldValidation |
| Old path/physical/user gating fixture assertions and docs | Now assert superseded behavior | Readiness, truthful-deferral, current-schema/install-negative tests; raw historical evidence stays |
| Dead touched constants/imports/qualification-only topology validation code | No longer a live release prerequisite | Later field-testing plan/owner, not dormant policy code |
No changes to immutable-retry/signing mechanisms, no old/new paths in parallel. Old records/CLI flags fail current admission; no conversion of old physical claims or legacy flags to release permission.

## Persisted Data / State Transition Decision
Repository DESIGN.md was read as the migration authority; E20/E22 trace actual writers/readers.
| Subject / volume | Current semantics / constraints | Decision / rationale |
| --- | --- | --- |
| One committed empty release-lock | package/base pins, null engine, qualification empty; no public releases | **Discard or Rebuild** only control fields into current shape; retain pins and measured engine identity. History preserved in Git, readiness defaults null until actual evidence |
| Generated embedded/loose release.json and CI candidates | release.py/candidate writes; cmd main/VerifyRelease reads; installer stores informational copy under version directory | **Discard or Rebuild** new candidate from reviewed source. Old API002 retained untouched for history, never passed to new promotion. No published-client compatibility obligation and no installed-copy scan/migration |
| Tracked development release.json stub | Non-installable development metadata, not release proof | Update minimal schema/status defaults if needed; keep empty targets/no measured engine, never commit generated release assets |
| Root-owned attachment/hosted/pending records, actual user files/mounts | Release is not persisted inside them; service uses only engine packages/image | **Not Affected**; no migration/startup gate or rewrite |
| Tags/releases/assets | Empty now; later immutable published identity | **Directly Usable — No Migration** using existing reconciliation; never overwrite |
| Secrets, historical evidence and owned retained old candidate | Provisioned / required historical proof | **Directly Usable — No Migration**; preserve, no re-export or cleanup by SD |

No migration plan is warranted. ReleaseReadiness refs must use durable repo paths not ticket paths that move during archival; no new state daemon/database.

## Data-Flow Spines / Narratives / Actors
| ID / scope | Arrow chain and narrative | Governing owner / subjects |
| --- | --- | --- |
| DS1 Primary | Explicit build-only dispatch → fixed reviewed checkout → measured engine/OCI + native checks/build → new retained candidate/envelope. All four jobs succeed; no release permission/secret/registry push | Existing workflow/candidate; CandidateIdentity |
| DS2 Primary | Verified current candidate → API affected checks → Delivery evidence audit + release-first user authority/plan → readiness record/lock → read-only publisher preflight. Deferred field/user tests are explicit dispositions, not missing successes | readiness.py; ReleaseReadiness, API/Delivery evidence owners |
| DS3 Primary | Reviewed main + readiness → final native metadata/signing → retained payload → exact annotated tag/draft/assets → exact OCI/public access → normal public release/download receipt. Final bytes differ by metadata/signatures, source/engine/OCI stay bound | payload.py/publication.py/signing; PublicationIdentity |
| DS4 Primary | Versioned download → checksums/bounded exact archive/equal manifest → schema/target/deferred-state admission → notice → owned CLI install/version. Actual setup still requires unchanged host checks/admin/storage consent | Existing install.sh/VerifyRelease; ReleaseManifest |
| DS5 Bounded within DS3 | Observe remote state → resolve annotation-bound original payload → verify/reconcile missing exact stages or refuse conflict/expiry. No new signatures/rebuild for retry | Existing publication owner |
Return/event spine: **N/A**, no asynchronous product subsystem added. Follow-up custody is a human/task handoff outside runtime, not a callback or release-blocking worker.

## Contract Decisions
### D1 — Singular readiness record and effect boundary
Rename qualification.py → `packaging/release_support/readiness.py`, retaining bounded ref/hash checks and exact candidate/source/engine/OCI/ancestry checks while replacing physical/user requirement validation. Do not merely weaken `userVerified` to optional or add `--skip-tests`.

New exact lock shape: `ubuntuBaseImage`, `ubuntuPackages`, `engine`, `releaseReadiness` (null or `{path,sha256}`), `note`. Defaults null/engine-null refuse publishing. Engine manifest `lock` writes the measured engine and clears releaseReadiness; no old qualification fields emitted. Readiness publication validation requires all four targets in canonical order. Source hash remains based on pins + measured engine + every production file, never on mutable evidence refs.

Use durable `packaging/releases/v0.1.0/readiness.json` and adjacent reviewed/sanitized evidence/notes/plan snapshots, generated by Delivery from real records after new API coverage. References may point to other stable in-repo evidence files but **not moving tickets/in-progress paths**. A signed public receipt must survive ticket archival and same-payload resume. Do not commit synthetic fixtures or populate readiness during this SD/design round.

Readiness exact fields:
- `schema:1`, `kind:"release-first"`, `version`, `targets` (exact four), `candidate` (existing actual `{recordSha256,envelope}`), `sourceHash`, `engineManifestSha256`, `oci`.
- `authorization`: `{kind:"publish-before-field-testing", requirementsRevision:"R3/SR004", version, evidence:{path,sha256}}`. Version must equal candidate/requested release. Evidence is the genuine user direction, not a test statement. Human review confirms meaning; parser verifies identity, not truth.
- `checks`: exactly `native` and `releaseControls`; each `{status:"passed", evidence:{path,sha256}}`, with actual current API/CI records. Candidate envelope remains validated by actual Actions API and full artifact traversal. Reject failed/skipped/not-tested claims here; field deferrals belong only below. These are prepublication checks, not a fabricated overall historical API Pass.
- `fieldValidation`: exactly `{filesystem:"deferred", user:"deferred"}` for this release-first contract. No supported `passed` shortcut in this change, no independent topology rows or executed-user placeholders.
- `postpublicationPlan`: `{path,sha256}` to the approved nonempty scoped plan and named custody. `review`: existing `{candidateCommit,sourceHash,evidence}` covering actual reviewed source and any intervening diff. `releaseNotes`: hashed reviewed Markdown.

Keep exact shape/type/duplicate-key/no-traversal/regular-file/bounds/hash checks; candidate metadata/run/workflow/attempt/current source/engine/OCI equality and ancestor checks remain. Release readiness cannot be inferred from null lock, candidate success alone or arbitrary consent text. Default empty readiness refuses `--check-publish`; explicit audited R3 deferred record passes the intended prerequisite without any field/user Pass.

Update release.py, publication.prepare/bind/publish and payload.assemble/verify to use this one owner. Preflight productionHash comes from validated readiness/candidate sourceHash, not removed qualifiedSourceHash. Update provenance to `schema:2`, `releaseReadiness` ref plus explicit `fieldValidation`, replacing qualification; keep all other immutable members/signing/source/OCI bindings. Verify emitted disclosure against readiness during payload verification and same-payload resume. Add a deterministic disclosure paragraph to the public release body/notes from validated state, so omission of that paragraph cannot hide deferral. Preserve reviewed prose as well; do not put credentials/private access details in public evidence or notes.

### D2 — Runtime distribution admission without a field claim
Current runtime release metadata becomes schema2 with `schema`, `version`, `sourceHash`, `ubuntuPackages`, `engineImage`, `engine` (existing optional development omission), `releaseTargets`, `fieldValidation`. Explicit named Go field type for the two validation statuses; not a generic map carrying arbitrary policy. Replace QualifiedTargets; do not retain an alias.

Candidate metadata: schema2, releaseTargets=[], fieldValidation={filesystem:deferred,user:deferred}; candidate version can still run for build smoke, but public installer admission refuses it. Final metadata: same source/engine/OCI/version, releaseTargets exactly four only after readiness validation, same truthful deferred statuses. `--release --candidate <dir>` replaces --qualified; final canonical image digest remains required. Candidate-only isolated registry alias capability keeps the exact OCI/source invariant and empty targets; not part of this prepublication physical test campaign.

`VerifyRelease` remains bounded/regular-file, validates the current release schema locally (including no legacy/unknown claim fields), exact typed downloaded/embedded equality including engine identity/status, and valid release target membership for runtime GOOS/GOARCH. Require nonempty valid unique target set and exactly supported deferred field status; legacy qualifiedTargets-only, missing status/schema, unknown/passed status and mismatched engine/source still refuse. Local strict release decoding must not change config.Decode's installed-state additive-field policy. No fallback or installed-state migration.

After successful verify-release, the existing CLI dispatch emits a concise stderr notice: this official release's shared-filesystem/physical and user testing is deferred; distribution/signature checks are not field qualification. Keep `version` stdout exact for existing automation. No extra approval prompt/flag or gating on a newly installed host's test status. Installer still calls verify-release before writes; it naturally displays the notice, then installs and invokes explicit `version` for smoke. Fix misleading “qualified version” errors to “versioned release”; keep all archive/checksum/member/size/container/OS protections. Normal create/connect remains explicit consent; this task does not invoke it on live user storage.

### D3 — Candidate invalidation, signing and publication retained
All changed source/control/workflow/installer/runtime inputs remain hashed. API002 run39113335636/1, artifact12131531399 and retained bytes are **historical and stale for the replacement source**. New reviewed source requires a new successful candidate; no editing old records, self-declared same source or removing files from source_hash to save a run. Use the existing complete engine-build/OCI path for that candidate; pin/source recipe unchanged. After candidate creation, only reviewed readiness/docs/test-only descendants with equal production hash/engine/OCI can advance to final main without another candidate build.

Keep existing manual candidate/publish dispatch, false default, native four-runner matrix and cancellation guards, publication-on-exact-main requirement, least privileges, no automatic tag recursion. All six signing secrets remain provisioned; actual import, selected Developer ID/team, hardened-runtime/timestamp codesign, explicit Accepted notary and sanitized receipts/always-cleanup remain mandatory for both Mac architectures. No new user credential request absent real validation error. macOS15 hosted native tests are not macOS26 field qualification.

Final payload before writes remains four exact four-member archives, installer, runtime/engine manifests, full modified source/inventories/notices/licenses, reviewed truthful notes, updated provenance and complete checksums. Signing/metadata change final binary hashes; attribute them, do not assert equality to unsigned candidate. At minimum inspect final per-target metadata/version and signatures from actual final artifacts; anonymous public asset hashes and canonical OCI index/children must match. Delivery's owned-HOME public install/version smoke and native Mac signature/download verification remain, but no physical/shared-filesystem test or end-user test is smuggled back into publication readiness.

Unchanged remote order: retain payload → nonforce annotated exact-SHA tag bound to payload artifact/run/attempt/hash → exact normal draft → add only missing byte-equal assets and verify → skopeo --all --preserve-digests exact OCI → confirm specific package public/anonymous child access → publish non-prerelease/latest → public download checks. Never clobber/delete/move tags/assets/images, rebuild or re-sign a bound retry. Use a fresh same-input manual dispatch to inspect remote state; no failed-job-only replay with stale preflight. Missing/expired/conflicting payload/access fails precisely, leaves honest partial effects and task open. No arbitrary broad token/org change.

### D4 — Truthful docs, validation and follow-up
Root/packaging RELEASE, README, TESTING and engine README must consistently say: first official normal v0.1.0 is authorized **before** field/user validation; current source/native/release-control/signing/integrity/download gates remain. Four downloadable build targets and unchanged intended host floors are not field-qualified support. Explicit deferred statement in README/notes/provenance/installer; no permanent “unavailable” claim after successful publication, and no premature working-link claim before it.

Field tests from API002 Q01–Q06/U01 move to explicit postpublication disposition in the **new** API ledger/revision. Historical API001 Fail/API002 Blocked and raw evidence stay unchanged. API judges new changed release-boundary coverage under R3; no reused percentage/blanket Pass, no old application or full filesystem campaign. Delivery may finalize this release once current required gates and follow-up custody are complete; deferred field testing does not keep this release task open. Follow-up reports any discovered defect and uses a new approved fix-forward version, never mutating v0.1.0.

## Ownership / Interfaces / Dependency Rules
| Boundary | Owner / input → output | Forbidden alternate |
| --- | --- | --- |
| release.py facade | CLI argument plumbing → candidate/readiness/payload/publication | Inline policy duplicate, --skip/--qualified compatibility |
| readiness.py | Lock + exact candidate + bounded genuine refs → audited readiness/error | Test execution, invented approval or physical Pass |
| candidate.py / identity.py | Existing artifact/source/native metadata identities; shared schema output | Stale record editing, excluding changed inputs from hash |
| payload.py | Readiness + final native/signing → complete retained immutable payload | Publisher signs/rebuilds, missing deferral provenance |
| publication.py | Validated exact payload/remote observations → existing ordered publication/receipt | Manual bypass, clobber, releasing before signing |
| setup.Release / VerifyRelease | Current generated schema → local equality/target/claim admission | Runtime reads GitHub/readiness ledger or converts installed host state |
| API / Delivery | Execute affected checks / judge evidence, prepare actual readiness and publish | SD/reviewer fabricates their results |

Dependencies unchanged: workflow → thin facade → cohesive release_support owners → existing engine validator/effect adapters; installer → existing CLI. Readiness reuses candidate and identity helpers, not a new policy service. Named shared values: ReleaseReadiness and ReleaseManifest have different lifecycle/claim scope; external envelope cannot be embedded into its own hash. Public runtime does not carry user statement/PM task IDs/raw test logs.

## Off-Spine Concerns / Capability Reuse
- Reuse identity bounded JSON/path/hash and engine manifest verifier; rename only qualification owner to readiness. No generic shared-utils expansion.
- Signing/secret hygiene remains narrow existing shell capability; no policy/publication ownership there.
- Logging/retention/cleanup remain current workflow/effect owners; preserve raw failed runs and no-secret logs.
- Host safety owners untouched; current Go regression tests demonstrate preservation, not actual field qualification.
- Postpublication custody stays in task/Delivery/PM artifacts, not runtime or automatic test infrastructure.

## Names, Structures And Responsibility Tightening
Names are intentionally distinct: ReleaseReadiness authorizes distribution; ReleaseManifest describes the exact binary; fieldValidation records missing field evidence, not a success bit. CandidateIdentity and PublicationIdentity retain existing separate source/run/byte meanings. Naming drift risk is addressed by removing qualifiedTargets/--qualified rather than retaining misleading aliases.

Draft allocation considered letting publication.py interpret the deferred exception. Re-tightening rejects that: metadata generation, payload verification and resume also need the same invariant, so readiness.py is the one control owner. Reuse candidate.runtime_metadata for the Python output shape and setup.Release for Go's typed read boundary; no third ad-hoc serializer in shell. Shared fieldValidation fields have one meaning each and replace, rather than overlap, qualified/userVerified fields. Release target set is distribution permission; candidate inventory is actual artifact membership. Both are compared, not independently inferred. Duplicate authority fields in provenance are identity assertions checked against readiness, not editable alternative policy.

Capability allocation: existing packaging control **Extend**, existing installer/CLI admission **Extend**, engine/source/signing/host owners **Reuse**, durable release evidence directory **Create** as data only (stable archive-safe path), no new runtime subsystem. Applied pattern is the existing staged immutable publication with reconciliation; the policy change does not create a rollback framework. Final responsibilities are projected below.

## Target Subsystem / Folder / File Mapping
| Paths / action | Responsibility and justification | Excluded |
| --- | --- | --- |
| packaging/release_support/qualification.py → readiness.py | Replace obsolete control owner with exact readiness/ref validation | Dormant physical gating fallback |
| packaging/release_support/{candidate,payload,publication}.py; __init__.py | Current runtime schema, readiness-consumer/provenance/notice changes; existing lifecycle boundaries | New promotion/signing engine |
| packaging/release_support/identity.py | Existing whole-source hashing remains; focused shared schema constants only if needed | Exempt changed files or broad utility refactor |
| packaging/release.py | --release + current metadata/check-publish dispatch | --qualified alias/bypass flag |
| packaging/release-lock.json; packaging/engine/manifest.py | New null readiness default; clear it on measured-engine lock write | Fake populated readiness or package/backport change |
| packaging/releases/v0.1.0/ | Durable actual readiness/approval/plan/notes/selected evidence snapshots by Delivery after validation; archive-stable | Generated binaries, credentials or synthetic results |
| internal/setup/service.go; internal/cli/verify-release.go; internal/cli/run.go | Typed current release metadata, local strict equality/admission and successful-verification stderr notice | Host lifecycle/config-decoder changes |
| cmd/autobyteus-nfs/release.json | Minimal tracked development stub if schema update needed; non-installable empty targets | Committed generated final metadata/assets |
| scripts/public/nfs/install.sh | Existing verify path and correct release language; integrity preserved | User-test prompt, live setup in smoke |
| .github/workflows/release-nfs.yml | Current flag/description and needed readiness plumbing; existing matrix/guards | New automatic trigger, early push or permissive failure handling |
| internal/cli/{cli_test,engine_release_test}.go + focused admission tests | Actual new schema, wrong target/claim/equality refusal, notice stdout/stderr | Physical success claims |
| scripts/tests/nfs_release_fixture.py, test_nfs_{release_records,release_publication,release_workflow,source_identity,engine_packaging,packaging,installer_fixture}.py | Update real owner consumers and controls, new false-claim/stale/readiness/engine-reset cases; preserve retry/signing coverage | Weakening tests to string-only happy paths |
| README.md, RELEASE.md, TESTING.md, packaging/RELEASE.md, packaging/engine/README.md | R3 policy, claim boundaries, runnable instructions after publication | Historical report rewrite |

Folder check: release_support remains a compact cohesive control/effect group with existing owners, **Mixed justified / low over-split risk**; .github transport only; internal existing runtime/config/value owner only; packaging/releases immutable release evidence, not application persistence. No new framework/subsystem needed. Source-size/refactor check during implementation must keep these boundaries clear.

## Concrete Shapes / Compatibility Rejection
Good: releaseTargets=[four], fieldValidation={filesystem:deferred,user:deferred}, signed exact payload → install + truthful warning. Bad: qualifiedTargets=[four], userVerified=true because user said publish.
Good: new current candidate + new API release-boundary result, old API002 remains Blocked. Bad: change old result to Pass to satisfy gate.
Good: same annotation-bound final bytes on resume. Bad: new signature/packing bytes under existing tag.

Rejected compatibility: old --qualified alias, old QualifiedTargets admission fallback, accepting old qualification schema as readiness, keeping old physical-required branch under an emergency override, or reusing old candidate under new source. No published consumers require these; use one current contract. Installed-state migration **N/A**, not touched.

## Change / Refactor Sequence
1. Implement current readiness/lock/reset and schema tests; replace old module/fields/flags atomically across callers. Keep readiness null until genuine new candidate/evidence.
2. Implement metadata/Go installer admission and notice; update generated-development defaults/fixtures/workflow flags and all affected policy docs. Preserve engine/source/safety/signing/immutable mechanisms.
3. Implementation local checks; configured independent source review. API updates current ledger first, executes affected current-schema/installer/release controls and new complete hosted candidate, preserves old failures and explicit deferrals. No physical-host questionnaire before publication.
4. Delivery prepares archive-stable actual readiness/authorization/check references/notes/plan from that evidence; fresh main integration/reviewed diff under repo policy. New production changes require new candidate; evidence-only descendants do not if exact hash/engine/OCI/ancestry match.
5. Actual authorized signed normal publication with retained gates. Verify public bytes/install/version/signature, record exact identities, follow-up custody and owned cleanup. If real signing/access/integrity gate fails, report precise blocker; no fake completion/manual bypass.
6. Terminal receipt forwards scoped postpublication testing/fixes once to PM. No duplicate dashboard or redispatch of closed tasks.

## Validation Intent / Acceptance Coverage
| AC | Required affected proof, not SD test results |
| --- | --- |
| AC001 | New four-native hosted candidate with complete engine/OCI, actual run/envelope/metadata; old candidate rejected after any changed production input |
| AC002 | Real readiness/approval/check refs; reject null, wrong version/source/engine/OCI/attempt, missing refs/plan/review, fabricated passed field/user status; valid explicit deferred contract admits preflight |
| AC003 | Retained real Developer ID/Accepted notarization for both Mac targets; negative fixtures/cleanup; final downloaded signature identities |
| AC004 | Gated actual normal publication + existing conflict/expiry/main-drift/cancellation/resume controls; no beta or overwrite |
| AC005 | Native Go actual schema/equality/target refusal including legacy-only/candidate/unknown status; installer real command with isolated no-setup version, warning and exact stdout; checksum/archive negatives |
| AC006 | Engine lock clears readiness; complete source hash covers replacements; final exact engine/OCI identity; provenance/notes deferred state and metadata differences explicit |
| AC007 | New scoped API evidence, actual publication/public downloads; archived historical Blocked untouched and deferred plan named, no full filesystem prerequisite |
| AC008 | Guides/README/notes consistent with R3, licenses/other-owner preservation, archive-stable evidence, current-main finalization and own cleanup |

Native Go race/vet/build/version and Python affected suites, actionlint/Bash and actual Bash3.2 workflow regression remain proportionate. Mutants should detect removed readiness/source checks, false field Pass or accepted legacy targets; synthetic records cannot enter real readiness. The actual newly executed scope determines API confidence, not a preassigned Pass/percentage.

## Tradeoffs / Risks / Guidance
Publishing before field tests is the user's explicit tradeoff, not evidence of reliability. Notices and later tests reduce misunderstanding, not runtime risk. This recovery must not turn simple release-first into a multi-policy platform: implement one explicit current contract and reuse existing owners. Secrets are provisioned; test in intended signing jobs, never print/export again. No SD production code/test/CI/publication action. Once completed, classify Large/High and route through fresh rules for the changed design only; downstream review should focus on this delta and retained invariants, not restart settled product choices.
