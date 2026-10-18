from common import *
bases={'N':'fc5d2ff3f404de3a683994766dfd47c258efb374','S':'3712cd9bf0db998501d162db7f8655f169e3def6'}
lines=['# Proportional successful-test review scope','','No API-authored production or durable test edits. This round executes the cumulative current R2 tests, not only IR002 import cleanup. CRR002 source Pass remains separate. This index selects the task delta; it is not a cumulative forwarding manifest.','','N='+str(N),'S='+str(S),'','## Current R2 durable coverage delta']
for label,root in [('N',N),('S',S)]:
 data=subprocess.check_output(['git','-C',str(root),'diff','--name-status',bases[label],'HEAD'],text=True)
 rows=[]
 for line in data.splitlines():
  p=line.split('\t')[-1]
  if p.startswith('tickets/') or (label=='S' and p.startswith('autobyteus-nfs/')):continue
  if p.endswith('_test.go') or ('/tests/' in p and p.endswith(('.ts','.py','.mjs','.json'))) or '/__tests__/' in p:
   rows.append(line)
 lines+=['','### '+label+' relative to '+bases[label],'','~~~text',*rows,'~~~']
lines+=['','## Review emphasis',
'- N installation_state/install_state/standalone_state: actual lock/trusted bounded readers; no resource/binary side effect on refusal; exact host-only writer and additive-field direct-use policy.',
'- S private preparation/bootstrappers/runtime profile: no bindings/no acquisition; actual temp FS/aliases/project collision/current managed source; pre-await ownership and deterministic cancellation.',
'- Codex/Grok process fixtures use actual owned child processes but fake protocol/model; Claude close-error retry is a deterministic client double. No inference/native-provider qualification claim.',
'- Registered/native resolvers preserve selected identity and errors, no mount discriminator. Ordinary REST/GraphQL and actual native PTY/WebSocket proof is local, not NFS.',
'- Removed binding/Git/project materializer/paired fixtures assert obsolete R1 coupling; replacements prove R2. Generic launcher stop/mapping controls survive.',
'- Guide production component is unchanged; EN/zh text changed. IR001 renders carried only after byte equality; fresh 4-file component checks expected.',
'- Raw execution artifacts and AC proof table in canonical API report. No old shared-network-workspaces af9f23 test-review scope for this new task.']
(E/'test-review-scope.md').write_text('\n'.join(lines)+'\n')
print('wrote selected scope')
