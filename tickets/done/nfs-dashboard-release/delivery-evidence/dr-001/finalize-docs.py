import datetime,hashlib,json,os,pathlib,re,shutil,subprocess,time
N=pathlib.Path('/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/nfs-dashboard-release');T=N/'tickets/done/nfs-dashboard-release';E=T/'delivery-evidence/dr-001';S=pathlib.Path('/Users/normy/nfs-dashboard-release-ytwviz3y');P='448cef839b4919a1e3ae0489e8d86ae36f5cee33';commands=[]
def save(name,x):(E/name).write_text(json.dumps(x,indent=2)+'\n')
def run(args,cwd=N,env=None):
 p=subprocess.run(args,cwd=cwd,env=env,capture_output=True,text=True);commands.append({'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':args,'cwd':str(cwd),'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr});save('docs-finalization-commands.json',commands);assert p.returncode==0,p.stderr;return p.stdout.strip()
assert run(['git','rev-parse','HEAD'])==P
run(['git','fetch','origin','main']);assert run(['git','rev-parse','origin/main'])==P
# This is the separate post-publication documentation continuation, not a replay of P.
assert run(['git','branch','--show-current'])=='codex/nfs-dashboard-release'
files=run(['git','ls-files']).splitlines()+run(['git','ls-files','--others','--exclude-standard']).splitlines()
new=run(['git','ls-files','--others','--exclude-standard']).splitlines();assert all(p.startswith('tickets/done/nfs-dashboard-release/') for p in new)
changed=run(['git','diff','--name-only']).splitlines();assert all(p.startswith('tickets/done/nfs-dashboard-release/') or p in ('README.md','TESTING.md','docs/dashboard.md') for p in changed)
new_changed=sorted(set(new+changed));folded={}
for path in files:
 for component in pathlib.PurePosixPath(path).parts:
  assert not re.search(r'[<>:"\\|?*\x00-\x1f]',component) and not component.endswith((' ','.'))
  assert component.split('.')[0].upper() not in {'CON','PRN','AUX','NUL',*[f'COM{i}' for i in range(1,10)],*[f'LPT{i}' for i in range(1,10)]}
 key=path.casefold();assert key not in folded or folded[key]==path;folded[key]=path
for path in new_changed:
 f=N/path;assert f.is_file() and not f.is_symlink() and f.stat().st_size<10*1024*1024
save('docs-precommit.json',{'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'base':P,'changedOutsideTicket':[p for p in changed if not p.startswith('tickets/')],'portableNamesAndCaseCollisions':'Pass','newFilesWithinOwnTicket':len(new),'publishedBytesNotChanged':True,'scope':'README/TESTING/dashboard availability + own current evidence only; no runtime/test/lock/readiness/workflow delta'})
shutil.copyfile(__file__,E/'finalize-docs.py')
# Stage enumerated own paths only, including new current receipts; never add-all.
paths=sorted(set(run(['git','diff','--name-only']).splitlines()+run(['git','ls-files','--others','--exclude-standard']).splitlines())-{str((E/'docs-finalization-commands.json').relative_to(N))})
assert all(p.startswith('tickets/done/nfs-dashboard-release/') or p in ('README.md','TESTING.md','docs/dashboard.md') for p in paths)
run(['git','add','--',*paths]);run(['git','diff','--cached','--check','--',*[p for p in paths if not p.endswith('.log')]]);run(['git','commit','-m','docs: record published v0.2.0 dashboard and verified distribution'])
doc=run(['git','rev-parse','HEAD'])
# Sanitized scanner output; no suppression additions.
p=subprocess.run(['gitleaks','git','--redact','--no-banner','--log-opts=origin/main..HEAD','--report-format=json','--report-path',str(E/'docs-prepush-secrets.json')],cwd=N,capture_output=True,text=True)
(E/'docs-prepush-secrets.log').write_text(p.stdout+p.stderr);assert p.returncode==0,'Secret scan failed; no push'
assert json.loads((E/'docs-prepush-secrets.json').read_text())==[]
run(['git','push','origin','HEAD:refs/heads/codex/nfs-dashboard-release']);run(['git','fetch','origin','main']);assert run(['git','rev-parse','origin/main'])==P
run(['git','switch','finalize/nfs-dashboard-release']);assert run(['git','rev-parse','HEAD'])==P
run(['git','merge','--no-ff',doc,'-m','Merge verified v0.2.0 release documentation'])
q=run(['git','rev-parse','HEAD']);assert run(['git','rev-parse','HEAD^{tree}'])==run(['git','rev-parse',doc+'^{tree}'])
clone=S/'docs-integrated-check';home=S/'docs-integrated-home';tmp=S/'docs-integrated-tmp';home.mkdir(mode=0o700);tmp.mkdir(mode=0o700)
run(['git','clone','--no-hardlinks','--no-checkout',str(N),str(clone)]);run(['git','checkout','--detach',q],clone)
env=dict(os.environ,HOME=str(home),TMPDIR=str(tmp),PYTHONDONTWRITEBYTECODE='1');assert not run(['git','status','--porcelain=v1'],clone)
assert run(['python3','-B','packaging/release.py','--source-hash'],clone,env)=='9b6e429252421eba35c7757fe1eaf309642dba119e0cccbb35c764f358c484eb'
run(['python3','-B','-m','unittest','discover','-s','scripts/tests','-p','test_nfs_dashboard_packaging.py','-v'],clone,env)
assert not run(['git','status','--porcelain=v1'],clone)
for path in (clone,home,tmp):shutil.rmtree(path)
run(['git','fetch','origin','main']);assert run(['git','rev-parse','origin/main'])==P
run(['git','push','origin','HEAD:refs/heads/main'])
refs=run(['git','ls-remote','origin','refs/heads/main','refs/heads/codex/nfs-dashboard-release','refs/tags/v0.2.0','refs/tags/v0.2.0^{}'])
actual={line.split()[1]:line.split()[0] for line in refs.splitlines()};assert actual['refs/heads/main']==q and actual['refs/heads/codex/nfs-dashboard-release']==doc and actual['refs/tags/v0.2.0']=='51e84a18e9283c9f6dda9be5d396dcb4b1b6f75f' and actual['refs/tags/v0.2.0^{}']==P
save('docs-finalization.json',{'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':'Documentation finalized; ordinary CI/receipt cleanup pending','publishedSource':P,'documentationTicket':doc,'finalMain':q,'tree':run(['git','rev-parse','HEAD^{tree}']),'parents':run(['git','show','-s','--format=%P','HEAD']).split(),'remoteRefs':actual,'integratedChecks':'Independent clone same source hash and2embedding tests Pass; clean; clone/home/tmp removed','noPublicationReplay':'Tag P and all public assets unchanged; Q documentation-only after publication'})
print('DOCS FINALIZED',doc,q,flush=True)
# Monitor both exact new ordinary push runs, plus any additional pipeline triggered for this release.
runs={}
for _ in range(20):
 allruns=json.loads(run(['gh','api','repos/AutoByteus/autobyteus-nfs/actions/runs?per_page=50']))['workflow_runs']
 for label,sha in [('ticket',doc),('main',q)]:
  found=[r for r in allruns if r['head_sha']==sha and r['event']=='push' and r['path']=='.github/workflows/ci.yml'];assert len(found)<=1
  if found:runs[label]=found[0]['id']
 if len(runs)==2:break
 time.sleep(3)
assert len(runs)==2;save('docs-ci-runs.json',runs)
history=[]
for _ in range(90):
 rows=[]
 for label,rid in runs.items():
  d=json.loads(subprocess.check_output(['gh','api',f'repos/AutoByteus/autobyteus-nfs/actions/runs/{rid}'],text=True));save('docs-ci-'+label+'.json',d);rows.append({'label':label,'run':rid,'status':d['status'],'conclusion':d['conclusion'],'source':d['head_sha']})
 history.append({'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'runs':rows});save('docs-ci-monitor.json',history);print(json.dumps(rows),flush=True)
 if all(r['status']=='completed' for r in rows):break
 time.sleep(20)
else:raise RuntimeError('CI monitoring bound')
for r in rows:
 rid=r['run'];j=json.loads(subprocess.check_output(['gh','api',f'repos/AutoByteus/autobyteus-nfs/actions/runs/{rid}/jobs?per_page=100'],text=True));save('docs-ci-'+r['label']+'-jobs.json',j)
 p=subprocess.run(['gh','run','view',str(rid),'--repo','AutoByteus/autobyteus-nfs','--log'],capture_output=True);assert p.returncode==0;(E/('docs-ci-'+r['label']+'.log')).write_bytes(p.stdout);r['rawLogSHA256']=hashlib.sha256(p.stdout).hexdigest()
save('docs-ci-summary.json',rows);assert all(r['conclusion']=='success' for r in rows)
print('Final documentation CI Pass',flush=True)
