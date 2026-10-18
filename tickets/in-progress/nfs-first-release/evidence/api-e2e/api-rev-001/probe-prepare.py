from pathlib import Path
import json,subprocess,os,datetime
E=Path(__file__).resolve().parent;N=E.parents[5];T=E.parents[2];P=Path(json.loads((E/'scratch.json').read_text())['path']);head=json.loads((E/'input-audit.json').read_text())['head']
with (T/'api-e2e-coverage-investigation.md').open('a') as f:f.write('\nR02-preflight temporary probe added before execution: real release.py CLI, actual git HEAD/show byte comparison against current checked-out workflow, emulated GitHub event/env only. Positive candidate-mode preparation writes owned outputs; old workflow, wrong event, beta and non-main publication refuse. No Actions dispatch or external writer invoked. This supplements module mocks, not hosted acceptance.\n')
base={'HOME':str(P/'home'),'TMPDIR':str(P/'tmp')+'/','PATH':'/usr/bin:/bin:/usr/sbin:/sbin','PYTHONDONTWRITEBYTECODE':'1','GITHUB_REPOSITORY':'AutoByteus/autobyteus-nfs','GITHUB_EVENT_NAME':'workflow_dispatch','GITHUB_SHA':head,'GITHUB_REF':'refs/heads/codex/nfs-first-release','WANT_PUBLISH':'false'}
rows=[]
for name,extra,tag,expect,needle in [('valid',{},'v0.1.0',0,'candidate'),('old-workflow',{'GITHUB_SHA':'7e375984be2bea7a4d536e43cc59d6bc2b116870'},'v0.1.0',1,'Dispatch workflow differs'),('wrong-event',{'GITHUB_EVENT_NAME':'pull_request'},'v0.1.0',1,'Dispatch/source identity differs'),('beta',{},'v0.1.0-beta.1',1,'strict normal'),('non-main-publish',{'WANT_PUBLISH':'true'},'v0.1.0',1,'Publish must use exact dispatch main')]:
 env=base|extra|{'GITHUB_OUTPUT':str(P/(name+'-out')),'GITHUB_STEP_SUMMARY':str(P/(name+'-summary'))}
 args=['/usr/bin/python3','packaging/release.py','--operation','prepare','--tag',tag,'--source-commit',head,'--directory',str(P/(name+'-work'))]
 p=subprocess.run(args,cwd=N,env=env,capture_output=True,text=True,timeout=30)
 (E/('prepare-'+name+'.log')).write_text('$ '+' '.join(args)+'\ncwd '+str(N)+'\n'+p.stdout+p.stderr)
 assert p.returncode==expect and needle in p.stdout+p.stderr,(name,p.stdout,p.stderr)
 if name=='valid':
  r=json.loads(p.stdout);assert r['source']==head and r['mode']=='candidate';assert 'mode=candidate' in (P/(name+'-out')).read_text()
 else:assert not (P/(name+'-out')).exists()
 rows.append(dict(case=name,exit=p.returncode,expected=expect,passed=True,scope='Actual CLI/git; emulated dispatch env, no remote effect'))
 with (T/'api-e2e-test-case-ledger.md').open('a') as f:f.write('| '+datetime.datetime.now(datetime.timezone.utc).isoformat()+' | R02-preflight | Pass '+name+' | prepare-'+name+'.log |\n')
(E/'prepare-results.json').write_text(json.dumps(rows,indent=2)+'\n')
print('5 actual CLI/git preflight controls pass; emulated event, not hosted')
