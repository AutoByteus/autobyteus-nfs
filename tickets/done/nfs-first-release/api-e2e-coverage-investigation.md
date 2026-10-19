# API/E2E Coverage Investigation — API-REV-004

## Basis and trigger
Canonical ticket tickets/done/nfs-first-release (archive is not completion). NFS-only worktree /Users/normy/autobyteus_org/autobyteus-nfs-worktrees/nfs-first-release, codex/nfs-first-release, target origin/main. Task project_task_97c6ab09-83cb-46df-bf28-d07b39259dd5. R3/SR004 Approved/Ready; ARCH002; Large/High Reviewed.

Read requirements-doc.md, investigation-notes.md, solution-revision-record.md, design-spec.md, approval-record-sr004.md, postpublication-testing-plan.md, design-review-report.md/architecture-review-revision-record.md, implementation-handoff.md Checks Run and IR005/implementation-revision-record.md, code-review-report.md/CRR007 history, API003 plan/report/history/progress, delivery-revision-record.md DR005–007 and their failure/diagnostic receipts. No requirement/design change. Original DR005 signing cause is UNKNOWN; local DR007 Accepted is development arm64 only, not hosted P12/import/Intel/final release. Do not repeat credentials provisioning.

IR005 source75f4dbe5527a7159f536bafcf9448bc2d6a01604 changes six paths: signer, workflow, two Python suites, TESTING, packaging release guide. Fixed sanitized failure diagnostics and keychain cleanup; strict command/Accepted+exit0 gates retained. Prior API003 candidate/readiness is stale for new production. New complete real candidate required. Fresh remote ticket staging belongs to Delivery, not main finalization by API. Already finalized main7683494/ticketb599e476 must not be reset/replayed.

## Supported scenarios / boundaries
SCN001 new candidate; SCN002/003 actual signing lifecycle; SCN005 failed command/cleanup/corrupt input refusal; SCN006 immutable recovery; SCN007 truthful receipt; SCN008 deferred field custody. No unsupported/contrived scenario added. Changed boundaries: shell lifecycle, keychain cleanup and diagnostic confidentiality, workflow artifact allowlist/external CI. Go host state/runtime/installer/engine recipe unaffected; application/UI/browser/field work out of scope. Actual signed publication remains Delivery after this current API/test gate.

## Instructions and environment
Root AGENTS.md, TESTING.md, RELEASE.md, DESIGN.md, README.md/go.mod/workflow and packaging/RELEASE.md apply; no closer instructions. Updated skill evidence-files/reuse rules apply: reuse clearly evidenced unchanged IMP checks, do not repeat to claim independence. New evidence is flat evidence/<Case>-04-* with context and excerpts. Strict candidate/envelope JSON retains exact schema; companion logs supply context.

Build-only release-nfs.yml on exact reviewed staged ref/source, release_tag=v0.1.0,publish=false, omit candidate_run_id. Go1.27.2 native4, measured engine2/full OCI and aggregation required. Read-only Actions API facade fetch/verify actual selected run/artifact. No signing secrets, registry writes, main push, live storage/keychain or user app action by API. Keep binaries/generated metadata outside repo; private owned candidate root. Local safe refusal uses existing retained old candidate read-only and current CLI; no public effects. No local Go setup needed. Personal execution; no delegation.

## Existing coverage / reuse decisions
Checks Run read before planning. IMP-05-01 full52/51executed/1childskip and IMP-05-02 focused17 overlap; IMP-05-03–07 static/hash/missing-input; IMP-05-08 four mutants plus09 baseline detect actual diagnostic gaps. Headers/quoted outcomes present. Reuse if current non-ticket tree matches75f4dbe. No-candidate refusal is not stale-candidate proof: add real old-candidate refusal through current facade. Prior API003 unchanged Go/runtime/installer/readiness controls retain scoped evidence only; never reuse old complete candidate for new source. All current signing/workflow/records/installer/Go tests Still Valid. No durable additions/updates/removals needed by API. IR005 changed durable files: scripts/tests/test_nfs_release_signing.py and test_nfs_release_workflow.py for later proportional review.

## Planned cases
| Case | AC | Kind | Steps / existing check | Reason |
|---|---|---|---|---|
| R01 |003/004/006/008|Reused|IMP-05-01/02/08/09 via implementation Checks Run|Exact current inputs, readable outcomes; tests exercise real shell with external doubles, no Apple claim|
| R02 |001/002/006/008|Reused + Temporary Probe|IMP-05-03–07; actual current release.py --check-publish --candidate <old API003 retained candidate>|Do not confuse missing candidate with stale identity; actual old record is a supported stale-input scenario|
| R03 |001/005/006|Journey|New exact current-source build-only hosted run, all4 native checks, engine2/fullOCI/aggregation; no-public-effect observations|Production hash changed; old candidate cannot be promoted|
| R04 |001/002/006|Temporary Probe|Actual selected artifact envelope/fetch/verify and copied wrapper mismatch refusal|Run-specific external boundary not replaced by fixture parser tests|
| R05 |005|Temporary Probe|Actual new downloaded Darwinarm64 version/candidate admission refusal in owned HOME|New distribution bytes/identity, quick boundary smoke; no setup|
| C01 |008|Temporary Probe|Owned cleanup; final retained candidate verification; only own files staged, earlier artifacts preserved|No deleting old retained candidates or local-notary diagnostic|
| Q01-01–Q06-07 / U01 |007|Not Tested — Deferred|Approved postpublication plan|43 IDs not a release/closure prerequisite, not Passed|
| D01/D02 |002/003/004/005/006/007/008|Not Tested — Downstream|Delivery fresh main/stable genuine readiness/actual both-Mac signature+Accepted/finalpayload/publication/download/plan custody|Mandatory later release acceptance, not this build-only gate|

## Transition / cleanup / decisions
Host state Not Affected; generated release records/candidate must be rebuilt/reaccepted, old history and immutable records retained. No compatibility fallback/migration. No API edit to old readiness/lock. Preserve /Users/normy/nfs-local-notary-xq_ym2f6 and old API002/API003 candidates; no access to private credentials. Temporary native HOME removed, new actual candidate retained through Delivery. Source identity and tracked diff checked, not a cumulative incoming manifest. Progress required; append only. Proceed Yes; durable changes None; no upstream ambiguity/reroute before validation. If new real failure occurs, preserve and classify normal origin; do not guess credentials. Results/confidence are in report, not this plan.
