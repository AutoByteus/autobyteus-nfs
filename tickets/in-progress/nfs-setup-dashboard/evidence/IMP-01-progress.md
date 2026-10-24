# IMP-01 — Initial implementation in progress (not a handoff)

2026-10-24, current source2445aab (production5f8cabf); R1/SR001 + SR003 /
ARCH002, Large/High unchanged. Personal execution, no delegation or remote/source
publication. No completed IR verdict yet; remaining owned Mac native work and
cleanup prevent a ready claim.

Completed implementation: one shared admin owner (including the complete serial
supervisor), private same-binary sudo pipe, ordinary-user loopback dashboard,
strict auth/Origin/Host/wire boundaries, exact retained review/consent, explicit
readiness/reconnect/drained detach, embedded role UI and scoped documentation.
No config/setup/backend/Docker/release policy or stored-schema edits.

Executed self-checks (not independent API/E2E acceptance):
- Darwinarm64 Go1.27.2 race all10packages + vet, bothOS/botharch compilation.
- Ubuntu24.04arm64 native race all10packages + vet, Python78collected77executed
  and1expected childskip. A two-test OS-fixture error and unavailable-compiler
  preparation failure are retained, not relabeled. Test-only failure cleanup
  was added after full run; affected native admin rerun recorded separately.
- Mac Python independent archive had1 Git-context error; proper independent
  Git clone rerun is in progress, no release test softened.
- Real Chromium/WebKit embedded rendering: full18 scenarios at first UI snapshot,
  current10 normal/stop scenarios and2 final error scenarios; root/clipboard
  doubles explicitly labeled. Direct image inspection supports feedback notes.
- Actual owned Ubuntu public role → terminal approval → installed same-binary
  helper → HTTP-controlled native server and sequential LinuxDocker server,
  nonroot mounted reads/writes, readiness, reconnect, busy refusal and drained
  detach; source/marker preserved. Real helper identity/lock/pipe/denial proof
  preceded native storage mutations. Docker server remains for Mac client.

Owned resources: /Users/normy/nfs-dashboard-imp-1ed_m7l0 (0700), isolated Tart
HOME/TART_HOME, Ubuntu dashboard-ubuntu at192.168.64.8; source
/home/admin/dashboard-data and Docker mount /Volumes/dashboard-docker currently
retained intentionally. Mac Tahoe base download still active (59% at12:38Z);
not booted and no Mac native server/client proof yet. No host root store,
mounts/exports, host Docker, canonical checkout, PM or app resources touched.
Tart/Go/Playwright and development binaries live only in owned scratch. Current
measured engine copied read-only from retained exact candidate; original remains
untouched. No cleanup-complete, API Pass, TaskDone or release claim.

Check evidence is by IMP ID under this directory. Failed attempt logs and exact
source-copy/compile inputs remain. Current upstream documents are unchanged.
