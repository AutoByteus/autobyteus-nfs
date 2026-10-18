from common import *
from collections import Counter
commands=[json.loads(l) for l in (E/'commands.jsonl').read_text().splitlines()]
assert all(c['pass_'] for c in commands)
cleanup=json.loads((E/'cleanup.json').read_text());assert cleanup['pass_']
mutants=json.loads((E/'mutation-results.json').read_text());assert len(mutants)==3 and all(m['assertion_sensitive'] for m in mutants)
for mode in ['linux','darwin']:
 for check in ['environment','focused','race','vet','python','shell','source-hash','publish-refusal','build','version']:
  selected=[c for c in commands if c['name']==mode+'-'+check];assert len(selected)==1 and selected[0]['pass_']
write('execution-summary.json',dict(revision='API-REV-003',candidate='09cac96225fe4f36fb0dcbe6ddec01248992874f',runtime='83726b27400b405a7a6a79bd962d8e2419daa561',commands=commands,command_count=len(commands),all_command_expected_exits_matched=True,counts=json.loads((E/'test-counts.json').read_text()),mutations=mutants,cleanup=cleanup,attempts=[dict(kind='API cleanup environment Local Fix',first='cleanup-attempt-1/cleanup-console.log',cause='initial guard rejected exited UID1001 Go zombie adopted by sleep PID1',diagnosis='cleanup-process-diagnosis.log',resolution='live processes still refused; verified Z state/Ppid1 allowed exact owned container removal; namespace and scratch absent',status='resolved')],source_test_changes_by_API=[],carried='S01-S06/API002 + four-target/engine compile and actionlint/API001, exact limits retained',hosted='Not executed; prior runs remain failed/cancelled; Delivery-owned',result='Pass',confidence=95.0))
print('commands',len(commands),'expected exit matches; cleanup resolved and complete')
