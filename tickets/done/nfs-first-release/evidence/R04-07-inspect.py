# R04; actual read-only facade inspection;6cb497f/22205cc; localMacarm64/Python3.9.6 + GitHub GET;2026-10-19UTC.
from pathlib import Path
import subprocess,json,datetime,tempfile,os
E=Path(__file__).resolve().parent;T=E.parent;N=T.parents[2]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def save(name,o):(E/f'R04-07-{name}.json').write_text(json.dumps(o,indent=2)+'\n')
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=N,text=True).strip()
with (T/'api-e2e-test-progress.md').open('a') as f:f.write(f'| {now()} | R04 | Started | Not Tested | Actual inspect-bound, new owned APFS path; exact envelopes/full P validators/jobs, no admission/effects. |\n')
root=Path(tempfile.mkdtemp(prefix='nfs-api007-inspect-',dir=Path.home()));(root/'tmp').mkdir()
save('ownership',{'case':'R04','date':now(),'commit':head,'environment':'localAPFS owned0700','root':str(root),'directory':str(root/'inspection'),'cleanup':'Remove only this created root after R07/C01; prior retained resources untouched'})
cmd=['/usr/bin/python3','packaging/release.py','--operation','inspect-bound','--tag','v0.1.0','--directory',str(root/'inspection'),'--output',str(E/'R04-07-inspection.json')]
p=subprocess.run(cmd,cwd=N,text=True,capture_output=True,timeout=1800,env={**os.environ,'TMPDIR':str(root/'tmp'),'PYTHONDONTWRITEBYTECODE':'1'})
(E/'R04-07-inspection.log').write_text(f'# R04; command{cmd!r}; cwd{N}; commit{head}; localMacarm64/Python3.9.6/liveGET;{now()}\n'+p.stdout+p.stderr+f'\nExit:{p.returncode}\n')
save('command',{'case':'R04','command':cmd,'commit':head,'date':now(),'environment':'localAPFS/live read-only GitHub Actions','exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
assert p.returncode==0,p.stderr
r=json.loads((E/'R04-07-inspection.json').read_text());assert r['executorPublicationAdmission']=='not performed' and r['authorization'] is None
assert r['verifiedPayloadJobId']==117940491787 and r['payloadSourceCommit']=='238bdc183e8affac99ffdee9be9cb333b0eb126f' and r['executor']['commit']==head
assert not list((root/'tmp').iterdir())
save('verified',{'case':'R04','date':now(),'commit':head,'environment':'Actual current facade/full validators','step':'Assert original tag-derived source, exact job, no admission and snapshot cleanup','pass':True,'snapshotScratchEmpty':True,'inspection':r})
p=T/'api-e2e-execution-coverage-report.md';p.write_text(p.read_text().replace('| R04 |002/003/006|','| R04 |002/003/006|'))
lines=p.read_text().splitlines()
for index,l in enumerate(lines):
 if l.startswith('| R04 |'):
  a=l.split('|');a[-3]=' Pass ';a[-2]=' R04-07-inspection.json/command.json/verified.json: actual job117940491787/full old validators; admission not performed; snapshots removed. ';lines[index]='|'.join(a)
p.write_text('\n'.join(lines)+'\n')
with (T/'api-e2e-test-progress.md').open('a') as f:f.write(f'| {now()} | R04 | Completed | Pass | Actual original envelopes/downloads/full P validators/job/signing proof; admission not performed. |\n')
print('INSPECT PASS',root,flush=True)
