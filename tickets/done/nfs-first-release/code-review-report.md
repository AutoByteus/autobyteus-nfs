# Code Review Report — nfs-first-release

## Review Round Meta

- **2026-10-19 / CRR-011 / Implementation Review / round11 / Full Re-Audit of affected signing boundary.** IR007 is a bounded four-path Local Fix, but adds search-list configuration to the prior diagnostic correction; all24 structural checks and full10-category scorecard re-evaluated. No full runtime/architecture/field campaign.
- Task autobyteus-nfs-3 / project_task_97c6ab09-83cb-46df-bf28-d07b39259dd5. Worktree `/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/nfs-first-release`, branch codex/nfs-first-release, target origin/main. Canonical archive `tickets/done/nfs-first-release`; archive is not completion.
- Intake **bf6aea661f3551ee7aab2f35f8e537a23b59dce4**, source **3f67e36193c246ca08b49cda818be5c0f94eba51**, base **79e35392bfe4f795464fecd8c034670b622c1684**. All127 current non-ticket inputs equal tested source. Finalized main72b8a4/f830/768 ancestry preserved.
- Context: requirements-doc.md **R3/SR004 Approved**, design-spec.md **SR004 Ready**, approval-record-sr004.md/postpublication-testing-plan.md; investigation-notes.md/solution-revision-record.md; design-review-report.md/architecture-review-revision-record.md **ARCH-REV-002 Pass**. Same authority; no new intended behavior or approval.
- Implementation-handoff.md **Checks Run read before execution**, implementation-revision-record.md **IR007**, prior source CRR009/report/history and successful-test CRR010 reviewed. NFS AGENTS/DESIGN/TESTING, shared design principles/Example9 and reviewer template apply; no guideline conflict.
- Trigger: Delivery **DR011**, run39210821088/1 at main72b8a4; both Mac receipts **sign/exit1/cleanupcomplete/unclassified**. Exact failing boundary: existing codesign --force --timestamp --options runtime --keychain ... --sign ... binary in fresh release mode. Delivery failure-assessment.json is independent evidence; notary/payload/publication not reached.
- **Original DR011 cause remains unknown**, raw capture was deleted, not recovered. Current source review is not an API failure-origin request or successful-test gate. API005/prepublication95, CRR009 sourcePass100 and CRR010 testPass remain exact-input history, not current IR007 validation.

## Routing Classification Review

**Large / High / Reviewed confirmed.** Signed-release keychain lifecycle remains security-sensitive; independent source review required. **Pass100 — bounded source repair accepted**, not real hosted signing/release Pass. Failure classification N/A. Fresh source-Pass route to affected API/new complete current-source candidate.

## Review Scope

Only packaging/sign-macos.sh, scripts/tests/test_nfs_release_signing.py, TESTING.md and packaging/RELEASE.md change. Reviewed capture/import/partition → configure owned membership → selected identity/codesign → strict verify/Accepted → exact restore/delete/receipt, plus workflow/payload gate applicability. No Go/runtime/host/engine/workflow/lock/readiness change from intake.

No app/frontend/Guide/superrepo/PM work, credential replacement, trust/default-keychain change, broad -A access, timestamp weakening, retry/unsigned fallback or speculative new machinery. Evidence-only probes are inspected for attribution, not reviewed as product code or rerun.

## Upstream Behavior And Production-Path Basis Confirmation

**Confirmed.** Requirements demand the same genuine Developer ID/Accepted release and private cleanup. Keychain lookup repair implements that contract, not a new signing policy. No behavior-basis ambiguity prevents this bounded source decision; unknown original hosted cause remains a separate empirical limit.

| Behavior | Status | Current path / preserved outcome |
| --- | --- | --- |
| BEH001 | Confirmed | Manual candidate dispatch → current source/native4/engine/OCI → identified retained candidate. Hashed signer change invalidates prior candidate applicability. |
| BEH002 | Confirmed | Current candidate/evidence → genuine readiness → exact source/engine admission; no old record relabel. |
| BEH003 | Confirmed | Fresh release workflow → signer saved list/import/partition → owned membership → validated identity/signature/Accepted → exact cleanup → native archive/final payload → immutable publisher. Configuration/signing failures stop this chain. |
| BEH004 | Confirmed | Public download/manifest admission/notice/version/install unchanged; no actual install executed here. |
| BEH005 | Confirmed | Host/source/state/permissions/consent/detach and engine/runtime source byte-preserved. |
| BEH006 | Confirmed | Guides explain lookup evidence and limits; final receipts and deferred-plan custody unchanged. |

## Supported Product Scenario And Reachability Gate

| Scenario / contract | Actor/event and independent goal | Supported entry → forward path / lifecycle / consequence | Validity / use |
| --- | --- | --- | --- |
| SCN001 / REQ001/002 | Maintainer requests current candidate | Manual publish=false → exact checkout → native4/engine/OCI → retained candidate without public effects | Supported Normal Scenario; Use |
| SCN002/003 / REQ004/006 / D3 | Maintainer requests genuine signed normal release | Authorized fresh dispatch → current readiness/final build → new temporary keychain/imported selected identity → codesign lookup/sign/strict verify/Accepted → payload/publish | Supported Normal Scenario; Use. Required signing journey exists independently of the probe. |
| SCN003/007 / REQ004/010 / D3 cleanup | Release signer temporarily changes its process user's keychain lookup context | Saved original list → only own new keychain prepended → signing → saved entries restored exactly before own deletion; unrelated original entries survive | Supported Normal Scenario/cleanup contract; Use |
| SCN005 / REQ006 / D3 fail-closed | Required configuration or signing command fails | Actual signer stage returns nonzero → EXIT cleanup → safe stage/code/diagnostic → native job failure, no notary/payload progression | Supported Explicit Edge Scenario; Use. Existing fail-closed contract and actual failed release, not invented concurrent activity. |
| SCN007 / REQ010 / D3 privacy | Failed signing needs useful nonprivate evidence | Nonzero codesign → private bounded parser → exact literal identity-not-found or existing safe states → original exit/cleanup/receipt only | Supported Explicit Edge Scenario; Use. Exact observed local literal supports matching, not hosted causal attribution. |
| SCN006/004/008 | Maintainer recovers publication; user downloads; Delivery transfers follow-up | Existing bound-payload retry, public admission and postpublication custody paths unchanged | Supported explicit edge/normal scenarios respectively; Use unchanged evidence |

### Candidate Finding And Mechanism Gate

| Candidate | Observation / mechanism | Independent trigger and lifecycle consequence | Evidence | Disposition / scope |
| --- | --- | --- | --- | --- |
| CG018 | Add only owned temporary keychain to preserved original search list | SCN003/REQ004 requires signing with an imported temporary identity. Normal create/import/partition precedes codesign. Missing search membership can prevent lookup despite explicit --keychain; preserving/restoring prior list is D3/REQ010 contract. | Real local IMP07-01/02/03; current script76–91; stateful fixture and omit/drop/swallow/restore mutants | Promote mechanism — this ticket; satisfactory bounded repair, no current finding |
| CG019 | Recognize exact identity-prefixed no-identity message without leaking identity | SCN007/D3 requires safe failure evidence. Local real codesign emitted this form, previously unclassified. Match entire line using selected identity, emit fixed literal only; nonzero still authoritative. | IMP07-01/03 booleans and probe source; parser new match + shell allowlist; positive/prefix rejection tests | Promote mechanism — this ticket; satisfactory, no current finding |

The local synthetic reproduction establishes lookup behavior at that boundary, **not** that a self-signed identity is an approved release input or that DR011 had this cause. No real Developer ID/P12/password/Intel/timestamp/notary success is inferred. Unsupported concurrency or speculative credential/trust repair is not required.

## Prior Finding Resolution

| Reference | Prior | Current disposition / evidence |
| --- | --- | --- |
| CR-001 Mac empty array | Resolved | Still resolved; mandatory native argv/workflow unchanged. |
| CR-002 unused imports | Resolved | Still resolved; touched shell/embedded/test bindings are used. |
| DR009 diagnostic portion | CRR009 source accepted | Actual DR011 uploaded sanitized unclassified receipts; diagnostic pipeline ran, original codesign cause still unknown. |
| DR011 lookup/diagnosis request (no CR ID) | Local Fix requested | IR007 lookup repair accepted on controlled native evidence plus source/local controls. Original hosted cause and real release remain unverified, not marked resolved. |

## Structural / Design Checks

All24 checks reevaluated for this affected signing boundary; unchanged owners carry prior evidence with verified byte applicability.

| Check | Result | Evidence | Required action |
| --- | --- | --- | --- |
| Task design health assessment is present, evidence-backed, and preserved by the implementation | Pass | Existing signing owner handles local lookup correction; R3 decomposition and release-first authority unchanged. | None |
| Implementation matches approved behavior-defining supplemental artifacts | Pass | R3 approval/postpublication plan preserved: actual Developer ID/Accepted required; field/user Deferred. | None |
| Data-flow spine inventory clarity and preservation under shared principles | Pass | DS3 workflow→signer→lookup/codesign/Accepted→retained payload→publisher; failure/cleanup return traced separately. | None |
| Ownership boundary preservation and clarity | Pass | Signer owns captured list, temporary keychain setup and restoration; no caller reaches its private snapshot. | None |
| Off-spine concern clarity (off-spine concerns serve clear owners and stay off the main line) | Pass | JSON/argv translation and fixed diagnostic matching serve the signer only; no new coordinator. | None |
| Existing capability/subsystem reuse check (no fresh helper where an existing subsystem should own it) | Pass | Reuses existing search.json, Python stdlib, EXIT cleanup and receipt upload. | None |
| Reusable owned structures check (repeated structures extracted into the right owned file instead of copied across files) | Pass | One saved list used for configure and restore; one shared stateful signing fixture, no per-target copy. | None |
| Shared-structure/data-model tightness check (no kitchen-sink base, no overlapping parallel shapes, specialization/composition used meaningfully) | Pass | One additional literal diagnostic; no new release/host schema, credential or readiness representation. | None |
| Repeated coordination ownership check (shared policy has a clear owner instead of being repeated across callers) | Pass | One signer sequences configuration/lookup and owns cleanup, both Mac jobs call it. | None |
| Empty indirection check (no pass-through-only boundary) | Pass | Embedded Python translates saved JSON into exact argv and replaces itself with security to preserve command status. | None |
| Scope-appropriate separation of concerns and file responsibility clarity | Pass | 179-line signer remains one signing lifecycle; evidence-only native probes are not product code. | None |
| Ownership-driven dependency check (no forbidden shortcuts or unjustified cycles) | Pass | No app, Go, engine or publisher coupling; existing system command boundary retained. | None |
| Authoritative Boundary Rule check (callers do not depend on both an outer owner and that owner's internal manager/repository/helper/lower-level concern) | Pass | Workflow invokes signer and receives safe receipts; it does not independently manage the private keychain/list. | None |
| File placement check (file/folder path matches owning concern or explicitly justified shared boundary) | Pass | Configuration beside keychain setup, diagnostic beside existing parser; appropriate packaging owner. | None |
| Flat-vs-over-split layout judgment (layout is readable for the scope and not artificially fragmented) | Pass | Small local block is clearer than a new generic keychain service/helper framework. | None |
| Interface/API/query/command/service-method boundary clarity (one subject, one responsibility, explicit identity shape) | Pass | Two-argument signer boundary unchanged; list entries supplied as separate argv, never evaluated shell text. | None |
| Naming quality and naming-to-responsibility alignment check (files, folders, APIs, types, functions, parameters, variables) | Pass | configure-search-list stage and identity-not-found observation are specific; prior means the saved ordered list. | None |
| No unjustified duplication of code / repeated structures in changed scope | Pass | Configure adds owned entry; cleanup restores prior only. Distinct operations, same authoritative snapshot. | None |
| Patch-on-patch complexity control | Pass | Full affected-boundary re-audit: actual lookup repair replaces a missing setup step; no retry, trust override, fallback or broader diagnostic framework. | None |
| Dead code removed in the touched files and modules (Core Principle 7) | Pass | json/os/sys and fixture shlex imports referenced; new stage/enum used; no dormant branches or wrappers. | None |
| Relevant test scenarios and assertions are clear and requirement-aligned | Pass | Stateful fixture proves membership/order/exact restore/configure exit, timestamp/runtime preserved; observed literal privacy checks retained. | None |
| Test fixtures/helpers are reasonably reusable and test structure remains coherent | Pass | Existing run_case/fake commands extended with JSON list state and shared temporary setup. | None |
| No stale, duplicated, or compatibility-only tests are retained in changed scope | Pass | Prior diagnostic/Accepted/signal/no-clobber controls still apply; no disabled or compatibility alternative. | None |
| API/E2E readiness for the next workflow stage | Pass | Exact-source full58/57executed/1skip,23overlap focused, four mutants and original-control evidence clear; fresh candidate remains required. | None |

## Source File Size And Structure Audit

| Source file | Before nonempty | After | >500 | Added+deleted / >220 | Ownership/placement | Action |
| --- | --- | --- | --- | --- | --- | --- |
| packaging/sign-macos.sh | 169 | 179 | Pass | 11+1=12; below trigger | One signing lifecycle; configuration belongs beside creation/import and existing restoration | None |

Base79e3539/current3f67e36; nonempty includes comments. Test/fixture/docs exempt. No forced split or generic helper needed.

## Legacy / Backward-Compatibility Verdict

| Check | Result | Notes |
| --- | --- | --- |
| No backward-compatibility mechanisms | Pass | One current setup path; no old signer fallback. |
| No legacy old-behavior retention | Pass | Missing membership corrected directly, not retried conditionally. |
| Dead code removed in touched scope | Pass | Changed imports/variables/enum referenced; no obsolete disabled branch/test. |
| Approved persisted transition decision followed | Pass | Host state Not Affected. User search list is temporarily configured and restored; no schema migration. |
| No version-specific dual reads/writes/fallback | Pass | Current private JSON list snapshot is one representation; no historical decoder. |
| Transition mechanics match design | Pass | Changed source needs current candidate/readiness; old evidence preserved, not rewritten. |

## Dead / Obsolete Items Requiring Removal

None found in touched scope. No unrelated cleanup expansion.

## Docs-Impact Verdict

**Yes, addressed** by TESTING.md and packaging/RELEASE.md. They state preserved list/order, configure-failure refusal, local synthetic reproduction, observed diagnostic rather than cause, unchanged actual signing requirements and private cleanup. No claim hosted failure was solved or field qualification completed.

## Additional Material Premise Validation

Architecture premises unchanged. **CG018 — new verified lookup premise**, not a newly invented product behavior:
- Independent origin: SCN003/REQ004/D3 official signed-release requirement.
- Concrete caller: fresh native Mac workflow invokes sign-macos.sh with final binary/receipt; script creates and imports own temporary keychain then selects identity/codesign.
- State/consequence: new keychain may not be on user search list; real IMP07-01 reports creation without membership. IMP07-03 same synthetic imported/partitioned identity and explicit --keychain yields failure1 → owned+prior sign0/strict verify0/runtime true → removed-again failure1. Exact prior list restored.
- Method inspected: each A/B/A stage signs a fresh copy, generated self-signed identity only, no real credentials. -v valid-identity query is false for that untrusted synthetic identity; non-v explicit query sees it. Probe uses --timestamp=none only to avoid Apple requests. It does **not** execute the complete production validation path or prove actual hosted credentials.
- Supported Normal Scenario / Reachable for required temporary-identity lookup; proportionate response is preserving originals while adding own membership, then existing cleanup. Source retains actual --timestamp, Developer ID/team, strict verify, runtime and Accepted gates. Full hosted success still requires current execution.
- CG019 merely records the exact observed diagnostic form; no claim the deleted DR011 output contained it.

## Review Scorecard

**10.0/10 = 100.00/100**, simple mean for source-quality visibility, not API confidence or real release completion. No supported evidenced current source defect warrants a deduction.

| Priority | Category | Score | Why | Weakness holding down | Improvement |
| --- | --- | --- | --- | --- | --- |
| 1 | Data-Flow Spine Inventory and Clarity | 10 | Complete signed-release path and configuration/failure/restore subpath explicit. | None established in reviewed source scope | None required; downstream execution retains stated limits |
| 2 | Ownership Clarity and Boundary Encapsulation | 10 | One signer owns temporary search-list lifecycle; no caller bypass. | None established in reviewed source scope | None required; downstream execution retains stated limits |
| 3 | API / Interface / Query / Command Clarity | 10 | Exact argv, same entrypoint, nonzero propagation; safe receipt vocabulary. | None established in reviewed source scope | None required; downstream execution retains stated limits |
| 4 | Separation of Concerns and File Placement | 10 | Bounded lookup setup in existing packaging owner. | None established in reviewed source scope | None required; downstream execution retains stated limits |
| 5 | Shared-Structure / Data-Model Tightness and Reusable Owned Structures | 10 | Single saved list/current diagnostic shape; shared stateful fixture. | None established in reviewed source scope | None required; downstream execution retains stated limits |
| 6 | Naming Quality and Local Readability | 10 | Specific configuration stage and observed literal, no causal overclaim. | None established in reviewed source scope | None required; downstream execution retains stated limits |
| 7 | API/E2E Readiness | 10 | Clear exact-input local evidence permits affected API; no claim current hosted gate is complete. | None established in reviewed source scope | None required; downstream execution retains stated limits |
| 8 | Runtime Correctness And Behavioral Fidelity | 10 | Membership/order/exit/restore supported by source and local controls; real hosted cause and success still unproven. | None established in reviewed source scope | None required; downstream execution retains stated limits |
| 9 | No Backward-Compatibility / No Legacy Retention | 10 | Single current path; no old behavior fallback or migration. | None established in reviewed source scope | None required; downstream execution retains stated limits |
| 10 | Cleanup Completeness | 10 | Captured list restored before owned deletion; cleanup failure remains failure; original exit preserved. | None established in reviewed source scope | None required; downstream execution retains stated limits |

## Evidence And Checks

Read implementation Checks Run first; source unchanged and results clear. **No reviewer product test/lint/build/keychain/Apple/hosted execution.** No new finding needed reproduction. Source/identity and own-artifact audits only.

| Evidence / owner | Result and attribution | Limit |
| --- | --- | --- |
| IMP-07-01/02/03 implementation | Real local empty/synthetic-keychain lookup, A/B/A; original list byte-exact restore and own scratch/keychain deletion recorded | Local macOS26.5.2arm64; synthetic identity, no trust change, no real Developer ID/P12/notary; no hosted-cause attribution |
| IMP-07-04/05 implementation | Precommit identical product focused23; committed3f67e36 full58 collected57executed1 expected standalone Go-child skip, Pass | Fixtures execute real shell with external doubles; focused overlaps full |
| IMP-07-06–11/14 implementation | Bash/ShellCheck/actionlint/hash/recipe pass; no-candidate expected refusal | No-candidate is not actual stale-candidate execution |
| IMP-07-12/13 implementation | Four mutants detected: omit membership/drop originals/swallow config error/skip restore; original signer fails new stateful control | Intentional controls, not current product failures |
| IMP-07-15/16/19/20 implementation | Copy identity/cleanup/import/size/history pass; precommit labels and bookkeeping corrections disclosed | Runner cleanup says no real-keychain access for fixture run only; native probes are separately attributed above |
| DR011 Delivery | Both real Mac sign/exit1/cleanupcomplete/unclassified; no notary | Raw output deleted; actual cause unresolved |
| CR-11-01 reviewer |127 current source bytes equal3f67e36; four paths;179nonempty/delta12; finalized-main ancestor preserved | Read-only review audit, not independent product execution |

Full commands/raw logs linked by implementation Checks Run. Reviewer first guessed absent IMP-07-20-metadata-notes.md, then listed/read actual IMP-07-20 evidence; read-only filename correction, no product/test failure. No copied cumulative manifest. Prior API005/CRR009/010 keep exact-input scope.

## Findings / Follow-ups

**None new.** No new finding ID, deduction or cause-specific prescription. CR-001/002 remain resolved. Existing postpublication-plan custody retained; no extra Task or notification.

## Classification / Recommended Recipient

**Pass**, failure classification N/A. Fresh most-specific source-Pass rule → affected API/new complete current-source candidate. Then Delivery owns genuine current readiness/freshmain and real both-Mac signing/Accepted/publication. This is not a same-input blind rerun or permission to relabel API005.

## Residual Risks

- Preserved-engine sourcehash **7cb7b6d25794cbacbcf0286d9d0760347d9f15999eb51e981765e4ba8ed37a1a**, prior measured **0a209d1efe327e13feeabe426c90e411728813a7261467c0428271eeee1db8e3**; recipe **299db7012dcc543f8606632695d286548d1513c13ace8b108eb712984fd39274** unchanged. Future measured candidate identity governs readiness; no reproducibility equality assumption.
- DR011/009/005 failed history remains. This repair addresses evidenced local lookup, not conclusively the original hosted cause. Both real Mac credentialed signing/Accepted, final payload/publication/public OCI/download/signature/install remain mandatory.
- Six secrets provisioned; no speculative reprovision. DR007 development arm64 Accepted is not hosted P12/Intel/final payload proof.
- Field/shared-filesystem/physical/user tests Deferred, not Passed or release/closure blockers. Approved custody Delivery → terminal SD → requesting PM unchanged.
- No reviewer source/test writes, runtime resources, retained-candidate/localnotary access, credential/remote/push/dispatch/main replay/reset/tag/release/TaskDone/Terminal actions. NFS reviewer artifacts only.

## Latest Authoritative Result

**CRR-011 / Implementation Review / Pass100.00**. Supported-scenario and material-premise gates Pass. Bounded lookup repair accepted; original hosted cause and actual signing/release unverified. Canonical CRR010 successful-test and API/Delivery reports unchanged. Continue normal affected API, not architecture restart or immediate publication.
