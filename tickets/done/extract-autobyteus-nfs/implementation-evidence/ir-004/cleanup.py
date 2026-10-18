from pathlib import Path
import json,subprocess,shutil
E=Path(__file__).resolve().parent
setup=json.loads((E/'check-environment.json').read_text()); P=Path(setup['scratch']);env=setup['env']
assert P.parent==Path('/Users/normy/autobyteus_org') and P.name.startswith('nfs-extract-ir004-')
assert P.exists() and not P.is_symlink()
checks=json.loads((E/'checks-result.json').read_text())
assert len(checks)==3 and all(c['exit']==0 for c in checks)
toolchain={}
for name,cmd in [('node',['node','--version']),('pnpm',['pnpm','--version']),('typescript',['node','-p',"require('./autobyteus-server-ts/node_modules/typescript/package.json').version"])]:
 toolchain[name]=subprocess.check_output(cmd,cwd=P/'repo',env=env,text=True).strip()
(E/'toolchain.json').write_text(json.dumps(toolchain,indent=2)+'\n')
ps=subprocess.check_output(['ps','-axo','pid=,command='],text=True)
commands=[line for line in ps.splitlines() if str(P) in line]
cwd=subprocess.run(['/usr/sbin/lsof','-a','-d','cwd','-Fn'],text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
cwds=[line for line in cwd.stdout.splitlines() if line.startswith('n'+str(P))]
assert not commands,commands
assert not cwds,cwds
assert cwd.returncode==0, cwd.stderr
shutil.rmtree(P)
(E/'cleanup.json').write_text(json.dumps(dict(scratch=str(P),owned_process_matches_before=commands,owned_cwd_matches_before=cwds,cwd_inventory_exit=cwd.returncode,scratch_removed=not P.exists(),live_app_vm_container_mount_provider_resources_started=False,scope='Only exact owned IR004 copy/home/temp. No source checkout, retained engine, D0/PM data, prior dist or other resources removed.'),indent=2)+'\n')
print('Owned scratch removed; no matching process or cwd before removal.')
