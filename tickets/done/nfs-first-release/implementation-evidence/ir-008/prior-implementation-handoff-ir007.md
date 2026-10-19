# Implementation Handoff — nfs-first-release

## Current result and authorities

**IR-007 — Local Fix implemented and locally checked; targeted source review.**
Demonstrated local codesign lookup defect corrected. **Original DR011 hosted cause
is not conclusively identified; real hosted signing/release remain unverified.**

Task autobyteus-nfs-3 / project_task_97c6ab09-83cb-46df-bf28-d07b39259dd5.
Worktree `/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/nfs-first-release`,
branch `codex/nfs-first-release`, target origin/main. Canonical ticket is
`tickets/done/nfs-first-release`; archive is not TaskDone. Intake79e35392bfe4f795464fecd8c034670b622c1684;
source **3f67e36193c246ca08b49cda818be5c0f94eba51**. Evidence/docs commit supplied in handoff.

- Approved R3/SR004, Ready SR004, ARCH-REV-002 remain controlling:
  requirements-doc.md, approval-record-sr004.md, design-spec.md,
  investigation-notes.md, solution-revision-record.md, design-review-report.md,
  architecture-review-revision-record.md and postpublication-testing-plan.md.
- Trigger: Delivery release-deployment-report.md / delivery-revision-record.md
  **DR011**, evidence delivery-evidence/dr-011/failure-assessment.json and actual
  signing receipts/logs. No separate finding ID; this is the existing packaging
  Local Fix, not a requirements/design dispatch.
- Prior IR006 / CRR009 sourcePass100 / CRR010 testPass / API005 prepublication95
  retain exact-input scope. Current IR007 source/API review pending. Prior handoff
  preserved in implementation-evidence/ir-007/prior-implementation-handoff-ir006.md.
- **Large / High / Reviewed confirmed** (design classification): privileged
  release signing lifecycle remains security-sensitive; bounded four-path delta
  does not alter classification. Selected route: independent source review.
  No new design impact, approval or field questionnaire; direct-route self-review N/A.

## Diagnosis and correction

DR011 run39210821088/1 at finalized main72b8a4 failed both Macs with
sign/exit1/cleanupcomplete/unclassified; no notary/payload/publication. Original
raw codesign output was deliberately deleted. No claim that it was recovered,
that a particular credential was invalid, or that a chain/ACL cause was observed.

Instead of another guess-only diagnostic increment, real local empty/synthetic
keychain probes tested the concrete superrepo search-list lead. Create-keychain
was observed NOT to add its exact path to the user list. With an imported newly
generated synthetic identity and otherwise unchanged command, the A/B/A result:
without membership → no identity found/exit1; prepend only owned keychain →
sign0/strict verify0/runtime flag present; remove again → same failure1.
Explicit security lookup saw the synthetic identity; its untrusted -v query did
not claim valid Developer ID. The probe disabled timestamp solely to avoid Apple
requests. It proves this local lookup defect, NOT hosted credential/chain/Intel
or release success. Full method/limits: evidence/IMP-07-17-investigation.md and
IMP-07-01/02/03 scripts/results. Exact original search lists restored; all own
keys/P12s/keychains/binary copies removed; no real user credentials accessed.

`packaging/sign-macos.sh` now explicitly prepends only its new temporary keychain
to the captured original list before identity validation/signing. Prior entries,
order, whitespace and argument boundaries are preserved. Configuration failure
preserves its exit and stops before signing; existing cleanup restores exactly
before deleting owned keychain. No default-keychain/trust change, broad -A access,
intermediate import, retry, unsigned fallback or credential replacement. Existing
Developer ID/team, --timestamp, hardened runtime, strict verify and Accepted-only
notary remain unchanged. The observed exact identity-prefixed no-identity literal
now maps to fixed `identity-not-found`; private output, unknown/ambiguous handling,
64KiB bound, original codesign exit, mode0600 and no-clobber receipt safety remain.

The signing command double now models search-list state: real shell success
requires owned membership, prior paths/order survive, and restoration is checked
after normal/failing/signalled paths. Added configuration-failure and ordering
controls; privacy/strict failure/notary/workflow tests retained. TESTING.md and
packaging/RELEASE.md explain the correction and evidence limits.

## Behavior / production path

| Basis | Path / preserved outcome |
| --- | --- |
| BEH001 / AC001 | Existing workflow candidate/native4 → exact source/engine/OCI. Signer hash changes; NEW applicable complete candidate required, no old fragment promotion. |
| BEH002 / AC002 | Singular readiness/current-source equality unchanged; Delivery must accept genuine current records after affected API validation. |
| BEH003 / AC003/004/006 | Workflow → signer → capture original list → owned-keychain configuration → selected identity/codesign → strict verify/Accepted → cleanup. Existing payload-before-public-effects order unchanged. |
| BEH004 / AC005/007 | Installer integrity, manifest admission, exact version/deferral output unchanged. |
| BEH005 / AC005/008 | Host source/state/permissions/consent/detach, Go runtime, engine and app boundaries untouched. No live NFS setup. |
| BEH006 / AC007/008 | Testing/package guides truthful; signed release first, field/user Deferred and postpublication custody unchanged. |

Scope Guardrail respected. Existing narrow signing owner remains appropriate;
no framework/refactor/design-health deviation. Source179 total lines, below500;
source delta12 lines, below220. Touched-file/embedded imports inspected, no dead
code or compatibility wrapper introduced. Shared shape remains the same receipt
with one additional literal enum. Host persisted data/migration **Not Affected**;
search list is transient and restored, not a new host schema. Frontend **N/A**.

## Checks Run

Primary evidence is `evidence/IMP-07-*` below this ticket. Exact argv/exits/times
for fixture checks are in IMP-07-results.json; native scripts contain exact argv.
All checks are implementation-scoped, not API or release acceptance. Unchanged
checks may carry downstream; no repeat solely for independence.

| Check | Commit / environment | Exact command or step / exercised boundary | Result and look-for |
| --- | --- | --- | --- |
| IMP-07-01 | intake79e3539 / native macOS26.5.2 arm64 | `python3 tickets/done/nfs-first-release/evidence/IMP-07-01-keychain-probe.py`; empty owned keychain and missing-identity actual codesign | JSON: `createdKeychainInSearchList: false`, `identityPrefixedNoIdentityFound: true`; restore/delete0, exact list restored. |
| IMP-07-02/03 | intake79e3539 / native arm64 | `python3 tickets/done/nfs-first-release/evidence/IMP-07-02-identity-probe.py` and `IMP-07-03-identity-probe.py`; synthetic import/partition/sign membership controls | JSON03 original1 → with-owned0/verify0/runtime true → removed-again1; `searchListExactlyRestored: true`, `ownedScratchRemoved: true`. NOT actual Developer ID/notary. |
| IMP-07-04 | precommit HEAD79e3539, identical3f67e36 signer/tests / independent Darwin copy, Python3.9.6/Bash3.2/private HOME/TMP | `/usr/bin/python3 -m unittest scripts.tests.test_nfs_release_signing scripts.tests.test_nfs_release_workflow -v` | focused.log/result: `Ran 23 tests in 91.454s`, `OK`; footer clarifies precommit identity. |
| IMP-07-05 | committed3f67e36 / same isolated environment | `/usr/bin/python3 -m unittest discover -s scripts/tests -p 'test_nfs_*.py' -v`; all release packaging fixtures | python.log: `Ran 58 tests in 141.187s`, `OK (skipped=1)`;57 executed, expected standalone Go-child skip. |
| IMP-07-06/07/08 | 3f67e36 / independent copy | `/bin/bash -n packaging/sign-macos.sh`; `/opt/homebrew/bin/shellcheck packaging/sign-macos.sh`; `/opt/homebrew/bin/actionlint .github/workflows/release-nfs.yml` | syntax/shellcheck/actionlint logs: `Observed exit: 0; expected exit: 0`. |
| IMP-07-09/10/14 | 3f67e36, original79e3539 signer control / independent copy | `/usr/bin/python3 packaging/release.py --source-hash`; `/usr/bin/python3 -c 'import sys;sys.path.insert(0,"packaging/engine");import source;print(source.recipe_hash())'` | source-hash/recipe-hash/original-hash logs; exact identities below, recipe unchanged. |
| IMP-07-11 | 3f67e36 / independent copy | `/usr/bin/python3 packaging/release.py --check-publish` without candidate | Expected exit1: `Identified candidate is required`. Not a real stale-candidate or publication execution. |
| IMP-07-12 | 3f67e36 disposable mutants / independent copy | `SKIP_FOCUSED=1 python3 tickets/done/nfs-first-release/evidence/IMP-07-run-checks.py` from repository root; exact unittest selectors recorded | Four mutant logs each expected exit1: omit membership, replace original list, swallow configure failure, skip restore. Actual test assertions detect each. |
| IMP-07-13 | original79e3539 signer + new tests / independent copy | Current `SigningTest.test_temporary_keychain_preserves_existing_search_entries_and_order` via same runner | Original-control.log expected failure at sign/exit1; original omission detected, not merely a source-text assertion. |
| IMP-07-15/16 | 3f67e36 / independent copy | Runner final byte comparison and owned-copy removal | copy.json: `allCopiedInputsStillMatch: true`; cleanup.json: `absent: true`. Native cleanup separately in01–03. |
| IMP-07-17/18/19/20 | intake79e3539 →3f67e36 / read-only source/evidence audit | Investigation, tool-version/manual capture; `python3 tickets/done/nfs-first-release/evidence/IMP-07-19-audit.py` | investigation.md separates facts/limits; audit.json records four paths/imports/size/history/main; metadata notes20 disclose label/input clarifications. |

No unexpected failing product check. Intentional original/mutation failures are
retained. No Go/Linux/four-target rebuild, real credentialed signing, Apple
notarization, new hosted candidate, remote writes, public downloads or field/user
campaign executed here. Prior exact-input results retain their limits. No engine
bytes copied/rebuilt or changed; no fixture-generated readiness. Owned probe and
fixture scratch cleaned; retained candidates, local diagnostic, other owners and
ignored caches preserved. See notes20 for evidence metadata corrections.

## Identity, risks and next owner

New source hash **7cb7b6d25794cbacbcf0286d9d0760347d9f15999eb51e981765e4ba8ed37a1a**.
Prior measured source `0a209d1efe327e13feeabe426c90e411728813a7261467c0428271eeee1db8e3`.
Engine recipe **299db7012dcc543f8606632695d286548d1513c13ace8b108eb712984fd39274** unchanged.
Workflow, actual measured engine/OCI lock, genuine readiness, all Go inputs and
prior finalized main72b8a4/f830/768 ancestors unchanged. API005 candidate at
`/Users/normy/nfs-first-candidate-api005-61mqnd8a/candidate`, older API002/003/004
and `/Users/normy/nfs-local-notary-xq_ym2f6` untouched. Existing readiness/candidate
is not current for changed source and must not be relabelled.

Fresh configured source review → applicable current API/new complete candidate
→ Delivery-owned genuine readiness and actual BOTH-Mac signing/Accepted, retained
payload/publication/public-download verification. Delivery controls necessary
remote staging; implementation performed no push/main merge/dispatch. No claim
that the exact original hosted output was identity-not-found. If the changed
hosted path still fails, act on its actual controlled evidence rather than guessing
credentials or weakening gates. All six secrets remain provisioned.

DR011 and old DR005/009 failed history preserved; DR007 local DEVELOPMENT Accepted
is not final-release proof. Field/user tests Deferred, not prerequisites;
postpublication plan custody remains Delivery → terminal Solution Designer → PM.
No release, TaskDone, user-verification or Terminal claim. No new approval loop,
old filesystem/editor/VM/provider campaign or duplicate outcome dispatch.

Fresh route: most-specific Large/High implementation-owned Local Fix →
`/software_engineering_team/code_reviewer` only; evidence/IMP-07-21-routing.json.
