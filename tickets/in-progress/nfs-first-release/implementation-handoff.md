# Implementation Handoff — nfs-first-release

## Upstream Artifact Package

Task **autobyteus-nfs-3 / project_task_97c6ab09-83cb-46df-bf28-d07b39259dd5**.
Project project_6416db5b-926a-4865-8705-d8ebb2425780.
Worktree `/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/nfs-first-release`,
branch `codex/nfs-first-release`; target `origin/main`. Canonical ticket is
`tickets/in-progress/nfs-first-release/` in that worktree.

- Requirements: requirements-doc.md, **R2/SR002 Approved**; normal first v0.1.0,
  unchanged four targets and physical/current-source/user/signing gates.
- Investigation: investigation-notes.md; history: solution-revision-record.md.
- Completed design: design-spec.md **SR003 Ready**; solution-design-handoff.md.
- Selected independent review: design-review-report.md and
  architecture-review-revision-record.md **ARCH-REV-001 Pass**. Original review
  resumed after poweroff, not a second dispatch.
- Relevant supplement: evidence/intake/signing-certificate-upload-receipt.json.
  All six entries provisioned; import/password pairing/notary not yet validated.
  Do not repeat credential provisioning absent an actual validation failure.
- Triggering rework: code-review-report.md / code-review-revision-record.md **CRR002 Fail**,
  CR-001 = API001 R03-F001; actual failed candidate39111348848/attempt1.
  Input reviewca048be893516d79bc1ea895b929af17580e25dd; API72dc48b.
  DR001 staged reviewed branch518f4b51 only; eight Delivery untracked files remain
  unmodified/unstaged. No main merge is required for that staging prerequisite.
- Original architecture-review input2051fd9559f4f4fa7beae68723429f8199b50004, design cbf7b35,
  approved base origin/main7e375984be2bea7a4d536e43cc59d6bc2b116870. Remote target
  was not refreshed/finalized by implementation; Delivery must check it afresh.

## Current Implementation Summary

**IR-002 Local Fix Complete — ready for targeted source re-review**, not release
acceptance. Source commit **8436d0cf6048cd3b4cadbf28815e3d9f82ba6b34**. Personal
execution only; no delegation, push, hosted dispatch, release/tag or live-user action.

- Cycle Rework; implementation-revision-record.md **IR-002**, preserving IR001 baseline.
- Solution R2/SR002 + SR003; architecture ARCH-REV-001.
- CRR001 Pass100 is historical; **CRR002 Fail / API001 Fail62.86%** remain
  current downstream verdicts until their respective owners re-review/re-execute.
  Finding CR-001/R03-F001 corrected locally, not independently closed. DR001 is staging context.
- Replaced existing-tag/clobber/early-image publication with manual build-only
  candidate → exact qualification → final signed retained payload → annotated
  exact tag/draft/assets → identical OCI/anonymous availability → normal release.
- Candidate and final payload identities are distinct; signed/qualified binaries
  are not claimed byte-identical to unqualified candidates. Final package reuses
  the exact measured engine packages and OCI, never rebuilt under old evidence.
- Default lock remains engine=null, qualification=null, no qualified targets or
  physical/user proof. Source hash with that **unqualified** lock is
  `26af7e5bcab00ae22d4bdebe1820c6d38b0dc51a44f1b834036334ea79528298`.

## Current Bounded Correction — IR-002

Actual supported Mac candidate aborted under `/bin/bash` before metadata/native
checks: empty optional array expansion with nounset. The workflow now starts its
argument array with the mandatory metadata arguments, appends only the exact
fresh qualification flags, and invokes the quoted nonempty array. Strict mode,
all four runners and qualification/cancellation/publication gates are unchanged.
No shell-version branch, error masking or runtime/engine change.

The new executable regression reads the actual workflow prefix (strict mode and
OCI JSON pipeline included), doubles only release.py OCI/metadata, and asserts
exact candidate/fresh argv and failure propagation under `/bin/bash`. Original
source fails with five assertions; corrected suite passes. TARGET strings do not
constitute native execution for those architectures. TESTING.md documents scope.

Workflow is production-hashed: a **NEW reviewed current hosted candidate** is
required. Do not relabel/hand-assemble API001's seven failed-run partial artifacts.
They remain retained failure evidence. Physical host assignment/user verification,
real signing, public payload/publication and Delivery current-main gates remain.

## Routing Classification

- **Task size Large; architectural risk High; Confirmed** against design's Task
  Size And Architectural Risk and current ir-002/final-checks.json (IR001 structural audit retained).
- Irreversible cross-service publication, evidence/signing trust, failure recovery
  and four-target scope remain material; no downgrade from local green checks.
- Selected route **Code Review** by fresh rules (ir-002/routing.json).
- Direct-route lightweight self-review **Not Applicable**; ordinary implementation
  self-check completed, not a substitute for independent review.
- New Design Impact/Requirement Gap: **None**. Rootless OCI materialization is the
  designed layout transport retaining identical blobs, not a changed runtime or gate.

## Reviewed Behavior Implementation Trace

| Behavior | Approved change / preserved outcome | Actual path | Implementation result / limits |
| --- | --- | --- | --- |
| BEH001 / REQ001–002 / AC001 | No pre-created release; nonpublic candidate | release-nfs.yml prepare/engine/binaries/candidate; release.py; identity.py/candidate.py | IR002 corrects native candidate argv under Bash3.2; exact flags/strict failures locally tested. Earlier actual hosted candidate failed; NEW current hosted aggregate still required. Identity and nonpublication gates retained |
| BEH002 / REQ003–004/006 / AC002–003/006 | Applicable current evidence and real signing gates | qualification.py; release-lock.json; candidate.py; sign-macos.sh | Exact six target/mode rows/four targets, independent host/kernel and physical categories, actual-user statement references; Accepted-only signing. Fixtures cannot prove receipts true; real qualification/signing pending |
| BEH003 / REQ001/005–006 / AC004/006 | Normal publication with safe same-input retry | payload.py; publication.py; workflow payload/publish | Retain final complete bytes before effects; fresh-main check, tag annotation binding, draft normal/verify-tag, no-clobber assets, all-child preserve-digests/anonymous OCI, public downloads. Missing/expired/conflicting input refuses. New manual dispatch resumes original payload; no actual remote effects exercised |
| BEH004 / REQ005/007–008 / AC005/007 | Exact supported prebuilt download/install | install.sh; payload.py; README; packaging/RELEASE.md | Strict normal version, downloaded manifest/archive checksums, bounded four-member regular archive, exact metadata equality before CLI admission; no-setup explicit version smoke. Real final/public native smoke pending |
| BEH005 / REQ003/007/010 / AC002/005/008 | Host-only behavior, consent/state/source/permission safety | unchanged cmd/internal, engine recipes/pins | Byte-preserved, Mac/Linux native local race controls green; no application source/Guide change, live storage or installed-state mutation |
| BEH006 / REQ009–010 / AC008 | Independent truthful release policy/receipt/cleanup | root RELEASE/TESTING/README, packaging/RELEASE; staged publication journal | Removed extraction paired/unborn/manual-precreate/beta contradiction; license/pins preserved; owned local cleanup complete. Source finalization and actual release receipt remain Delivery-owned |

Scope Guardrail respected: **Yes**, UC001–005 only. No old filesystem/editor,
provider, VM campaign, dashboard nfs-2, app integration, paid infrastructure,
new backend/OS, Gatekeeper bypass or qualification weakening.

## Key Files And Ownership

- Workflow schedules runner/needs/permissions/artifact retention; pinned actions,
  publish=false default, fail-fast=false native matrix, no automatic publication.
- Thin release.py CLI; identity.py owns one source/version/path/hash algorithm.
  candidate.py owns exact engine/OCI/native/run/artifact validation; qualification.py
  only validates audited references and never fabricates them.
- payload.py separates final assembly/signature/member validation from publication.py
  external reconciliation. The latter never rebuilds/re-signs a bound retry.
- sign-macos.sh confines all six inputs to Mac signing, ephemeral keychain/0600
  certificate, selected Developer ID/team/runtime/timestamp, Accepted notary and
  sanitized receipt; cleanup on success/failure. No raw binary stapling claim.
- Durable fixtures in scripts/tests exercise parsers/files/actual shell/installer,
  with explicit external doubles. See checks-and-limits.md for what is real.

## Assumptions And Known Risks

Hosted Actions artifact API/download shape, actual BuildKit OCI, signing team/P12
pair, package association and scoped public visibility must be exercised downstream.
Candidate loss/expiry fails closed. Source or workflow changes invalidate the
candidate; qualification/docs/test-only descendants may retain it with identical
production hash/engine/OCI and reviewed diff. Publication is not atomic; visible
partial tag/image/asset effects remain, never deleted to fake rollback.

An isolated qualification registry may alter only generated unqualified metadata's
image hostname/reference, retaining the exact OCI digest/engine/source/version;
no runtime override or host daemon workaround was added. The real retained engine
was not consumed locally; fixture packages are not qualification. Public downloads
are deliberately still described as pending. Native source review does not judge
whether a referenced physical/user receipt is truthful; API/Delivery must do so.

## Task Design Health Assessment Implementation Check

- Reviewed posture: Larger Requirement / release behavior completion.
- Root cause confirmed: Missing Invariant / Duplicated Policy Or Coordination in
  distribution, not runtime filesystem layering.
- Refactor Needed Now, bounded packaging/workflow: **implemented** separate
  candidate/qualification/final-payload/publication owners with existing engine
  validator and runtime admission reuse. Matches assessment **Yes**.
- Design Impact route **N/A**; no architecture-owned boundary bypass needed.

## Legacy / Compatibility Removal Check

- No compatibility wrapper, beta route, old publisher or qualification fallback.
- Existing-tag-only, image rebuild/push before signing, upload-clobber and
  path-count-as-proof routes removed, not retained beside the new flow.
- Dead touched imports removed; current AST import/reference plus manual owner
  audit green. No unrelated dead-code cleanup/follow-up invented.
- Shared structures tight: runtime Release unchanged; candidate, qualification,
  final payload and external retention envelope carry different explicit meanings.
- Shared design principles reapplied. Size guardrails **Yes**: source max359
  nonempty lines. Candidate268/publication235 and workflow delta exceed220 signal;
  assessed as cohesive artifact/effect/scheduling owners. Final payload split out
  to121 lines. No >500 source file or broad generic framework.

## Persisted Data Transition Check

Per design Persisted Data / State Transition Decision:
- Host state **Not Affected**; no migration, deletion, version fallback or setup.
- Qualification/generated candidate **Discard or Rebuild**, only from a new actual
  candidate/evidence. Empty committed lock retained; no historical Pass promoted.
- External published identity/secrets **Directly Usable — No Migration**; exact
  current records/reconciliation, no tag/asset overwrite or private repo storage.
- Follows approved decision **Yes**, no deviation/migration implementation.

## Environment And Local Implementation Checks

### IR-002 current delta checks

Evidence root `implementation-evidence/ir-002/`: checks-and-limits.md,
checks-result.json, final-checks.json, source-inputs.json and cleanup.json.
- Mac system Bash3.2.57 arm64: original prefix fails new7test suite with5assertions;
  fixed7pass, including candidate/fresh four TARGET strings, metadata failure17,
  missing TARGET and OCI valid-output/nonzero pipeline refusal.
- Independent119-input copy/private HOME/TMP, Python3.9.6: all41 collected,
  40executed+1Go-child-only skip. No native Go rerun in this bounded round.
- actionlint, extracted-prefix Bash syntax/shellcheck, source hash and expected
  empty-lock refusal pass. Removing fresh flags, nounset or pipefail is detected
  by three independent-copy mutation runs (assertions, not harness errors).
- Other116 source inputs unchanged; no unused touched-test import. Workflow359
  nonempty lines, production delta5lines; no size/refactor pressure introduced.
- Eight Delivery-owned untracked files preserved byte-for-byte/unstaged; IR001
  history prefix preserved; own scratch removed. No hosted/remote/live actions.
- No unexpected failed attempt. Baseline/mutations are intentional red controls.
  Current results do not reclassify API001 or claim hosted/source-review Pass.

### IR-001 historical broader implementation checks — unchanged owners only

These remain attributed to source886b55e, not a new acceptance run of the current
workflow. Broader native/OCI/compile checks were not repeated solely for this argv
correction; the current shell and packaging boundary was exercised above.


Evidence root: `implementation-evidence/ir-001/`; canonical detailed report
checks-and-limits.md; current final-checks.json, checks-result.json,
linux-checks-result.json, source-audit.json, mutations.json, cleanup.json.

- Independent Mac APFS source copy, private HOME/TMPDIR/cache, verified official
  Go1.27.2, Python3.9.6: race7packages/vet/build/version pass; Python38 collected,
  37executed+1Go-child skip (native Go exercises child).
- Pinned Ubuntu24.04 arm64 local nonprivileged check container, read-only inputs
  extracted to guest filesystem, nonroot checks, Go1.27.2/Python3.12.3:
  race7packages/vet/build/version pass; Python38 collected35executed+3explicit
  container/Go-child skips. No Docker socket, live export or host mount operation.
- Four CGO-disabled builds pass, darwin/linux × arm64/amd64: **compile only**,
  not four-platform runtime acceptance. Current default version is unqualified.
- actionlint1.7.11, Bash syntax, shellcheck, source hashing and expected empty-lock
  publication refusal pass. Six scratch guard mutations detected by assertions.
- Real skopeo1.13.3 transports synthetic two-platform OCI with exact index/child
  equality. Root-owned OCI tar causes skopeo chown failure; verified owned layout
  fixes that local mechanism while retaining every blob byte. Final test is green.
- Full final independent copy and Linux archive equal final source inventory.
  Go/engine/pins/licenses/ordinary CI unchanged from input. No generated assets
  committed; evidence records only identities/logs.
- All raw failures retained in attempts.md/attempt directories. Protected native
  source and host-bridged-lock failures were harness placement, not weakened guards.
  Current results supersede intermediate snapshots without erasing them.

All listed local checks are **implementation-local checks**, not API/E2E sign-off. No physical
hosting, genuine user verification, real credential/notary, hosted build or public
release check was executed by implementation. API001’s later hosted failure is
separately attributed above. No secrets read or re-provisioned. Owned scratch and
containers removed; canonical/PM/history/old assets/shared cache preserved.

## Frontend Rendered-Result Check

**Not Applicable** — release tooling/workflow/installer/docs only; no rendered app,
UI interaction, Guide activation or dashboard changes.

## Downstream Coverage And Execution Still Required

1. Targeted independent source re-review of IR002/CR-001 and the new executable
   shell regression; prior unrelated source review remains historical. No duplicate Designer/API dispatch from implementation.
2. API NEW scoped actual hosted build-only candidate on current reviewed source:
   full aggregation after both Mac jobs; actual engine pairs/full OCI/artifact
   envelope, native four-runner checks,
   no public effects. Inventory authorized independent physical/test registry
   resources; execute complete candidate target/mode ledger and genuine user checks.
3. Verify current source/engine/OCI and metadata-only registry alias evidence;
   preserve real failures/skips. New source changes need a new candidate/evidence.
4. Delivery judges evidence, records qualification, refreshes/integrates main and
   runs authorized normal v0.1.0 publication. Actual P12/identity/Accepted notary,
   retained final payload, tag/draft/no-clobber/anonymous-image/public downloads,
   native final installer/signature checks and stage-specific retry must be proven.
5. Source finalization alone cannot complete this Task. Report concrete prerequisite
   failures, not invented Pass or a new credential request based on historical
   placeholders. No current release URL, user verification, AC007/TaskDone/Terminal
   claim exists. No implementation target merge/push/tag/release/deploy occurred.
