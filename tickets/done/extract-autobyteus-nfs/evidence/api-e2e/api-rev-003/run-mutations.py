from common import *
import shutil
cfg=json.loads((E/'environment.json').read_text());P=Path(cfg['scratch']);name=cfg['container']
cases=[
 ('ignore-status-preflight','internal/setup/status.go','if err = backend.VerifyGanesha(*h, s.Store.Directory, h.Backend == "ganesha-docker"); err != nil {','if err = backend.VerifyGanesha(*h, s.Store.Directory, h.Backend == "ganesha-docker"); false {','TestHostedConfigStatusRefusesBeforeReadiness','status ignored hosted config'),
 ('ignore-detach-preflight','internal/setup/lifecycle.go','if err = backend.VerifyGaneshaForDetach(*h, s.Store.Directory, h.Backend == "ganesha-docker"); err != nil {','if err = backend.VerifyGaneshaForDetach(*h, s.Store.Directory, h.Backend == "ganesha-docker"); false {','TestHostedConfigDetachPreflightsBeforeEffects','detach touched dependencies before checking config'),
 ('reject-partial-detach','internal/backend/ganesha_native.go','if _, err := os.Lstat(filepath.Join(root, "ganesha", "ganesha.conf")); os.IsNotExist(err) {\n\t\treturn nil','if _, err := os.Lstat(filepath.Join(root, "ganesha", "ganesha.conf")); os.IsNotExist(err) {\n\t\treturn err','TestHostedConfigDetachCurrentOrPartialRetryReachesExistingChecks','did not stop at Linux mount boundary')]
event('N04','Started','Independent native Linux assertion-sensitivity controls in three disposable mutated copies')
results=[]
try:
 for label,rel,old,new,selector,diagnostic in cases:
  dest=P/label;shutil.copytree(P/'candidate',dest);p=dest/rel;s=p.read_text();assert s.count(old)==1;p.write_text(s.replace(old,new,1))
  target='/home/checker/'+label
  run('prepare-mutation-'+label,['docker','exec',name,'bash','-euc','cp -a /inputs/'+label+' '+target+' && chown -R checker:checker '+target],P)
  cmd=['docker','exec','--user','1001:1001','--workdir',target,name,'env','-i','PATH=/usr/local/go/bin:/usr/bin:/bin','HOME=/home/checker','TMPDIR=/home/checker/tmp','GOTOOLCHAIN=local','go','test','-race','./internal/setup','-run',selector,'-count=1','-v']
  result=run('mutation-'+label,cmd,P,expected=1)
  log=(E/('mutation-'+label+'.log')).read_text();result.update(expected_diagnostic=diagnostic,assertion_sensitive=diagnostic in log and '[build failed]' not in log)
  results.append(result);write('mutation-results.json',results);assert result['assertion_sensitive']
  event('N04','Checkpoint',label+' failed the intended assertion (expected exit1, not compilation failure)','N/A',result['log'])
 event('N04','Completed','All3 actual Linux mutant controls caught missing/overstrict preflight; canonical production/tests unchanged','Pass','mutation-results.json; mutation-*.log')
except Exception as ex:
 event('N04','Completed',str(ex),'Fail','mutation-results.json; commands.jsonl');raise
