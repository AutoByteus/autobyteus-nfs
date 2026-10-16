from pathlib import Path
import subprocess,tempfile,shutil,json,os
E=Path(__file__).resolve().parent;S=Path('/Users/normy/autobyteus_org/autobyteus-worktrees/extract-autobyteus-nfs')
p=Path(tempfile.mkdtemp(prefix='nfs-consumer-ir001-'));(E/'consumer-scratch-path.txt').write_text(str(p)+'\n');dest=p/'repo';dest.mkdir()
for rel in subprocess.check_output(['git','-C',str(S),'ls-files','-z']).decode().split('\0'):
 if not rel or rel.startswith('tickets/'):continue
 f=S/rel
 if not f.is_file():continue
 d=dest/rel;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,d)
for x in ['home','tmp']:(p/x).mkdir()
env={'PATH':'/Users/normy/.nvm/versions/node/v22.21.1/bin:/opt/homebrew/bin:/usr/bin:/bin','HOME':str(p/'home'),'TMPDIR':str(p/'tmp'),'CI':'true','COREPACK_ENABLE_DOWNLOAD_PROMPT':'0'}
with (E/'consumer-install.log').open('w') as log:
 r=subprocess.run(['pnpm','install','--frozen-lockfile','--filter','autobyteus-server-ts...','--filter','autobyteus-web...'],cwd=dest,env=env,stdout=log,stderr=subprocess.STDOUT)
(E/'consumer-install-result.json').write_text(json.dumps({'returncode':r.returncode,'path':str(dest),'env':env},indent=2)+'\n');print('install exit',r.returncode,flush=True)
raise SystemExit(r.returncode)
