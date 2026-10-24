# API/E2E Coverage Investigation — nfs-setup-dashboard

API-REV-001 plan, 2026-10-24. R1/SR001 Approved, SR003/ARCH002; Large/High/Reviewed. Current d9beb0f796894c37a371217768b9e33afcde315a; product5f8cabf8, final tests2445aabf. No prior API result. NFS task only; no release or field qualification.

## Authorities and execution discovery
Read requirements, investigation (no supplements), solution/design and revision history, ARCH002 report, implementation handoff/revision including Checks Run FIRST and legacy/data decisions, CRR001 report. Root AGENTS.md, DESIGN.md, TESTING.md, README.md, docs/dashboard.md, go.mod are applicable; no closer instructions. Historical solution handoff says pending review, superseded by ARCH002/CRR001. Source tree owns plain embedded HTML/JS, Go admin/session, bounded HTTP/private pipes, same installed executable sudo and serial service. No app/Node runtime dependency. Development tests use private HOME/TMP/source; native mutations only disposable owned guests, never host mounts/configuration or existing Docker nodes.

TESTING defines Go race/vet, Python packaging, build/cross-compile and build-tagged Chromium/WebKit preview. Preview doubles root IPC and clipboard, so it is not a native integrated acceptance result. Native tests require ordinary controlling TTY, actual sudo/private pipes, actual packaged-engine inputs and current self-contained binary. Retained pinned engine may be verified/read, never rewritten. Old toolchain/VM/scratch removed by IMP14; provision fresh owned environment as needed. No release metadata writes in repository. No physical/AMD64 runtime or signing claim.

## Changed boundaries and durable-test decisions
| Coverage | Decision | Current behavior / limit |
|---|---|---|
| admin session/resources/pipe tests | Still Valid | root admission, retained exact plan, consent/cancel/expiry/replay/global lock, EOF/EPIPE and in-flight drain, saved-user identity; controlled filesystem/clock boundaries only |
| admin supervisor and CLI boundary tests | Still Valid | complete relocated serial owner, no SUDO/TTY requirement, active-only pending refusal, cleanup/stop, no nested coordination |
| dashboard real HTTP/privilege tests + adminwire strict protocol | Still Valid | Host/Origin/token/bounds, no auto-work, dedup, private bootstrap, directories only, pipe handshake/correlation; fixture child not actual sudo |
| browser.cjs + build-tagged fixture | Still Valid | actual assets/DOM in Chromium/WebKit, forms, roles, keyboard, widths, pending/errors/expiry/slow/stop; root+clipboard doubled |
| existing setup/config/backend/docker/platform/CLI and packaging suites | Still Valid | preserved invariants/direct saved-state readers and asset source identity; no new format or migration |
| IMP04/06/09 native earlier builds | Reuse only unchanged exercised mechanisms | exact source deltas must be mapped; never blanket-current UI/PID/error proof |
| IMP10–13 current native Mac/Linux, service and CLI | Reuse with input/binary provenance | real HTTP/TTY and mounted bytes; no visible browser-to-native claim |
| complete browser→ordinary HTTP→sudo→pipe→actual host effects | Use Temporary Executable Probe Only | missing integrated proof; requires disposable native resources, not a CI sudo test. Preserve reproducible harness/evidence in ticket |

No stale coverage/removal or production change planned. Existing field/physical task excluded. No contrived competing users/tabs; ordinary repeat/cancel/reload and independent CLI busy during own review are supported. No unsafe hard-NFS fault injection just to make a hang.

## Planned cases / scenario mapping
| Case | Kind | Scenarios / criteria | Proof and surface |
|---|---|---|---|
| API-01 | Reused | SCN001–010; AC001–008 | Inspect exact IMP02/07 current repository results and test assertions, source-diff relevance; count once, compiler-only targets explicit |
| API-02 | Reused | SCN001–010; AC001–008 | Map IMP04/05/06/09–13 current/unchanged renderer/native/CLI/service boundaries and actual input limits; do not repeat clear checks for independence |
| API-03 | New actual integrated | SCN001/002/004/005/006/007/008/009; AC001/002/004/005/006/007 | Fresh Ubuntu ordinary-user TTY/public server in owned guest, actual browser bootstrap/authorize/native server exact review/cancel/consent/configured vs ready/reload/reconnect/lock/expiry/safe detach and source preservation. Inspect pending/error behavior if real supported failure reaches it; no manufactured data migration |
| API-04 | New actual integrated | SCN002/004/006/009/010; AC002/004/005/008 | Current browser/Linux Docker server mode sequentially on same owned guest, actual daemon/engine/current control, installed service and disconnect; only if API03 remains healthy |
| API-05 | New affected client/authorization control | SCN003/007/008/009; AC003/006/007 | Current actual browser client Connection paste/override/malformed/occupied targets/exact review/cancel and real sudo/lock/5min expiry; native client mount proof from current IMP10/11. Add actual client commit only if necessary to close evidence gap safely; record layer separation |
| API-06 | New cleanup | SCN006/009/010; AC005/008 | public drain/detach, source/marker/sentinel preservation before removal, no owned service/helper/mount/container, shutdown/delete exact owned guest(s), source/tool/retained-engine preservation |

## Evidence reuse / remaining gap
Repository evidence can be reused only after final-input diff and decisive raw results inspection. Reused cases are attributed Implementation, not API re-execution. Renderer and native control journeys separately are strong but leave integrated browser-native ordering/authentication unknown; required API03–05 close that gap. No broad storage filesystem campaign. New failure will be reproduced/isolated before origin routing, not silently repaired. Cross-target source-build compatibility is compiled only; field resources not requested.

## Environment and cleanup plan
Fresh private scratch under /Users/normy, isolated TART_HOME and task-named Ubuntu clone; immutable base clone/read-only cache if available, otherwise pinned public Tart tool/image. No host admin/network configuration. Actual browser in guest preferred; if host browser accesses only the guest's exact loopback origin via private SSH forward, document that test transport explicitly, never claim native guest browser association. Public fixture account only, no private credentials. Build current isolated source with measured retained engine, development metadata and empty releaseTargets. Keep capability URLs/tokens out of committed logs/screenshots. Terminate only known owned processes; no force-unmount or kill admitted storage work. Source sentinels survive public detach before disposable VM deletion. Final report's Cases is the canonical ledger.

API04 refinement before execution: exercise supported daemon-unavailable setup interruption using only the fresh owned guest Docker service (no running storage before first apply). Stop its daemon after exact review, allow the real Apply to return incomplete/pending, restore that same daemon, inspect and freshly consent to same-identity PendingPlan. This is actual local-dependency failure/recovery, not hand-edited private state or fake root IPC. No force-cancel/hard-NFS test.

API07 newly discovered supported chooser typing timing, AC007: API03 initial attempt entered a path before initial listing finished and observed old path. Use a focused native browser probe with normal sequential keyboard input and actual directory responses to distinguish a test-order mistake from real user input loss. Do not alter production or assert cause from reading alone. It runs before API04.

API07 result: real native keyboard input at80ms/key reproduced path replacement by actual initial-listing GET at502ms (no artificial delay). Same settled input exact. This is new chooser functionality (REQ009/AC007), preliminary Local Fix to implementation; no product edits. Independent API04/05 can safely continue with settled chooser/manual fields so later owner has a complete affected matrix. Full result cannot Pass with this finding.
