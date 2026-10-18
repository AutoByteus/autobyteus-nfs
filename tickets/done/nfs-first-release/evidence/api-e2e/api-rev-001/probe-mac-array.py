from pathlib import Path
import subprocess,json,datetime,tempfile,shutil,os,hashlib
E=Path(__file__).resolve().parent;N=E.parents[5];T=E.parents[2]
workflow=(N/'.github/workflows/release-nfs.yml').read_text();start=workflow.index('          args=()\n',workflow.index('name: Native checks and exact engine metadata'));end=workflow.index('\n          go test -race',start)
body='\n'.join(x[10:] for x in workflow[start:end].splitlines())+'\n'
# The exact three workflow lines execute; inert python stub makes entry/argv observable,
# not a fake engine/qualification. The shell failure occurs before that command is called.
probe='set -euo pipefail\npython3() { printf "called\\n" >> "$HOME/called"; printf "<%s>\\n" "$@"; }\n'+body
(E/'mac-array-exact-snippet.sh').write_text(probe)
with (T/'api-e2e-coverage-investigation.md').open('a') as f:f.write('\nR03-F001 investigation before rerouting: both actual Mac jobs fail args[@]:unbound variable at exact workflow native-check line5, before metadata/Go tests. Execute extracted three source lines under local /bin/bash with candidate vs fresh control; inert python command makes entry/argv observable, no engine/source modification. This supported candidate-mode shell path is within AC001. No durable-test or production fix before origin review.\n')
root=Path(tempfile.mkdtemp(prefix='nfs-first-array-api001-',dir=Path.home()));rows=[]
try:
 for shell in ['/bin/bash','/opt/homebrew/bin/bash']:
  if not Path(shell).exists():continue
  ver=subprocess.check_output([shell,'--version'],text=True).splitlines()[0]
  for mode in ['candidate','fresh']:
   h=root/(Path(shell).parts[1]+'-'+mode);h.mkdir()
   env={'PATH':'/usr/bin:/bin','HOME':str(h),'TAG':'v0.1.0','MODE':mode,'TARGET':'darwin-arm64','image':'metadata-only-control'}
   p=subprocess.run([shell,str(E/'mac-array-exact-snippet.sh')],env=env,cwd=h,capture_output=True,text=True)
   name='mac-array-'+('system' if shell=='/bin/bash' else 'brew')+'-'+mode+'.log';(E/name).write_text('$ '+shell+' '+str(E/'mac-array-exact-snippet.sh')+'\n'+ver+'\nMODE='+mode+'\n'+p.stdout+p.stderr)
   row=dict(shell=shell,version=ver,mode=mode,exit=p.returncode,called=(h/'called').exists(),log=name);rows.append(row)
 assert next(x for x in rows if x['shell']=='/bin/bash' and x['mode']=='candidate')['exit']==1
 assert not next(x for x in rows if x['shell']=='/bin/bash' and x['mode']=='candidate')['called']
 assert next(x for x in rows if x['shell']=='/bin/bash' and x['mode']=='fresh')['exit']==0
finally:
 shutil.rmtree(root)
 (E/'mac-array-reproduction.json').write_text(json.dumps(dict(workflowSha256=hashlib.sha256(workflow.encode()).hexdigest(),exactExtractedLines=body,rows=rows,scratch=str(root),scratchAbsent=not root.exists(),scope='Exact workflow shell expansion reproduction; stubbed python boundary, not filesystem/signing/engine proof'),indent=2)+'\n')
with (T/'api-e2e-test-case-ledger.md').open('a') as f:f.write('| '+datetime.datetime.now(datetime.timezone.utc).isoformat()+' | R03-F001 | Reproduced candidate empty-array exit1 before command entry on system Bash; fresh-mode nonempty control exit0. No fix. | mac-array-reproduction.json |\n')
print(json.dumps(rows,indent=2))
