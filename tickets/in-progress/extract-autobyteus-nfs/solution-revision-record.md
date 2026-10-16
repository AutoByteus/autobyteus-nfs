# Solution Revision Record — extract-autobyteus-nfs

## Revision Index
| ID | Phase | Trigger | Prior status | Current status | Affected IDs | Result |
| --- | --- | --- | --- | --- | --- | --- |
| SR-001 | Requirements | New Task fdb2c737; 2026-10-16 user separation direction | N/A | R1 Approved; design N/A | SCN/UC/BEH-001–004, REQ/AC-001–008, DEC-001–005 | Ready for architecture |
| SR-002 | Design | SR-001 approval + architecture investigation | R1 Approved/design N/A | R1 Approved/design Ready | Same IDs | Architecture Design Complete; Large/High |
| SR-003 | Requirements recovery | Direct user filesystem-only correction; held implementation | R1 superseded / design Needs Revision | R2 Approved / design Needs Revision | BEH003,005–006; SCN003,006–007; REQ/AC003,006,009–010 | Ready for replacement architecture |
| SR-004 | Architecture recovery | Approved R2 / SR003 + full affected owner traces | R2 Approved / design Needs Revision | R2 Approved / design Ready | REQ/AC001–010; BEH001–006 | Architecture Design Complete; Large/High |

## SR-001 — Independent repository requirements baseline
- Initial Baseline. Trigger: /project_task_manager assignment carrying explicit user direction; finding IDs N/A.
- Prior requirements/design N/A; initial bootstrap draft completed to R1 Approved, design not yet authored.
- Evidence: current source 3712cd9bf0db998501d162db7f8655f169e3def6, unborn destination plus PM metadata; embedded build/fixture/workflow coupling, existing installed contract and unqualified publication policy.
- Intended behavior: new repository-separation request, unchanged runtime semantics. All four supported scenarios established. No fictional earlier architecture/review result.
- Canonical requirements and investigation updated; no behavior-defining supplements. Product fields N/A.
- Approval: Solution Designer within explicit direction; exact R1/SR-001; user informed in conversation message beginning “The NFS source, installer, packaging and service tests will move to the standalone repository.” No Needs user decision.
- Design/review/routing/classification: N/A before design. No handoff yet; next action architecture investigation and design.
- Remaining gaps: technical path/source-hash/consumer/finalization decisions for architecture, not product blockers.

## SR-002 — Completed extraction architecture
- Phase Design; classification Design Impact (initial architecture completion after R1, not a downstream failure). Trigger SR-001 approved standalone outcome; finding IDs N/A.
- Prior R1 Approved/design N/A → R1 Approved/design Ready / Architecture Design Complete.
- Intended behavior unchanged. SCN/UC/BEH-001–004 and REQ/AC-001–008 mapped; DEC-001–005 implemented technically; R1 approval unchanged, no new behavior supplement/user question.
- Canonical investigation extended E01–E11/A01–A05; design created with clean-cut root module/owned distribution, pinned consumer fixture, unchanged installed state, nonpublishing policy and ordered two-repo finalization.
- New independent review/implementation/API artifacts N/A — not applicable yet. Old Task proofs remain historical, not forward approvals.
- Task size Large; architectural risk High: module/build/distribution/consumer ownership and two-repo finalization change, not file-count inflation. No runtime schema migration or new filesystem capability.
- Route: fresh rules select `/software_engineering_team/architecture_reviewer` for Architecture Design Complete / Large / High. See solution-design-handoff.md. No direct implementation/PM duplicate forwarding.
- Remaining product/technical design blocker: None. Actual implementation/validation/finalization remains downstream work.


## SR-003 — User-directed filesystem-only boundary
- Material Requirement Gap/change, not failure of an executed test. User's own words in `user-filesystem-boundary-correction.md`: AutoByteus must not care whether storage is mounted, only use filesystem APIs.
- R1/SR002 approval was revoked for affected coupling, requirements temporarily Draft/design Needs Revision. ARCH-REV-001 at 5d354b9 passed only R1; no new pass inferred. Implementation checkpoint `implementation-evidence/ir-001/hold-checkpoint.json` confirms safe hold, N0c9fd27/S390e0c76, no running owned process/resource, retained preparation failure/scratch. Existing commits/work preserved.
- R2 corrects core requirements: remove two-way app/NFS attachment dependency; generic path behavior; NFS host-only responsibilities; uniform existing private configured-skill profiles; normal Git ownership policy. Keep licenses, no-release/live-safety/finalization and all unrelated work protections.
- New SCN006–007/UC005–006/BEH005–006/REQ009–010/AC009–010; existing IDs retained. DEC001/004/005 revised, DEC006–008 added. Prior canonical baseline remains in Git381231ee; prior review artifacts untouched.
- Approval: Solution Designer within user's corrected direction, exact R2/SR003; conversation message beginning “Exactly. The boundary should be a directory path—not an NFS attachment contract.” User informed about ordinary errors and private runtime storage. No Needs user decision.
- Next: architecture investigation/replacement design against R2; previous forward-ready design no longer authorizes affected implementation. No route at this requirements-only boundary; no renewed approval questionnaire.


## SR-004 — Filesystem-only product boundary design
- Material design recovery after approved changed intent, not repeated R1 forwarding. R2/SR003 unchanged and approved; current design Ready. Requirements and technical design are separate authorities.
- Evidence E12–20: app mount/admission/terminal/Git/private-profile call graph, generic launcher mapping, NFS mixed engine/app-node ownership, exact state/installer/pending ordering, implementation hold. Full R1 historical evidence/approvals retained in Git and prior log entries; current core spec rewritten to eliminate contradiction.
- Target: independent Go host sharing/mount service; app ordinary paths only; private configured-skill policy no filesystem selector; no implicit Git trust; no public app descriptor/node management or paired fixture. Preserved host safety, licenses, closed publication, source/private data, generic launcher and finalization protections.
- State decision: no automatic transformation. Node-free host state directly usable; active old node obligations preserved and refused at NFS installation/administrative boundary before replacement/resource changes. No old runtime, public descriptor dependency, app startup check or history scan.
- Revised design includes file removals/engine retained types, all runtime/launcher callers, data-disposition reasoning, required executable controls, docs/policy reconciliation, two-repo finalization and owned cleanup boundaries. No new implementation/test success claimed.
- Classification: Large/High because runtime/privileged boundary ownership plus distribution/finalization are materially affected. ARCH-REV-001 Pass remains historical R1/SR002 only. Implementation owner confirmed held/no running resources, no tests reached.
- Approval basis: R2/SR003 with recorded user notification; no new product question. Current independent review and execution remain downstream requirements.
- Routing: fresh rules select `/software_engineering_team/architecture_reviewer` for revised Architecture Design Complete / Large / High with R2 Approved and user informed. Exact selection in solution-design-handoff.md. No direct implementation redispatch or duplicate PM message.
