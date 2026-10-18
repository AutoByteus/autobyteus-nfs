# IR005 / DR002 hosted Linux boundary correction

Current N56c0c59 (published22e934b); archived ticket remains canonical.
Paired N/S target pushes are complete, not to be replayed. S has no new impact;
its worktree stays retired. Authority R2/SR003/SR004/ARCH002, Large/High unchanged.

## Investigation and impact
hosted_config_test.go assumed Runner observes mounts on both OSes. Darwin invokes
mount through Runner; Linux reads /proc/self/mountinfo directly. An absent default
mount lets detach advance: native root-owned package-mask Store correctly rejects
the nonroot fixture, while the intentionally unusable Docker client panics.
No production defect established. Preserve those trust checks and runtime paths.

Correct only fixture boundary/expectations: on Linux use an already-present
unrelated /proc mount and verify its identity read-only, so Unmount refuses before
job/package/engine effects. Darwin retains its injected mount-error boundary.
Keep malformed/config-mismatch refusal and current/missing retry cases meaningful;
assert records/config remain unchanged. No mount/proc writes, privileged tests,
live storage daemon or product dependency injection for tests.

## Planned evidence
- Reproduce hosted failures from independent baseline source on native Linux,
  nonroot Ubuntu24.04 disposable development container, Go1.27.2 + C compiler.
- Run affected setup tests then full Go race/vet/build/version and service Python
  fixtures on corrected native Linux; distinguish Docker-host installer skip.
- Repeat affected/full Go race/vet on native Darwin arm64 independent copy;
  unchanged service semantics, packaging source hash and expected publish refusal.
- Mutation controls in disposable copies: omitted status/detach config preflight,
  missing-config detach rejection. Each must fail focused assertions.
- Preserve hosted failure logs. Local Linux arm64 success is NOT hosted Ubuntu
  amd64 matrix completion; Delivery owns the new hosted run/terminal receipt.
No fresh S suite, engine build/qualification, old VM/editor/provider campaign,
target push or release. Prior current S API002 evidence carries with limits.
