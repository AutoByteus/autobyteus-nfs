from pathlib import Path
import subprocess,shutil,json
E=Path(__file__).resolve().parent;P=Path((E/'scratch-path.txt').read_text().strip())
name=json.loads((E/'linux-container.json').read_text())['name']
cases=[
 ('ignore-status-preflight','internal/setup/status.go','if err = backend.VerifyGanesha(*h, s.Store.Directory, h.Backend == "ganesha-docker"); err != nil {','if err = backend.VerifyGanesha(*h, s.Store.Directory, h.Backend == "ganesha-docker"); false {','TestHostedConfigStatusRefusesBeforeReadiness','status ignored hosted config'),
 ('ignore-detach-preflight','internal/setup/lifecycle.go','if err = backend.VerifyGaneshaForDetach(*h, s.Store.Directory, h.Backend == "ganesha-docker"); err != nil {','if err = backend.VerifyGaneshaForDetach(*h, s.Store.Directory, h.Backend == "ganesha-docker"); false {','TestHostedConfigDetachPreflightsBeforeEffects','detach touched dependencies before checking config'),
 ('reject-partial-detach','internal/backend/ganesha_native.go','if _, err := os.Lstat(filepath.Join(root, "ganesha", "ganesha.conf")); os.IsNotExist(err) {\n\t\treturn nil','if _, err := os.Lstat(filepath.Join(root, "ganesha", "ganesha.conf")); os.IsNotExist(err) {\n\t\treturn err','TestHostedConfigDetachCurrentOrPartialRetryReachesExistingChecks','did not stop at Linux mount boundary')
]
out=[]
for label,rel,old,new,selector,diagnostic in cases:
 dest=P/label;shutil.copytree(P/'candidate',dest);p=dest/rel;s=p.read_text();assert s.count(old)==1;s=s.replace(old,new,1);p.write_text(s)
 target='/home/checker/'+label
 subprocess.run(['docker','exec',name,'bash','-euc','cp -a /inputs/'+label+' '+target+' && chown -R checker:checker '+target],check=True)
 cmd=['docker','exec','--user','1001:1001','--workdir',target,name,'env','-i','PATH=/usr/local/go/bin:/usr/bin:/bin','HOME=/home/checker','TMPDIR=/home/checker/tmp','GOTOOLCHAIN=local','go','test','-race','./internal/setup','-run',selector,'-count=1','-v']
 run=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
 (E/('mutation-'+label+'.log')).write_text('$ '+' '.join(cmd)+'\n'+run.stdout)
 result=dict(name=label,exit=run.returncode,expected_failure=run.returncode==1 and diagnostic in run.stdout and '[build failed]' not in run.stdout,diagnostic=diagnostic)
 out.append(result);(E/'mutation-results.json').write_text(json.dumps(out,indent=2)+'\n')
 print(result,flush=True);assert result['expected_failure']
