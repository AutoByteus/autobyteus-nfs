from common import *
import re,hashlib
rows=[json.loads(x) for x in (E/'commands.jsonl').read_text().splitlines()]
go=[json.loads(x) for x in (E/'nfs-race.log').read_text().splitlines() if x.startswith('{')]
out=dict(commands=rows,go=dict(packages_pass=sum(x['Action']=='pass' and not x.get('Test') for x in go),tests_top_level_pass=sum(x['Action']=='pass' and bool(x.get('Test')) and '/' not in x['Test'] for x in go),tests_including_subtests_pass=sum(x['Action']=='pass' and bool(x.get('Test')) for x in go),skips=[x for x in go if x['Action']=='skip']),vitest={},python={})
for name in ['consumer-narrow','consumer-unit','consumer-fixture-confirm','consumer-unit-confirm','consumer-routes','consumer-path-pty','consumer-guide','consumer-guide-confirm']:
 p=E/(name+'.log')
 if not p.exists():continue
 text=re.sub(r'\x1b\[[0-9;]*m','',p.read_text())
 out['vitest'][name]=dict(summary=[x.strip() for x in text.splitlines() if re.match(r'\s*(Test Files|Tests|Duration)',x)],tests_files=[x.strip() for x in text.splitlines() if re.match(r'\s*[✓↓×]',x)])
for name in ['nfs-python','consumer-launcher']:
 p=E/(name+'.log')
 if p.exists():out['python'][name]=[x for x in p.read_text().splitlines() if 'skipped' in x or x.startswith(('Ran ','OK','FAILED'))]
write('execution-summary.json',out)
print(json.dumps({k:v for k,v in out.items() if k not in ['commands','vitest']},indent=2))
for k,v in out['vitest'].items():print(k,v['summary'])
