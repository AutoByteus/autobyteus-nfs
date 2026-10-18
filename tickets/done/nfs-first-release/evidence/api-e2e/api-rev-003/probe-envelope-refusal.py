# Case R04; source 585d416c2746cf2963058d591b0753d0db8088f5; executed 2026-10-18 UTC; environment local macOS26.5.2 arm64; Python3.9.6/Bash3.2.57
# Step: probe-envelope-refusal.py; exact command/steps in body or companion result JSON. Reader annotation 2026-10-18T10:40:08.210765+00:00; original captured body follows unchanged.
from pathlib import Path
import json,subprocess,datetime
E=Path(__file__).resolve().parent;N=E.parents[5];T=E.parents[2]
with (T/'api-e2e-coverage-investigation.md').open('a') as f:f.write('\nR04 additional actual-boundary negative before final result: change only a copy of the real envelope wrapper digest and invoke fetch-candidate. Actual GitHub run/artifact metadata must reject mismatch before download destination creation. This tests explicit corrupt-retention input, not a second synthetic candidate; preserve real envelope/candidate unchanged.\n')
e=json.loads((E/'candidate-envelope.json').read_text());e['digest']='sha256:'+'0'*64
path=E/'wrong-envelope-control.json';path.write_text(json.dumps(e,indent=2)+'\n')
root=Path(json.loads((E/'retained-candidate-resource.json').read_text())['root']);dest=root/'refused-envelope-destination';assert not dest.exists()
args=['/usr/bin/python3',str(N/'packaging/release.py'),'--operation','fetch-candidate','--envelope',str(path),'--directory',str(dest)]
p=subprocess.run(args,cwd=N,capture_output=True,text=True,timeout=60,env={**__import__('os').environ,'PYTHONDONTWRITEBYTECODE':'1'})
(E/'actual-envelope-refusal.log').write_text('# Case R04; commit585d416c2746cf2963058d591b0753d0db8088f5; local Macarm64/current CLI or real Actions-read API; date '+datetime.datetime.now(datetime.timezone.utc).isoformat()+'\n$ '+' '.join(args)+'\n'+p.stdout+p.stderr)
r=dict(command=args,exit=p.returncode,expected='Retained artifact envelope differs',destinationAbsent=not dest.exists(),pass_=p.returncode==1 and 'Retained artifact envelope differs' in p.stderr and not dest.exists(),scope='Real GitHub read-only metadata comparison; deliberately wrong copied wrapper digest, unchanged actual candidate/envelope')
(E/'actual-envelope-refusal.json').write_text(json.dumps(r,indent=2)+'\n')
assert r['pass_'],r
with (T/'api-e2e-test-progress.md').open('a') as f:f.write('| '+datetime.datetime.now(datetime.timezone.utc).isoformat()+' | R04 | Completed | Pass | actual API envelope mismatch refused before destination/download; correct candidate untouched; evidence actual-envelope-refusal.json |\n')
print(json.dumps(r,indent=2))
