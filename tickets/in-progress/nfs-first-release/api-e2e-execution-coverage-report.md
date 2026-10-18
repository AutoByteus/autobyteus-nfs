# API/E2E Execution Coverage Report — nfs-first-release

## Round
- **API-REV-003: Pass / 95.00% — affected prepublication validation only.** This result permits the proportional test-review gate. It is **not release readiness acceptance, a public release result, or task completion**.
- Plan/upstream links: [api-e2e-coverage-investigation.md](api-e2e-coverage-investigation.md). History: [api-e2e-revision-record.md](api-e2e-revision-record.md). Progress: [api-e2e-test-progress.md](api-e2e-test-progress.md). R3/SR004 Approved/Ready, ARCH002, IR004 cumulative R3, CRR005 source Pass100; DR004 source staging only.
- Trigger: new R3 release-first controls and candidate after IR004 review. Prior API001 Fail62.86 and API002 Blocked73.57 remain historical, not relabeled. API002's old candidate cannot qualify changed production/recipe inputs.
- Deviations: one temporary command used a nonexistent recipe-hash subcommand; preserved and corrected using the existing API in a second clean copy. Mid-run skill update moved current results into this report and append-only progress; the earlier ledger remains history. A final reporting-path checker also needed a `ticket:` prefix resolution correction (`artifact-audit-attempts.md`); corrected integrity audit passed without rerunning completed tests. No scope/gate relaxation by API.
- Evidence folder (E): `/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/nfs-first-release/tickets/in-progress/nfs-first-release/evidence/api-e2e/api-rev-003`.
- Observations/execution: 2026-10-18 UTC. `evidence-context.md` explains exact records, annotated raw logs and excerpts. No generated binary/engine bundle/runtime release manifest is committed.

## Routing Classification
Task size **Large**; architectural risk **High**; input **Reviewed**; successful output **Code Review**, then Delivery. Proportional successful-test review **Required** for the cumulative R3 durable coverage. API changed no production or durable tests. No new architecture/source-review loop requested.

## Tested Builds And Environments
| Env | Commit tested | Platform/runtime | Important configuration |
|---|---|---|---|
| L | `585d416c2746cf2963058d591b0753d0db8088f5`;120 inputs equal product `850dfeb97e2ec396b2b134e760dc9ee802873d6b` | Local macOS26.5.2 build25F84 arm64; Python3.9.6, Bash3.2.57 | Two exact independent APFS source copies outside /private and /tmp; private HOME/TMP; no account variables. No local Go run this round. Exact cwd/argv in local logs. |
| H | Same exact source/workflow/dispatch SHA | Ubuntu24.04 arm64/amd64, macos-15 arm64 / macos-15-intel amd64; Go1.27.2 | Actual run39118784695/attempt1, publish=false. Matching native race/compiler execution, not cross-compilation as proof; no signing secrets, registry push or NFS setup. Hosted Mac15 is not Mac26 field qualification. |
| A | Current facade from same N worktree; actual H artifact | L plus authenticated read-only Actions API | Artifact12133493094; exact envelope/run/attempt, not latest-run selection. Candidate under private owned parent0700; no test registry or live storage. |

## Cases
All evidence paths below are relative to E unless prefixed `ticket:`. Exact argv and cwd are in the listed logs/results; excerpts retain literal output. Subprobes are not extra unique cases.

| ID | Criteria | Boundary / command or steps | Env | Result | Evidence files / exact key line | Notes |
|---|---|---|---|---|---|---|
| R01 | AC002/004/005/006 | From owned source: `/usr/bin/python3 -m unittest scripts/tests/test_nfs_release_workflow.py -v`; records discovery then `-m unittest discover -s scripts/tests -p 'test_nfs_*.py' -v` | L | Pass | `workflow-current.log`, `records-focused.log`, `python-all.log`, `test-counts.json`, `release-control-excerpt.log`: `Ran 45 tests in 29.336s`; `OK (skipped=1)` | 45 collected/44 executed/1 expected standalone Go-child skip. Focused7+12 overlap45, not additional unique tests. Synthetic readiness/Apple/publication inputs remain fixtures. |
| R02 | AC001/002/008 | From owned source: actionlint both workflow files; Bash/ShellCheck native prefix and install/sign scripts; `python3 packaging/release.py --source-hash`; `python3 -c "import sys;sys.path.insert(0,'packaging/engine');import source;print(source.recipe_hash())"`; expected `python3 packaging/release.py --check-publish` refusal | L | Pass | `local-results.json`, `local-control-results.json`, `actionlint.log`, `prefix-syntax.log`, `prefix-shellcheck.log`, `shell-syntax.log`, `shellcheck.log`, `source-hash.log`, `recipe-hash-corrected.log`, `readiness-refusal.log`, `attempts.md`: `Release refused: Current engine and structured release readiness required` | 14 local command attempts,13 expected outcomes,1 resolved harness error. Original `recipe-hash.log` exit2 and `cleanup-local.json` allPassed=false remain intact; corrected4 controls pass. This is not a production failure. |
| R03 | AC001/005/006 | `gh workflow run release-nfs.yml --repo AutoByteus/autobyteus-nfs --ref codex/nfs-first-release -f release_tag=v0.1.0 -f source_sha=585d416c2746cf2963058d591b0753d0db8088f5 -f publish=false`; follow exact run/attempt to completion and collect logs | H | Pass | `dispatch-receipt.json`, `hosted-final.json`, `hosted-execution-summary.json`, `hosted-log-index.json`, `hosted-excerpt-{117650827602,117650827631,117650827653,117650827778}.log`, `post-run-remote.json`: `"conclusion": "success"`; Mac arm64 `2026-10-18T10:25:46.1301260Z Ran 45 tests in 13.085s` | 10 successful jobs/0 failed/0 cancelled/2 intended payload/publish skips. Both engine builders, full OCI and candidate aggregation succeeded. Each of4 native jobs: race7 packages/vet/Python45(44 executed/1 child skip)/build/version/archive pass. Nonverbose Go logs do not establish individual test counts/skips. Main/tags/releases unchanged at observation. |
| R04 | AC001/002/006 | From N: release.py `candidate-envelope` artifact12133493094/run39118784695/attempt1/workflow585d416; `fetch-candidate`; `verify-candidate`; exact-digest metadata alias; wrong digest/version/null-readiness and copied-envelope mismatch refusals. Full exact argv in results. | A | Pass | `candidate-reference.json`, `actual-candidate.json`, `candidate-validation-results.json`, `candidate-metadata-diff.json`, `actual-envelope-refusal.json`, `candidate-local-retention.json`, `candidate-control-excerpt.log`: `Release refused: Retained artifact envelope differs`; `Release refused: Candidate metadata inputs differ`; `"releaseTargets": []` | Complete19-file candidate verified and retained. Alias changes only engineImage; schema2/deferred/source/engine/OCI unchanged. registry.invalid never resolved/contacted. Wrong wrapper refused by actual API before destination creation. No release readiness populated. |
| R05 | AC005 | Actual downloaded Darwinarm64 `autobyteus-nfs version`; `verify-release <own release.json>` for equal candidate, false user=passed, and extra legacy qualifiedTargets. Private HOME, no setup. | L | Pass | `candidate-native-version.json`, `candidate-native-version.log`: `"stdout": "v0.1.0\n"`; `"noInstallEffects": true`; `"scratchAbsent": true` | Actual binary SHA30e0f81e… from artifact. version exit0 exact stdout/empty stderr;3 admission refusals exit1 with specific messages. Positive release notice/targets exercised by native Go fixtures in R03, not a real signed/public install. |
| C01 | AC008 | Completed own cleanup/preservation audit and second `release.py --operation verify-candidate --directory /Users/normy/nfs-first-candidate-api003-p_t67xqw/candidate`; compare historical candidate members/record | L/A | Pass | `finalize-audit.py`, `final-checks.json`, `artifact-checks.json`, `artifact-audit-attempts.md`, `final-candidate-verify.log`, `cleanup-local.json`, `cleanup-local-controls.json`: `"sourceMismatches": []`; `"protectedMismatches": []`; `"retainedCandidateFinalVerification": true`; `"historicalAPI002CandidateMemberHashesPreserved": true` | 120 source/1186 protected inputs unchanged. Both local scratch copies/native extraction removed. Delivery20 files preserved and excluded from API staging. New candidate deliberately retained, not leaked runtime resources. |
| Q01-01 through Q06-07 (42 IDs) | REQ003/AC007 | Six field modes ×7 operations; no execution under release-first scope | N/A | Not Tested — Deferred | `ticket:postpublication-testing-plan.md`, `ticket:approval-record-sr004.md` | Not passed, not a prepublication/task-closure prerequisite. No physical/independent-client/shared-filesystem proof inferred from builds. |
| U01 | REQ003/AC007 | Genuine user field execution, not run | N/A | Not Tested — Deferred | Same approved plan/approval | No userVerified claim and no questionnaire. Follow-up custody is required downstream. |
| D01 | AC002/003/004/006/007/008 | Delivery accepts actual readiness, fresh main, final signed payload, Accepted notarization, immutable publication | N/A | Not Tested — Downstream | `ticket:implementation-handoff.md` Downstream Work; packaging/RELEASE.md §§2–4 | Mandatory future release gate, not an unavailable API execution dependency. Fixtures do not prove Apple/registry/publication. |
| D02 | AC003/005/006/007/008 | Delivery public download/checksum/version/signature/OCI proof, final receipt and plan custody | N/A | Not Tested — Downstream | Same release guide and approved plan | Mandatory future release-completion proof; no public-install success asserted. |

**Case accounting:51 unique IDs =6 Pass +0 Fail +0 Blocked +45 Not Tested (43 approved Deferred,2 Downstream).** Earlier API002's50-case result remains unchanged. All6 planned API-owned affected prepublication cases completed. D01/D02 are ordered later work, not an exemption from release acceptance.

## Acceptance-Criteria Proof
The eight full release criteria are not all complete. Split rows identify current API-stage proof versus the remaining mandatory Delivery proof; they do not change the criteria. No part is classified Only The User Can Check in this round. Field/user work is explicitly deferred by approved requirements instead.

| Criterion / portion | Critical | Cases | Result | Basis / remaining owner |
|---|---|---|---|---|
| AC001 new complete exact current candidate/no publication | Yes | R02–R04 | Proven | Actual new run, native4/engine2/fullOCI/19file identity and remote observation. |
| AC002 changed readiness/admission contract and current checks | Yes | R01–R05 | Proven | Direct schema/parser/CLI controls and actual current evidence. Synthetic authorities never entered product lock. |
| AC002 actual stable readiness acceptance for publication | Yes | D01 | Not Proven | Delivery must prepare and semantically audit genuine stable references after this result/test gate. |
| AC003 actual both-Mac Developer ID/Accepted notary/downloaded signatures | Yes | D01/D02 | Not Proven | Signing controls pass R01; actual Apple stage not invoked by publish=false. Mandatory downstream. |
| AC004 immutable/recovery/failure-control implementation | Yes | R01/R02 | Proven | Current retained-payload/conflict/stage-order fixtures. Remote publication boundaries doubled. |
| AC004 actual normal immutable release/tag/assets/image | Yes | D01 | Not Proven | No public release created here; downstream actual workflow required. |
| AC005 strict target/claim/metadata/integrity admission contract | Yes | R01/R03/R05 | Proven | Native current four-target suite plus actual candidate refusal/version. |
| AC005 public released install/notice/download/version | Yes | D02 | Not Proven | Candidate intentionally not installable; final signed release metadata/binaries must be exercised later. |
| AC006 current candidate integrity, stale/refusal and provenance controls | Yes | R01/R04 | Proven | Actual wrapper/member/engine/fullOCI/fourarchive verification and specific negative controls. |
| AC006 published engine/OCI equality and attributable final-binary delta | Yes | D01/D02 | Not Proven | No published payload exists in this run. Final metadata/signatures legitimately change binary bytes. |
| AC007 prepublication checks/honest deferral and historical outcome preservation | Yes | R01–R05/C01 | Proven | Current evidence completed; old API002 outcome and bytes retained; approved plan exists. |
| AC007 first signed public release complete and custody handed off | Yes | D01/D02 | Not Proven | Delivery→terminal SD→requesting PM custody still required. Not TaskDone. |
| AC008 affected claim/control consistency and API-owned cleanup/preservation | Yes | R01/R02/C01 | Proven | Current schema/refusal/lock tests, original source review, cleanup audit. No license or runtime storage change. |
| AC008 final docs/main push/receipt/follow-up transfer | Yes | D01/D02 | Not Proven | Delivery remains owner; no main finalization by API. |

## Validation Confidence Scorecard
Scores cover **affected prepublication API validation**, not completed release/signing/publication or deferred field quality. The later criteria above remain hard completion gates regardless of this score.

| Category | Post-repository | Final | Evidence / uncertainty | Further evidence |
|---|---:|---:|---|---|
| Requirement and acceptance-criteria proof |50%|95%|R01–R05/C01 prove all current API-stage obligations; full release not yet proven | Delivery actual later criteria |
| Changed-boundary execution directness |90%|100%|Actual new hosted native checks, real artifact facade and downloaded CLI, not just import delta or mocked workflow | No material uncertainty for exercised current boundary |
| Cross-boundary realism and mock gap |75%|95%|Real Actions/engine/OCI/native/download boundaries; signing/publication fixtures explicitly separate | Actual signed/public workflow downstream |
| Environment/configuration/identity/fixtures |75%|95%|Exact source/ref/run/attempt/wrapper/record/member hashes; native four runners; no stale assets | Final payload identity; field platforms deferred |
| Failure/edge/lifecycle/recovery |90%|90%|Strict claim/tamper/retry fixtures, actual corrupt-envelope and candidate CLI refusals; bounded gap: public interruption/recovery is fixture-level here | Real public stage and any encountered recovery; never induce destructive public corruption |
| User-surface confidence (CLI; browser/shell N/A) |75%|95%|Native positive admission/notice tests and actual version/refusal; no public installer assertion | Public final binary/installer/signature checks downstream |
| Durable coverage quality/relevance |95%|95%|Current R3 durable suites valid, original Bash regression retained; all4 native suites current | Proportional successful-test review; real release controls next |

- Simple unweighted means: post-repository550/7 = **78.57%**; final665/7 = **95.00%**. No applicable final category below90%; current-stage95% target met.
- Every critical **current API-stage** obligation directly proven: **Yes**. Every full release acceptance criterion proven: **No** (D01/D02 portions above). This staged result does **not** waive missing critical release evidence or authorize completion/publication by itself. It follows the approved design/packaging sequence: API evidence → successful-test review → Delivery readiness and actual signed publication.
- Confidence-limiting residuals: publication/signing recovery still doubled; final installable binary differs in metadata/signature and needs fresh final checks. Deferred field/user behavior receives no passing score or qualification claim.

## Broader Validation Decision
**Required and executed** — CLI + Live API + actual hosted native/engine build. Repository success could not establish current Mac argv/matrix execution, real retained wrapper/member identity or downloaded binary admission. R03/R04/R05 closed those specific gaps. Browser/desktop validation **not applicable**: no UI or application boundary changed. No API execution dependency remains unavailable. Signing/publication is the ordered next owner stage, not mislabeled environmental blockage.

## Persisted Data / Compatibility
Approved **Discard or Rebuild** for readiness/generated distribution metadata; installed host state Not Affected. R01 reset/strict schema tests, R03 new complete candidate, R04 empty releaseTargets/deferred metadata and R05 legacy/false-claim refusals prove the current path. Historical external candidate/evidence remains preserved, not migrated or reinterpreted. No version-specific runtime fallback, dual read/write or compatibility-only coverage observed. Legacy invalid scope/reroute: None.

## Durable Coverage Changes
**API-added/updated/removed durable paths: None.** Temporary run-specific scripts/evidence only. Existing reviewed R3 coverage is adequate; no redundant synthetic suite added. The successful-test gate should assess the cumulative R3 additions/updates since API002, proportionately (not repeat full source review):
- Added: `internal/cli/release_admission_test.go` (R03/R05).
- Updated: `internal/cli/{cli_test.go,engine_release_test.go}` (R03).
- Updated: `scripts/tests/{nfs_release_fixture.py,test_nfs_engine_packaging.py,test_nfs_installer_fixture.py,test_nfs_packaging.py,test_nfs_release_publication.py,test_nfs_release_records.py,test_nfs_release_workflow.py,test_nfs_source_identity.py}` (R01/R02).
- Existing actual signing-shell fixture remains valid and executed, but unchanged. IR003 mutations and CRR005 AST/source checks are upstream attributed evidence, not reruns counted here.
- Removed durable paths: None. R3 assertions replace obsolete qualification assumptions within current files; no compatibility-only test retained. Source comparison: `git diff 96c8de3 850dfeb -- internal/cli/*test.go scripts/tests`.

## Mocked / Emulated Dependencies
| Dependency | Method | Limit |
|---|---|---|
| Signing / notary | Actual shell with fake commands/fixture credentials in R01 | Tests Accepted-only and cleanup logic, not a real certificate/team/password/Apple receipt |
| Publication registry/GitHub | Record/OCI fixtures and doubled remote effects | Recovery/immutability parser/order proof, not public visibility or registry copy |
| Public installer | Actual hash/tar with fixture download/inert binary; native Go admission tests | Does not replace D02 actual public final binary/install |
| Metadata alias | Exact real OCI digest, registry.invalid reference, metadata only | No first-use pull or runtime override; field tests deferred |
| Actual candidate facade | Real GitHub API/download/retained bytes; only wrong-envelope copy corrupted | No mock gap for observed fetch/refusal; strict record schema left unchanged |

## Temporary Methods / Cleanup And Retention
| Item | Owner | Disposition / proof |
|---|---|---|
| Two local exact-source copies/private HOME+TMP | API003 | Removed; cleanup-local*.json; initial harness failure retained, corrected separately |
| Downloaded native smoke extraction/HOME | API003 | Removed; no .local install effects, candidate-native-version.json |
| New candidate | API003 retained for Delivery | `/Users/normy/nfs-first-candidate-api003-p_t67xqw/candidate`,19files/128137587bytes, parent0700; ZIP removed after verification. Metadata-only alias retained beside it. Keep through release. |
| Old API002 candidate | Prior API ownership/history | `/Users/normy/nfs-first-candidate-api002-n940gd8s/candidate` preserved byte-for-byte, not usable for current R3 source |
| Hosted workers | Provider | All jobs complete, post-job cleanup logged; provider disposal not independently audited |
| Processes/mounts/VMs/containers/registries | None left/created by local API tests | No live storage command, no user app/node touch. Temporary child processes completed. |
| Source/protected tickets/Delivery untracked files | Other owners/source baseline |120/1186 unchanged; Delivery20 files excluded from staging, DR004 owner updates retained. No generated source assets committed. |

### Retained current candidate identity
Actual [run39118784695/attempt1](https://github.com/AutoByteus/autobyteus-nfs/actions/runs/39118784695), artifact12133493094, expiry2027-01-16T10:19:22Z. Authoritative exact values are `candidate-reference.json` and `actual-candidate.json`:
- Wrapper `sha256:018a143ae3dbd1a39e17ca1673095b0cf67fae04d831946c3553f8f9df891106`.
- Measured production sourceHash `a425e3f887f3156d920d022801df9069ba5bc2d49bdb0e4dd8097ee76a01fe9e`.
- Engine manifestSHA `ad01714923ce370162f90c4fcfcf53fd122dce32a36a5bbba1b51bd45df8df80`.
- OCI root `sha256:9bcb8c3ffc64615d57d12d76a06be7742fcb6a7fc840ab127921131c73413992`; both child digests/full layer members verified.
- Empty-lock sourceHash c7fd64e8… is **not** measured candidate identity. Actual final binary bytes will differ after metadata/signing; do not demand candidate-binary equality for the signed payload.

## Latest Authoritative Result
**Pass95.00% for API-REV-003 affected prepublication validation**, ready for proportional successful-test review on Large/High route. No new product failure. R03-F001 remains closed by actual current both-Mac execution as well as guard; CR-002 source cleanup accepted upstream and current suites green. The one API harness command error is resolved with original failed evidence retained.

Full release proof remains **Not Proven** for AC002 final readiness, AC003, AC004 publication, AC005 public install, AC006 published equality, AC007 release completion/custody and AC008 finalization portions. D01/D02 must complete before release/task success; no source Pass or this scoped API Pass substitutes. Q42/U01 explicitly Deferred/Not Tested under R3, not Pass and no host questionnaire.

Next recipient: fresh successful-output rule recorded in E/routing.json after evidence commit. No main merge/push, signing, notarization, tag/release/registry publication, deployment, TaskDone, user-verification or Terminal claim by this round.
