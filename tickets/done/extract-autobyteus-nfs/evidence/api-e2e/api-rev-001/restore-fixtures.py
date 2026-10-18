from common import *
import re,hashlib
c=json.loads((E/'environment.json').read_text());R=Path(c['S'])/'repo'
log=(E/'consumer-unit.log').read_text()
missing=sorted(set(re.findall("ENOENT: no such file or directory, open '("+re.escape(str(R))+r"/tickets/[^']+)'",log)))
assert len(missing)==11,len(missing)
with (T/'api-e2e-coverage-investigation.md').open('a') as f:f.write('''
## Execution discovery correction — S03 fixture closure
Initial broader units: 102 files passed, 2 failed, 4 skipped; 1186 tests passed, 12 failed, 6 skipped. All12 failures are ENOENT reads of11 tracked replay files under root tickets/done. The API archive excluded root tickets as irrelevant evidence, but these two durable suites directly consume those historical data fixtures. Tests remain Still Valid; this is API-owned incomplete fixture setup, not a product/runtime finding. Restore only those exact current-commit tracked fixture bytes into owned archive, hash-verify, rerun both affected suites then the full same regression command. No assertion/source/config alteration and no live provider call. Preserve original failed log and commands.
''')
event('S03','Checkpoint','All 12 failures are missing 11 tracked replay fixtures excluded by archive setup; restore exact current bytes without test edits','N/A','consumer-unit.log; fixture-restoration.json')
rows=[]
for absname in missing:
 p=Path(absname);rel=str(p.relative_to(R))
 data=subprocess.check_output(['git','-C',str(S),'show','HEAD:'+rel])
 assert data==(S/rel).read_bytes(),rel
 p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
 rows.append(dict(path=rel,sha256=hashlib.sha256(data).hexdigest(),bytes=len(data)))
write('fixture-restoration.json',dict(classification='API environment/fixture Local Fix',source_head=subprocess.check_output(['git','-C',str(S),'rev-parse','HEAD'],text=True).strip(),files=rows,production_changes=False,test_changes=False,assertion_changes=False))
with (E/'attempts.md').open('a') as f:f.write('- S03 initial broad command failed 12 replay cases because API source archive omitted 11 tracked root tickets/done fixture files. Original consumer-unit.log retained. Restored exact source-commit bytes only; fixture-restoration.json lists hashes. No product/test changes or live provider use.\n')
print('Restored',len(rows),'exact fixtures')
