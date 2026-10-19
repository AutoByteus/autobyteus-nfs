# IMP-06-16 — Local attempts and limits

- Step/command: independent-copy `FOCUSED_ONLY=1 python3 evidence/IMP-06-run-checks.py`.
- Initial commit: b279d556e2c0f5e90ca24b61c7e67bc809644947 plus uncommitted IR006 edits, not clean b279 source.
- Environment/date: Darwin arm64, Python3.9.6, Bash3.2; private HOME/TMP and command doubles; 2026-10-19.

Attempt1 ran21 tests, exit1 with46 assertion/subtest failures. New fixture parameter
`diagnostic` was accidentally overwritten with the observed JSON dictionary before
constructing the expected record. It compared a string field with that dictionary.
The fixture variable was renamed `record`; no product change was needed for this
failure. The attempt used a frozen independent copy, so correcting the worktree
during that run did not alter its executed inputs. Raw logs/result/cleanup are
preserved in implementation-evidence/ir-006/attempt-1/. They are failure evidence,
not the final current checks. Their header HEAD identifies the base; this note
makes the uncommitted test/source delta explicit.

No real codesign/private keychain/Apple calls occurred. All command boundaries were
fake scripts. Source/signature/field qualification is not conferred by these tests.
Final committed-source checks and their IDs are separate. Unknown actual hosted
codesign cause remains a limitation regardless of fixture outcomes.

Attempt2's same production tree, corrected fixture and independent private copy
passed21 focused tests (`IMP-06-01-focused.log`). Base HEAD was still b279d55 when
copied; those exact product/test bytes were then committed as2c12ec6 without a
further product/test change. The final full suite and mutation/source checks run
from committed2c12ec6. Attempt2 results/cleanup are retained separately; no outcome
is silently overwritten. Focused tests are not redundantly rerun outside the full
suite (`SKIP_FOCUSED=1` for the final runner).

Excerpt from attempt1 raw log (lines32–33; full path above):

```text
    self.assertEqual(diagnostic, {'schema':1, 'status':'Failed', 'stage':stage,
AssertionError: {'sch[104 chars]ic': 'not-collected'} != {'sch[104 chars]ic': {'schema': 1, 'status': 'Failed', 'stage'[85 chars]ed'}}
```

Final line: `FAILED (failures=46)`. This is the overwritten expected-record
variable, not a codesign or hosted failure. Corrected final current checks are
separate from this preserved attempt.
