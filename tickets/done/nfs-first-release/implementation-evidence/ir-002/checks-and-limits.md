# IR-002 — bounded Mac candidate shell correction

Authority: CRR002 Fail / CR-001 = API R03-F001, R2/SR002 Approved, SR003 Ready,
ARCH001; Large/High confirmed. Input ca048be893516d79bc1ea895b929af17580e25dd.
Source correction **8436d0cf6048cd3b4cadbf28815e3d9f82ba6b34**.

## Delta and supported boundary

SCN001/BEH001/REQ001–002/AC001 reaches native candidate metadata under the actual
Mac `/bin/bash` with nounset. Instead of expanding an empty optional array, build
one nonempty array containing the always-required metadata arguments, append only
`--qualified --candidate work/candidate` for fresh, then pass the quoted array.
No `set +u`, ignored status, dropped target, shell-version branch or second command
implementation. Native checks and all downstream qualification/signing gates stay.
Only production delta is that native run-block construction; the prepare job's
separate Ubuntu-only invocation is unchanged. Tests/docs are the other two files.

## Executable regression and current checks

The durable workflow suite extracts the actual native run prefix through metadata,
including strict mode and OCI JSON pipeline, and runs `/bin/bash -e -c` locally.
Only release.py OCI/metadata calls are inert; the shell and JSON pipeline actually
execute. Exact candidate/fresh argv is asserted for four TARGET environment values.
Those values are **not four native CPU executions**. Metadata failure17 must stop;
missing TARGET must refuse; valid OCI output with exit23 must still fail pipefail.

- `baseline-regression.log`: new tests against unchanged original workflow exit1,
  seven tests/five assertion failures. Four candidate TARGET cases abort before
  metadata entry; candidate failure-control also never enters. Fresh controls pass.
  This deliberately failing baseline is regression sensitivity, not product Pass.
- `fixed-regression.log`: same executable tests on correction, seven tests pass.
- `python-all.log`: fresh independent119-input copy/private HOME/TMP, Python3.9.6,
  **41 collected /40 executed /1 Go-child-only skip**, exit0. No Go-child rerun in
  this scoped round; prior IR001/API001 native evidence retains its exact limits.
- `shell-version.log`: local actual system GNU Bash3.2.57, arm64-apple-darwin25.
  Hosted logs identify /bin/bash but do not print its version; none inferred here.
- actionlint1.7.11, extracted-prefix Bash syntax and shellcheck pass. Workflow
  job-mode/permissions/cancellation controls remain green. No entire Actions runner
  or metadata/native Go build is exercised by the new shell fixture.
- Default `--check-publish` exits1 (expected empty qualification); current unqualified
  production hash is **26af7e5bcab00ae22d4bdebe1820c6d38b0dc51a44f1b834036334ea79528298**.
- Three deliberate independent-copy mutations (omit fresh qualification arguments,
  remove nounset, remove pipefail) each fail assertions, no test errors. Raw logs
  and commands in checks-result.json. Original empty-array baseline is separate.
- final-checks.json/source-inputs.json: exact independent source; only workflow,
  its test and TESTING.md changed; other116 non-ticket inputs unchanged. No unused
  imports in touched test; workflow359nonempty lines, five-line bounded delta.

No unexpected failing check or harness retry in this round. Baseline/mutations are
expected failures; all current local checks pass. run-checks.py's unused `os` import
was removed after execution; this has no command/test/source impact.

## Preservation, cleanup and required next proof

Eight preexisting Delivery-owned untracked files were hashed before work and
verified unchanged. Only this round's explicit source/artifact paths staged;
Delivery records stay untracked. IR001/history and upstream API/reviewer evidence
preserved; append-only IR002 does not change old verdicts. Own independent source,
private HOME/TMP and test temporary directories removed; no container/VM/mount,
credential/keychain, hosted dispatch, remote/tag/release/registry effect created.

Go/runtime, engine recipes/pins, qualification, signing, publisher and installer
source are unchanged; no broad campaign or credential provisioning warranted by
this fix. Local result does not close API R03 or reclassify CRR002/API001.
The workflow is production-hashed: API must use a **new reviewed current-source
hosted candidate** with both Mac jobs and full aggregation. Failed run39111348848
and its seven partial artifacts remain failure evidence, never hand-assembled or
relabeled as the new candidate. Physical resource assignment/user verification,
real P12/password/team/Accepted-notary, final payload/publication/downloads and
Delivery current-main gates remain open. No TaskDone/Terminal/release claim.
