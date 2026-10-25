# NFS CLI feedback release — Delivery report

## Current result / scope
**v0.2.1 public release verified; final documentation CI/branch cleanup pending.**
DR-001 release-only round,2026-10-24→2026-10-25. Package nfs-cli-feedback-release
follows autobyteus-nfs-7; no separate PM key/UUID supplied or invented. New
requirements/design/sizing/review N/A — Release Requested, already merged source.
Historical source R1/SR001 Approved, SR002 Ready, Small/Low/Direct remains provenance,
not new independent-review or OS-password proof. No TaskDone/user verification.

## Authorization and project guide
User exact **“release please”**, after being told the feedback fix was merged but
not released. Solution Designer supplied release-request-handoff.md and isolated
workspace. Normal patch v0.2.1 selected after fresh tag/draft/run inventory; no
preexisting v0.2.1 or active publication. Stable packaging/releases/v0.2.1/authorization.json
records NEW permission, adopting existing R3/SR004 safeguards without reusing old
v0.1.0/v0.2.0 authorization or inventing an SR approval. Field/user tests Deferred.
Guides: root RELEASE.md and packaging/RELEASE.md, initially at cf62eece7d1e8799a608d5d13b87dbd599db9a56;
prepared release revision77632d13c414276140f0390e559600cf4a7b40a3. Followed normal
candidate→genuine readiness→main→fresh publication→observed same-byte resume→
public checks. No procedure deviation; guide prose changed only for version authority
as explicitly allowed by handoff. No new product/software/packaging executable fix.

## Integration, source availability and immutable publication identity
Initial fetch/merge origin/maincf62eece7d1e8799a608d5d13b87dbd599db9a56 was Already current
before edits. Candidate built from exactly that source/workflow. Prepublication
preparation changed only version evidence/authority/notes/plan, guide prose and
measured engine/readiness lock, not runtime/tests/recipe/signing/installer/workflow.
Source review follows actual Small/Low direct route: current implementation
self-review, API00195% and Delivery diff acceptance; no fabricated reviewer Pass.
Genuine source-review.json states that boundary and the intermediate delta.

Fresh target unchanged; ticket e055164d25c36c46d07aaa3a4b4aaea595de8684 committed/pushed,
--no-ff main **77632d13c414276140f0390e559600cf4a7b40a3 (P)** pushed and remotely confirmed.
Ticket/main trees equal. Ordinary CI40123701043/40123703942 Success, each MacARM/LinuxAMD
10Go race packages/vet/build/version/Python78collected77executed1Gochildskip/Bash.
Archive was moved before that commit, explicitly NOT a completion claim.
No replay/reset/canonical-main or prior-version merge. Postpublication docs tail
will be recorded separately; the published source/tag remains P, never the later
main receipt. See source-finalization.json and source-ci-summary.json.

## Candidate, readiness and measured identities
Build-only run **40122429749/1**:10success/2expected payload-publish skips. All4native
Go1.27.2 targets passed10race packages/vet/Python78collected77executed1childskip/
build/version/archive; engine2, completeOCI and aggregation passed. No signing in
candidate. Counts overlap and are not additive unique tests. Actual envelope and
bounded19file129941623byte retained directory verified by production facade.
- Candidate artifact12571548710; wrapper sha256:3c78c95ff417180c95583485235a8039b38d93531b90cc771e266d336b431b74;
  expiry2027-01-22T18:48:57Z; recordSHA668613d0374e219b597af9c7ee3107d88103e3caf93d1b4af1374f568c7393cd.
- Actual measured sourceHash **ca0e207ab0efd06bbe7b5811af59efec7af7403a8d0efcc7ad434f9dce794b6d**.
- Engine manifest69cfdb792a35ddfac1388956d8b57a61c7efdb271cd0a63c300d863fdead2bf2.
- WholeOCI sha256:2d5e77ec5dbee63199af0f19611a88c1aecb6a0da619682d9e42f60d00a3b2c0;
  both child identities are in candidate-measured.json/public-verification.json.

Two actual engine build-inventory hashes differ from prior lock; recipe/package/
source/pin/size fields unchanged. Baseline fbc95116… computed with the prior engine
is NOT the measured candidate identity. Delivery attempt1's extra equality assertion
was wrong and stopped after successful envelope/fetch/verify; its failure is retained
in candidate-verification-attempt1.txt. Correct measured-manifest hash reproduces
candidate identity; no validator weakened, new candidate or stale readiness promoted.
Candidate version passed and candidate-only release admission correctly refused.
Old readiness correctly refused; genuine new stable readiness prepared after these
checks; --check-publish exit0 and unchanged measured source verified before dispatch.

## Signing, partial publication and exact-byte recovery
Original fresh publication **40123737340/1**: all4final native jobs and payload
job120962911793 passed. BOTH actual Mac Developer ID/runtime/timestamp/strict checks
and Apple **Accepted** notarization passed; binary hashes/team/submission identities
are in final-native-signing.json and public-signatures.json. Overall original run
remains **Failure**, because publisher refused “Known release is missing; cannot
recreate” after confirming tag and attempting draft reconciliation. Not a signing
or notary failure; exact underlying visibility cause is not established.

Preserved annotated tag **110df500cb8438975271109d7feccc64f87cd2e2**, P, draft422931518,
and original retained payload artifact12572518441/wrapper
sha256:d6040fcbd5167d4d0743c22fa27ca27f7b71bb3127394edc37a868f2087b8d4d,
expiry2027-01-22T19:06:02Z/publicationSHA
d4807c3bf7cb522c69f64c44298edbaf9e7fcb180aef6b70fed60cb43676a4e0.
Fresh direct-ID/list inventory found the exact draft/0assets; inspect-bound exit0
independently validated original envelope/source/jobs/bytes (no admission claimed).
Current main stayed P. New authorized manual **resume40230515652/1 Success**:
prepare and publish success, engine/native/candidate/signing/payload skipped by
design. No tag movement, asset replacement, rebuild, re-sign or code change.
Final receipt artifact12612659888: published release422931518, same bound payload,
wholeOCI anonymous linux-amd64/linux-arm64 and Ubuntu x64 owned-HOME installer smoke.
Nonblocking recurring fresh-draft reliability concern: **FU-001**, follow-ups.md;
only Solution Designer sends it for deduplicated future custody, not a new fix cycle.

## Actual public verification and distribution
**Normal/latest https://github.com/AutoByteus/autobyteus-nfs/releases/tag/v0.2.1**.
18anonymous versioned HTTPS asset downloads exactly equal retained signed payload;
all17checksummed files pass. All4native archives have exactly4regular members,
metadata equals public manifest, and retained byte hashes match. New version has
all4distribution targets with filesystem/user Deferred, not qualified platforms.
Both downloaded Mac binaries pass strict DeveloperID/team/runtime/timestamp and
actual online `codesign --verify --strict --verbose=4 --check-notarization -R=notarized`.
Standalone-code method per TESTING.md; no fake stapling/Gatekeeper policy changes,
no app-style assessment or local Intel execution claim.
Actual public installer plus installed `version` passed in owned MacARM64 HOME,
exact stdoutv0.2.1 and deferral stderr; installed bytes equal signed payload. Actual
UbuntuAMD64 public install/version and anonymous completeOCI proof are in final
publisher receipt/log. No live-user installation or upgrade performed.

Actual downloaded MacARM64 binary/Run/currentHTTP/PTY and sandboxed Chromium156
exercised both roles,1280/390, private session, one Authorize request, waiting→
local-helper-start-failure→Stop, token removal/exit0/bootstrap cleanup; zero browser
errors. Per-process sandbox explicitly refused sudo/open before execution, verified
with harmless exec controls. NOT a protocol/root/HTTP double, but also NOT real
sudo/password/cache/OS denial or successful admin admission. Terminal transcripts
prove no false confirmation/readiness. Screenshots personally inspected; they
capture transient waiting frames, not settled failure/successful approval screens.
No automatic browser-opener or storage operation. Source success/reminder/Stop
proof remains separately attributed ordinary-child testing, no original-password
diagnosis. Exact receipt: public-feedback-smoke.json, public-*-terminal.log and
visual-review.md; no private tokens persisted.

## Documentation, cleanup, custody, limits
README now advertises actualv0.2.1/download URL, exact bounded verification and no
automatic upgrade. docs/dashboard.md accurately marks feedbackv0.2.1+ and excludes
v0.2.0; root/packaging guide authority prose is truthful. Bound stable readiness/
authority/notes/plan and all previous release records remain unchanged. Release
notes prepared before effects, used byte-exact by publication. No docs-sync/handoff
summary required for release-only route; this report and revision/notes are primary.

Own browser/tools/cache/install/HOME/TMP/downloads and redundant inspection candidate
removed after evidence retention; no matching runtime processes. A first cleanup
guard safely refused its own checker-parent argv; corrected to exclude only known
checker/ancestor PIDs before deleting, not runtime exemptions. No force-kills or
root cleanup. Retain0700 /Users/normy/nfs-cli-release-vdwkpql_/candidate and
/Users/normy/nfs-cli-release-vdwkpql_/final-inspection/payload as exact provenance.
No old candidates, canonical PM/data, source archive, superrepo or user storage touched.
Oldv0.1.0/v0.2.0 assets/tags checked unchanged; only newv0.2.1 published.

Persisted data Not Affected; no migration/deployment/root/storage transition. No
rollback action. Rollback/fix-forward uses a newly authorized version; immutable
published tag/assets are never moved/replaced. Installation remains explicit.
Field/physical/user tests remain Deferred, not Passed and not closure prerequisites.
Version-bound approved plan: packaging/releases/v0.2.1/postpublication-testing-plan.md,
Delivery→terminal Solution Designer→requesting PM under existing nfs-4. No duplicate
field Task, host questionnaire or automatic dispatch. FU001 separate future concern.

## Remaining local gates
Publication/public checks/runtime cleanup Complete. Final docs ticket/--no-ff main
pushes, their ordinary CI, local branch cleanup and final terminal receipt pending.
No further release/signing/test campaign is implied. Final receipt will distinguish
published P, postdocumentation main and any local-only post-effect record.
