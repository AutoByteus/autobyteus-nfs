from pathlib import Path
import json,hashlib,subprocess,os,shutil,datetime
E=Path(__file__).resolve().parent;N=E.parents[5];T=E.parents[2];a=json.loads((E/'input-audit.json').read_text());s=json.loads((E/'scratch.json').read_text());P=Path(s['path']);S=Path(s['source'])
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def git(*args):return subprocess.check_output(['git','-C',str(N),*args],text=True).strip()
assert P.parent==Path.home() and P.name.startswith('nfs-first-api001-') and S==P/'source'
assert all(x['passed'] for x in json.loads((E/'local-results.json').read_text()))
assert all(x['passed'] for x in json.loads((E/'native-results.json').read_text()))
events=[json.loads(l) for l in (E/'go-race.log').read_text().splitlines() if l.startswith('{')]
assert not [x for x in events if x.get('Action')=='fail']
counts=dict(packages_pass=sum(x.get('Action')=='pass' and not x.get('Test') for x in events),top_tests_pass=sum(x.get('Action')=='pass' and bool(x.get('Test')) and '/' not in x['Test'] for x in events),all_tests_pass=sum(x.get('Action')=='pass' and bool(x.get('Test')) for x in events),skips=[dict(package=x['Package'],test=x['Test']) for x in events if x.get('Action')=='skip' and x.get('Test')])
(E/'test-counts.json').write_text(json.dumps(dict(native_darwin=counts,python=dict(collected=38,executed=37,skips=1,skip_reason='Standalone Go-child mode; fresh native Go parent executes it'),narrow_tests='Overlap broad; do not unique-add',actual_CLI_git_controls=5),indent=2)+'\n')
(E/'native-binary.json').write_text(json.dumps(dict(file='owned scratch/out/autobyteus-nfs (removed after checks)',sha256=h(P/'out/autobyteus-nfs'),version='development-unqualified',platform='macOS26.5.2 arm64',source_input=a['head'],runtime_changed=False,qualified=False),indent=2)+'\n')
source_bad=[name for name,d in a['source'].items() if h(N/name)!=d or h(S/name)!=d];assert not source_bad,source_bad
protected_bad=[name for name,d in a['protected_ticket'].items() if h(N/name)!=d]
allowed='tickets/in-progress/nfs-first-release/code-review-evidence/crr-001/routing.json'
assert not set(protected_bad)-{allowed},protected_bad
head=git('rev-parse','HEAD');diff=git('diff','--name-only',a['head'],head)
assert not git('diff','--name-only',a['head'],head,'--',':!tickets')
processes=subprocess.check_output(['ps','-axo','pid=,command='],text=True).splitlines();owned=[x for x in processes if str(P) in x and not x.strip().startswith(str(os.getpid())+' ')];assert not owned,owned
p=subprocess.run(['lsof','-nP','-d','cwd','-Fn'],capture_output=True,text=True);cwd=[x for x in p.stdout.splitlines() if x.startswith('n'+str(P))];assert not cwd,cwd
receipt=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),source_inputs=len(a['source']),source_mismatches=source_bad,protected_inputs=len(a['protected_ticket']),protected_changes=protected_bad,external_owner_change='Reviewer appended handoff receipt in518f4b5; inspected exact docs-only delta, preserved',head=head,head_delta_paths=diff.splitlines(),own_host_processes=owned,own_cwds=cwd,scratch=str(P),containers_created=0,shared_live_containers_untouched=True,real_candidate_created=False,qualification_lock_unchanged=True)
shutil.rmtree(P);assert not P.exists();receipt['scratch_removed']=True
(E/'cleanup-local.json').write_text(json.dumps(receipt,indent=2)+'\n')
with (T/'api-e2e-test-case-ledger.md').open('a') as f:
 f.write('| '+receipt['utc']+' | R02-native | Pass native Darwin race7packages/vet/build/version; direct Go-child skip covered by parent; NOT physical NFS/hosted proof | native-results.json, test-counts.json |\n')
 f.write('| '+receipt['utc']+' | C01-local | Pass local owned scratch/toolchain/cache cleanup;119inputs preserved; reviewer routing receipt appended externally, not restored | cleanup-local.json |\n')
print(json.dumps(counts), 'local cleanup complete')
