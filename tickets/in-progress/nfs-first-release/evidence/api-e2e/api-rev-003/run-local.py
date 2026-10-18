# Case R01/R02; source 585d416c2746cf2963058d591b0753d0db8088f5; executed 2026-10-18 UTC; environment local macOS26.5.2 arm64; Python3.9.6/Bash3.2.57
# Step: run-local.py; exact command/steps in body or companion result JSON. Reader annotation 2026-10-18T10:40:08.210765+00:00; original captured body follows unchanged.
from pathlib import Path
import subprocess,tempfile,json,hashlib,datetime,os,shutil,textwrap
E=Path(__file__).resolve().parent;N=E.parents[5];T=E.parents[2];audit=json.loads((E/'input-audit.json').read_text())
root=Path(tempfile.mkdtemp(prefix='nfs-first-api003-',dir=Path.home()));src=root/'source';src.mkdir()
for name,h in audit['source'].items():
 p=N/name;assert hashlib.sha256(p.read_bytes()).hexdigest()==h
 d=src/name;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,d)
for n in ['home','tmp']: (root/n).mkdir()
env={'PATH':'/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin','HOME':str(root/'home'),'TMPDIR':str(root/'tmp'),'PYTHONDONTWRITEBYTECODE':'1','LANG':'en_US.UTF-8'}
(E/'scratch.json').write_text(json.dumps({'root':str(root),'source':str(src),'owner':'API003','inputs':120},indent=2)+'\n');rows=[]
def cmd(case,name,args,expect=0,contains=None):
 p=subprocess.run(args,cwd=src,env=env,capture_output=True,text=True,timeout=600);(E/(name+'.log')).write_text('$ '+' '.join(args)+'\ncwd '+str(src)+'\n'+p.stdout+p.stderr)
 row={'case':case,'name':name,'command':args,'exit':p.returncode,'expected':expect,'pass':p.returncode==expect and (contains is None or contains in p.stdout+p.stderr)};rows.append(row);(E/'local-results.json').write_text(json.dumps(rows,indent=2)+'\n')
 with (T/'api-e2e-test-case-ledger.md').open('a') as f:f.write('| '+datetime.datetime.now(datetime.timezone.utc).isoformat()+' | '+case+' | '+('Pass' if row['pass'] else 'Fail')+' '+name+' | '+name+'.log |\n')
 print(name,row['pass'],flush=True);assert row['pass'],row
try:
 cmd('R02','bash-version',['/bin/bash','--version']);cmd('R02','python-version',['/usr/bin/python3','--version'])
 cmd('R03-F001','workflow-current',['/usr/bin/python3','-m','unittest','scripts/tests/test_nfs_release_workflow.py','-v'])
 cmd('R01','records-focused',['/usr/bin/python3','-m','unittest','discover','-s','scripts/tests','-p','test_nfs_release_records.py','-v'])
 cmd('R01','python-all',['/usr/bin/python3','-m','unittest','discover','-s','scripts/tests','-p','test_nfs_*.py','-v'])
 cmd('R02','actionlint',['/opt/homebrew/bin/actionlint','.github/workflows/ci.yml','.github/workflows/release-nfs.yml'])
 w=(src/'.github/workflows/release-nfs.yml').read_text();block=w.split('      - name: Native checks and exact engine metadata (not physical qualification)\n',1)[1].split('        run: |\n',1)[1].split('          go test -race ./...\n',1)[0];prefix=root/'native-prefix.sh';prefix.write_text(textwrap.dedent(block))
 cmd('R02','prefix-syntax',['/bin/bash','-n',str(prefix)]);cmd('R02','prefix-shellcheck',['/opt/homebrew/bin/shellcheck','-s','bash',str(prefix)])
 cmd('R02','source-hash',['/usr/bin/python3','packaging/release.py','--source-hash'],contains='c7fd64e87b62509165d8655cc576fba9261867a306f13a93ad420776304e4a60')
 cmd('R02','recipe-hash',['/usr/bin/python3','packaging/engine/manifest.py','source-hash'],contains='299db7012dcc543f8606632695d286548d1513c13ace8b108eb712984fd39274')
 cmd('R02','publish-refusal',['/usr/bin/python3','packaging/release.py','--check-publish'],1,'Current engine and structured release readiness required')
finally:
 mismatches=[name for name,h in audit['source'].items() if hashlib.sha256((src/name).read_bytes()).hexdigest()!=h or hashlib.sha256((N/name).read_bytes()).hexdigest()!=h];assert not mismatches
 shutil.rmtree(root);(E/'cleanup-local.json').write_text(json.dumps(dict(root=str(root),absent=not root.exists(),sourceCount=120,mismatches=mismatches,commandsCompleted=len(rows),allPassed=all(r['pass'] for r in rows),liveResourcesCreated=False),indent=2)+'\n')
print('Local execution complete; current counts and broader decision recorded separately.')
