from pathlib import Path
import ast,json,shutil,subprocess
N=Path(__file__).resolve().parents[5]
S=Path('/Users/normy/autobyteus_org/autobyteus-worktrees/extract-autobyteus-nfs')
# Only tracked inputs. Never traverse/copy ignored assets or old ticket history.
files=subprocess.check_output(['git','-C',str(S),'ls-files','autobyteus-nfs'],text=True).splitlines()
for name in files:
    rel=Path(name).relative_to('autobyteus-nfs');dst=N/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(S/name,dst)
    if dst.suffix=='.go' or dst.name=='go.mod':dst.write_text(dst.read_text().replace('github.com/AutoByteus/autobyteus-workspace/autobyteus-nfs','github.com/AutoByteus/autobyteus-nfs'))
extra=['scripts/public/nfs/install.sh','.github/workflows/release-nfs.yml']+['scripts/tests/'+x for x in ['test_nfs_engine_packaging.py','test_nfs_installer_fixture.py','test_nfs_release_workflow.py']]
for name in extra:
    dst=N/name;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(S/name,dst)
for p in [N/'packaging/release.py',N/'.github/workflows/release-nfs.yml',N/'scripts/tests/test_nfs_engine_packaging.py',N/'scripts/tests/test_nfs_release_workflow.py']:
    t=p.read_text()
    for prefix in ['packaging','internal','cmd','go.mod','out']:
        t=t.replace('autobyteus-nfs/'+prefix,prefix)
    p.write_text(t)
p=N/'packaging/release.py';t=p.read_text().replace('parents[2]','parents[1]');a=t.index('SOURCES =');b=t.index('\n\n\ndef source_hash',a)
t=t[:a]+'''SOURCES = ['internal', 'cmd/autobyteus-nfs/main.go', 'go.mod',
           'scripts/public/nfs', 'packaging/Dockerfile', 'packaging/engine',
           'packaging/release.py', '.github/workflows/release-nfs.yml',
           'testdata/attachment.json', 'docs/integration-contract.md',
           'LICENSE', 'THIRD_PARTY_NOTICES']'''+t[b:];p.write_text(t)
p=N/'internal/platform/directory_modes_test.go';p.write_text(p.read_text().replace('filepath.Abs("../../..")','filepath.Abs("../..")'))
p=N/'scripts/public/nfs/install.sh';p.write_text(p.read_text().replace('AutoByteus/autobyteus-workspace','AutoByteus/autobyteus-nfs'))
p=N/'packaging/Dockerfile';p.write_text(p.read_text().replace('COPY autobyteus-nfs/THIRD_PARTY_NOTICES','COPY THIRD_PARTY_NOTICES'))
p=N/'.github/workflows/release-nfs.yml';t=p.read_text().replace("  push:\n    tags: ['v*']\n",'').replace('Existing repository tag (vX.Y.Z or beta); no separate version stream','Existing NFS tag (vX.Y.Z or beta); never creates a tag or release').replace("${{ github.event_name == 'push' || inputs.publish }}","${{ inputs.publish }}").replace('          cd autobyteus-nfs\n','').replace('../engine-candidate/','engine-candidate/')
t='\n'.join(x for x in t.splitlines() if not ('autobyteus-web/package.json' in x))+'\n';p.write_text(t)
raw=(S/'scripts/tests/test_nfs_packaging_and_launcher.py').read_text();lines=raw.splitlines(keepends=True);cls=next(x for x in ast.parse(raw).body if isinstance(x,ast.ClassDef));launcher=[];service=[]
for f in cls.body:
    text=''.join(lines[f.lineno-1:f.end_lineno])
    (launcher if f.name.startswith(('test_shell_','test_launcher_')) else service).append(text)
header='import subprocess\nimport unittest\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[2]\n'
(N/'scripts/tests/test_nfs_packaging.py').write_text('"""Nonpublishing service-only refusal fixtures; no real install or mounts."""\n'+header+'\nclass NfsPackagingTest(unittest.TestCase):\n'+ '\n'.join(service).replace('autobyteus-nfs/packaging/','packaging/')+'\n\nif __name__ == "__main__":\n    unittest.main()\n')
(S/'scripts/tests/test_nfs_launcher.py').write_text('"""Offline launcher fixtures: fake installed CLI/Docker, no mounts or /etc writes.\nRun: python3 -m unittest scripts/tests/test_nfs_launcher.py -v\n"""\nimport tempfile\n'+header+"MODULE = ROOT / 'scripts/public/docker/autobyteus-docker.d/bash/nfs-attachment.sh'\n\nclass NfsLauncherTest(unittest.TestCase):\n"+'\n'.join(launcher)+'\n\nif __name__ == "__main__":\n    unittest.main()\n')
shutil.copy2(S/'CLA.md',N/'CLA.md')
(N/'.gitignore').write_text((N/'.gitignore').read_text()+'''/autobyteus-nfs
/engine-candidate/
/engine-parts/
/artifacts/
/scripts/tests/__pycache__/
''')
print({'moduleFiles':len(files),'extra':extra,'N':str(N)})
