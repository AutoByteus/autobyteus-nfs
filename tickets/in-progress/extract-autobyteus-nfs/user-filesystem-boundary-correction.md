# User boundary correction — filesystem-agnostic AutoByteus

2026-10-16; package extract-autobyteus-nfs; Task project_task_fdb2c737-fb08-48cf-8aca-e04df2d02ae8. This is a material requirement change to R1/SR-002, not another approval of the old integration.

The user challenged coupling via attachment files and stated: “the logic should never care about what their file system is right? because they work on the applciation layer” and then “also autobyteus should not care about whether its a mounted or not. because it just use file system apis”. Solution Designer informed the user that AutoByteus must use ordinary workspace paths/filesystem APIs, not mount tables, NFS identification, attachment files or NFS CLI queries; setup/readiness is outside the application.

R1/SR-002 provisions preserving NFS-specific application/launcher admission, public attachment contract and cross-repo fixture coupling are no longer an authorized implementation basis. ARCH-REV-001 Pass applies only to the superseded R1/SR-002, not this direction. Remaining extraction/license/no-release/live-safety/preservation constraints remain.

Current intended boundary: NFS owns filesystem-sharing setup and its own internal state; AutoByteus uses supplied paths and ordinary filesystem results/errors without classifying local/mounted/NFS storage. This requires tracing application admission, terminal/workspace fallbacks, runtime skill/private-state selection and Docker launcher coupling before a replacement design is ready. Do not simply delete checks and leave callers or existing state unsafe; no live resource manipulation or automatic migration is authorized.

Coordination prerequisite: implementation is active against the old basis (N has extraction commits and untracked implementation evidence). Need implementation owner's checkpoint of changes/ongoing processes and a safe hold of affected old-basis work. Preserve all work/evidence; do not reset, clean, finalize, push or publish based on obsolete integration requirements. No new implementation dispatch is made by this notice.

Canonical ticket: /Users/normy/autobyteus_org/autobyteus-nfs-worktrees/extract-autobyteus-nfs/tickets/in-progress/extract-autobyteus-nfs. Replacement requirements/design are under Solution Designer recovery; final reviewed replacement will use normal routing. This notice is input/hold context, not an implementation-ready specification.


## Checkpoint resolved / current authority
Implementation owner returned `implementation-evidence/ir-001/hold-checkpoint.json`: safe hold, no running owned process/resource; N0c9fd27 / S390e0c76 retained. Go preparation failed before tests; owned scratch retained for implementation cleanup. No reset or live action. Recovery is now completed as requirements R2/SR003 and design SR004, both in the canonical five-document package. This original notice remains the input record; its “recovery in progress” language above describes the earlier checkpoint, not a competing current spec. ARCH-REV-001 is historical; replacement independent review is required before affected implementation resumes.
