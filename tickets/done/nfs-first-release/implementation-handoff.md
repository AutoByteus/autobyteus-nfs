# Implementation Handoff — nfs-first-release

## Current result / identity

**IR-009 — Implementation Complete; Ready for independent Code Review.**
The SR005 executor/payload recovery contract and draft-ID correction are implemented
and locally checked. This is not hosted recovery or release acceptance; Delivery
DR013 remains the latest actual publication outcome (Blocked).

Task autobyteus-nfs-3 / project_task_97c6ab09-83cb-46df-bf28-d07b39259dd5.
Worktree `/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/nfs-first-release`,
branch `codex/nfs-first-release`, target `origin/main`. Canonical ticket is
`tickets/done/nfs-first-release` (T); its archived location does not mean TaskDone.
Review input630cc997; production4c665e0eb23adf1f9bb45363a496b7786e76b138,
final source/tests **22205cc84a29e6aa66ba5673b0a60c8db95ddc80**. The last commit adds
only four publication controls; production is identical. Evidence/docs commit is
supplied in the handoff message. No push or target finalization this round.

## Upstream package / revision links

- Requirements: T/requirements-doc.md; **R3/SR004 Approved**, approval-record-sr004.md.
- Investigation and solution history: T/investigation-notes.md,
  solution-revision-record.md, solution-design-handoff.md.
- Design: T/design-spec.md **SR005 Ready**, D2–D5/DS5; independent
  T/design-review-report.md **ARCH-REV-003 Pass**, architecture-review-revision-record.md.
  ARCH003 supersedes the design document's earlier pending-review notation.
- Trigger: Delivery DR013 in release-deployment-report.md / delivery-revision-record.md,
  actual draft discovery failure; IR008 / evidence/IMP-08-02-design-impact.md.
- Cycle **Rework**. T/implementation-revision-record.md appends IR009 after IR001–008.
  Prior result IR008 Design Impact is resolved by SR005 authority, not silently bypassed.
- Current IR009 source/API verdicts **N/A — pending**. Prior IR007/API006/CRR012 and
  DR013 signing receipts retain their exact scopes; they do not accept SR005 code.
- T/postpublication-testing-plan.md remains controlling: field/shared-filesystem/
  physical/user testing Deferred, not publication or closure prerequisites.

## Classification / scope / health

**Large / High / Reviewed confirmed**, matching design classification. Distinct
source authorities, full validators, workflow admission and irreversible public
state justify this classification despite unchanged NFS runtime. Selected route:
**Code Review**, selected by fresh handoff rules (IMP-09-13). Direct-route self-review N/A;
implementation self-checks below are not independent review. New design impact: None.
Scope Guardrail retained: **NFS ONLY**, no app/superrepo/shared-skills/PM changes.

Reviewed posture: Bug Fix with bounded identity-boundary refactor; root cause was
published-only draft lookup plus conflated executor/product identity. **Refactor
Needed Now**, implemented as SourceContext and recovery admission owners, not a
new publication framework. Publication retains draft/effect sequencing. Its
306-addition/135-deletion delta exceeded the220-line signal and was assessed;
projection/admission were split as designed. All changed production files are
below500 nonempty lines (publication388, candidate273, new context85/admission59).
No further design escalation was established.

## Behavior implementation trace

| Behavior / criteria | Actual production path | Outcome |
| --- | --- | --- |
| BEH001 / AC001,006 | candidate.py + SourceContext default current; source_hash unchanged | Fresh candidate remains strict; old candidate is rejected at new executor. |
| BEH002 / AC002,006 | source_context.py → candidate/readiness/payload; recovery.py | Full original P hash/workflow/lock/evidence/engine/OCI/native checks; separate P→H→E ancestry, fixed full-tree scope, H/E hash equality and committed genuine-evidence references. Missing actual authorization refuses. |
| BEH003 / AC003,004,006 | publication.context_for/retained/inspect_bound/prepare/publish; workflow recover | Current E executes every validator against Git-proven P data; exact successful original payload/native/signing job identity; no old code execution. Recover skips build/native/sign/payload/bind. |
| BEH003 / AC004 | publication.discover/reconcile_release/upload/verify_assets | Bounded publisher-visible unique inventory + direct ID; known missing417014769 refuses. One confirmed POST only when authorized absent; selected-ID streaming uploads/readback, no clobber/retry/delete. |
| BEH003 / AC004,006 | publication guard, promote, final correlation | E-main/tag-object/binding/selected-release rechecks before effects; ambiguous outcomes stop; completed-identical release is read-only; exact OCI and public bytes retained. |
| BEH004/005 / AC005,008 | unchanged Go/config/installer/signer/engine | Runtime/schema/host/consent/storage safeguards unchanged; no live setup. |
| BEH006 / AC007,008 | facade outputs, external receipt, RELEASE/packaging guide/TESTING | E/workflow/run/hash, P, H/auth ref and selected release ID are distinct; original public notes/provenance/assets are not rewritten. Deferred-field custody remains truthful. |

## Key ownership / transition checks

- `source_context.py` bounds regular Git entries/blobs/snapshot and removes owned
  projection on exit. `recovery.py` owns fixed admission, never creates authority.
  Existing candidate/readiness/payload verifiers receive one explicit context.
- Published-only draft discovery and tag-addressed upload were replaced, not kept
  as fallback. By-tag is only conflict/final published correlation. No global
  ROOT/hash override, source exclusion, old executor or bypass flag introduced.
- Dead touched imports removed/none remain; AST use audit plus caller inspection
  passed. No unrelated dead-code follow-up found. Shared structures remain tight;
  separate PublicationContext and SourceContext express distinct authorities.
- Persisted transition: **Directly Usable — No Migration** for original bound
  candidate/payload/tag/readiness; separate new Delivery authorization only.
  Installed host data **Not Affected**. No transformation, re-sign, repack or rebind.
- Source hash algorithm/SOURCES, original lock/releases, engine recipes/pins,
  runtime/installer/signer and license/notices unchanged. Executor hash:
  `e3e814176d8315f0426df379035a995b6c0e6d5f89f82483f121b074c79eea21`.
- No real `packaging/recovery` record exists yet. Test records are synthetic in
  removed scratch. Evidence references require human review; parsing hashes does
  not certify the truth of the referenced human judgement.

## Checks Run (implementation scope, not API/E2E sign-off)

All final checks used macOS26.5.2 arm64, Python3.9.6; independent local Git clones
with private HOME/TMP/cache, no network, except the explicitly read-only retained
input checks. Bash3.2.57, actionlint1.7.11. E below means T/evidence/.
Exact harness commands and underlying argv are in each named script/result.

| Check | Command / steps | Commit tested | Exercises / criteria | Result / evidence / look for |
| --- | --- | --- | --- | --- |
| IMP-09-06 | `python3 T/evidence/IMP-09-06-run-checks.py`: `python3 -m unittest discover -s scripts/tests -p 'test_nfs_*.py' -v` |4c665e0|All packaging/release/signing doubles, real C/P/H/E fixtures; BEH001–006|**Pass**,72 collected/71 executed/1 expected Go-child skip. E/IMP-09-06-python.log: `Ran 72 tests in 330.543s`, `OK (skipped=1)`.|
| IMP-09-06,10 | Same harnesses: `actionlint .github/workflows/ci.yml .github/workflows/release-nfs.yml`; `/bin/bash -n scripts/public/nfs/install.sh packaging/sign-macos.sh`; `python3 packaging/release.py --source-hash`; `git diff --check <commit>^ <commit>` |4c665e0,22205cc|Workflow/shell/hash/whitespace; AC001–004|**Pass**,all exits0 in E/IMP-09-{06,10}-checks.json; hash e3e814… both. Separate full delta `git diff --check 630cc997 HEAD` also clean.|
| IMP-09-10 | `python3 T/evidence/IMP-09-10-run-checks.py`: `python3 -m unittest discover -s scripts/tests -p test_nfs_release_publication.py -v` |22205cc|Affected publication suite after four added controls: tag conflicts, equal-size corrupt assets, failed promotion/retry, public-download integrity; AC004/006|**Pass**, E/IMP-09-10-python.log: `Ran 15 tests in 53.114s`, `OK`. Other suites carry from06: only this test file changed. No claim all76 were rerun together.|
| IMP-09-05 | `python3 T/evidence/IMP-09-05-mutations.py` |4c665e0, unchanged production at22205cc|Remove admission/full-tree scope, substitute E for P, restore by-tag lookup, recreate known draft, omit main freshness; AC002–004/006|**Pass controls**,all6 detected with exit1; E/IMP-09-05-mutations.json + per-mutant logs. Six distinct controls; baseline tests green.|
| IMP-09-07 | `PYTHONDONTWRITEBYTECODE=1 python3 T/evidence/IMP-09-07-retained-inputs.py` |4c665e0, same production at22205cc|Real retained candidate/payload; current full P validators; saved DR013 jobs/draft; AC002–004/006|**Pass**, E/IMP-09-07-retained-inputs.json: `retainedInputsUnchanged: true`, `snapshotCleanup: true`; exact original receipt3b0c…; `Reviewed recovery authorization required`. Saved endpoints are NOT fresh API proof.|
| IMP-09-11 | `PYTHONDONTWRITEBYTECODE=1 python3 T/evidence/IMP-09-11-source-audit.py` |22205cc|Scope, imports, size, hash algorithm, originals and other-owner authority preservation|**Pass**, E/IMP-09-11-source-audit.json: empty unusedLocalImports, realRecoveryAuthorizationAbsent, priorIR001to008PrefixPreserved.|

E/IMP-09-09-checks-and-limits.md provides short excerpts and precise limitations.
Initial IMP-09-01 had2 errors in10 tests from an owned Mac `/var` alias in the new
snapshot assertion; canonicalizing the owned snapshot root fixed it without
weakening source symlink refusal. IMP-09-02 then54 focused tests passed. IMP-09-03
was interrupted by the user; no final verdict, partial log retained and owned
scratch removed after confirming no process. IMP-09-04 was earlier actual-byte
proof atccf3d5b, superseded by07. These are disclosed attempts, not current Pass.

Not rerun: Go/race/native Linux/four-target builds, engine candidate, actual Mac
signing/notary or field/user campaign, because their product inputs/bytes are
unchanged by this executor repair. The Go-parent installer fixture was not run;
its Python-child skip is explicit. No fresh hosted/API inspect-bound, real upload,
OCI/public-download/install/signature campaign, actual recovery authorization or
publication. Those belong to subsequent affected API/Delivery work.
Frontend rendered-result check: **Not Applicable**, no rendered surface changed.

## Immutable state / limits / downstream work

Preserve P **238bdc183e8affac99ffdee9be9cb333b0eb126f**, tag object
**f4a04fd0c80a6625708ba002b4cef5507a03f514**, draft **417014769**; payload job117940491787,
artifact12169472209, run39215470944/1, wrapper b552faea…,
publication.json **3b0cbedd15782871e0c88c51b6847abcf276e7db00aab6f10c4dd387b4133dc8**,
expiry2027-01-17T07:21:36Z. Full identities are in07 and unchanged DR013 reports.
Original P hash3e1af43a… remains separate from executor e3e814….

Actual BOTH-Mac DeveloperID/runtime/timestamp/strictverify/Accepted is **carried
from DR013**, not newly executed here. Current full payload validation confirms
both recorded Accepted receipt binary hashes against retained archives. ARM
52450985-4e16-482e-b22a-d7b15b8791b7 and Intel563db88f-7ded-48ba-9d90-bcdbf8705961
remain original submissions. Old failed signing histories remain failures.

Retained paths `/Users/normy/nfs-first-final-dr013-gmvotux9/payload` and
`/Users/normy/nfs-first-candidate-api006-a8aune30/candidate` are unchanged; all older
candidates/local diagnostic preserved. Main238/72/f830/768 ancestors preserved.
No remote freshness query this round; DR013 is the last actual observation.

Next: independent source review of SR005's full affected identity/validation and
ID-publication path, then affected API proof using current code, including actual
read-only inspect-bound and proportional executor/admission checks. No repeat
successful candidate/native/signing campaign solely for this bound repair.
Delivery alone judges genuine evidence, adds stable authorization for reviewed H,
fresh-integrates E with no executable drift, refreshes remote state and performs
same-byte hosted recover/public OCI/download/install/signature verification.
Expiry, hidden/missing known draft, conflict, changed main or inadequate evidence
must block rather than alter immutable inputs. No tag/draft delete/move/manual
upload, new payload/version or synthetic real authority.

All owned check/mutant/interrupted scratch removed; no running owned monitor.
Unowned caches and other-owner docs/history preserved. No source push, main merge,
credentials/keychain/Apple/live-storage/PM actions, release, TaskDone or Terminal.
Field/user plan custody remains Delivery → terminal Solution Designer → requesting
PM after actual completion. No delegation or duplicate outcome dispatch.

## Selected handoff

Fresh most-specific completed implementation-owned Local Fix / Large-or-High rule
selects only `/software_engineering_team/code_reviewer`; see
`evidence/IMP-09-13-routing.json`. Current implementation and local validation are
complete. No direct API, duplicate Designer/Delivery/PM dispatch or new approval.


Raw-log whitespace exception: IMP-09-03-python.log:47 (interrupted unittest
progress line) and IMP-09-05-recreate-known-draft.log:7 (raw unittest subtest
progress line) retain their original trailing space. They are evidence, not
source/style defects. Header-only silent-command logs explicitly annotate no
output/exit0. All other staged source/docs/evidence whitespace is clean.
