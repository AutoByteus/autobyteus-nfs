from pathlib import Path
import json,subprocess,hashlib
E=Path(__file__).resolve().parent; T=E.parent.parent; N=T.parent.parent.parent
S=Path('/Users/normy/autobyteus_org/autobyteus-worktrees/extract-autobyteus-nfs')
head=subprocess.check_output(['git','-C',str(S),'rev-parse','HEAD'],text=True).strip()
assert head=='60b67dabecaf5569a8e26128dbdb26117c988811'
assert json.loads((E/'unused-locals.json').read_text())['diagnostics']==[]
assert all(x['exit']==0 for x in json.loads((E/'checks-result.json').read_text()))
assert json.loads((E/'cleanup.json').read_text())['scratch_removed']
(E/'checks-and-limits.md').write_text("""# IR-004 — CR-002 bounded cleanup

Input N5c2c95895422a9f51857546e3bd38fa98a51e591; service83726b unchanged.
S5559abbf →60b67dabecaf5569a8e26128dbdb26117c988811.
Approved R2/SR003, SR004/ARCH002, Large/High unchanged.

Removed exactly one unused local Skill import in the Claude bootstrapper test.
The domain class, configured-skill types, all fixtures and every assertion are
unchanged: the complete file equals predecessor bytes minus that single line.
No production file, dependency, schema, runtime API or approved behavior changed.

## Fresh implementation-scoped checks
- Before fix: same TS5.9.3 unused audit (25 R2 production +4 overlap tests),
  expected exit1 / sole6133 for Skill. This confirms the review finding, not a
  new runtime defect or failed harness attempt.
- After fix: audit exit0, zero6133/6192/6196 diagnostics. noResolve/noEmit unused
  analysis is not full semantic typecheck.
- Fresh current-source copy, clean HOME/TMPDIR, frozen filtered server+backend-SDK
  prerequisite install and documented server prebuild: exit0. Shared builds and
  Prisma generation are setup, not application acceptance.
- Documented vitest run of the affected ClaudeSessionBootstrapper file:
  exit0, **1 file /1 test Pass /0 skips**, preserving team approval state and
  current collaboration prompt assertions. No credentials/live provider required.
- All7307 copied inputs remain identical to current tracked source; exact delta,
  production/N input preservation and source whitespace checks pass.
- No failed preparation/test attempts in this round. Package manager's existing
  ignored @google/genai build-script warning and Prisma's update notice are raw
  setup output, not a reason to upgrade dependencies.

## Impact and limits
validation-plan.md precedes execution. Test-only import deletion means IR003
remaining local suites/typecheck carry with their original exact-input limits;
the1666-test campaign was not repeated. Current S integrated API validation,
especially S04 composed APIs/S05 native run-memory-PTY, remains API-owned after
source review. API001 S evidence is historical pre-integration, not a fresh Pass.
Unchanged N01–03 and service source83726b retain original evidence/limits.
CRR004 Fail remains the independent verdict until targeted re-review; implementation
does not assign reviewer/API success. Frontend loop N/A: no visual/interaction delta.

Owned scratch/home/temp removed after no matching command/cwd was observed.
No live app, VM, Docker node, mount, provider or protected D0/retained-engine action.
No target fetch/finalization/push/tag/release/deploy/TaskDone/user verification.
Delivery must refresh targets and sync the already-recorded stale S RELEASE.md
R1 tail; AC007 remains pending. No reopened editor/filesystem/provider campaign.
""")
p=T/'implementation-handoff.md';s=p.read_text()
s=s.replace('**IR-003 — DR-001 latest-base integration Local Fix complete; Ready for targeted independent source review.**','**IR-004 — CR-002 one-import Local Fix complete; Ready for targeted independent source re-review.**',1)
s=s.replace('Current source/tests **5559abbf017566f0030d95b023614f7418d3f212**.','Current source/tests **'+head+'** (one test-only import deletion atop5559abbf017566f0030d95b023614f7418d3f212).',1)
s=s.replace('current integration evidence is implementation-evidence/ir-003 (**E3**).','integration evidence is implementation-evidence/ir-003 (**E3**); current bounded-fix evidence is implementation-evidence/ir-004 (**E4**).',1)
s=s.replace('then appends IR003.','then IR003/IR004; prior entries are preserved.',1)
old='Current trigger: **DR-001 Blocked / implementation-owned Local Fix**, delivery-revision-record.md, handoff-summary.md and delivery-evidence/dr-001/integration-state.json. N intake checkpoint27db7441523e7b9c1a2ee3263ae83f857ef30d80 preserved review receipt6afc792. **CRR-002 source Pass100%, API-REV-001 Pass95%, CRR-003 successful-test Not Applicable** remain upstream results for their exact inputs, not failures or integrated-current verdicts. CR001 was resolved in IR002; no new numbered reviewer finding. The integrated candidate requires current review/affected validation. Older filesystem/editor Tasks and their verdicts are not inherited or reopened.'
new='Current trigger: **CRR-004 Fail99.8% / implementation-owned Local Fix, CR-002 only**, code-review-report.md and code-review-revision-record.md. Reviewer artifact95dd311879067672fd7572b7d042aa60bcfed1e4 / receipt5c2c95895422a9f51857546e3bd38fa98a51e591. Full R2 integration re-audit found only one unused local Skill import in the touched Claude test; no runtime/design defect established. IR004 requests targeted re-review, not a new full audit. DR001 integration recovery is preserved in IR003. **CRR002 source Pass100%, API-REV-001 Pass95%, CRR003 successful-test Not Applicable** remain historical exact-input results, not integrated-current verdicts. Current independent source verdict remains CRR004 Fail until reviewer action. CR001 resolved in IR002; no old filesystem/editor Task reopened.'
assert old in s;s=s.replace(old,new,1)
section="""## IR-004 current bounded cleanup and checks
- CR002: removed only the unused local Skill import from S/autobyteus-server-ts/tests/unit/agent-execution/backends/claude/backend/claude-session-bootstrapper.test.ts. The actual domain class/configured-skill types, fixtures and every assertion remain. Entire-file byte comparison equals predecessor minus the single import; no production/shared input changed.
- Same29-file TypeScript5.9.3 unused audit reproduces sole6133 before the fix, then exits0 with no diagnostics. It is noResolve/noEmit unused analysis, not a semantic typecheck.
- Fresh current-source owned copy, frozen server+backend-SDK prerequisite installation and documented prebuild pass. Affected Claude test **1 file /1 test Pass /0 skips**, with current collaboration-prompt/approval assertions. All7307 copied inputs hash-match current source.
- E4/validation-plan.md records impact before execution. IR003 other local checks/production typecheck remain valid within recorded scope; no1666-test repeat. API-owned integrated S04/S05 remain downstream. N source83726b unchanged; prior N proof carries with original limits.
- No new failed preparation or test attempt; pre-fix audit exit1 is the expected confirmed finding. E4/checks-and-limits.md, checks-result.json, unused-locals.json, delta-audit.json and cleanup.json are fresh evidence.
- Large/High confirmed, no Design Impact/Requirement Gap; frontend loop Not Applicable for test-import-only cleanup. No rendered behavior, live provider, storage, mount, VM or editor campaign.
- Exact owned scratch/home/temp removed after process/cwd checks; worktrees/retained assets/D0 untouched except the declared source/evidence edits. No target actions or completion claims. AC007 and stale S RELEASE.md R1 prose remain Delivery-owned.

"""
s=s.replace('## IR-003 current integration and checks',section+'## IR-003 historical integration and checks',1)
s=s.replace('**not newly executed in IR003**','**not newly executed in IR003/IR004**',1)
s=s.replace('Darwin arm64; IR003 Node22.21.1/pnpm10.28.2/TypeScript5.9.3 in E3/toolchain.json;','Darwin arm64; current IR004 Node22.21.1/pnpm10.28.2/TypeScript5.9.3 in E4/toolchain.json; IR003 versions in E3/toolchain.json;',1)
s=s.replace('E3/cleanup.json for this round','E4/cleanup.json for this round, E3/cleanup.json for integration',1)
s=s.replace('1. Targeted source review of DR001 integration recovery: all five overlap paths, current prompt/fixture shapes, upstream lifecycle/memory interaction and E3 results. R2/ARCH002 unchanged; no duplicate full architecture review.','1. Targeted source re-review of CR002: one unused test import removed, E4 same29-file unused audit and affected Claude test green. CRR004 already audited the integrated R2 boundaries; no reason to repeat the full source/1666-test campaign solely for this cleanup. R2/ARCH002 unchanged.',1)
p.write_text(s)
history=T/'implementation-revision-record.md'
assert history.read_bytes()==(E/'prior-implementation-revision-record.md').read_bytes()
with history.open('a') as f:f.write("""
## IR-004 — CR-002 touched-test unused import cleanup
- Trigger: code_reviewer, code-review-report.md / code-review-revision-record.md, CRR-004 Full Re-Audit Fail99.8%, sole finding CR-002. Prior implementation result IR003 integrated recovery Ready; independent reviewer found mandatory cleanup only, not a runtime/design defect.
- Current result: one-import cleanup and focused implementation checks complete; Ready for targeted source re-review. No reviewer/API verdict assigned.
- Related revisions: Approved R2/SR003, Ready SR004, ARCH-REV-002 unchanged; CRR004 current, CRR002/003 historical; API-REV-001 exact-input historical, DR001 pending delivery integration/completion. No new approval.
- Reason: mandatory Core7 cleanup in the already-touched Claude bootstrapper test. Preexisting binding provenance/reviewer gap stays in CRR004; historical verdicts are not rewritten.
- Behaviors/requirements: BEH006 / REQ010 / AC010 preserved; no intended behavior change. BEH004/AC007 remains Delivery-owned.
- Delta: delete only local Skill import from S/autobyteus-server-ts/tests/unit/agent-execution/backends/claude/backend/claude-session-bootstrapper.test.ts. Exact1deletion; complete file equals prior minus this import, preserving every fixture/assertion and real domain/configured-skill types. No production/shared input changes.
- Identities: S60b67dabecaf5569a8e26128dbdb26117c988811 atop5559abbf017566f0030d95b023614f7418d3f212. N intake5c2c95895422a9f51857546e3bd38fa98a51e591, service83726b27400b405a7a6a79bd962d8e2419daa561 unchanged.
- Validation: same TS5.9.3 unused audit25 production+4 overlap tests reproduces sole6133 before fix and zero after. Fresh owned current-source copy/frozen filtered prerequisites/prebuild exit0; affected Claude bootstrapper1file/1test Pass,0skips;7307 copied inputs unchanged. The unused audit is not semantic typecheck. IR003 production typecheck/remaining local checks and unchanged N evidence carry with attribution, not rerun. No1666-test repeat.
- Classification: Large/High retained; no Design Impact/Requirement Gap. Frontend loop N/A for test import cleanup.
- Cleanup: exact owned source/home/temp removed after no matching process/cwd observed. No live app/storage/VM/container/provider resources, retained-engine/D0/PM changes or failed setup/test attempts. Baseline audit exit1 is the expected confirmed finding.
- Limits/next: targeted source re-review then current affected API validation, especially S04/S05. API001 pre-integration S pass is not current acceptance. Delivery owns fresh refs/docs sync (existing stale S RELEASE.md R1 tail), ordered N→S finalization and AC007. No target merge/push/tag/release/deploy/TaskDone/user verification.
- Evidence: implementation-evidence/ir-004 (E4), validation-plan.md, unused-before.json, unused-locals.json, checks-result.json, checks-and-limits.md, delta-audit.json, input-integrity.json, cleanup.json. Apply fresh configured route once; no duplicate dispatch.
""")
input_audit=json.loads((E/'input-audit.json').read_text())
unchanged=[x['path'] for x in input_audit['ticket_inputs'] if x['path'] not in ['implementation-handoff.md','implementation-revision-record.md']]
for rel in unchanged:
 expected=next(x['sha256'] for x in input_audit['ticket_inputs'] if x['path']==rel)
 assert hashlib.sha256((T/rel).read_bytes()).hexdigest()==expected,rel
assert history.read_bytes().startswith((E/'prior-implementation-revision-record.md').read_bytes())
(E/'final-checks.json').write_text(json.dumps(dict(revision='IR-004',finding='CR-002',result='Ready for targeted source re-review',S_head=head,N_service_unchanged=True,history_byte_prefix_preserved=True,unchanged_upstream_ticket_inputs=unchanged,unused_diagnostics=0,affected_test_files=1,affected_tests_passed=1,affected_tests_skipped=0,copied_input_count=7307,scratch_removed=True,classification='Large/High',remaining_API='Integrated S04/S05 and current affected S validation remain downstream; unchanged N evidence carries with limits',AC007='Delivery pending',no_target_or_release_actions=True),indent=2)+'\n')
print('IR004 handoff/history persisted; prior history prefix and upstream inputs preserved.')
