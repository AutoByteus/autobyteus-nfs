# Design Spec — Extract AutoByteus NFS

## Solution And Approval Basis
- Current revision **SR-002**; design **Ready / Architecture Design Complete**.
- Approved requirements **R1 / SR-001** in requirements-doc.md; Solution Designer within user's explicit separation direction; user informed in conversation. No behavior-defining supplement; no changed intended runtime behavior.
- Canonical evidence: investigation-notes.md, particularly E01–E11 and A01–A05. Workspace aliases S/N/D0 and their full paths are defined there and below.
- Authorities read 2026-10-16: solution-designer SKILL; references/architecture-design.md; full references/design-principles.md; source root DESIGN.md, AGENTS.md, TESTING.md, RELEASE.md; server/web AGENTS; design template. No project DESIGN.md yet in destination, and no closer NFS policy. No conflict with general principles. No design-examples sections needed.
- S = `/Users/normy/autobyteus_org/autobyteus-worktrees/extract-autobyteus-nfs`; N = `/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/extract-autobyteus-nfs`. Both task branches `codex/extract-autobyteus-nfs`; source base3712cd9bf0db998501d162db7f8655f169e3def6 → origin/personal; destination empty base → origin/main. D0 = `/Users/normy/autobyteus_org/autobyteus-nfs`, canonical requested checkout with PM metadata.

## Current-State Read / Intended Change
The service already owns CLI, privileged configuration, backend lifecycle, Docker selected-node operations and public attachment production. The app consumes those installed interfaces. Repository coupling instead appears in Go module identity, Python fixture roots, release source hashing, workflow version/build paths, installer download repository and a TS fixture read. Lift the tracked module into the standalone root, move service-owned distribution/tests with it, preserve installed behavior, and make app consumption explicit without importing NFS internals or requiring an NFS checkout. This is an ownership refactor, not a new filesystem design.

## Task Size And Architectural Risk
- **task_size: Large**. The delta spans independent module/developer checks, release supply inputs and workflow, app consumer fixture/test ownership, policy/docs and ordered two-repository finalization. It is not Large merely because 101 tracked embedded files move.
- **architectural_risk: High**. Material source/distribution ownership and qualification-identity boundaries change; privileged service packaging and two-repo integration can break despite unchanged runtime algorithms. Contract shape/persistence/concurrency are intentionally unchanged.
- Payload surfaces: docs, license/provenance, fixture snapshot. Structural surfaces: module path, packaging ROOT/SOURCES, installer repository, workflow triggers/version owner, consumer test dependency, independent finalization targets.
- Escalation: new runtime behavior, serialized field/path change, license/secret/publishing-policy change beyond this design, an incompatible app consumer, or concurrent source changes that cannot be preserved require return to Solution Designer. Do not silently broaden or weaken tests/qualification.

## Architecture Investigation Evidence
| Evidence | Exact source group in investigation | Decision supported | Remaining uncertainty |
| --- | --- | --- | --- |
| E02, A01 | main, CLI/config/runtime imports | root module lift with mechanical import rewrite | actual builds pending |
| E04–07, A02 | release.py, workflow, installer, mixed fixtures | self-contained source identity; moved tooling, split tests | CI execution/signing not claimed |
| E08–09, A03 | launcher-attachment producer, shell/TS consumers, fixture | preserve public boundary; pin consumer fixture | fresh consumer tests pending |
| E10 | LICENSE/LICENSING/CLA/notices/Guide | preserved terms, no publication enablement | remote secrets untouched/unverified |
| E01, A05 | source/destination Git snapshots | two isolated worktrees; ordered no-force finalization | later ref/owner races must be rechecked |

## Change Scope
Covers UC-001–004 / REQ-001–008: service module, service-owned installer/packaging/Python tests/workflow, minimal NFS repository policies/provenance, source consumer fixture and active documentation/release ownership references.
Deliberately left alone: app launcher production shell, TS binding/admission, web Guide implementation, Docker node protocol, source/identity/lifecycle algorithms, persisted records, runtime skill wrappers, app release/version helpers, pnpm dependency set, historical tickets, other apps/editor/updater. Only a demonstrated extraction-caused consumer issue may justify a bounded addition; new behavior returns upstream.
Follow-ups discovered: **None newly requiring a Task**. Prior deferred candidates remain with PM, not re-dispatched. Publication/platform qualification and remote signing credentials remain unavailable/unproven, not blockers for this no-release extraction. No live deployment.

## Relevant Behavior And Production-Path Map
| Behavior / approved REQ / AC | Trigger and preserved or changed outcome | Current evidence | Target spine |
| --- | --- | --- | --- |
| BEH-001 / REQ-001,002 / AC-001,002 | Contributor develops/checks standalone repository, no sibling source | E02,04,06 | DS-001 |
| BEH-002 / REQ-002,004,005 / AC-002,004,005 | Maintainer builds candidates; integrity/license/publication refusals remain, release no longer tied to desktop version | E04–07,10 | DS-002 and DS-003 |
| BEH-003 / REQ-003,006 / AC-003,006 | Existing service/app attachment use retains installed public contract and refusal behavior | E08–09 | DS-004, DS-005 |
| BEH-004 / REQ-007,008 / AC-007,008 | Maintainer integrates repositories, records exact identities and safe cleanup | E01 | DS-006 |

## Supplemental Task Artifacts
No new supplements. Prior DR002 context/archives are read-only historical evidence indexed in investigation, not current acceptance gates. Independent review artifacts: **N/A — not applicable yet**; this package requests the configured review, not an inherited review Pass.

## Task Design Health Assessment
- Posture: **Refactor**; design issue **Yes**; root cause **Boundary Or Ownership Issue / File Placement Or Responsibility Drift**.
- Trigger evidence: release.py mixes service and app source identity; same-repo workflow requires web package version; mixed Python file tests both service release and app launcher; TS fixture crosses sibling source boundary.
- Refactor needed now: **Yes**, these prevent the requested independent home. Reassign development/distribution owners, remove obsolete embedded paths, retain intentional deployed contract.
- No new runtime coordinator or shared framework needed. Existing config, setup, backend and docker boundaries remain coherent for this delta. No concurrency/refusal mechanism is added merely because a theoretical failure can be invented.
- Residual risks: independent future revisions can drift at consumer boundary; pinned fixture/provenance and explicit cross-repo validation are proportionate. No dynamic network lookup in app/unit tests.

## Terminology
“Independent” means no superrepo checkout/import is needed to develop/build/check NFS; it does not remove optional integration with a running supported AutoByteus node. “Consumer snapshot” is immutable test data with producer identity, not another maintained service implementation. “Qualification” is the separately gated platform/publication claim, not compilation or a passing fixture.

## Legacy Removal Policy / Removal Plan
No compatibility wrapper, symlinked embedded module, submodule, Go replace directive, old/new source fallback or forwarding installer is retained. Existing OS paths are unchanged contracts, not legacy repository compatibility.
| Remove from S | Why / replacement | Scope |
| --- | --- | --- |
| autobyteus-nfs/ tracked tree | Superseded maintained implementation; N root owns it | This change |
| .github/workflows/release-nfs.yml | Superseded distribution owner; N owns workflow | This change |
| scripts/public/nfs/install.sh | Unpublished source bootstrap; new repo owns future downloads | This change |
| test_nfs_engine_packaging.py, test_nfs_installer_fixture.py, test_nfs_release_workflow.py | Service-owned tests move to N | This change |
| service cases in test_nfs_packaging_and_launcher.py, old filename | Split service cases to N test_nfs_packaging.py and retain app cases as S test_nfs_launcher.py | This change |
| TS sibling fixture URL and obsolete same-repo release/docs claims | Pinned local consumer fixture and external NFS docs | This change |
No dead runtime code identified in the touched module after entrypoint/reference trace; moved runtime remains reachable. Remove obsolete path imports/test branches, not safeguards. Old tickets contain historical paths intentionally retained; they are not active owners. No unrelated cleanup discovered/authorized.

## Persisted Data / State Transition Decision
**Not Affected.** E08–09/A01 show config.Store/current JSON fields, installed executable/private/public paths, source marker, UUID/OS identity, jobs and consumer read paths unchanged. Go import namespace and build ROOT are not serialized or installed resource addresses. No data enumeration, migration, reset, backup choreography or new startup gate is warranted. Runtime volume unknown and irrelevant because no data access/write is required. Preserve bytes/permissions and ownership; task scratch only may be regenerated. Migration plan **N/A — no transformation**.

## Data-Flow Spine Inventory And Narratives
| ID / scope | Start → meaningful end | Owner and narrative |
| --- | --- | --- |
| DS-001 Primary / BEH-001 | Contributor clone → root Go module / Python fixtures → existing internal packages → build/test output → development binary | NFS developer workflow owns declared prerequisites and source paths; package tests remain real Go owners with scratch doubles at OS boundaries |
| DS-002 Primary / BEH-002 | Maintainer manual build request → NFS release.py identity/manifest → pinned engine inputs + Go native build → archive integrity/notices → retained candidate evidence | NFS packaging owns inputs and build identity; release workflow orchestrates bounded build jobs, not app version/state |
| DS-003 Primary / BEH-002 | Future explicitly authorized existing NFS tag/release → current-source/physical/user/candidate gate → signing and exact engine reuse → qualified assets on NFS release → installer verify-release → versioned user CLI | Preserved future publication contract only; no execution/qualification/authorization in this Task. Installer owns transfer/integrity; Go CLI owns setup consent, never delegated to download shell |
| DS-004 Primary / BEH-003 | User's supported setup/selected-node action → CLI trusted plan/consent → setup.Service/config/backend/Docker → published attachment + actual source/mount → app launcher/TS admission | Service retains lifecycle/storage authority. App launcher reads the installed CLI boundary; TS validates public descriptor and observed source/marker. This spine is moved, not redesigned |
| DS-005 Primary contract / BEH-003 | Maintainer changes/pins producer contract → N testdata parsed by Go → exact fixture snapshot in S with revision/hash → actual TS parser + shell contract controls → integration verdict | Producer owns fixture contract; app owns snapshot and consumption checks. No live/network cross-check on every unit test |
| DS-006 Primary operational / BEH-004 | Reviewed paired candidates → fresh integration and evidence → N origin/main established → S integration pinned to N commit → S origin/personal --no-ff → durable receipt/owned cleanup | Delivery owns two-repo sequencing and reports partial success honestly; no fictitious atomic transaction |

### Return / Event And Bounded Local Spines
No new asynchronous channel. Existing cli output/errors and descriptor publication carry DS-004 outcome. Existing service supervisor/reconnect and Docker recovery loops stay within service/setup/docker owners and keep their existing guards; no loop/state changes. DS-002 workflow needs/if results form a bounded build gate sequence (prepare → engine-packages/engine-inputs → engine → binaries → publish) with existing failure/cancel semantics. Tests continue to model that exact gate graph, not replace it with a general workflow interpreter.

## Ownership, Main-Line Nodes And Off-Spine Concerns
| Owner / node | Concrete authority | Off-spine concerns | Must not own |
| --- | --- | --- | --- |
| NFS cmd/cli/setup | Command dispatch, consent, privileged plan/application, source identity and attachment lifecycle | config store/validation; platform OS adapters; backend and docker | app source/version lifecycle |
| NFS packaging/release.py | Self-contained candidate metadata, source digest, manifest qualification/refusal | engine manifest/build recipe, license inventory, build outputs | app source hashing or implicit platform acceptance |
| NFS workflow | Candidate job ordering and explicit future publication | native toolchains/signing/artifact transfer | desktop release/version, new release auto-creation |
| Installer | HTTPS/checksum/member/embedded-metadata checks, owned download/install scratch | tar/SHA/platform detection | consent bypass, global storage mutation |
| AutoByteus launcher/runtime | Selected-node recreation/admission via existing installed boundary | local fixture + parser tests | Go service internals or owning installation/exports |
| Delivery | Safe branch integration/push/receipt/cleanup | provenance and fresh ref checks | unrelated canonical work or automatic public release |
Naming remains concrete: existing cli/config/backend/setup/docker/platform/service and packaging; no generic “shared helpers” extraction. Main nodes remain self-descriptive; ambiguity risk low.

## Ownership Boundaries / Dependency Rules
- Public service boundaries remain CLI commands (`launcher-attachment --nodes <node>` included), public five-field attachment descriptor and source marker; N internal packages stay behind them.
- App launcher may call installed `~/.local/bin/autobyteus-nfs` and inspect the selected Docker daemon/owned volume; TS may read `/etc/autobyteus-nfs/attachment.json`, actual mount and marker. Neither imports Go code or private state.
- The service's selected-node qualification intentionally inspects installed supervisor UID and `/app/autobyteus-server-ts/dist/workspaces/shared-workspace-binding.js` inside a node; preserve those strings. NFS source independence does **not** license removing app-aware probes.
- N developer/build/test commands may use local files and documented toolchains/artifact inputs, never `../autobyteus-workspace*`, app package.json or pnpm. S developer checks may use the pinned local fixture, never require a neighboring N checkout/network fetch.
- No vendored app launcher/runtime in N, no submodule/symlink/Go replace, no service implementation left in S. Consumer fixture duplication is narrow data, not duplicate policy.
- Boundary APIs/identity shapes unchanged: node name identifies selected node; storage UUID identifies source; daemon ID qualifies Docker context; release source hash plus exact engine manifest identify build inputs. No ambiguous generic ID/API is introduced.

## Interface / Shared-Structure Checks
Existing config.Connection / NodeAttachment and TS parsed binding retain singular field semantics, not a new common DTO package. Go producer test fixture is authoritative; consumer snapshot is explicitly pinned. CLI seven-line response order is unchanged (storageId, mountRoot, volume, descriptorDirectory, daemonId, export device, mount options). Contract consistency and malformed/wrong-daemon refusal remain test obligations. Entry main is thin dispatch to cli; no new facade or coordinator. Existing engine source/manifest logic is reused byte-for-byte where possible, not duplicated. Patterns: existing OS adapters/store only; no new registry/state machine.

## Final File Responsibilities / Target Folder Mapping
Draft candidates were the existing owners. The shared-structure check found no runtime structure to extract; the only split is mixed tests. The following is the final responsibility/path map (Rename/Move means tracked content, preserving modes; never blind copy ignored outputs).
| Change | Source → target | Responsibility / placement constraint |
| --- | --- | --- |
| Move/modify | S/autobyteus-nfs/{cmd,internal,go.mod,testdata,.gitignore,README.md,LICENSE,THIRD_PARTY_NOTICES,packaging} → same names at N root | Keep existing internal concern folders. Rename module and all internal import prefixes to `github.com/AutoByteus/autobyteus-nfs`; no runtime logic edits. Keep go1.25.0 declaration and current pinned CI toolchain1.27.2 unless a concrete prerequisite requires separate decision |
| Modify test path | N/internal/platform/directory_modes_test.go | `filepath.Abs("../..")` reaches new repo root; Python fixture still in scripts/tests; preserve test semantics and explicit skips |
| Move | S/scripts/public/nfs/install.sh → N/scripts/public/nfs/install.sh | Retain path to minimize fixture/workflow churn; change download repository to `AutoByteus/autobyteus-nfs`; placeholder remains unqualified |
| Move/rebase | Three service Python tests → N/scripts/tests/same names | Root remains parents[2]; embedded `autobyteus-nfs/` path prefix removed inside assertions/imports; preserve negative controls |
| Split | S/scripts/tests/test_nfs_packaging_and_launcher.py → N/scripts/tests/test_nfs_packaging.py + S/scripts/tests/test_nfs_launcher.py | Service refusal/build-only cases move; launcher selection/stop policy cases remain. No helper import spanning repositories |
| Move/modify | S/.github/workflows/release-nfs.yml → N/.github/workflows/release-nfs.yml | All checkout/build/output/license paths rooted at N; independent manual candidate/distribution workflow (below) |
| Add | N/.github/workflows/ci.yml | Nonpublishing native Go/Python developer regression workflow on push/PR; no app checkout, mounts, secrets or publication. Use pinned Go and native Linux/macOS runners; honest platform-dependent skips |
| Modify | N/packaging/release.py, Dockerfile, packaging/RELEASE.md | Rebase ROOT/local source identity and Dockerfile notices path; one distribution owner |
| Add | N/{AGENTS.md,DESIGN.md,TESTING.md,RELEASE.md,LICENSING.md,NOTICE,CONTRIBUTING.md,CLA.md,EXTRACTION.md}; N/docs/integration-contract.md | Minimal independent policies, exact inherited terms/CLA, provenance, installed contract and tested support boundary. Do not import app-wide unrelated instructions |
| Add/modify | S/autobyteus-server-ts/tests/fixtures/shared-network-workspaces/{attachment.json,provenance.json}; S/autobyteus-server-ts/tests/unit/workspaces/shared-workspace-binding.test.ts | Consumer fixture snapshot, pinned N repo/commit/path/SHA; existing parser test reads local fixture and checks recorded digest. |
| Modify | S/autobyteus-server-ts/docs/modules/shared_network_workspaces.md; S/RELEASE.md NFS section | External service docs/contract/qualification links, no same-repo release owner |
| Preserve | S launcher/TS production, web/utils/nfsLauncherCommands.ts, root version helpers/global TESTING | No implementation change required; Guide release remains null, generic source testing policy not ticket-specific |

N .gitignore also excludes owned binary root output, engine-candidate/engine-parts/artifacts and Python cache/generated out where applicable; do not hide source or PM metadata by broad ignore patterns. Documentation-only EXTRACT provenance is not a vendored old tree. Layering follows existing cmd → cli/setup → config/platform/backend/docker; folders retain real responsibilities without artificial fragmentation.

## Concrete Build And Qualification Decisions
### Module and standalone build
Lift module, not entire superrepo history. `go test -race ./...`, `go vet ./...`, `go build -o out/autobyteus-nfs ./cmd/autobyteus-nfs` from N; Python tests under scripts/tests with explicit commands. Python stdlib/Bash are test/build prerequisites, not user runtime dependencies. No pnpm/node/package.json/go.work/sibling replace for service development. Empty development engine-assets/README permits ordinary build; it is not a release-ready Linux engine. Preserve generated release.json separation from committed development metadata.

### Local source identity
N/packaging/release.py `ROOT = Path(__file__).resolve().parents[1]`; `LOCK=ROOT/'packaging/release-lock.json'`; engine module directory ROOT/packaging/engine; embed ROOT/internal/backend/engine-assets. SOURCE inputs become owned paths:
`internal`, `cmd/autobyteus-nfs/main.go`, `go.mod`, `scripts/public/nfs`, `packaging/Dockerfile`, `packaging/engine`, `packaging/release.py`, `.github/workflows/release-nfs.yml`, `testdata/attachment.json`, `docs/integration-contract.md`, `LICENSE`, `THIRD_PARTY_NOTICES`.
Keep deterministic relative filenames/bytes plus ubuntuBaseImage/ubuntuPackages/engine identities; retain test/cache/deb exclusions. Exclude generated release.json, outputs, qualification receipt files and qualifiedSourceHash itself to avoid circularity. Missing declared input fails, never silently skips. No source checkout is read outside N.

This hash attests **NFS source and declared integration contract**, not arbitrary app revisions. Future physical/managed-node publication evidence must explicitly identify tested NFS sourceHash/engine identities and AutoByteus consumer commit/image IDs. Those receipts are local N evidence files (not a required app checkout); the app's own release/Guide decision separately validates its pinned consumer. This explicit two-owner evidence replaces the old monolithic app-source digest, not the physical/current-source/user qualification gates. No new metadata runtime schema is needed. Keep lock `qualifiedTargets=[]`, `qualifiedSourceHash=""`, `physicalEvidence=[]`, `userVerified=false`, `engine=null`; extraction cannot populate them from prior proof. Changing scope/path hash must never inherit old qualification.

### Workflow and future version ownership
Remove the desktop package-version assertion and inherited superrepo push-tag publication trigger. Destination release workflow is **workflow_dispatch only** with existing `release_tag`, optional candidate_run_id and `publish=false` default; `WANT_PUBLISH` comes solely from explicit publish input. Release tag metadata is NFS-owned, no second package/version file. A future maintainer must separately authorize/create the NFS tag and existing release before publish; no `gh release create` or automatic tags/main pushes from this workflow. No tag is created now.
Keep six-job dependency graph, cancellation/failure handling, exact prior-engine candidate reuse, corrected engine verify/equality, immutable OCI identity, four target/native builds, size cap, Mac signing/notarization and existing-release requirement. Paths change consistently including removal of `cd autobyteus-nfs`, engine-candidate relative COPYRIGHT path, out/archive/signing paths. Build-only stays no login/image push/GitHub release upload. GHCR namespace remains ghcr.io/<owner>/autobyteus-nfs; no published package ownership/credentials mutation performed. App main/tag workflows lose only superseded NFS workflow, not desktop/server release behavior.

### Contract snapshot and evidence
N/testdata/attachment.json stays the producer fixture (exact original bytes). Add integration-contract.md documenting five-field descriptor, trusted installed paths, seven-line launcher response and optional app-node image expectations. Source fixture provenance records `{repository, commit, path, sha256}` for a real committed N fixture; no placeholder or fabricated commit at delivery. S unit test uses local snapshot and validates its digest and actual TS parser. During implementation/API paired check, compare snapshot with `git show <pinned-N-commit>:testdata/attachment.json` from a separate checked-out/archive producer; run Go producer and TS consumer checks. Ordinary tests stay offline. Updating consumer pin requires explicit review of contract and checks, not a runtime fetch or auto-sync mechanism.

### Licensing and provenance
Copy NFS LICENSE byte-for-byte; preserve THIRD_PARTY_NOTICES, engine source lock/patch/corresponding-source and copyright obligations. Copy CLA verbatim. New LICENSING/NOTICE/CONTRIBUTING adapt repository/branch references and applicable component scope only, preserving AGPL-3.0-only/commercial terms, copyright/contact, contribution requirements and the existing section7 permission verbatim; do not imply NFS has a released Apache predecessor. Link source licensing provenance. No SDK/license changes in S. N packaging still includes own LICENSE, notices plus Go/runtime engine copyright as existing flow requires.
EXTRACTION.md records source URL, exact extraction source commit3712cd9b (or explicitly updated integrated source if affected code changes), old embedded path and external file moves/split, date/Task, mechanical import/path changes, excluded generated assets/history, and immutable old bounded delivery links. Preserve author attribution without rewriting/importing unrelated Git history. Future N commit is recorded by S consumer provenance/delivery, not a self-referential N source file.

## New Repository Policies / Finalization
N AGENTS directs local DESIGN/TESTING/RELEASE and explicit path staging. DESIGN records existing service/runtime ownership, installed-path safety, no runtime schema/behavior change by repository relocation, no app-source build dependencies. TESTING declares developer prerequisites and layers, isolated scratch/no live resources, skip honesty and separate runtime/platform qualification. RELEASE is root finalization/no-release authority; packaging/RELEASE is detailed distribution contract, linked rather than contradictory.
N target origin/main, task branches codex/*; no public release by default. Initial history is the reviewed task branch root; no fake empty base or unrelated-history merge. Subsequent main changes follow normal reviewed --no-ff flow. Refresh/check origin main before every push; never force or overwrite another owner's new work. Source RELEASE still requires origin/personal integration, --no-ff and fresh check before push, in isolated worktree, never shared canonical source.

Ordered completion:
1. Validate paired candidates before finalization. Refresh S origin/personal and D0/N origin; if current NFS/consumer-owned source changes upstream, reconcile into N and tests/provenance rather than delete them blindly. Unrelated source changes integrate normally and targeted confidence is reconsidered.
2. Establish N origin/main from reviewed initial history after confirming remote main remains absent (or integrate actual new history without force, returning a concrete blocker if competing ownership cannot be safely reconciled). No publication workflow should fire on this push.
3. Pin S fixture/docs provenance to the actual committed N producer; prove equality and targeted checks on final integrated S; merge/push S personal per policy. If step3 fails after step2, report partial finalization, preserve commits, do not delete N/force rollback.
4. D0 is the user-requested working checkout: after remote finalization, safely populate its still-unborn main through an ordinary non-force checkout/tracking setup only if no new owner content/conflicts appeared. Preserve PM task-plans byte-for-byte. Do not use D0 for authoring/finalization, force-reset it, or update another owner's established checkout silently. Record any actual obstruction explicitly.
5. Archive this Task's canonical evidence in N per delivery lifecycle; source may link the exact N ticket/commit rather than duplicate all artifacts. Record both repository target/ticket/final commit IDs and remote confirmation. Clean task-owned scratch/toolchains/build outputs and safely removable task worktrees/branches only after durable evidence. Canonical repositories/PM files and old shared-network-workspaces retained checkout/assets are not disposable. No global clean/prune.

## Verification Guidance (intent, not claimed results)
Implementation owns self-checks, API/E2E owns final executable evidence, Delivery integrates/verifies/finalizes. Respect each repository TESTING/RELEASE. No old application/editor/full-VM campaign is a gate for this extraction.
| Checks / AC | Required evidence and scope |
| --- | --- |
| Standalone completeness AC-001,006 | Fresh `git archive`/clone into owned scratch with no sibling source, declared file/import/dependency audit; all documented local Go/Python commands run there. Do not validate only from a superrepo-rich working directory |
| Runtime preservation AC-003 | Normalize only approved Go import namespace and compare production files against recorded extraction source. Keep flags/state/paths/schema/backend recipes/engine pins and deployed app-module strings unchanged. Run full Go race/vet plus platform compile; unexpected semantic diff routes upstream |
| Build matrix AC-002 | Native build/version smoke, CGO_ENABLED=0 builds Darwin/Linux arm64/amd64, compile applicable test packages; distinguish compile from runtime. Use owned output dirs, no committed binaries/debs/generated release metadata |
| Packaging AC-002,005 | All moved Python tests incl real Go permission-fixture invocation; source-hash deterministic/local-only and input mutation invalidation; unqualified publication refusal; malformed archive/manifest/digest/path controls; workflow gates and actionlint/shell syntax. Assert no desktop version/readout/sibling source and no automatic publication trigger |
| Engine path AC-002,004 | Fresh standalone metadata/embed/build/archive exercise with actual retained corrected arm64 engine artifact copied read-only into owned scratch and verified by current manifest logic; retain its identity/source notices. E11 locates it. Synthetic both-arch fixture proves merge controls, not actual amd64 runtime artifact. Rebuild unchanged engine only if needed; never relabel missing amd64/signing/hosted Actions as Pass |
| Consumer AC-003,006 | Fixture pin/hash equality against committed producer; Go producer+TS binding unit tests; preserved launcher tests and shell syntax; relevant server production typecheck/build prerequisite if required by its test guideline; Guide null-release utility test as scoped regression. No paid provider/UI launch/live mount needed |
| Licensing/docs AC-004,006 | License-byte/provenance/links and exact recipe diff audit; source licensing/hygiene guards where applicable; independent docs instructions exercised, active references free of superseded ownership excluding old tickets |
| Delivery AC-007,008 | Fresh refs, integrated candidate identities and sufficient affected checks, evidence-only verification, no tags/releases/remote-secret changes, preserved canonical/PM/old archive state, owned cleanup receipts and truthful limits |

If actual current candidate functionality cannot pass a required extraction check, report that failure; do not downgrade the AC or add old full-product gates. Platform/signing/publication gates remain explicit **not qualified/not executed**, not silently Passed or a reason to deploy.

## Backward-Compatibility Rejection Log
| Candidate | Decision / clean-cut replacement |
| --- | --- |
| Embedded symlink, submodule, wrapper installer, Go replace to sibling | Rejected: still two-home/dependent experience; independent repo and explicit external docs/installed interface |
| Copy app source/launcher into N to keep old source hash | Rejected: unrelated maintained code and false ownership; local N hash plus explicitly revision-bound consumer evidence |
| Consumer tests fetch mutable main during every run | Rejected: hidden network/drift; pinned local fixture with provenance and integration equality |
| Import old qualification/source hash to avoid new checks | Rejected: different source identity, bounded old proof; lock remains unqualified and fresh extraction checks required |

## Tradeoffs / Risks / Implementation Guidance
Snapshot extraction makes old history a linked provenance rather than rewritten new history; user asked a maintained home, not history surgery. Consumer fixture pin duplicates a tiny data contract but keeps independent/offline tests and clear authority. Two-repo sequencing is recoverable and explicit, not atomic. Retain compact existing package layout; only real ownership splits justify new files. No new runtime validation layers or speculative migrations.
Implement the mapping, not an unrelated style cleanup. Preserve file modes, tests and licenses; stage explicit paths. Keep generated metadata/assets in owned scratch; exact old archive remains read-only. If ordinary root builds work but a relevant native/engine prerequisite is unavailable, record exact check and limitation, never claim all publication targets qualified. Completed design classification is Large/High because of real ownership/distribution impact, not because of historical ticket volume.
