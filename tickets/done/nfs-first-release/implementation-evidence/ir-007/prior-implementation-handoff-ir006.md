# Implementation Handoff — nfs-first-release

## Current Round / Result

**IR-006 — Local Fix: diagnostic portion complete / ready for targeted source review.**
**Actual hosted codesign cause and release remain unresolved; DR009 is not fixed.**
Task autobyteus-nfs-3 / project_task_97c6ab09-83cb-46df-bf28-d07b39259dd5.
Worktree `/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/nfs-first-release`,
branch codex/nfs-first-release. Canonical ticket `tickets/done/nfs-first-release`:
archive does not imply TaskDone. Intake b279d556e2c0f5e90ca24b61c7e67bc809644947;
current source **2c12ec61f6339d0d264280b7117787ec821425af**. Evidence/doc commit supplied with handoff.

R3/SR004 Approved/Ready, ARCH-REV-002; **Large/High/Reviewed confirmed**. No new
requirement/design decision. Existing requirements-doc.md, design-spec.md,
approval-record-sr004.md, design-review-report.md and postpublication-testing-plan.md
remain authorities. CRR007 sourcePass100 / CRR008 testPass / API004 prepublication95
remain exact-input history, not acceptance of IR006. Current-delta CRR/API: pending.
Prior implementation handoff is preserved at implementation-evidence/ir-006/
prior-implementation-handoff-ir005.md; implementation-revision-record.md is cumulative.

## Trigger / Diagnosis / Scope

Delivery DR009 actual publish=true run39204643596/1 at finalized mainf830c50 failed
both Mac jobs117904866164/117904866080: sanitized receipt **sign / exit1 / cleanup
complete**. Native4 checks passed, Linux packaged; notary/payload/publish not reached.
The successful import/partition/selected-identity stages do not prove codesign's
internal cause. Original raw codesign output was suppressed, so no defensible
credential/chain/ACL fix can yet be chosen. DR007 local arm64 development notary
Accepted is separate, not hosted P12/keychain/Intel/final-publication evidence.
See Delivery's failure-assessment.json and signing-artifact-receipts.json under
delivery-evidence/dr-009/ and investigation evidence IMP-06-14/15.

Only the requested bounded diagnostics correction is made: four paths, no new
framework. Actual codesign command/arguments, keychain setup/search-list/trust,
strict verification, Accepted-only notary, cleanup and publication gates remain.
No speculative intermediate import, trust override, credential reprovision,
unsigned fallback, target omission, retry, runtime/host/app change or delegation.
Previously pushed mainf830c50 (and7683494) remains ancestor; no replay/undo/push.

## Implemented Delta

- `packaging/sign-macos.sh`: codesign output privately captured in existing owned
  scratch, mode0600; on nonzero exit a bounded64KiB+1 parser emits only fixed
  observation categories. Exact binary/identity-related lines are recognized;
  unknown/ambiguous, oversized and unavailable/undecodable outputs stay explicit.
  A shell allowlist also rejects unexpected parser stdout. No private excerpt,
  account, identity, argument or tool log is printed/uploaded. Capture is deleted
  by existing cleanup. Original codesign exit survives parser failure. Command
  success is not reclassified by text; later strict signature/notary checks remain.
- Same exclusive failure receipt/stderr now includes `diagnostic`; other stages
  say not-collected. A category is an observation, not a root-cause verdict.
- Existing signing suite adds allowlist/privacy, output bounds/decoding, parser
  failure and success-precedence checks with command doubles. Prior stage/TERM,
  no-clobber/cleanup, six-input, Accepted-only and workflow-upload controls retained.
- `TESTING.md`, `packaging/RELEASE.md`: document the above distinction and limits.
  Workflow unchanged; existing exact receipt-only globs cannot retain private text.

Source size169 total lines (audit reports nonempty count), changed source delta51,
below500/220 guardrails. Touched Python and embedded imports checked; no unused
bindings. Frontend loop **Not Applicable**: no rendered surface. Host/persisted
state unaffected; diagnostic receipts are operational evidence, not release or
host schema migration. No design/health deviation demonstrated.

## Behavior / Production-Path Trace

| Behavior / criteria | Actual path and outcome |
| --- | --- |
| BEH001 / AC001 | Candidate engine/OCI/native4 pipeline unchanged; signing production hash changes, requiring NEW complete current-source candidate. |
| BEH002 / AC002 | Singular readiness/current-source admission unchanged. Existing readiness/candidate now stale for IR006; never relabelled. |
| BEH003 / AC003/004/006 | Workflow → existing signer → private codesign capture → fixed diagnostic on failure → cleanup → existing receipt-only upload. Nonzero still prevents notary/package; success still needs strict verify and Accepted. |
| BEH004 / AC005/007 | Installer integrity, manifest admission and exact version/deferral output unchanged. |
| BEH005 / AC005/008 | Go host source/state/permissions/consent/busy-detach/engine/app boundaries untouched; no live setup. |
| BEH006 / AC007/008 | Current testing/package guides state diagnosis limits; signed-release-first and deferred field/user plan retained. |

## Source / Retained Data

Current source hash **dd6cde88374cce42ec8b44c24e41abff3af6f01803890824dd783848e0d101a5**; previous measured source
`d5aac8cd30dd41526436c52cbc73d74ee5e15b8fb701d07d8ccf8a0cf0e976fd`. Engine recipe
`299db7012dcc543f8606632695d286548d1513c13ace8b108eb712984fd39274` unchanged. Measured engine lock,
readiness records, complete OCI, workflow and all Go inputs unchanged. Current
API004 candidate `/Users/normy/nfs-first-candidate-api004-a7bxyrbb/candidate` remains
untouched; older API002/003 and `/Users/normy/nfs-local-notary-xq_ym2f6` also retained.
Delivery owns genuine new readiness acceptance after applicable current evidence.
No fixture writes or fabricated receipts entered the stable lock.

## Checks Run

All local checks: Darwin arm64/Python3.9.6/Bash3.2, independent source copy/private
HOME/TMP. **Command doubles only, no real keychain/Apple operation.** Full final
execution uses committed2c12ec61f6339d0d264280b7117787ec821425af; IMP-06-01 preliminary copy
used its identical product/test bytes before the commit (base HEADb279d55).
Primary files are in `evidence/`; exact argv/exits/times in IMP-06-results.json.
Unchanged downstream roles can reuse these outcomes rather than repeat them for
independence; actual hosted signing is not substitutable by fixtures.

| Check ID | Commit / Environment | Command / exercised code | Result and evidence / look for |
| --- | --- | --- | --- |
| IMP-06-01 | identical2c12ec6 tree before commit, HEADb279 / independent Darwin arm64 | `python3 -m unittest scripts.tests.test_nfs_release_signing scripts.tests.test_nfs_release_workflow -v`; signer and workflow doubles, identical precommit tree | Pass21; IMP-06-01-focused.log: `Ran 21 tests in 85.765s`, `OK`. |
| IMP-06-02 | 2c12ec6 / local Darwin arm64 | `python3 -m unittest discover -s scripts/tests -p 'test_nfs_*.py' -v`; all packaging/release fixtures, current commit | Pass56 collected/55 executed/1 expected Go-child skip; IMP-06-02-python.log: `OK (skipped=1)`. |
| IMP-06-03/04/05 | 2c12ec6 / local Darwin arm64 | `/bin/bash -n packaging/sign-macos.sh`; `/opt/homebrew/bin/shellcheck packaging/sign-macos.sh`; `/opt/homebrew/bin/actionlint .github/workflows/release-nfs.yml`; grammar/lint/workflow integration | Pass; corresponding syntax/shellcheck/actionlint logs: `Observed exit: 0; expected exit: 0`. |
| IMP-06-06/07/11 | 2c12ec6; original signerb279 for11 / independent Darwin arm64 | `python3 packaging/release.py --source-hash` current and original signer; `source.recipe_hash()` with packaging/engine import; source/engine identity | Pass; source-hash/recipe-hash/original-hash logs show identities above. |
| IMP-06-08 | 2c12ec6 / local Darwin arm64 | `python3 packaging/release.py --check-publish` without candidate; facade required-input guard | Expected refusal exit1; no-candidate-refusal.log: `Identified candidate is required`. Not claimed as a stale-candidate execution. |
| IMP-06-09 | 2c12ec6 disposable mutants / independent Darwin arm64 | Four owned-copy mutations: force unknown category, raw parser stdout, hide command exit, ignore bound; targeted actual SigningTest methods/argv in results | All detected, expected exit1; mutant logs. Tests verify safety and diagnostic behavior, not Apple cause. |
| IMP-06-10 | b279 signer + new tests / independent Darwin arm64 | Current stage-failure test against original b279 signer in owned copy | Expected failure; original-control.log: absent diagnostic field. Original command exit remains5, no intentional original-code weakening. |
| IMP-06-12/13 | 2c12ec6 / local Darwin arm64 | Byte comparison of independent copy and worktree; remove owned source/HOME/TMP | Pass; copy.json `allCopiedInputsStillMatch: true`; cleanup.json `absent: true`. |
| IMP-06-14/15 | b279/DR009 intake / local read-only | Read DR009 evidence, primary Apple/GitHub guidance and installed man/security error descriptions; no keychain access | Investigation .md and installed-contracts.log separate supported observations from unknown hosted cause. |
| IMP-06-16 | b279+initial edits then2c12ec6 tree / local attempts | Read retained failed/corrected local attempts, not a current product check | attempts.md: initial fixture variable shadowing caused46 assertion failures; corrected21 pass. Raw failures preserved. |
| IMP-06-17 | 2c12ec6 / local Darwin arm64 | `python3 evidence/IMP-06-17-audit.py`; changed paths/imports/size/history/main | Pass; audit.json: only4 paths, no unused imports, prior history prefix/main ancestor preserved. |
| IMP-06-18 | NFS2c12ec6; superrepo5096011; Apple-Actions63fff01 / read-only source | `git show` historical desktop workflow/adapter; exact upstream action inspection | superrepo-comparison.md: explicit list membership is a lead; no proof of actual DR009 cause or copied weakening. |

No Go/Linux/four-target/native Apple/hosted/new candidate/release rerun in this
implementation round. Those earlier results carry only their exact unchanged
scope. No field/user campaign (approved Deferred) or frontend checks (N/A).
Attempt1 was a fixture expected-record variable-shadowing bug; corrected without
product edits. Source tests never access real credentials; all own scratch removed.
Four raw unittest diagnostic lines retain trailing whitespace: line7 of each
classify-all-unknown/leak-private-output/hide-signing-exit mutant log and the original
control log. Explicit exceptions are listed in IMP-06-17-audit.json; all other
source/docs/evidence pass hygiene. No cumulative upstream hash index added.

## Existing-Project Reference Supplement

User-requested superrepo comparison was personally read-only checked at5096011,
with exact Apple-Actions source63fff01. See IMP-06-18-superrepo-comparison.md.
Explicit temporary-keychain search-list membership is a concrete difference to
investigate if the real diagnostic warrants it, not established DR009 cause.
No broad -A, search-list replacement, disabled timestamp, raw stderr/argv or
Electron-specific behavior was copied. Existing IR006 scope/source remains2c12ec6;
this supplement does not restart review or create another round.

## Next / Classification

1. Targeted source review of IR006 privacy, original failure semantics, parser bounds,
   meaningful controls and unchanged signing gates. **Not a claimed DR009 root fix.**
2. Affected API continuation and NEW complete real current-source candidate/evidence.
   API004/old readiness cannot be promoted for these signing-script bytes.
3. Delivery owns staging, current-main/new readiness and authorized hosted signing.
   Use its next exact diagnostic/category to identify and minimally repair the
   actual boundary if still failing. No secret reprovision or keychain/trust change
   based solely on a category; no raw private stderr or xtrace.
4. Both Mac actual Developer ID and Accepted notary, retained final payload before
   public effects, immutable non-clobber retry/public OCI/download/signature/install
   checks remain mandatory. Source finalizations already completed remain preserved.
5. Field/shared-filesystem/physical/user tests remain Deferred, not a publication
   hold; plan custody after actual release remains Delivery→terminalSD→requestingPM.

No remote write/dispatch, target merge/push, secret changes, live storage, release,
tag, deployment, TaskDone, user verification or Terminal claimed by implementation.
