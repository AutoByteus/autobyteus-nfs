"""IR002 bounded shell/local packaging checks; no hosted or publication actions."""
import ast,hashlib,json,shutil,subprocess,tempfile,time
from pathlib import Path
E=Path(__file__).resolve().parent;ROOT=E.parents[4]
S=Path(tempfile.mkdtemp(prefix='nfs-release-ir002-check-',dir='/Users/normy/autobyteus_org'))
source=S/'source';source.mkdir();(S/'home').mkdir();(S/'tmp').mkdir()
(E/'scratch-path.txt').write_text(str(S)+'\n')
names=subprocess.check_output(['git','ls-files','-z'],cwd=ROOT).decode().strip('\0').split('\0')
inputs={}
for name in names:
 if name.startswith('tickets/'):continue
 p=ROOT/name;out=source/name;out.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,out)
 inputs[name]=hashlib.sha256(p.read_bytes()).hexdigest()
(E/'source-inputs.json').write_text(json.dumps(inputs,indent=2)+'\n')
env={'PATH':'/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin','HOME':str(S/'home'),'TMPDIR':str(S/'tmp'),'PYTHONDONTWRITEBYTECODE':'1'}
results=[]
def run(name,argv,expected=0):
 start=time.time()
 with (E/(name+'.log')).open('w') as log:
  r=subprocess.run(argv,cwd=source,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=180)
 result={'name':name,'argv':argv,'exitCode':r.returncode,'expected':expected,'pass':r.returncode==expected,'seconds':round(time.time()-start,2)}
 results.append(result);print(result,flush=True)
 (E/'checks-result.json').write_text(json.dumps(results,indent=2)+'\n')
 return r.returncode
try:
 run('shell-version',['/bin/bash','--version'])
 run('python-version',['/usr/bin/python3','--version'])
 run('actionlint-version',['/opt/homebrew/bin/actionlint','-version'])
 run('python-all',['/usr/bin/python3','-m','unittest','discover','-s','scripts/tests','-p','test_nfs_*.py','-v'])
 run('actionlint',['/opt/homebrew/bin/actionlint','.github/workflows/ci.yml','.github/workflows/release-nfs.yml'])
 workflow=source/'.github/workflows/release-nfs.yml';text=workflow.read_text()
 block=text.split('      - name: Native checks and exact engine metadata (not physical qualification)\n',1)[1].split('        run: |\n',1)[1].split('          go test -race ./...\n',1)[0]
 import textwrap
 prefix=S/'native-prefix.sh';prefix.write_text(textwrap.dedent(block));shutil.copyfile(prefix,E/'native-prefix.sh')
 run('prefix-bash-syntax',['/bin/bash','-n',str(prefix)])
 run('prefix-shellcheck',['/opt/homebrew/bin/shellcheck','-s','bash',str(prefix)])
 run('source-hash',['/usr/bin/python3','packaging/release.py','--source-hash'])
 run('publish-refusal',['/usr/bin/python3','packaging/release.py','--check-publish'],1)
 # Mutate only the independent copy, restoring after each observation.
 mutations=[('fresh-arguments', 'then args+=(--qualified --candidate work/candidate); fi', 'then :; fi'),
            ('nounset', 'set -euo pipefail', 'set -eo pipefail'),
            ('pipefail', 'set -euo pipefail', 'set -eu')]
 for name,before,after in mutations:
  assert before in text;workflow.write_text(text.replace(before,after))
  run('mutation-'+name,['/usr/bin/python3','-m','unittest','discover','-s','scripts/tests','-p','test_nfs_release_workflow.py','-v'],1)
  s=(E/('mutation-'+name+'.log')).read_text();assert 'FAIL:' in s and 'ERROR:' not in s
  workflow.write_text(text)
 assert all(x['pass'] for x in results)
 current={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in inputs}
 assert current==inputs
 initial=json.loads((E/'input-audit.json').read_text())
 preserved={}
 for name,record in initial['preservedUntracked'].items():
  p=ROOT/name;assert p.stat().st_size==record['size'] and hashlib.sha256(p.read_bytes()).hexdigest()==record['sha256'];preserved[name]=record
 changed=[name for name in inputs if inputs[name]!=initial['source'][name]['sha256']]
 assert set(changed)=={'.github/workflows/release-nfs.yml','scripts/tests/test_nfs_release_workflow.py','TESTING.md'},changed
 tree=ast.parse((source/'scripts/tests/test_nfs_release_workflow.py').read_text());refs={n.id for n in ast.walk(tree) if isinstance(n,ast.Name) and isinstance(n.ctx,ast.Load)}
 unused=[(n.lineno,a.asname or a.name.split('.')[0]) for n in ast.walk(tree) if isinstance(n,(ast.Import,ast.ImportFrom)) for a in n.names if (a.asname or a.name.split('.')[0]) not in refs]
 assert not unused,unused
 (E/'final-checks.json').write_text(json.dumps({'result':'Local checks pass; targeted source review required','inputSourceCount':len(inputs),'exactIndependentCopy':True,'changedInputs':changed,'otherSourcesUnchanged':len(inputs)-len(changed),'unusedImports':unused,'workflowNonemptyLines':sum(bool(x.strip()) for x in text.splitlines()),'preservedDeliveryUntracked':preserved,'defaultQualification':'unchanged/empty','hostedCandidate':'NOT rerun; new source hash requires NEW API-owned candidate'},indent=2)+'\n')
finally:
 shutil.rmtree(S)
 (E/'cleanup.json').write_text(json.dumps({'scratch':str(S),'absent':not S.exists(),'resources':'Only local subprocesses/independent copy; no containers/VMs/mounts/secrets/remote effects'},indent=2)+'\n')
