# Evidence context — artifact audit attempt

Case C01/report packaging; local macOS arm64; source585d416c2746cf2963058d591b0753d0db8088f5; 2026-10-18UTC. Step: final report-path checker, not runtime validation.

First inline Python checker incorrectly treated the report's documented `ticket:` prefix as part of a filename. It reached the explicit-reference assertion after source/protected/Delivery/history/JSON/annotation/progress checks, then stopped before producing artifact-checks.json:

```text
Traceback (most recent call last):
  File "<stdin>", line 21, in <module>
AssertionError: ['ticket:postpublication-testing-plan.md', 'ticket:approval-record-sr004.md', 'ticket:implementation-handoff.md']
```

Those files exist under the ticket. Correction: resolve `ticket:` references against T, not E; no report/evidence scope or product changes. The containing shell continued to cleanup and diff checks, hence its aggregate exit0 was not asserted as audit success. Corrected output is artifact-checks.json; completed test cases were not rerun. Original runtime recipe-command error remains independently recorded in attempts.md/local-results.json.

Final authored-text whitespace check initially rejected the three newly added Markdown context headers (attempts.md, skill-update.md, validation-plan.md): their generated first line had one trailing space. Only those added headers were trimmed and annotation offsets adjusted; captured original bodies/hashes are unchanged. Raw hosted-log whitespace remains explicitly excepted in artifact-checks.json.
