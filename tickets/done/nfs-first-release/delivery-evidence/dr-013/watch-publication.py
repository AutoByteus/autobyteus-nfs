from pathlib import Path
import subprocess,json,time,datetime
E=Path(__file__).resolve().parent;repo='repos/AutoByteus/autobyteus-nfs';ids=[39215470944,39215449472,39215443295]
def api(url):return json.loads(subprocess.check_output(['gh','api',url],text=True))
prior=None
for i in range(90):
 runs=[]
 for rid in ids:
  r=api(f'{repo}/actions/runs/{rid}');runs.append(r);(E/f'run-{rid}-latest.json').write_text(json.dumps(r,indent=2)+'\n')
 jobs=api(f'{repo}/actions/runs/{ids[0]}/attempts/1/jobs?per_page=100');(E/'publication-jobs-latest.json').write_text(json.dumps(jobs,indent=2)+'\n')
 artifacts=api(f'{repo}/actions/runs/{ids[0]}/artifacts?per_page=100');(E/'publication-artifacts-latest.json').write_text(json.dumps(artifacts,indent=2)+'\n')
 o={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'runs':[[r['id'],r['status'],r['conclusion']] for r in runs],'jobs':[[j['id'],j['name'],j['status'],j['conclusion']] for j in jobs['jobs']],'artifacts':[[a['id'],a['name']] for a in artifacts['artifacts']]}
 with (E/'publication-observations.jsonl').open('a') as f:f.write(json.dumps(o)+'\n')
 state=json.dumps([o['runs'],o['jobs'],o['artifacts']])
 if state!=prior:print(json.dumps(o),flush=True);prior=state
 if all(r['status']=='completed' for r in runs):
  (E/'publication-watch-complete.json').write_text(json.dumps(o,indent=2)+'\n');break
 time.sleep(30)
else:raise SystemExit('Monitor window ended; runs may still be active, not completion')
