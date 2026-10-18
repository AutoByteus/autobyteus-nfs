from common import *
import re,hashlib
commands=[json.loads(l) for l in (E/'commands.jsonl').read_text().splitlines()]
expected=['install','build','typecheck','nuxt-prepare','overlap','narrow','unit','integration','core','routes','path-pty','launcher','guide','localization','web-boundary']
assert [c['name'] for c in commands]==['consumer-'+n for n in expected]
assert all(c['pass_'] for c in commands)
counts={}
for c in commands:
 data=re.sub(r'\x1b\[[0-9;]*m','',(E/c['log']).read_text())
 counts[c['name']]=[l.strip() for l in data.splitlines() if re.match(r'^\s*(Test Files|Tests\s|Duration\s|Ran \d+ tests|OK \(skipped=)',l)]
write('test-counts.json',counts)
write('execution-summary.json',dict(revision='API-REV-002',current_S=json.loads((E/'input-audit.json').read_text())['S']['head'],current_N_service='83726b27400b405a7a6a79bd962d8e2419daa561',checks=commands,counts=counts,carried_N=['N01','N02','N03'],N_carry_evidence='carry-validity.json + ../api-rev-001 logs, no new N execution',test_changes=[],production_changes=[],overlap='narrow34 and overlap28 repeated within broad units; never sum as unique',cleanup=json.loads((E/'cleanup.json').read_text()),all_current_commands_pass=True))
print(json.dumps(counts,indent=2))
