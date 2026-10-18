from pathlib import Path
import hashlib,json,subprocess
E=Path(__file__).resolve().parent; T=E.parent.parent; N=T.parent.parent.parent
S=Path('/Users/normy/autobyteus_org/autobyteus-worktrees/extract-autobyteus-nfs')
def git(root,*args):return subprocess.check_output(['git','-C',str(root),*args])
prior='5559abbf017566f0030d95b023614f7418d3f212'
p='autobyteus-server-ts/tests/unit/agent-execution/backends/claude/backend/claude-session-bootstrapper.test.ts'
removed=b'import { Skill } from "../../../../../../src/skills/domain/models.js";\n'
before=git(S,'show',prior+':'+p); after=(S/p).read_bytes()
assert before.count(removed)==1
assert before.replace(removed,b'')==after
changed=git(S,'diff','--name-only',prior,'HEAD').decode().splitlines()
assert changed==[p],changed
assert not git(S,'status','--porcelain')
assert not git(N,'diff','--name-only','83726b27400b405a7a6a79bd962d8e2419daa561','HEAD','--','.',':(exclude)tickets')
domain='autobyteus-server-ts/src/skills/domain/models.ts'
assert git(S,'show',prior+':'+domain)==(S/domain).read_bytes()
out=dict(S_head=git(S,'rev-parse','HEAD').decode().strip(),S_prior=prior,N_head_before_handoff=git(N,'rev-parse','HEAD').decode().strip(),N_service='83726b27400b405a7a6a79bd962d8e2419daa561',changed=changed,numstat=git(S,'diff','--numstat',prior,'HEAD').decode().strip(),entire_test_equals_prior_minus_one_unused_import=True,all_assertions_and_fixtures_unchanged=True,Skill_domain_class_unchanged=True,N_product_inputs_unchanged=True,before_sha256=hashlib.sha256(before).hexdigest(),after_sha256=hashlib.sha256(after).hexdigest())
(E/'source.diff').write_bytes(git(S,'diff','--unified=0',prior,'HEAD'))
(E/'delta-audit.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
