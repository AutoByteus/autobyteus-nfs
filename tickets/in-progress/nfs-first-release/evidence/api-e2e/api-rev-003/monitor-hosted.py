# Case R03; source 585d416c2746cf2963058d591b0753d0db8088f5; executed 2026-10-18 UTC; environment read-only Actions observation; actual hosted Ubuntu24.04/macOS15 four-native run39118784695/1
# Step: monitor-hosted.py; exact command/steps in body or companion result JSON. Reader annotation 2026-10-18T10:40:08.210765+00:00; original captured body follows unchanged.
from pathlib import Path
import datetime,json,subprocess,time
E=Path(__file__).resolve().parent;T=E.parents[2]; receipt=json.loads((E/'dispatch-receipt.json').read_text()); run=receipt['run']['id']; attempt=receipt['run']['run_attempt']
repo='AutoByteus/autobyteus-nfs'; previous=None
for n in range(1,91):
 def api(path): return json.loads(subprocess.check_output(['gh','api','repos/'+repo+'/'+path],text=True))
 r=api('actions/runs/'+str(run));j=api(f'actions/runs/{run}/attempts/{attempt}/jobs?per_page=100');a=api(f'actions/runs/{run}/artifacts?per_page=100')
 assert r['id']==run and r['run_attempt']==attempt and r['head_sha']=='585d416c2746cf2963058d591b0753d0db8088f5'
 states=[(i['id'],i['name'],i['status'],i['conclusion']) for i in j['jobs']]
 now=datetime.datetime.now(datetime.timezone.utc).isoformat(); key=[r['status'],r['conclusion'],states,[(i['id'],i['name']) for i in a['artifacts']]]
 if key!=previous:
  p=E/f'hosted-checkpoint-{n:03}.json';p.write_text(json.dumps(dict(utc=now,run=r,jobs=j,artifacts=a),indent=2)+'\n')
  print(json.dumps(dict(utc=now,status=r['status'],conclusion=r['conclusion'],jobs=states,artifacts=[(i['id'],i['name']) for i in a['artifacts']])),flush=True)
  with (T/'api-e2e-test-case-ledger.md').open('a') as f: f.write(f'| {now} | R03 | Hosted checkpoint {r["status"]}/{r["conclusion"]}; completed job conclusions retained; no run Pass inferred | {p.name} |\n')
  previous=key
 if r['status']=='completed':
  (E/'hosted-final.json').write_text(p.read_text()); break
 time.sleep(30)
else:
 print('MONITOR LIMIT reached; run unresolved, not cancelled.',flush=True)
