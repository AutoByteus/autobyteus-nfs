# Case R03; source 585d416c2746cf2963058d591b0753d0db8088f5; executed 2026-10-18 UTC; environment read-only Actions observation; actual hosted Ubuntu24.04/macOS15 four-native run39118784695/1
# Step: collect-hosted.py; exact command/steps in body or companion result JSON. Reader annotation 2026-10-18T10:40:08.210765+00:00; original captured body follows unchanged.
from pathlib import Path
import json,subprocess,datetime,re,hashlib
E=Path(__file__).resolve().parent;N=E.parents[5]
def api(s):return json.loads(subprocess.check_output(['gh','api','repos/AutoByteus/autobyteus-nfs/'+s],text=True))
r=json.loads((E/'dispatch-receipt.json').read_text())['run'];run=r['id'];f=json.loads((E/'hosted-final.json').read_text());assert f['run']['status']=='completed'
before=json.loads((E/'pre-dispatch.json').read_text());after=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),tags=api('tags?per_page=100'),releases=api('releases?per_page=100'),main=api('git/ref/heads/main'),task=api('git/ref/heads/codex/nfs-first-release'),run=api(f'actions/runs/{run}'),artifacts=api(f'actions/runs/{run}/artifacts?per_page=100'),priorFailedRun=api('actions/runs/39111348848/attempts/1'))
after['tagsUnchanged']=after['tags']==before['tags'];after['releasesUnchanged']=after['releases']==before['releases'];after['mainUnchanged']=after['main']['object']['sha']=='7e375984be2bea7a4d536e43cc59d6bc2b116870'
(E/'post-run-remote.json').write_text(json.dumps(after,indent=2)+'\n');assert after['tagsUnchanged'] and after['releasesUnchanged'] and after['mainUnchanged'];assert after['priorFailedRun']['conclusion']=='failure'
index=[];summary=[]
for j in f['jobs']['jobs']:
 if j['conclusion']=='skipped':continue
 p=subprocess.run(['gh','api',f'repos/AutoByteus/autobyteus-nfs/actions/jobs/{j["id"]}/logs'],capture_output=True);name='hosted-job-'+str(j['id'])+'.log';header=(f'# Case R03; gh api actions/jobs/{j["id"]}/logs; source {r["head_sha"]}; environment {j["name"]}; observed '+datetime.datetime.now(datetime.timezone.utc).isoformat()+'\n# Raw command bytes follow unchanged.\n').encode();(E/name).write_bytes(header+(p.stdout if p.returncode==0 else p.stderr))
 index.append(dict(jobId=j['id'],name=j['name'],conclusion=j['conclusion'],log=name,exit=p.returncode,bytes=len(p.stdout),rawBodySha256=hashlib.sha256(p.stdout).hexdigest(),fileSha256=hashlib.sha256((E/name).read_bytes()).hexdigest()));assert p.returncode==0
 lines=p.stdout.decode('utf-8-sig',errors='replace').splitlines();native='binaries' in j['name']
 selected=[l for l in lines if any(s in l for s in ['##[error]','FAIL','unbound variable','Ran 45 tests','OK (skipped=','skipped ', 'ok  \t','test "$(out/autobyteus-nfs version)"','Package four regular members','Artifact upload has successfully completed'])]
 if native:(E/('hosted-excerpt-'+str(j['id'])+'.log')).write_text(header.decode()+'\n'.join(selected)+'\n')
 summary.append(dict(jobId=j['id'],name=j['name'],result=j['conclusion'],nativePackagePassLines=[l for l in lines if re.search(r'Z ok\s+github.com/',l)],pythonSummary=[l for l in lines if 'Ran 45 tests' in l or 'OK (skipped=' in l],explicitPythonSkips=[l for l in lines if 'skipped ' in l],errors=[l for l in lines if '##[error]' in l or 'unbound variable' in l],scope='Hosted build/fixture/archive execution, not physical NFS/signing/user qualification'))
(E/'hosted-log-index.json').write_text(json.dumps(index,indent=2)+'\n');(E/'hosted-execution-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(dict(run=run,conclusion=f['run']['conclusion'],jobs=[(x['name'],x['result'],len(x['nativePackagePassLines'])) for x in summary],tagReleaseMainUnchanged=True),indent=2))
