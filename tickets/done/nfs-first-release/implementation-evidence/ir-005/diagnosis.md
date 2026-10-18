# DR005 boundary assessment — no credential diagnosis inferred

Original actual run39121007787/attempt1 on main7683494 failed both Mac signing
steps (jobs117656510844/117656510925) after all four native checks passed. In each
retained log lines299–311, the only result is sign-macos.sh exit1. The following
upload warns that no notary receipt exists. See delivery-evidence/dr-005/
failure-assessment.json and those logs; no new hosted observation is claimed here.

Source trace: the original script redirected import/partition/sign/verify to files
inside its private scratch and removed the scratch in EXIT. Other validations may
also fail before notary. Duration alone cannot distinguish import, keychain access,
identity availability, codesign or another boundary. No specific invalid secret,
password mismatch, Apple rejection or actual successful signature is established.

New executable baseline control doubles a failing import with fake private stdout/
stderr. Original script returns its code5 but produces no failure receipt or safe
stage. The new shell retains only fixed stage/exit/cleanup data outside scratch;
actual cause remains for a fresh authorized hosted execution. No credentials were
read locally, exported, changed or requested. No Apple/keychain commands were run
against live state; command doubles exercised the real shell.

Related concrete cleanup defect found locally: the strict keychain-list pipeline
could fail after its Python consumer wrote an empty JSON list; original EXIT would
restore that incomplete result. Use pending capture and promote it only when the
pipeline succeeds, so cleanup cannot apply a failed snapshot. The new fixture and
mutation explicitly detect restoring on a failed read. This is not alleged as the
cause of DR005; it preserves the existing cleanup contract on a real command error.

The implementation does not hide failures: normal strict-mode invocation is not
inside an if/|| predicate, notary command nonzero stays nonzero even with Accepted
JSON, rejection/pending cannot pass, and cleanup failure refuses the job while
preserving an earlier command's exit/stage. Both Mac targets and final payload/
publication gates are unchanged. Only the two sanitized receipt globs upload;
private logs/certificate/keychain never do.

Production signing/workflow bytes changed: current readiness/source evidence is
stale by design. Existing stable readiness data and measured engine are not edited
or fabricated. Source review then affected API/new complete candidate and Delivery's
current readiness/actual signing continuation are required. Source main's previous
finalization is preserved, not replayed. Field/user testing stays deferred; it is
not this blocker. Actual signing/root-cause resolution and release completion are
still outstanding, not hidden by local green fixtures.
