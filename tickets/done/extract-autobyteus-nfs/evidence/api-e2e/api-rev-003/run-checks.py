from common import *
import sys
mode=sys.argv[1];cfg=json.loads((E/'environment.json').read_text());P=Path(cfg['scratch']);name=cfg['container'];case='N01-'+mode
if mode=='linux':
 prefix=['docker','exec','--user','1001:1001','--workdir','/home/checker/candidate',name,'env','-i','PATH=/usr/local/go/bin:/usr/bin:/bin','HOME=/home/checker','TMPDIR=/home/checker/tmp','GOTOOLCHAIN=local'];env=None;cwd=P;binary='/home/checker/autobyteus-nfs'
else:
 prefix=[];cwd=P/'candidate';binary=str(P/'autobyteus-nfs')
 env=dict(PATH=str(P/'tools/go/bin')+':/usr/bin:/bin:/usr/sbin:/sbin',HOME=str(P/'darwin-home'),TMPDIR=str(P/'darwin-tmp'),GOCACHE=str(P/'darwin-cache'),GOMODCACHE=str(P/'darwin-home/go/pkg/mod'),GOTOOLCHAIN='local')
try:
 event(case,'Started','Current fixture through actual '+mode+' mount-observation path, nonroot focused first then race/vet')
 run(mode+'-environment',prefix+['sh','-c','id; uname -a; go version; cc --version | head -1; python3 --version; '+('cat /etc/os-release; grep " /proc " /proc/self/mountinfo' if mode=='linux' else 'true')],cwd,env)
 run(mode+'-focused',prefix+['go','test','-race','./internal/setup','-run','TestHostedConfig|TestDetachDoesNotRequireLiveSource','-count=1','-v'],cwd,env)
 event(case,'Checkpoint','Focused hosted-config/no-live-source detach passed; native path exercised, broader package closure running','N/A',mode+'-focused.log')
 run(mode+'-race',prefix+['go','test','-race','-json','-count=1','./...'],cwd,env)
 run(mode+'-vet',prefix+['go','vet','./...'],cwd,env)
 event(case,'Completed','Current focused plus all-package race/vet passed; skips retained separately','Pass',mode+'-focused.log; '+mode+'-race.log; '+mode+'-vet.log')
 case='N02-'+mode;event(case,'Started','Packaging/installer fixture controls, Bash/sourcehash and expected empty-qualification refusal')
 run(mode+'-python',prefix+['python3','-m','unittest','discover','-s','scripts/tests','-p','test_nfs_*.py','-v'],cwd,env)
 run(mode+'-shell',prefix+['bash','-n','scripts/public/nfs/install.sh'],cwd,env)
 run(mode+'-source-hash',prefix+['python3','packaging/release.py','--source-hash'],cwd,env)
 assert (E/(mode+'-source-hash.log')).read_text().splitlines()[-1]=='348046594b470f7b294aa2162f78ec349eb57c4edf74aa2db32112a9dc9da90e'
 run(mode+'-publish-refusal',prefix+['python3','packaging/release.py','--check-publish'],cwd,env,expected=1)
 event(case,'Completed','Packaging/Bash/hash/refusal passed within explicit native/container skip limits','Pass',mode+'-python.log; '+mode+'-source-hash.log; '+mode+'-publish-refusal.log')
 case='N03-'+mode;event(case,'Started','Current native build/version, not live installed service or target qualification')
 run(mode+'-build',prefix+['go','build','-o',binary,'./cmd/autobyteus-nfs'],cwd,env)
 run(mode+'-version',prefix+[binary,'version'],cwd,env)
 event(case,'Completed','Current native binary built/version executable passed; no service lifecycle invoked','Pass',mode+'-build.log; '+mode+'-version.log')
except Exception as ex:
 event(case,'Completed',str(ex),'Fail','commands.jsonl; '+mode+' logs');raise
