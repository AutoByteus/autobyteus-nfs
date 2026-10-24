# IMP-02 phase attempts
2026-10-24, input1a670d4c plus current admin/IPC delta, Darwin arm64 Go1.27.2.

- Initial independent archive `phase1`: existing seven package race checks passed; newly added admin/wire had no tests yet. This is not a completed phase acceptance.
- `phase2-focused`: adminwire/cli passed; actual broken-stdout child test failed with SIGPIPE after helper return. Inspection established the test harness writes PASS after the child test's deferred signal.Stop restores default behavior; helper has already returned/drained. Correct only harness: close child's fd1 after drain receipt so unrelated test-runner PASS cannot hit the deliberately broken pipe. Keep real pipe/drain assertions, no product SIGPIPE weakening. Rerun only affected admin suite; no claim yet for native root helper.
- Read-path mistakes: initial guessed setup/configuration.go and hosted_config.go were absent; actual CheckConfiguration is setup/apply.go. No source change from those lookup failures.
