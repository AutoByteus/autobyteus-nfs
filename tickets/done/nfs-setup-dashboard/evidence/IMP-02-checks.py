# IMP-02 | 2026-10-24 | input1a670d4c + working admin/IPC phase
# Darwin arm64 Go1.27.2, independent APFS copy/private HOME/TMP/cache.
# Usage: python3 <this-file> <unique-round-name> <go-test-package>...
from pathlib import Path
import shutil,subprocess,os,json,datetime,sys
w=Path.cwd();e=w/'tickets/in-progress/nfs-setup-dashboard/evidence';root=Path(json.loads((e/'IMP-01-environment.json').read_text())['scratch']);name=sys.argv[1];src=root/name;src.mkdir()
paths=set(subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard'],text=True).splitlines())
for rel in sorted(paths):
 p=w/rel
 if rel.startswith('tickets/') or not p.is_file():continue
 q=src/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)
env={'PATH':str(root/'go/bin')+':'+os.environ['PATH'],'HOME':str(root/'home'),'TMPDIR':str(root/'tmp'),'GOCACHE':str(root/'cache'),'GOTOOLCHAIN':'local'}
cmd=['go','test','-race','-timeout','90s']+sys.argv[2:]
record={'id':'IMP-02','date':datetime.datetime.now(datetime.timezone.utc).isoformat(),'baseCommit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'workingDelta':subprocess.check_output(['git','diff','--stat'],text=True),'source':str(src),'command':cmd,'environment':'Darwin arm64 Go1.27.2/private HOME/TMP/cache'}
with (e/('IMP-02-'+name+'.log')).open('w') as log:
 log.write(json.dumps(record)+'\n');log.flush();r=subprocess.run(cmd,cwd=src,env=env,stdout=log,stderr=subprocess.STDOUT)
record['exit']=r.returncode;(e/('IMP-02-'+name+'.json')).write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record))
