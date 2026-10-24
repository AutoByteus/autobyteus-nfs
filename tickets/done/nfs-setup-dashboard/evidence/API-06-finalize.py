# API-06 reporting after completed runtime and cleanup; 2026-10-24 current source.
from pathlib import Path
import json,datetime,subprocess,hashlib
n=Path.cwd();t=n/'tickets/in-progress/nfs-setup-dashboard';e=t/'evidence'
for case,expected in [('API-03','Pass'),('API-04','Pass'),('API-05','Pass'),('API-07','Fail')]:assert json.loads((e/(case+'-runtime.json')).read_text())['result']==expected
assert json.loads((e/'API-06-cleanup.json').read_text())['result']=='Pass'
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
assert not subprocess.check_output(['git','diff','2445aabf','--name-only','--','.',':!tickets'])
(e/'API-06-source-check.json').write_text(json.dumps({'case':'API-06','date':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':'git diff 2445aabf --name-only -- . :!tickets; inspect cleanup','commit':head,'productDelta':[],'durableTestsChanged':[],'result':'Pass'},indent=2)+'\n')
r=t/'api-e2e-execution-coverage-report.md';text=r.read_text();cases=text[text.index('| Case ID |'):text.index('## Acceptance-Criteria Proof')]
text=f'''# API/E2E Execution Coverage Report — nfs-setup-dashboard

## Round
**API-REV-001 / Fail / 81.43%**, 2026-10-24. Task autobyteus-nfs-2 / project_task_f1264eb8-5a99-4a19-949f-09d141c955a1. No prior API result. Plan: `api-e2e-coverage-investigation.md`; history: `api-e2e-revision-record.md`; working log: `api-e2e-test-progress.md`. Evidence: **{e}**. This is the NFS dashboard task, not older filesystem/editor/guide/release tasks.

One new case, API07, was added after the chooser input timing observation. Separate native-key reproduction establishes the finding; settled selection and other independent planned cases completed. Initial tool/harness failures remain preserved and are not product failures. No production or durable-test change.

## Routing Classification
Large / High / Reviewed (R1/SR001, SR003/ARCH002, CRR001). **Focused failure-origin Code Review required**, not successful-test review or Delivery. Preliminary Local Fix to implementation at the new chooser boundary. No new design/approval loop, release, target merge/push or TaskDone.

## Tested Builds And Environments
| Env | Input / executable | Platform / setup | Scope |
|---|---|---|---|
| ENV-IMP | IMP02/07 final2445aabf; native5f8cabf8 | Prior owned Mac26.6.2arm64 / Ubuntu24.04.5arm64; Go1.27.2; Chromium156/WebKit27.2 | Reused with exact delta map, attribution and limits in API01/02. Original environments removed by implementation; no inherited resource |
| ENV-API | Reviewed d9beb0f plus receipt-only **{head}**; sourceHash324bf4dbb24b8001324033a0abc131bc50a26e5d98284dcbb95d1be790e8cf13; Linux binary00351676d59a03f944359cf60b7f8b133a28317f3fd4a36bf7b142fbe5bd22e1 | Fresh owned Tart2.41.1 Ubuntu24.04.5arm64, kernel7.0.0-38, UID1000/GID109, ext4; new private TART_HOME; actual sudo NOPASSWD fixture, private pipes, native and Docker29.1.3 storage sequential | Current actual binary identical to implementation's current Linux build; same verified retained pinned engine, development-dashboard, empty releaseTargets/deferred field. Not release metadata admission |
| ENV-BROWSER | Actual embedded assets and actual guest HTTP/admin/storage, Chrome156.0.8078.47 on Mac | New private HOME/TMP/profile, sandbox enabled,1280 and390 widths, English UI; exact-port private SSH forwarding to guest127.0.0.1 only | Test transport, not product LAN exposure or guest OS browser association. Clipboard alone doubled to avoid touching operator clipboard; manual private-URL bootstrap actual; no root/API double |

## Cases
{cases}
## Acceptance-Criteria Proof
| AC | Critical | Cases | Result | Exact scope / remaining part |
|---|---|---|---|---|
| AC001 | Yes | API01/02/03/04/05 | Proven | Public role ordinary TTY, embedded assets, private fallback, no-auto-admin/work, root/no-TTY refusal carried; native pipeline current. No claim public v0.1.0 includes commands |
| AC002 | Yes | API01/02/03/04 | Proven | NativeLinux/Docker exact reviews, cancel/consent, actual mounted bytes, copied nonsecret JSON; exact-current Mac native server carried IMP10/12. Early chooser edit defect separately AC007 |
| AC003 | Yes | API01/02/05 + common commit pipeline API03/04 | Proven at recorded composite boundary | Actual browser paste/malformed/occupied/override/review; current native Mac/Linux client mounted byte/reconnect/detach proof carried IMP10/11. New API05 intentionally does not commit a client mount to the now-detached server; not a fresh whole browser/client-to-peer campaign |
| AC004 | Yes | API01/02/03/04 | Proven | Metadata not fresh-ready, current check/reconnect, actual daemon-loss pending, restore/same-ID fresh resume, wrong-role/restart; no private-state fabrication |
| AC005 | Yes | API01/02/03/04/06 | Proven | Consent/drain gating, stop keeps storage, source/marker retained on public detach and cleanup; busy/partial refusal at exact carried boundaries |
| AC006 | Yes | API01/02/03/04/05 | Proven | Actual loopback unauthorized refusal and ordinary helper, strict current HTTP/pipe tests, real sudo/identity/lock/EOF controls with input limits. NOPASSWD, not password-entry proof |
| AC007 | Yes | API01/02/03/05/07 | **Not Proven — Fail API-F001** | Actual normal native-key path corrupted by initial directory listing completion; same settled control Pass. Other narrow/keyboard/error/expiry/lifecycle controls pass at named boundaries |
| AC008 | Yes | API01/02/03/04/06 | Proven for API-owned scope | Preserved CLI/current native service and existing readers/build/assets. Delivery still owns fresh target integration/finalization/docs completion; not overridden here |

No behavior is labeled Only The User Can Check. Physical/field/general user qualification is outside this ticket and remains deferred, not passed. No new AMD64 runtime, reboot, signing, installer or publication claim.

## Validation Confidence Scorecard
| Category | Post-repository % | Final % | Supporting cases / residual |
|---|---|---|---|
| Requirement / AC proof | 90 | 50 | API01–06 strong, but critical AC007 fails API07 |
| Changed-boundary directness | 90 | 95 | Actual browser→HTTP→sudo→pipe→native/Docker; failure directly reproduced, not inferred |
| Cross-boundary realism / mock gap | 75 | 95 | Actual current integrated server/pending path; client final mount carried, clipboard doubled; no physical claim |
| Environment / identity / fixture fidelity | 95 | 95 | Verified exact current build/engine/native guest, no operator state; sandbox/private profile; NOPASSWD and SSH transport explicit |
| Failure / lifecycle / recovery | 95 | 95 | Actual pending recovery, expiry/global lock, refused source/target, stop/detach; controlled EOF/inflight tests reused, no unsafe outage injection |
| User surface | 90 | 50 | Readable real surfaces, but chooser completion corrupts an active native-key edit |
| Durable regression coverage | 95 | 90 | Strong current suites; native-key chooser scenario missed by settled-list coverage. API07 reproducer supplied; no production fix or new passing regression claimed |

Post-repository **90.00% (630/7)**; final **81.43% (570/7)**, arithmetic mean. Critical AC007 fails; final clean target95% not met, requirement/user categories below90. Scores do not override the finding.

## Broader Validation Decision
**Required and executed**: actual Browser + CLI/private IPC + native lifecycle, using only disposable resources. Closed the preview-root-double gap and found API-F001. Reused unchanged current Go/Python/native evidence instead of rerunning for independence. API05's actual five-minute lease was not clock-shortened. No external dependency blocker.

## Persisted Data / Legacy
Directly Usable — No Migration. API03/04 restart uses actual just-created saved state via normal current readers; API04 resumes actual saved pending intent with same storage identity. No hand-edit, schema upgrade, dual branch, root-path seam or compatibility wrapper. Existing removal/standalone guards covered in reused suites. No compatibility-only coverage retained/added.

## Durable Coverage Changed
**None.** New native and chooser probes live under ticket evidence; they are not project CI tests and require owned native preparation. No production diagnostics or patches. Successful-test review is not the route for this failed round. Existing upstream durable tests missed active-typing chooser completion; focused implementation regression requested after origin confirmation.

## Doubles and limits
- Reused preview: actual Chromium/WebKit/HTTP/assets, root protocol and clipboard double. Native evidence does not inherit that double's assertions.
- New API03–05: real root/native boundaries; clipboard only doubled. Real permission-denied OS user carried from IMP04; no password-entry or remote operator claim.
- API07: actual keyboard80ms/key, actual POST202/running and GET200/complete502ms later; **no artificial delay/response/clock/input-event double**. Same settled native-key control passes.
- Test SSH forwarding preserves exact loopback Origin/Host; it does not qualify native guest browser association, external clients or network topology.
- Native Mac and actual client/CLI/service results are reused with exact binary/input limits, not relabeled as fresh API execution. Counts overlap; do not add preview/scoped/full counts as unique tests.

## Temporary Methods / Cleanup
**Complete**, API06. Public source/drained detach before disposable teardown; original source/sentinel/marker and occupied-target sentinel recorded and retained until VM deletion. No task NFS mounts, Ganesha containers, product/helper processes or running owned jobs before shutdown. Owned Docker daemon stopped; guest shut down normally, exact owned VM deleted, private source/tools/browser/SSH/Tart scratch removed. Retained engine manifest and both architectures' packages reverified unchanged. Host mounts/exports/root config/Docker/network settings, existing browser/user data and other tasks untouched. No force-unmount, process-wide kill or forced storage cancellation.

API03 earlier preparation/chooser-order/modal-cleanup attempts and API05 diagnostic-wording assertion are preserved in their attempts files. API03 narrow screenshot named ready-390 actually captures the brief Applying state with a previous timestamped Ready observation; it proves responsive narrow rendering, not final readiness. Raw state and mounted bytes are the readiness evidence.

## Preliminary Failure Classification
**API-F001 / Local Fix → implementation**, pending Code Reviewer confirmation. New `internal/dashboard/web/forms.js:28` resets enabled path input on every listing render; line38 async completion triggers it during normal typing. Native-key reproduction and settled control prove the cause. This is current chooser functionality/REQ009/AC007, not an old editor/app issue or filesystem defect. See `API-07-finding.md`, actual response trace and screenshot. Do not repair production in API ownership or open a new approval/architecture/field campaign.

## Latest Authoritative Result
**Fail / 81.43%**. Seven planned/discovered cases completed: API01/02 scoped reuse Pass; API03/04/05/06 Pass; API07 Fail. No case silently skipped. AC007 not proven. Next: fresh most-specific failure-origin route, not Delivery/publication/TaskDone.
'''
r.write_text(text)
(t/'api-e2e-revision-record.md').write_text(f'''# API/E2E Revision Record — nfs-setup-dashboard

## API-REV-001 — 2026-10-24 initial reviewed validation
- Input: CRR001 Full Source Pass100, R1/SR001 Approved, SR003/ARCH002, Large/High. Current review d9beb0f plus receipt-only {head}; product5f8cabf8/finaltests2445aabf unchanged.
- Result **Fail81.43%**; post-repository90.00%; broader validation Required/executed. No prior API score/result invented.
- Canonical plan/report/progress remain `api-e2e-coverage-investigation.md`, `api-e2e-execution-coverage-report.md`, `api-e2e-test-progress.md`. Report Cases is the ledger; proof table gives AC mapping.
- API01/02 reuse attributed exact/unchanged implementation evidence with clear limits. New actual browser/sudo/pipe/native and sequential Docker, real pending recovery, client forms/global lock/actual expiry, cleanup all completed. API07 native-key chooser input overwrite fails AC007; API-F001 preliminary Local Fix to implementation, focused origin review requested.
- No production/durable-test changes or diagnostics; temporary reproducible harness/evidence committed. Initial setup/harness attempts retained; same settled chooser control passed, so no fabricated NFS failure.
- All new guest/browser/tools/source/SSH/scratch removed after public safe detach and source/marker/sentinel preservation; unchanged retained engine reverified. No old field/application/release campaign, target merge/push/tag/TaskDone or user-verification request.
- Fresh route/recipient receipt recorded in evidence/API-06-routing.json after result commit. Single required recipient only.
''')
print('Final report/history written, Fail81.43; product unchanged')
