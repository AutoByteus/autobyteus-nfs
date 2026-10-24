# IMP-13 — Preserved CLI forms, owned guests only

2026-10-24; current production5f8cabf / sourceHash324bf4db…8cf13;
Darwinarm64 binary86bff169…e8e1, Linuxarm64 binary00351676…22e1.
Exact builds are in IMP-06-current-native-build.json. Driver is
IMP-13-native-cli.py; commands and stdout/stderr are in each result/console log.
No production change was made for these implementation-scoped checks.

- Attempt1: create safely refused because the prior successful UI detach expressly
  retained OS-owned Apple nfsd, still listening on2049. No new setup applied.
  The orchestration shell lacked `set -e` and incorrectly continued two dependent
  checks: missing connection file on Linux, missing new peer sentinel on Mac.
  They failed before effects and remain failed in IMP-13-attempt1/. Corrected the
  harness exit propagation/host `set -e`. In this test-owned guest only, confirmed
  no active exports then explicitly disabled/stopped the daemon enabled by this
  fixture. This is fixture preparation, not changed detach policy or port bypass.
- Attempt2: actual CLI `create --yes --json` succeeded and preserved source marker
  and sentinel bytes; immediate root/no-SUDO status correctly refused while the
  newly installed service held the administrative lock. The overall attempt stays
  Fail in IMP-13-attempt2/. Did not repeat create or alter state. The continuation
  observes that same configured storage. Harness allows at most five explicit
  retries only for the exact no-admission lock refusal, retaining each result.
- Attempt3: root/no-SUDO status passed. The no-args PTY harness failed to answer
  the initial ordinary-user administrator consent before waiting for the later
  configured-state menu. Failed result remains in IMP-13-attempt3/. Child was
  still ordinary/unprivileged; PTY close ended it (final process inventory proves
  no survivor). Corrected the harness to answer `yes`, then select default status.
- Final Mac observation: root/no-SUDO status and actual no-args terminal
  administrator consent→configured status both passed, exit0.
- Final Linux: public connect/current binary→Mac source, nonroot read/write/fsync,
  status, reconnect and drained detach passed. Final Mac: peer bytes visible,
  public reconnect, direct root/no-SUDO drained detach passed; source/marker/bytes
  preserved. No runtime failure or requirement/design deviation established.

These checks do not replace the native dashboard controls (IMP06/09–12), claim
physical qualification, or sign off API/E2E. No raw private browser token or real
credential is needed for CLI checks. Final owned cleanup is IMP14.
