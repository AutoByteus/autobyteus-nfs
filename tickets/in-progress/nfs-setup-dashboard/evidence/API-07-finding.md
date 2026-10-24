# API-07 / API-F001 — chooser completion replaces an active path edit

2026-10-24. **Reproduced and Read**, current production5f8cabf8/final source2445aabf, reviewed d9beb0f plus receipt-only deeea2f. Ubuntu24.04.5arm64 actual public `server`, native sudo/installed helper; Chrome156 on Mac through an exact-port private SSH loopback test transport. No response, clock, filesystem or input-event double for this finding. Root work is not needed for the failing chooser itself; no storage operation occurs in this probe.

## Supported trigger / expected versus observed
Open **Browse folders**, focus its enabled **Absolute directory path**, select the existing text and type `/home/admin/api-dashboard` with ordinary keyboard events at80ms per key. The initial real POST returns202/running; actual GET completes502ms later. Expected: typed path stays `/home/admin/api-dashboard`. Actual: `/home/adminadmin/api-dashboard`. The field loses the in-progress prefix when the listing completes; remaining keystrokes append to the reset `/home/admin` value. Same native-key sequence after listing settles preserves the exact expected path.

`API-07-runtime.json` contains expected/actual, response times and unmodified directory JSON, control, no browser error, ordinary identity, loopback listener and orderly stop. `API-07-typing.png` visibly shows the malformed path. This is not a screenshot-only inference. No path was submitted to change storage; the field itself is the failing user-visible boundary.

## Cause and scope
`internal/dashboard/web/forms.js:25–28` unconditionally assigns `directory-path.value` on every listing render; line38 renders the asynchronous GET result after500ms even while that input is being edited. Native-key timing and actual response trace correlate the overwrite. Existing normal browser coverage waits for initial chooser readiness before interacting; the same settled control here passes. This new chooser belongs to REQ009/AC007 and SCN002 directory selection, not an old app/editor or NFS runtime issue. Main-form manual fallback and settled selection work; those alternatives do not make an enabled chooser field discarding input correct.

Preliminary **Local Fix → implementation**, pending focused failure-origin review. Preserve the user's active path edit across background listing completion while keeping explicit navigation/submission semantics coherent; add a focused regression. No API production edit, temporary diagnostic edit, new architecture or requirement approval is requested. Storage tests that passed remain valid at their exact boundaries.

## Reproduction package
`API-07-chooser.cjs` uses the shared native transport utilities from the API03 harness snapshot and `API-03-pty.py` (transfer it as **driver.py**, not pty.py). Preparation/build/resource details are in `API-03-build.py`, `API-03-resources.json`, `API-03-build.json` and the report. On the owned prepared environment:

```
HOME=$SCRATCH/home TMPDIR=$SCRATCH/tmp node tickets/in-progress/nfs-setup-dashboard/evidence/API-07-chooser.cjs
```

The script currently names this run's owned scratch; if recreating after cleanup, update that harness path/IP/SSH key location only, not production. A cheaper rootless reproduction can use the existing dashboardpreview fixture because directories are ordinary-user real I/O; that alternative has not been executed in this round and is not claimed as proof.

Earlier API03 immediate chooser-fill attempt motivated this probe but is not the basis for the native-key conclusion. Its modal-cleanup and other harness preparation mistakes remain separately preserved in API-03-attempts.md. This finding requires no secret, user's host, field campaign or publication.
