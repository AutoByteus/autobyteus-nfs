# API/E2E Coverage Investigation — nfs-first-release

## Investigation Meta
- Round API-REV-003; trigger CRR005 source Pass for IR004 after R3 release-first recovery. Prior API001/002 plans/results reviewed; canonical history is api-e2e-revision-record.md. The earlier in-flight plan is evidence/api-e2e/api-rev-003/validation-plan.md; this document now follows the updated plan-only skill format.
- Ticket/worktree: `/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/nfs-first-release/tickets/in-progress/nfs-first-release`; branch codex/nfs-first-release, target origin/main. NFS ONLY.
- Requirements requirements-doc.md R3/SR004 Approved; factual basis investigation-notes.md E19–22; solution-revision-record.md; design-spec.md SR004 Ready.
- Supplements approval-record-sr004.md and postpublication-testing-plan.md; exact direction delivery-evidence/dr-003/user-publish-first-direction.json (Delivery-owned).
- Architecture design-review-report.md / architecture-review-revision-record.md ARCH002 Pass. Implementation implementation-handoff.md / implementation-revision-record.md IR004 (cumulative IR003 replacement). Code code-review-report.md / code-review-revision-record.md CRR005 Pass100 (unaffected full R3 CRR004 review carried).
- Delivery delivery-revision-record.md DR004: source availability only, no main integration or publication. API history/report/progress are independent authorities; no upstream source Pass is an executable result.
- Prior API002 candidate must remain historical because production and engine recipe changed. No reuse as current evidence; no field-host questionnaire.

## Current Requirement And Design Basis
R3 separates release readiness from explicitly deferred filesystem/physical/user tests. Current prepublication native/release-control/source evidence and exact new candidate are required. Both Mac real Developer ID/Accepted notary, final signed payload, fresh main, immutable publication, canonical anonymous OCI and public download/signature checks remain later Delivery gates. This round validates the affected prepublication package for that next gate; it cannot claim the signed public release already exists.

## Supported Scenarios And Real Usage
SCN001 candidate; SCN002 readiness; SCN004 download/admission; SCN005 missing/stale/false claims; SCN006 exact-payload retry. SCN003 actual publication and SCN007 finalization are downstream, SCN008 field/fix-forward custody deferred. No new unsupported/contrived scenario. Corrupt copied envelope is SCN005 input-corruption control, not a fabricated second candidate.

## Changed Behavior / Boundaries
| Behavior / boundary | Change | Basis | Coverage consequence |
|---|---|---|---|
| BEH001 candidate | Preserved mechanism / new hashed inputs | AC001/006, DS1 | New complete actual run, not old artifact relabel |
| BEH002 readiness | Changed; qualification removed | AC002, DS2 | Exact authority/check/ref/source/engine/OCI and deferred status admission/refusal |
| BEH003 payload/publication | Changed control record/disclosure; immutable effects preserved | AC004/006, DS3/5 | Semantic rehashed tamper/refusal/retry fixtures; actual effects downstream |
| BEH004 native release/installer | Changed schema2 target/status/notice | AC005, DS4 | Native current admission tests; actual downloaded candidate refuses install, version remains exact |
| BEH005 host state/lifecycle | Preserved | AC005/008 | Existing guard coverage; no live storage campaign |
| BEH006 docs/custody | Changed release-first claims | AC007/008 | Honest deferred plan retained for Delivery→terminalSD→requestingPM |

API/transport here is CLI/Actions/artifact contract, not application HTTP. Runtime local release decoding, distribution permission, derived persisted control and external CI/download boundaries are affected. Frontend/browser/desktop shell/provider APIs/distributed NFS behavior are not changed; do not execute old application campaigns.

## Project Execution Discovery
Root `AGENTS.md`, `DESIGN.md`, `TESTING.md`, `RELEASE.md`, `README.md`, `go.mod`, `.github/workflows/{ci,release-nfs}.yml`, `packaging/RELEASE.md`, `packaging/engine/{README.md,manifest.py,source.py}`, current Go/Python tests govern execution. No closer testing guideline/instruction. Go module1.25 minimum, hosted pin1.27.2; Bash3.2 on local Mac; Python stdlib. No Node/sibling repo needed. Guideline conflict: None. Updated skill replaces ledger-result duplication with plan/report/append-only progress; old ledger remains historical, not a competing current authority.

| Component / data | Setup / readiness | Safety / cleanup |
|---|---|---|
| Local controls | Exact tracked non-ticket copy into owned APFS development directory, outside /private or /tmp; private HOME/TMP, explicit PATH, no account variables | No setup/root/storage; delete only owned copy after source equality check |
| Hosted candidate | Existing reviewed branch staging by Delivery; verify exact remote workflow bytes; `gh workflow run release-nfs.yml --repo AutoByteus/autobyteus-nfs --ref codex/nfs-first-release -f release_tag=v0.1.0 -f source_sha=<verified SHA> -f publish=false` | Omit candidate_run_id; no signing/publication; preserve exact run/attempt/artifacts, provider postjob cleanup |
| Actual artifact | Repository candidate-envelope/fetch-candidate/verify-candidate facade; Actions-read identity, exact unique artifact from run | No arbitrary latest selection; full member/engine/OCI/native verification; retain through release, no generated binaries/metadata in Git |
| Native smoke | Extract bounded regular candidate Darwinarm64 binary/manifest to owned HOME | version/verify-release only, no setup or quarantine bypass; remove copy |
| Final signing/publication | Delivery uses genuine stable readiness refs and reviewed current main after successful-test gate | Six secrets provisioned, no reprovision absent concrete failure; no API publication authority inferred |

## Persisted Data Transition Basis
Discard/Rebuild release-readiness and schema2 generated distribution metadata; current engine lock must clear readiness, legacy claims/flags refuse. Installed host records NotAffected; additive host decoder preserved. External immutable identities and history preserved; no migration, dual read/write or fallback. Required proof: R01/03/04/05 and native Go checks, with actual final signed metadata downstream.

## Existing Durable Coverage Inventory
| Path / tests | Intent / AC | Validity | Action |
|---|---|---|---|
| scripts/tests/test_nfs_release_workflow.py | Candidate/fresh/resume gates, actual Bash3.2 argv/failures AC001/004 | Still Valid | Execute first; CR-001 guard retained with --release |
| scripts/tests/test_nfs_release_records.py + nfs_release_fixture.py | Exact readiness, stable refs, candidate/OCI, provenance/mandatory disclosure AC002/006 | Still Valid replacement for old qualification contract | Focused then full; synthetic inputs remain fixtures only |
| scripts/tests/test_nfs_release_publication.py | Original-payload recovery, exact immutable stages, conflicts AC004/006 | Still Valid | Full suite; remote effects explicitly doubled |
| scripts/tests/test_nfs_release_signing.py | Accepted-only shell/cleanup AC003 | Still Valid | Full suite, not real Apple proof |
| scripts/tests/test_nfs_installer_fixture.py | Prewrite integrity/admission and notice AC005 | Still Valid | Full suite; downloader/binary doubles disclosed; Go parent covers permission child |
| scripts/tests/test_nfs_engine_packaging.py, test_nfs_packaging.py, test_nfs_source_identity.py | Engine-reset/new source hash/current shape AC002/006 | Still Valid | Full suite; no fake measured engine in product lock |
| internal/cli/release_admission_test.go + cli_test.go + engine_release_test.go | Schema/status/duplicates/target/equality; notice and exact stdout AC005 | Still Valid | Current hosted native Go/race on four targets |
| Remaining backend/platform/config/setup/Docker/service Go tests | Preserved host/pending/private/source safety | Still Valid | Hosted whole-module native race/vet; no mounted-filesystem claim |
| Old qualification fields/flag/gate assertions | Superseded R2 intent | Replace (IR003 already replaced) | No stale compatibility coverage retained or removal needed by API |

## Planned Cases
| ID | AC | Surface / kind | Command or steps | Temporary rationale |
|---|---|---|---|---|
| R01 |002/004/005/006|Existing tests|Focused workflow/records then `python3 -m unittest discover -s scripts/tests -p 'test_nfs_*.py' -v`|N/A|
| R02 |001/002/008|Existing static/temporary checks|actionlint, Bash/ShellCheck, `release.py --source-hash`, existing source.recipe_hash(), expected `--check-publish` refusal|No duplicate durable static runner needed|
| R03 |001/005/006|Hosted journey|Exact build-only dispatch; engine2/fullOCI/native4 race/vet/Python/build/version/aggregation; remote no-publication observation|Actual CI evidence, not local fixture replacement|
| R04 |001/002/006|Live API/CLI temporary probe|Actual envelope/fetch/verify; same-digest metadata alias; wrong digest/version/envelope/current-null readiness refusals|Real candidate/run-specific probe, existing durable parser controls retained|
| R05 |005|Downloaded native CLI temporary probe|Actual `version`; equal candidate metadata, false and legacy claims to `verify-release` must refuse|Proves retained binary boundary; final signed/installable metadata remains Delivery|
| C01 |008|Cleanup/preservation|Own source/scratch checks, old evidence preservation, actual candidate retained and reverified|Run-specific resources|
| Q01–Q06 (42) / U01 |003 requirement /007 AC|Not Tested — Deferred|Postpublication plan retains original IDs and field/user scope|Not prepublication/closure prerequisites, not Pass|
| D01/D02 |003/004/005/006/007/008|Not Tested — Downstream|Delivery actual readiness/signing/publication/public downloads/finalization|Required release completion, not performed by build-only candidate|

Progress log needed: Yes, `api-e2e-test-progress.md`. More than one case plus long hosted run. Skill changed mid-run: original ledger checkpoints retained; new cases use progress/report, no fabricated earlier start times.

## Durable Changes / Ambiguities
API additions/updates/removals planned: None; current durable assertions adequately target approved changed boundaries. No unresolved requirement/design ambiguity, no reroute before execution. Actual product failures follow normal failure-origin route. Record harness command/setup errors separately from product failures; do not change production behavior to satisfy an invalid probe.

## Investigation Decision
Proceed Yes. Source/durable edits No. Reroute required before validation No. Results, exact tested identities, confidence and broader decision are in the execution coverage report; historical outcomes in revision record.

R04 additional actual-boundary negative before final result: change only a copy of the real envelope wrapper digest and invoke fetch-candidate. Actual GitHub run/artifact metadata must reject mismatch before download destination creation. This tests explicit corrupt-retention input, not a second synthetic candidate; preserve real envelope/candidate unchanged.
