from pathlib import Path
import json,subprocess,datetime,re,hashlib
E=Path(__file__).resolve().parent;N=E.parents[5]
def api(s):return json.loads(subprocess.check_output(['gh','api','repos/AutoByteus/autobyteus-nfs/'+s],text=True))
before=json.loads((E/'pre-dispatch.json').read_text());after=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),tags=api('tags?per_page=100'),releases=api('releases?per_page=100'),main=api('git/ref/heads/main'),task=api('git/ref/heads/codex/nfs-first-release'),run=api('actions/runs/39111348848'),artifacts=api('actions/runs/39111348848/artifacts?per_page=100'))
after['tagsUnchanged']=after['tags']==before['tags'];after['releasesUnchanged']=after['releases']==before['releases'];after['mainUnchanged']=after['main']['object']['sha']=='7e375984be2bea7a4d536e43cc59d6bc2b116870'
(E/'post-run-remote.json').write_text(json.dumps(after,indent=2)+'\n')
assert after['tagsUnchanged'] and after['releasesUnchanged'] and after['mainUnchanged']; assert after['run']['conclusion']=='failure'
logs=json.loads((E/'hosted-log-index.json').read_text());summary=[]
for j in logs:
 s=(E/j['log']).read_text(encoding='utf-8-sig');lines=s.splitlines()
 selected=[l for l in lines if any(t in l for t in ['unbound variable','Process completed with exit code','ok  \t','ok\t','Ran 38 tests','OK (skipped=','SKIP','skipped ', 'v0.1.0','"index":','"linux-amd64":','"linux-arm64":'])]
 # Keep focused native proof without copying large successful compiler logs again.
 if 'binaries' in j['name']:
  (E/('hosted-excerpt-'+str(j['jobId'])+'.log')).write_text('\n'.join(selected)+'\n')
 summary.append(dict(jobId=j['jobId'],name=j['name'],result=j['conclusion'],nativePackagePassLines=[l for l in lines if re.search(r'Z ok\s+github.com/',l)],pythonSummary=[l for l in lines if 'Ran 38 tests' in l or 'OK (skipped=' in l],failedExpansion=[l for l in lines if 'unbound variable' in l],claimLimit='Mac failed before metadata/Go; Linux completed native pipeline; none is filesystem qualification'))
(E/'hosted-execution-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
(E/'failure-summary.json').write_text(json.dumps(dict(id='R03-F001',case='R03',acceptanceCriteria=['AC001','AC007'],secondaryBlocked=['AC002','AC003','AC004','AC005','AC006'],preliminaryClassification='Local Fix',recommendedOwner='implementation_engineer after code_reviewer failure-origin review',origin='Release workflow executable shell path, not NFS filesystem/runtime, signing credentials or physical-host dependency',source='518f4b51e251edaa6b5664f71c7171bde57bafc9',run=39111348848,attempt=1,jobs=[117628928559,117628928627],expected='Candidate-mode native job generates unqualified metadata then runs native race/vet/Python/build/version/archive on both Mac arches',observed='System /bin/bash aborts exact empty args[@] expansion with set -u before metadata/native checks; both exit1. Linux jobs succeed; candidate/payload/publish skipped.',reproduction='python3 tickets/in-progress/nfs-first-release/evidence/api-e2e/api-rev-001/probe-mac-array.py',remoteEffects='Build-only artifacts retained; no complete candidate; tag/release/main unchanged; publisher skipped, build push false; no signing or registry login path executed.',next='Fix supported Mac candidate shell invocation and add bounded executable regression through supported shell; source/workflow hash changes require new current candidate and relevant rerun, no reuse as complete qualification.'),indent=2)+'\n')
print(json.dumps(dict(tagsUnchanged=after['tagsUnchanged'],releasesUnchanged=after['releasesUnchanged'],mainUnchanged=after['mainUnchanged'],artifacts=[(a['id'],a['name'],a['expires_at']) for a in after['artifacts']['artifacts']],summary=summary),indent=2))
