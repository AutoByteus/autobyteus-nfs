# API/E2E Coverage Investigation — API-REV-006

## Basis / scope
NFS-only nfs-first-release/project_task_97c6ab09-83cb-46df-bf28-d07b39259dd5. Canonical tickets/done/nfs-first-release (archive not completion), codex/nfs-first-release→origin/main. R3/SR004 Approved/Ready, ARCH002, Large/High unchanged. Upstream: requirements-doc.md, investigation-notes.md, solution-revision-record.md, design-spec.md, approval-record-sr004.md, postpublication-testing-plan.md, design-review-report.md/architecture-review-revision-record.md; implementation-handoff.md Checks Run/IR007 and implementation-revision-record.md; code-review-report.md/CRR011 and history; delivery-revision-record.md DR011/failure-assessment.json; prior API005 Cases/history/progress. Independent review applies, no omitted authority.

IR0073f67e36193c246ca08b49cda818be5c0f94eba51 changes four paths: signer, signing tests, TESTING and package release guide. It prepends only the owned keychain to the captured original search list, preserves ordered argv, refuses configuration failure before signing, and restores originals before deletion. Adds exact identity-prefixed no-identity diagnostic literal. Actual DeveloperID/team/timestamp/runtime/strictverify/Accepted/privacy/exit/publication gates unchanged. Native synthetic A/B/A supports this local lookup repair, NOT original DR011 cause or actual hosted signing success. DR01139210821088/1 sign/exit1/cleanupcomplete/unclassified and DR005/009 remain historical failed, root causes UNKNOWN. Six secrets already provisioned; no speculative reprovision.

## Scenarios / boundaries / instructions
SCN001 fresh candidate; SCN002/003 real signing lifecycle; SCN005 configuration/identity/input/refusal; SCN006 immutable recovery; SCN007 truthful cleanup/receipt; SCN008 deferred custody. No contrived scenario. Changed boundary is shell keychain-list lifecycle and safe diagnosis, external signing integration. Runtime/Go/engine recipe/installer/workflow remain unchanged. App/UI/browser/field work out of scope.

Root AGENTS.md/DESIGN.md/TESTING.md/RELEASE.md, README/go.mod/.github/workflows/release-nfs.yml and packaging/RELEASE.md apply, no closer guidance. Updated role skill/evidence-files/reuse instructions apply. Exact current reviewed remote ticket staging is Delivery-owned; no main replay/reset/publication by API. Use actual publish=false workflow, v0.1.0, exact source/workflow SHA, omit candidate_run_id. Existing facade candidate-envelope/fetch-candidate/verify-candidate, gh read-only API and owned-HOME downloaded version/refusal. No root/live storage/real keychain/credential/provider use by this round. Store candidate outside repo under private APFS parent; preserve old002–005 and local-notary diagnostic.

## Durable validity / reuse
Checks Run read before planning. IMP07-04/05 current equivalent/committed source focused23/full58(57executed1expectedGochildskip),12 four mutants,13 original-signer control;06–11/14 syntax/lint/hash/no-candidate controls are clearly evidenced. Reuse after exact127input equality. IMP07-01–03 native mechanism probe remains supporting evidence only: generated synthetic identity, local arm64, no timestamp/DeveloperID/notary, A/B/A and exact restoration. No need to repeat real keychain side effects for independent credit. Existing signing/workflow/records/installer/Go tests Still Valid; no API durable additions/changes/removals. IR007 changed durable path scripts/tests/test_nfs_release_signing.py requires later proportional successful-test review. Old API005 complete candidate/readiness cannot cover newly hashed signer.

## Planned cases
| Case | AC | Kind | Steps / reuse | Why |
|---|---|---|---|---|
| R01 |003/004/006/008|Reused|IMP07-04/05/12/13, supporting native01–03|Exact current test inputs/readable results; mechanism probe not current hosted qualification|
| R02 |001/002/006/008|Reused + Temporary Probe|IMP07-06–11/14; current --check-publish --candidate <actual oldAPI005>|Real stale source refusal distinct from missing-input fixture|
| R03 |001/005/006|Journey|NEW exact-current hosted publish=false complete native4/engine2/fullOCI candidate; public-state observations|Production hash changed; old candidate not relabelled|
| R04 |001/002/006|Temporary Probe|Actual selected artifact envelope/fetch/verify; copied wrong-wrapper refusal|External current run/bytes not replaceable by fixtures|
| R05 |005|Temporary Probe|Actual downloaded Darwinarm64 version/candidate-admission refusal in ownedHOME|New distribution bytes; no setup/install|
| C01 |008|Temporary Probe|Candidate reverify/owned cleanup/source/history/other-owner preservation|No old retained assets or Delivery work altered|
| Q01-01–Q06-07/U01 |007|Not Tested — Deferred|Approved postpublication plan|43IDs notPassed, not prepublication/closure prerequisites|
| D01/D02 |002–008|Not Tested — ordered Delivery|Genuine current readiness/freshmain/actual bothMac signing+Accepted/finalpayload/immutablepublicbytes+OCI/signatures/install/custody|Mandatory later release proof, not this build-only gate|

## Transition / decision
Host state NotAffected; transient keychain state restored (reuse supporting current checks); generated current candidate/readiness rebuilt/reaccepted, old immutable history preserved. No compatibility fallback/migration. Personal execution only, no delegation. Progress required append-only; new flat evidence <Case>-06-* with headers/excerpts, strict JSON keeps facade schema. Proceed Yes, no durable edits, no upstream ambiguity or new approval/architecture loop. Real failures use normal origin routing; never infer original DR011 cause from synthetic probe or build-only success. Results/confidence belong in report.
