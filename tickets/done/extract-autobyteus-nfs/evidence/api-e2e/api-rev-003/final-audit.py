from pathlib import Path
import hashlib,json,subprocess
N=Path('/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/extract-autobyteus-nfs');T=N/'tickets/done/extract-autobyteus-nfs';E=T/'evidence/api-e2e/api-rev-003'
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def git(*args):return subprocess.check_output(['git','-C',str(N),*args],text=True).strip()
def write(name,data):(E/name).write_text(json.dumps(data,indent=2)+'\n')
a=json.loads((E/'input-audit.json').read_text());results={}
assert git('rev-parse','HEAD')==a['N_head']
for key in ['inputs','protected_ticket','ignored_cache','PM']:
 bad=[p for p,v in a[key].items() if not (N/p).is_file() or h(N/p)!=v]
 assert key=='PM' or not bad,(key,bad)
 results[key]={'count':len(a[key]),'mismatches':bad}
 if key=='PM' and bad: results[key]['disposition']='External post-cleanup change preserved; see external-PM-observation.json'
D0=Path('/Users/normy/autobyteus_org/autobyteus-nfs')
for key,args in [('head',['rev-parse','HEAD']),('branch',['symbolic-ref','HEAD'])]:assert subprocess.check_output(['git','-C',str(D0),*args],text=True).strip()==a['D0'][key]
assert not Path('/Users/normy/autobyteus_org/autobyteus-worktrees/extract-autobyteus-nfs').exists()
assert not Path('/Users/normy/nfs-extract-api003-47u9du58').exists()
p=subprocess.run(['docker','inspect','nfs-extract-api003-47u9du58'],capture_output=True,text=True);assert p.returncode!=0 and 'no such object' in p.stderr.lower()
old=subprocess.check_output(['git','-C',str(N),'show',a['N_head']+':'+str((T/'api-e2e-revision-record.md').relative_to(N))])
prior=json.loads((E/'prior-api-history.json').read_text());assert len(old)==prior['bytes'] and hashlib.sha256(old).hexdigest()==prior['sha256']
assert old[old.index(b'## API-REV-001'):].decode() in (T/'api-e2e-revision-record.md').read_text()
for mode in ['linux','darwin']:
 events=[json.loads(l) for l in (E/(mode+'-race.log')).read_text().splitlines() if l.startswith('{')]
 assert not [r for r in events if r.get('Action')=='fail']
 stats=json.loads((E/'test-counts.json').read_text())[mode]
 assert sum(r.get('Action')=='pass' and not r.get('Test') for r in events)==stats['packages_pass']
 assert sum(r.get('Action')=='pass' and bool(r.get('Test')) for r in events)==stats['all_tests_including_subtests_pass']
 assert (E/(mode+'-source-hash.log')).read_text().splitlines()[-1]=='348046594b470f7b294aa2162f78ec349eb57c4edf74aa2db32112a9dc9da90e'
assert len(json.loads((E/'mutation-results.json').read_text()))==3
assert not list(E.rglob('__pycache__'))
results.update(head=a['N_head'],branch=git('branch','--show-current'),prior_API_entries_byte_identical=True,counts_recomputed=True,D0_unchanged=True,S_still_retired=True,scratch_absent=True,container_absent=True,production_or_durable_API_delta=[],result='Pass')
write('final-checks.json',results)
print(json.dumps(results,indent=2))
