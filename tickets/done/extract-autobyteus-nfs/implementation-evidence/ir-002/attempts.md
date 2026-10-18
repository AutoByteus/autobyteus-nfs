# IR-002 attempts
The first optional transpile-equivalence audit failed before comparison because
its relative fileName was outside the production config's absolute rootDir
(TS6059). The same failure was repeated once to persist raw stderr; a diagnostic
probe also reproduced TS6059. Both sources were unchanged. Corrected the audit's
fileName to the actual absolute S source path, not compiler policy or production
code. attempt-1 retains the initial script, stderr and diagnostic. This was a
harness error, not a product/test pass. The separate production typecheck uses
the documented package script in an owned current-source copy.

The initial production typecheck's pretypecheck build failed (exit2): the narrow
server dependency install did not install the backend SDK's own node_modules.
That SDK is a script-only build prerequisite, not in the server dependency
closure. Missing SDK imports/Node types are setup errors. attempt-2 retains the
runner and logs; added the exact backend SDK dependency closure to the frozen
install and reran the same production typecheck without source/config changes.
