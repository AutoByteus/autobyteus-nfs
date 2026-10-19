# IMP-08-02 — Draft discovery defect and immutable recovery design gap

Step/command: inspect current publication/candidate/readiness/payload/workflow,
replay retained DR013 endpoint observations with offline doubles (IMP-08-01),
read official GitHub release API documentation.
Commit: a7eb8a819c604358a5b01bd66b1fe1ffda313b19.
Environment/date: Darwin arm64/Python3.9.6, local read-only source and owned fixture;
2026-10-19. No actual remote observation/write or retained payload modification.

## Established defect

Delivery DR013 actually created the owned annotated tag and empty draft before
publisher117940608133 failed. Its saved response inventory establishes by-tag404,
list/direct-ID draft417014769 present, exact body/binding, zero assets. This round
reuses that real remote evidence; it does not claim another hosted reproduction.

Current publication.release() only calls GET releases/tags/{tag} with missing404
accepted as None. reconcile_release() creates a draft, calls that same lookup,
then dereferences None. All release discovery callers (prepare, publish,
post-upload reconciliation, final lookup) depend on this function. The current
unit test replaces release() with an already returned draft, so it cannot expose
this API-semantic difference.

IMP-08-01 uses the actual recorded draft/body and controlled endpoint responses:
by-tag returns None, list/direct-ID fixtures contain the exact draft. Current
release()/reconcile_release() never asks for list/ID and raises the exact
'NoneType' error; its create request is recorded only by a command double. No
remote create was made. This is a reproduction of the defect, not a successful
fix or approval to create a second draft.

GitHub documents by-tag retrieval for published releases, while authenticated
release listings include drafts for users with push access. Exact reference:
https://docs.github.com/en/rest/releases/releases#get-a-release-by-tag-name
and https://docs.github.com/en/rest/releases/releases#list-releases
Read on2026-10-19. A fix must account for the caller's actual draft visibility,
bounded pagination, unique exact-tag discovery/direct-ID correlation, missing
post-create observation, and ambiguity/foreign body/binding refusal; not merely
catch TypeError, return a guessed ID or blindly create/adopt another draft.

## Why the normal Local Fix route cannot yet finish safe recovery

The draft algorithm itself is a bounded implementation defect. However, the
existing DS5 recovery contract only resumes with the SAME executing source/main.
No approved executor-versus-bound-payload distinction exists. Fixing the publisher
and then running a normal new candidate/signing cycle cannot repair the existing
immutable v0.1.0 tag without violating retained identity.

| Existing check / owner | Concrete consequence of a new publisher commit |
| --- | --- |
| identity.SOURCES / source_hash(): all release_support bytes hashed | Even a comment appended only in a disposable publication.py copy changes hash3e1af43a… to0eda1760… (IMP-08-01); an actual repair cannot be silently excluded. |
| candidate.verify(): source_hash(measured) == candidate.sourceHash; readiness validates candidate | The original candidate is not accepted against edited publisher bytes. Creating a new candidate instead cannot change the original tag/payload binding. |
| publication.prepare(): env GITHUB_SHA == source_commit == i.commit() on main | Selecting old source while running new dispatch main is refused; checking out old source retains the bug. No alternate reviewed executor input exists. |
| tag_binding(tag, source_commit) | Existing immutable tag target238 is compared with executing source. Controlled new-executor input refuses `Published tag points to different source`. |
| payload.verify(): receipt.sourceCommit == i.commit() | Even unchanged original bytes under a later executor commit refuse `Publication inputs differ` (full synthetic payload control). |
| publication.publish() → fresh_main(binding.sourceCommit) | Advancing main to corrected code makes the old binding fail `Remote main advanced; reintegrate before publication`; existing tag must NOT be retargeted. |
| workflow prepare/publish checkouts and packaging guide retry section | New manual resume still executes the same source identity; guide explicitly says same exact main/version/candidate. |

These refusals correctly enforce the CURRENT contract. Weakening any one of them,
patching old source in place, overriding i.commit/ROOT/sourceHash, manual upload,
changing receipt/provenance, re-signing or authorizing another version would not
be an implementation-local correction of that contract. R3/SR004 design D3 and
DS5 explicitly retain these mechanisms; it needs a narrow technical recovery
revision before dependent implementation continues. No new product/field decision
or user questionnaire is implied by this escalation.

## Request to Solution Designer

Specify how an independently reviewed corrected publication executor can consume
and validate the exact annotation-bound original source/candidate/signed payload,
with distinct explicit identities/authority and truthful executor evidence,
without weakening fresh publication, candidate/source/engine/OCI equality,
retention/job-success/binding checks or current-main authorization. Define the
allowed recovery code scope, source freshness checks and fail-closed behavior;
do not silently promote a new candidate or replace final bytes. Keep discovery
correction inside the existing publication owner and no arbitrary bypass path.
Return through the configured Large/High design-review route as required.

The implementation hold is intentional: no production or durable-test change
this round. The offline probe is ticket evidence, not a new release executor.
A subsequent implementation can add semantic draft/list/ID regression and exact
recovery/admission/ambiguity/no-effects controls against that completed design.
No repeated successful signing/native/engine campaign solely for a repair gate;
API/Delivery choose the affected checks under the completed authority.

## Immutable state and carried success

Delivery owns actual evidence: run39215470944/1 main238bdc183e8affac99ffdee9be9cb333b0eb126f
passed BOTH real Mac Developer ID/team/runtime/secure timestamp/strict verify and
Accepted notary. ARM52450985-4e16-482e-b22a-d7b15b8791b7;
Intel563db88f-7ded-48ba-9d90-bcdbf8705961. Downloaded payload signature/binary hashes
were independently checked by Delivery. No further signing/credential repair is
indicated. Old DR005/009/011 failures are not rewritten or their deleted cause
claimed recovered. API006/CRR012 scopes carry.

Preserve tag objectf4a04fd0c80a6625708ba002b4cef5507a03f514 →238,
empty draft417014769, candidateAPI006, and original successful payload job117940491787.
Annotation artifact12169472209/run39215470944/attempt1 expires2027-01-17T07:21:36Z;
wrapper sha256:b552faeaf6de1337ef8cf3056878b9bf0f1822faed5645033a8d5145fd1d0336;
publication.json SHA3b0cbedd15782871e0c88c51b6847abcf276e7db00aab6f10c4dd387b4133dc8.
Retained payload /Users/normy/nfs-first-final-dr013-gmvotux9/payload;
candidate /Users/normy/nfs-first-candidate-api006-a8aune30/candidate.
No new remote freshness claim; last actual tag/release/package observation belongs
to DR013. Main238/72/f830/768 finalizations, historical candidates, local diagnostic,
PM and other owners remain untouched. Field/user Deferred, not blockers.
