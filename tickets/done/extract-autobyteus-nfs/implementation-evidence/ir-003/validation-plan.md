# IR-003 integration impact plan (before checks)

Last passed source: S a2023feff3d498fb6c51cebf1c93360da3679a45
(IR002/CRR002, API-REV-001, CRR003 no test delta).
N service83726b27400b405a7a6a79bd962d8e2419daa561 remains byte-unchanged.
Current S 8c5c76a743760104119b08fc83ab74cd263f11f1 merges personal2f211340 and removes obsolete
Brief fixture guard callbacks. integrated-changed-paths.txt is the complete
old-validated→merged path diff; overlap.json names the five overlapping files.

Current TESTING.md requires impact-based reruns and invalidates S's previously
recorded checks when core/contracts/fixtures change. Those foundations changed
in personal (including own-run memory and input-preface/lifecycle observation).
Thus no previous S execution is counted as integrated-current proof.

| Prior case (API001 ledger) | Disposition | Reason / current responsibility |
| --- | --- | --- |
| E01 source/license/removal | Rerun focused source audit | N unchanged; S boundary after merge must be confirmed |
| N01 Go host/state | Still valid | Independent N production/tests/tool inputs unchanged |
| N02 Python/hash/workflow | Still valid | Independent N production/tests/tool inputs unchanged |
| N03 builds/engine | Still valid, with existing compile-only limits | No N source/engine change; no new qualification |
| S01 build/typecheck | Rerun here | Current contracts/core shared foundation and AgentRunManager merge |
| S02 narrow private profile/path | Rerun here inside broad unit command | Exact ownership and ordinary workspace behavior must survive |
| S03 backend/path unit regression | Rerun here | Prompt/fixtures/core/runtime merge; restore11 tracked replay inputs upfront |
| S04 local composed API | Rerun downstream API owner | Shared foundation invalidates old integrated claim; independent API execution outside this implementation role |
| S05 native run/memory/PTY E2E | Rerun downstream API owner | Own-run memory/core change; not treated as carried current Pass |
| S06 launcher/Guide | Rerun local tests/guards here | Shared-foundation policy; no live Docker or UI campaign |
| E02 cleanup | Rerun for owned resources here | Fresh scratch only, source/protected state unchanged |

Add narrow integration checks for all overlapping tests, plus upstream notice
publish/input lifecycle and memory-placement unit tests. Read before choosing:
Codex bootstrapper has no lease-manager dependency after R2; the latest prompt
uses literal current guidance, not removed WORK_REQUEST constant. Both conflict
imports are unused. Preserve all current prompt assertions and R2 constructor/
guard/private-profile behavior. CodexThreadManager still really uses its lease
fixture; do not remove that distinct import.

AgentRunManager auto-merge retains upstream optional inputPreface/lifecycle
observer and onPublished callback alongside direct R2 backend preparation and
exact release. Brief keeps configured teamKind/current prompt assertions;
remove only two obsolete no-op ownSkill/ownCodexClient guard callbacks.
Claude and Codex manager auto-merges preserve their current dependency shapes.
No production edit beyond incorporating upstream; no schema/design change.

Implementation scoped execution only: owned current-source copy, clean
HOME/TMPDIR, frozen whole-workspace install, documented prerequisite build,
production typecheck; current focused/broader units and narrow integration,
Guide/localization/boundary guards and launcher fixtures. Provider gates remain
off. Do not execute standalone host create/connect or old VM/editor campaigns.
The API-owned ledger/report remains unchanged; the two rerun obligations above
are passed onward, not waived by this local report.

Docs-sync observation for Delivery (not runtime fix): S RELEASE.md's NFS tail
still describes R1 launcher/descriptor consumers and a pin, contradicting R2.
Delivery has not yet run its docs sync; retain that item for its current scope.
No new requirements loop or separate Task implied.

## Final fixture-only cleanup after integrated checks
The merged Codex bootstrapper fixture still declared requestImplementation and
21 callers supplied unused async responses, although R2 no longer acquires a
client in bootstrap. Removed this dead test input and only its callers; no
assertion/production/shared fixture changed. Final source 5559abbf017566f0030d95b023614f7418d3f212.
All checks at8c5c76 remain valid for unchanged production/dependencies; rerun the
affected Codex test and other overlap controls at this final commit. Broad unit
counts are not inflated by adding this repeated subset. No second full campaign.
