from pathlib import Path
import subprocess,shutil
E=Path(__file__).resolve().parent;S=Path('/Users/normy/autobyteus_org/autobyteus-worktrees/extract-autobyteus-nfs');D=Path((E/'consumer-scratch-path.txt').read_text().strip())/'repo'
paths=set(subprocess.check_output(['git','-C',str(S),'ls-files','-z']).decode().split('\0'))|set(subprocess.check_output(['git','-C',str(S),'ls-files','--others','--exclude-standard','-z']).decode().split('\0'))
for rel in paths:
 if not rel or rel.startswith('tickets/'):continue
 s=S/rel;d=D/rel
 if s.is_file():d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(s,d)
 elif d.is_file():d.unlink()
print(D)
