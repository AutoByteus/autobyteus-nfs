# IMP-06 — terminal/browser observations and attempts
2026-10-24; source459c02f666e7d988adb87ba1a351f7289d3e8790. Mac26.5.2arm64,
owned real PTY + Chromium156.0.8078.4/Playwright1.64.1. Current Session/HTTP/assets,
ordinary-user helper protocol double. No root/password/OS cache/storage proof.

Final attempt3: six cases, fixture/browser exit0. Both role success transcripts
show waiting → confirmed → preparing → ready/storage disclaimer. Denied-before-
hello remains unconfirmed; inspection refusal retains confirmed but not ready.
PTY Ctrl+C while hello is held and actual-page Stop while inspection is held
both suppress later ready/reminder and finish only after releasing the controlled
child. No source/storage plan was submitted. Screenshot server/client ready
states inspected at1100x900: readable role titles, Not configured notice,
metadata-only explanation, available Stop/Inspect, expected role form and safety
aside, no overlap. No browser visual changes requested or made; mobile/full
layout campaign not repeated. Transcripts contain no private URL/token.

This harness drives New/Session and real HTTP with its own signal/Stop adapter,
NOT Run or the OS browser opener. Existing Run wiring was source-reviewed;
there is no actual sudo/password acceptance, native privilege or field claim.

Attempt1 timed out waiting for the success fixture to drain. The failure console
and original driver/fixture are retained, but its transient terminal capture
was not persisted. Attempt2 added capture and used HTTP.Shutdown rather than
Close (aligning the fixture response drain with Run); it still failed. Its
transcript established known local helper-start failure. Inspection found the
PTY driver explicitly supplied relative argv[0] `dashboard-preview`; the fixture
launches its own os.Args[0], so exec could not find that child on PATH. Attempt3
sets absolute argv[0] and all six cases pass without any product edit. This was
a harness preparation error, not a password/host defect. Failed attempts and
corrected driver are retained separately. All attempt processes were waited,
fixture gate directories and private connection files removed.

## Reproduce without overwriting this evidence
Create a fresh0700 scratch directory with home/tmp/cache and an independent
archive of459c02f. Copy IMP-06-preview.go.txt into that copy's
internal/dashboard/feedback_preview_test.go. Build with
`go test -c -tags=dashboardpreview -o "$R/dashboard-preview" ./internal/dashboard`.
Install Playwright1.64.1 under `$R/browser-tools`, Chromium under `$R/browsers` as
TESTING.md describes. Create an owned new evidence directory and copy the
IMP-06-browser.cjs and IMP-06-pty.py inputs into it. Run
`python3 "$NEW_EVIDENCE/IMP-06-pty.py" "$R" "$NEW_EVIDENCE"`.
The driver creates private fixture directories, actual PTYs and isolated browser
contexts, then drains/removes them. It must not be pointed at these historical
output files. No operator browser/keychain/sudo policy or storage is needed.
