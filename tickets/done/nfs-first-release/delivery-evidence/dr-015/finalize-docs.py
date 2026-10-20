from pathlib import Path
import subprocess,json,hashlib,datetime,os,re
N=Path.cwd();T=N/'tickets/done/nfs-first-release';D=T/'delivery-evidence/dr-015';BASE='3424f8dddef795d4a42e83ed8746268a4aab4d7d';HEAD='91f8e841114a1d55a107ea4b1fb2a2af5ae80092';OPS=[]
def git(*args):
 p=subprocess.run(['git',*args],capture_output=True,text=True);OPS.append({'argv':['git',*args],'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr});assert p.returncode==0, p.stderr;return p.stdout.strip()
def save(name,v):(D/name).write_text(json.dumps(v,indent=2)+'\n')
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def protected():
 c=Path('/Users/normy/autobyteus_org/autobyteus-nfs');return {'head':subprocess.check_output(['git','-C',str(c),'rev-parse','HEAD'],text=True).strip(),'pm':{str(p.relative_to(c)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((c/'task-plans').rglob('*')) if p.is_file() and not p.is_symlink()}}
try:
 assert git('rev-parse','HEAD')==HEAD;assert git('branch','--show-current')=='codex/nfs-first-release';assert not git('diff','--cached','--name-only')
 git('fetch','origin','main');assert git('rev-parse','origin/main')==BASE;git('merge-base','--is-ancestor',BASE,'HEAD')
 allowed=['README.md']+[str((T/n).relative_to(N)) for n in ['handoff-summary.md','docs-sync-report.md','release-deployment-report.md','delivery-revision-record.md']]
 assert set(git('diff','--name-only').splitlines())==set(allowed)
 git('diff','--check','--',*allowed)
 files=set(git('ls-files').splitlines())|set(git('ls-files','--others','--exclude-standard').splitlines());lower={}
 for p in files:
  assert p.casefold() not in lower or lower[p.casefold()]==p;lower[p.casefold()]=p
  for part in Path(p).parts:
   assert len(part.encode())<=255 and not re.search(r'[<>:"\\|?*\x00-\x1f]',part) and not part.endswith((' ','.'))
 save('portable-paths.json',{'checked':len(files),'result':'Pass','checks':'casefold uniqueness, portable components, no Windows-reserved characters/trailing-dot-space, component UTF8 bytes<=255'})
 # Compare actual product files to the executing reviewed E. README alone changes.
 products=git('ls-tree','-r','--name-only',BASE).splitlines();compared=0
 for p in products:
  if p.startswith('tickets/') or p=='README.md':continue
  assert (N/p).read_bytes()==subprocess.check_output(['git','show',BASE+':'+p]),p;compared+=1
 source=subprocess.check_output(['python3','packaging/release.py','--source-hash'],env=os.environ|{'PYTHONDONTWRITEBYTECODE':'1'},text=True).strip();assert source=='e3e814176d8315f0426df379035a995b6c0e6d5f89f82483f121b074c79eea21'
 a=json.loads((D/'intake.json').read_text());b=(T/'delivery-revision-record.md').read_bytes();assert hashlib.sha256(b[:a['priorRevisionBytes']]).hexdigest()==a['priorRevisionSha256']
 save('pre-finalization-verification.json',{'at':now(),'freshMain':BASE,'head':HEAD,'baseDelta':False,'productFilesEqualEExceptREADME':compared,'executorSourceHash':source,'originalRevisionPrefixUnchanged':True,'noIntegrationRerunReason':'No new base or executable delta; actual publication/public checks completed, push CI will run normally','canonicalBefore':protected(),'scope':'README + four Delivery docs + owned DR015 evidence; other owners/notes/authorities unchanged'})
 save('finalization-commands.json',OPS)
 git('add','--',*allowed,str(D.relative_to(N)))
 git('commit','-m','docs(release): verify public signed NFS v0.1.0 distribution')
 ticket=git('rev-parse','HEAD');git('push','origin','HEAD:refs/heads/codex/nfs-first-release')
 git('fetch','origin','main');assert git('rev-parse','origin/main')==BASE, 'Target changed; protect checkpoint and reintegrate before finalization'
 git('switch','-c','codex/nfs-first-release-finalize-dr015','origin/main')
 git('merge','--no-ff',ticket,'-m','Merge verified public NFS v0.1.0 delivery documentation')
 target=git('rev-parse','HEAD');assert git('rev-parse','HEAD^{tree}')==git('rev-parse',ticket+'^{tree}')
 git('push','origin','HEAD:refs/heads/main')
 remote={line.split()[1]:line.split()[0] for line in git('ls-remote','origin','refs/heads/main','refs/heads/codex/nfs-first-release','refs/tags/v0.1.0').splitlines()}
 assert remote['refs/heads/main']==target and remote['refs/heads/codex/nfs-first-release']==ticket and remote['refs/tags/v0.1.0']=='f4a04fd0c80a6625708ba002b4cef5507a03f514'
 save('source-finalization.json',{'at':now(),'ticketCommit':ticket,'targetBefore':BASE,'targetCommit':target,'remoteHeads':remote,'policy':'ticket commit/push, freshmain, fresh --no-ff finalize branch, exact tree equality/main push','treeEqual':True,'scope':'Post-publication docs/evidence only; original product/tag/release not changed','finalization':'Completed','pipelineMonitoring':'Pending','cleanup':'Pending','canonicalContentUnchanged':protected()==json.loads((D/'pre-finalization-verification.json').read_text())['canonicalBefore']})
 print(json.dumps({'ticket':ticket,'main':target,'remoteVerified':True},indent=2),flush=True)
finally:save('finalization-commands.json',OPS)
