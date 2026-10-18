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
- Triggering rework/finding: **N/A**, initial implementation.
- Input review2051fd9559f4f4fa7beae68723429f8199b50004, design cbf7b35,
  approved base origin/main7e375984be2bea7a4d536e43cc59d6bc2b116870. Remote target
  was not refreshed/finalized by implementation; Delivery must check it afresh.

## Current Implementation Summary

**Implementation Complete — ready for independent source review**, not release
acceptance. Source commit **886b55e1cf88f3f696334bd5e7b8c374946a594d**. Personal
execution only; no delegation, push, hosted dispatch, release/tag or live-user action.

- Cycle Initial; implementation-revision-record.md **IR-001**.
- Solution R2/SR002 + SR003; architecture ARCH-REV-001.
- CRR/API-REV/DR and triggering findings **N/A** for this Task.
- Replaced existing-tag/clobber/early-image publication with manual build-only
  candidate → exact qualification → final signed retained payload → annotated
  exact tag/draft/assets → identical OCI/anonymous availability → normal release.
- Candidate and final payload identities are distinct; signed/qualified binaries
  are not claimed byte-identical to unqualified candidates. Final package reuses
  the exact measured engine packages and OCI, never rebuilt under old evidence.
- Default lock remains engine=null, qualification=null, no qualified targets or
  physical/user proof. Source hash with that **unqualified** lock is
  `8c1bcc13194f919c41cf4de9ad825a48acb4281bd558374ac77cbb1426820bac`.

## Routing Classification

- **Task size Large; architectural risk High; Confirmed** against design's Task
  Size And Architectural Risk and current implementation/source-audit.json.
- Irreversible cross-service publication, evidence/signing trust, failure recovery
  and four-target scope remain material; no downgrade from local green checks.
- Selected route **Code Review** by fresh rules (ir-001/routing.json).
- Direct-route lightweight self-review **Not Applicable**; ordinary implementation
  self-check completed, not a substitute for independent review.
- New Design Impact/Requirement Gap: **None**. Rootless OCI materialization is the
  designed layout transport retaining identical blobs, not a changed runtime or gate.

## Reviewed Behavior Implementation Trace

| Behavior | Approved change / preserved outcome | Actual path | Implementation result / limits |
| --- | --- | --- | --- |
| BEH001 / REQ001–002 / AC001 | No pre-created release; nonpublic candidate | release-nfs.yml prepare/engine/binaries/candidate; release.py; identity.py/candidate.py | Exact source/workflow/run/attempt/member identities and external artifact envelope; no write permissions/secrets in candidate mode. Actual hosted build still required |
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
- Shared design principles reapplied. Size guardrails **Yes**: source max358
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

These are **implementation-local checks**, not API/E2E sign-off. No physical
hosting, genuine user verification, real credential/notary, hosted build or public
release check was executed. No secrets read or re-provisioned. Owned scratch and
containers removed; canonical/PM/history/old assets/shared cache preserved.

## Frontend Rendered-Result Check

**Not Applicable** — release tooling/workflow/installer/docs only; no rendered app,
UI interaction, Guide activation or dashboard changes.

## Downstream Coverage And Execution Still Required

1. Independent source review, including new durable tests and all failure/effect
   boundaries. No duplicate Designer/API dispatch from implementation.
2. API scoped actual hosted build-only candidate on current reviewed source:
   actual engine pairs/full OCI/artifact envelope, native four-runner checks,
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
