# IR-004 — CR-002 touched-file import cleanup

## Basis and exact change

R3/SR004 Approved / SR004 Ready / ARCH002 Pass; Large/High confirmed.
CRR004 Fail99 is the current reviewer result, not overwritten by local checks.
Stable input0d8d927a17b5737547df03fdbc25cc7fdf666d1e includes review484c85c and its
receipt. Source commit 850dfeb97e2ec396b2b134e760dc9ee802873d6b. Only two local bindings removed:
packaging/engine/manifest.py `LOCK`; scripts/tests/nfs_release_fixture.py `readiness`.
No runtime, assertion, live owner or consumer removed. AST delta audit equals the
baseline after deleting only those aliases. AST import-use scan across16 extant
IR003-changed Python files finds zero remaining unused local imports; this is not
a compiler/linter claim. Direct reference/caller trace corroborates no re-export.

## Fresh local checks

`run-checks.py` created an independent120-file copy under an owned local development
scratch with private HOME/TMPDIR, no sibling checkout, and Python3.9.6.
- `python3 -m unittest discover -s scripts/tests -p 'test_nfs_*.py' -v`: exit0,
 45 collected,44 executed,1 expected standalone Go-child skip. Parent fixture was
 not rerun in Go this round. All executed controls pass, including engine reset,
 source hash invalidation, readiness, payload/signing/publication fixtures and
 Bash invocation. No fixture is real Apple/GitHub/registry/field qualification.
- `python3 packaging/release.py --source-hash`: exit0, current
 `c7fd64e87b62509165d8655cc576fba9261867a306f13a93ad420776304e4a60` (before `d75c50c83a5848d45209e85511f271f36d5d99362fd87f41b8e24263203591ac`).
- Actual `source.recipe_hash()` command: exit0, current
 `299db7012dcc543f8606632695d286548d1513c13ace8b108eb712984fd39274` (before `a1e24a5b0d82b74ad0558f499d991095ac0fcda8b99de5b7bb892db15c1e985d`).
- `python3 packaging/release.py --check-publish`: expected exit1,
 "Current engine and structured release readiness required". Lock remains empty.

Raw commands, timings, outcomes in checks-result.json and individual logs.
No failed attempt. No Go/Linux/four-target/native/actionlint/hosted/signing rerun
was necessary for the two-import delta; earlier IR003 and CRR004 evidence remains
attributed to its exact inputs, not newly executed. Engine recipe changes because
manifest is an input: no new engine built, and a NEW real complete current-source
candidate plus affected API result is still required. API002/run39113335636/1/
artifact12131531399 remain historical Blocked73.57, not promoted or modified.

## Preservation and limits

Other118 inputs unchanged; no binary/generated metadata committed.16 Delivery-owned
untracked files excluded and hash-preserved. IR001–003 history prefix preserved.
Own scratch removed; no processes/resources retained. Old candidate untouched.
No push/target merge/dispatch/signing/live storage/user verification/TaskDone/Terminal.
Field/physical/shared-filesystem/user tests remain deferred, not release/closure
prerequisites. Actual both-Mac signatures/Accepted notary, final payload, authorized
publication/public downloads and current-main checks remain API/Delivery work.
Six signing entries provisioned; no credential access or re-provision request.
Frontend inspection N/A — no rendered surface change. Next: targeted source review.
