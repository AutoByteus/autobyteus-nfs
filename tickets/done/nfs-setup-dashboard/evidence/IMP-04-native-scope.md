# IMP-04 — isolated privilege boundary, 2026-10-24

Input1a670d4c plus the phase2 working admin/CLI/IPC implementation. Exact compiled
Linux arm64 binary SHA2560d99fb8015aebca032fe4f5ea959e56727089281332586546798e1c51863a45a;
independent source retained in the owned scratch native-helper-build directory.
Real sudo/private pipes/root installation/global flock ran in the new NAT-only
Ubuntu24.04.5 arm64 guest, NOT on the operator host. The planned client target was
never committed. No mount/export/backend/source changes were performed.

- Attempt1: actual sudo install+helper identity and exact plan/lock/consent/cancel/
  replay controls passed. Copy-over-running-binary harness step failed (exit1;
  stderr not retained, so ETXTBSY is a hypothesis, not measured cause).
- Attempt2: replaced that harness step with the real install boundary and a separately
  built alternate executable. Retained helper refused changed installed identity;
  original installation restored. Next transport case failed in Python with an
  undefined fixture variable after the explicit resume selector skipped its setup.
- Final transport continuation: actual broken output/released review lock,
  forged identity refusal and OS-denied user passed. Private state contains only
  operation.lock, with no attachment/pending storage state. Each original attempt
  and its raw result remains retained; none is relabelled overall Pass.

These complementary native controls permit continuing the design's next browser
phase. They do NOT prove browser mutation/storage effects, interactive password
entry, Mac privilege/transport, Linux amd64, installed service reconciliation,
NFS hosting/client mounts or release qualification. Current Mac26 guest download
is ongoing. Later native feature proof must use the completed current executable.
