# IMP-07 check preparation attempts

Linux guest attempt1: checksum-verified Go1.27.2 extracted successfully. The
owned Ubuntu base image has no C compiler; `cc --version` failed and Go refused
`-race` because cgo was unavailable. No product test executed in that attempt,
and race was NOT silently dropped. Original console/race logs retained.
Provisioning build-essential in the owned guest, plus docker.io for the already
approved isolated Linux Docker-storage interaction. No operator-host package,
Docker daemon, socket, mount or firewall is changed. Native NFS server retained.

## Actual Linux drain-fixture failure and Mac packaging harness correction

The first executable Linux race run (after installing the missing compiler in
our owned Ubuntu guest) failed two new admin drain fixtures: the broken-fd1 child
never reached `Runner`, and the service-stop fixture waited for that same seam.
`platform.Mounts` reads `/proc/self/mountinfo` directly on Linux, unlike Darwin's
command observation. The fake unmounted attachment failed before Runner. These
are test-harness assumptions, not evidence of a production drain failure. Both
fixtures now pause shared admission under the actual operation flock; this
covers the same helper/service worker-drain lifecycle on both OSes without
pretending a fake mount exists. Production mount/state/identity policy is unchanged.
Original guest failure/timeout is retained in IMP-07-linux-poll2.log.

The Mac all-Python run executed78 tests:76passed,1expectedchildskip,1error.
The missing-readiness test invokes source_context.current(), which requires Git;
our independent archive deliberately had no .git. This harness is inappropriate
for that release-identity check (TESTING.md explicitly calls for an independent
Git clone there). Retain IMP-07-mac-python.log and failed checks.json; rerun in
an independent shallow local Git clone, not by weakening the validator/test.
Mac vet and all four target builds in that run passed; builds are compilation only.
