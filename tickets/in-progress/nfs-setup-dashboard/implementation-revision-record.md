# Implementation Revision Record

## Revision Index

| Revision ID | Triggering Role / Report / Round | Finding IDs | Classification | Related Revision IDs | Result |
|---|---|---|---|---|---|
| IR-001 | Architecture Reviewer / design-review-report.md / ARCH-REV-002 | N/A; upstream ARCH-F001 resolved by SR003 | Initial Baseline | SR001–003; ARCH-REV-001–002; CRR/API/DR N/A | Ready for independent source review; implementation checks only |

## IR-001 — Shared administrative owner and embedded local setup dashboard

- Date: 2026-10-24. Prior authoritative implementation result: **N/A**. This is the
  first implementation baseline, not an inferred earlier Pass.
- R1/SR001 Approved, SR003 design, ARCH-REV-002 Pass. Task size **Large**, risk
  **High**, confirmed. No new design impact or approval change.
- Trigger: Architecture Reviewer handoff at1a670d4c over source base52c17fb5.
  ARCH-F001 was an upstream design omission; implementation follows the corrected
  complete DS6 supervisor sequence. No source-review/API/delivery rounds yet.
- Actual delta: `internal/admin` owns admission/global lock/Docker scope, retained
  exact plans and complete serial supervision; `adminwire` owns strict private
  transport; CLI preserves terminal/service entry forms and supplies fixed sudo
  bootstrap. `dashboard` adds nonroot local HTTP/session/process/chooser/embedded
  UI. Removed old service.Supervise/CLI callback and duplicate scope ownership.
  Setup/config/backend/Docker/source identity/installer/release policy unchanged.
- BEH-001–007, REQ-001–010, AC-001–008 implementation surfaces covered; acceptance
  judgments and source finalization remain downstream. No persisted schema change,
  compatibility fallback, app/node/Guide coupling or live-user storage mutation.
- Commits:502205f initial source;5f8cabf8ee31318a38aa9c0ed94e9c6960b9c409 final
  production;2445aabf61126b1bb64b05b5f925b140c67917b8 test-only portability/cleanup.
  Subsequent commits contain own docs/evidence, not product changes.
- Checks: native Mac/Linux race10packages/vet; Python78 collected77 executed plus
  expected1Gochildskip each; four-target compile; real Chromium/WebKit feedback;
  real isolated sudo/pipe/flock/identity; owned Ubuntu native/Docker and Mac native
  server/client mounted nonroot RW/status/reconnect/drained detach; same-service
  remount on bothOS; preserved CLI controls. Exact snapshots, failed attempts and
  limits are in `implementation-handoff.md` and IMP01–15 evidence, not relabeled.
- Source/marker/sentinels preserved by detach, then test-only VMs and owned scratch
  safely removed (IMP14). Original retained engine/candidates, canonical/PM/app
  resources untouched. No monitor, release/signing/push/target merge/TaskDone claim.
- Next route: independent Code Review under fresh Large/High completed rule;
  then API/E2E owns executable acceptance. Not a second design review/field campaign.
- Remaining limits: virtualarm64 only; amd64 compile-only; browser preview uses root
  and clipboard doubles; native controls use real HTTP/TTY but not visible guest
  browser clicks or password entry. Earlier nativeLinux source attribution is
  explicit. Physical/field/user qualification remains separate. No new follow-up.
