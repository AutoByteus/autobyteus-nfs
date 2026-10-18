# IR-004 attempts
Baseline no-unused exit1 intentionally reproduced CR002; fixed audit and runtime
test exit0 on their first post-fix runs. No preparation or test failure.
The final staged artifact whitespace check returned2 for raw prebuild.log line25
and claude-bootstrapper.log line115 blank EOF. The first exception scanner checked
trailing spaces only, so its assertion failed. Corrected the artifact validator
to recognize blank EOF, retained exact raw log bytes and explicitly excepted
these two logs. No source change or test rerun; final staged check excluding only
these raw logs passes. See artifact-whitespace.json.
