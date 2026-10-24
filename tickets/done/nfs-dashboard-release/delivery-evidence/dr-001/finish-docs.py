import datetime,hashlib,json,pathlib,shutil,subprocess
N=pathlib.Path('/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/nfs-dashboard-release');T=N/'tickets/done/nfs-dashboard-release';E=T/'delivery-evidence/dr-001';S=pathlib.Path('/Users/normy/nfs-dashboard-release-ytwviz3y')
assert json.loads((E/'public-verification.json').read_text())['result']=='Pass'
assert all(r['result']=='Pass' and r['exit']==0 for r in json.loads((E/'public-dashboard-smoke.json').read_text())['roles'])
for role in ('server','client'):
 d=json.loads((E/f'public-{role}-browser.json').read_text());assert d['result']=='Pass' and d['errors']==[] and d['noAdminRequests'] and d['stopAndTokenRemoval']
(E/'visual-review.md').write_text('''# Actual published v0.2.0 dashboard visual check

Delivery personally opened all four final public-server/client-1280/390 screenshots. Correct role/title, local branding, readable authorization and deferred-field notices, terminal-only password guidance and Stop control are visible. Desktop two-column and narrow stacked presentation have no clipped controls, overlapping text or document-wide overflow. Authorization is deliberately not granted; setup/configuration hidden, no private capability exposed. Measured scrollWidth equals1280/390. Browser156.0.8078.4, actual sandbox enabled. Real installed public binary/private HTTP/PTY, no root protocol double. OS opener alone denied for safe manual fallback; not an auto-open or privileged/storage test. Both native roles exited0 after actual Stop, browser errors0, no API operations. Initial omitempty assertion failure is separately preserved, not reclassified as passing.
''')
# Save the progress chronology before replacing the current canonical report.
shutil.copyfile(T/'release-deployment-report.md',E/'pre-final-progress.md')
p=N/'README.md';s=p.read_text();start=s.index('**Release status:**');end=s.index('\n## Validation boundary',start)
s=s[:start]+'''**Release status:** normal **[v0.2.0 is published](https://github.com/AutoByteus/autobyteus-nfs/releases/tag/v0.2.0)**,
including the standalone **server/client setup dashboard**, for macOS and Linux,
ARM64 and x64. Both Mac binaries are Developer ID signed and Apple-notarized;
downloaded signatures and online notarization checks passed. All18 public assets
match the retained signed payload; the whole multi-architecture container is
anonymously accessible. Public installer/version checks passed on Mac ARM64 and
Ubuntu x64. Both distributed dashboard roles were launched/stopped in an isolated
Mac ARM64 HOME without requesting administration or changing storage.
Mac x64 signature/notarization verification is not local Intel execution.
Shared-filesystem/physical and user testing remains **deferred**, not passed.
Distribution/signature/launch checks are not field qualification. The original
v0.1.0 release remains unchanged; it does not include the dashboard.
See [release procedure](packaging/RELEASE.md) and the
[current delivery record](tickets/done/nfs-dashboard-release/release-deployment-report.md).
''' +s[end:]
s=s.replace('The first release is normal v0.1.0, not beta. Download and inspect the versioned','The current release is normal v0.2.0, not beta. Download and inspect the versioned').replace('/releases/download/v0.1.0/autobyteus-nfs-install.sh','/releases/download/v0.2.0/autobyteus-nfs-install.sh')
s=s.replace('## Source-built local setup dashboard','## Local setup dashboard (v0.2.0+)').replace('The current source adds two **ordinary-user terminal** commands:','The published executable includes two **ordinary-user terminal** commands:')
s=s.replace('These commands are **not in the published v0.1.0 binary**. Build this source to\nuse them; this change does not publish an installer or update any release asset.','These commands are included in **v0.2.0 and later**, not the original v0.1.0\nbinary. Install the current version explicitly; no automatic upgrade is performed.')
s=s.replace('Installed commands: `create`, `connect`, `status`, `reconnect`, `detach`, `version`.','Installed commands: `server`, `client`, `create`, `connect`, `status`, `reconnect`,\n`detach`, `version`.')
p.write_text(s)
p=N/'docs/dashboard.md';s=p.read_text();s=s.replace('# Local NFS setup dashboard (source-built)','# Local NFS setup dashboard (v0.2.0+)')
s=s.replace('The dashboard is embedded in the current source build. **Published v0.1.0 does\nnot have these commands.** This source change is not a new release or platform\nqualification. You still need a supported native macOS26+ or Ubuntu24.04 host,','The dashboard is embedded in the **published v0.2.0 executable**; no separate web\ninstallation is required. Published v0.1.0 does not have these commands. See the\n[versioned download instructions](../README.md#versioned-download). Publication is\nnot field/platform qualification. You still need a native macOS26+ or Ubuntu24.04 host,')
p.write_text(s)
p=N/'TESTING.md';s=p.read_text().replace('## Source-built setup dashboard','## Setup dashboard — source tests and published launch')
s=s.replace('embedding; compilation does not retroactively add the UI to published v0.1.0.','embedding; compilation does not retroactively add the UI to published v0.1.0.\nThe dashboard is distributed starting with v0.2.0. Release launch checks use an\nactual downloaded installed binary, private HOME/TTY and an owned sandboxed\nbrowser without authorizing administration; they do not replace native storage\nor field testing.')
s+='''\n## Downloaded standalone Mac CLI verification\n\nFor the exact public binary, require strict signature/DeveloperID/team/runtime/\ntimestamp and equality to its genuine Accepted notary receipt, then run:\n\n```sh\ncodesign --verify --strict --verbose=4 --check-notarization -R=notarized /owned/path/autobyteus-nfs\n```\n\nThis forces an online notarization requirement. Apple DTS distinguishes this\n[other-code check from app assessment](https://developer.apple.com/forums/thread/130560).\nApp-style `spctl --assess --type execute` may report valid code that is not an app\nfor this standalone CLI; retain that observation, not a false Gatekeeper Pass.\nNever disable security policy or clear quarantine to manufacture a pass. Online\ncode checks and the advertised curl/CLI install are not fresh quarantined-Finder,\noffline, independent-host or physical/user qualification.\n'''
p.write_text(s)
# Scoped own cleanup; retain original new candidate and final signed payload.
ps=subprocess.check_output(['ps','-axo','pid=,command='],text=True)
owned=[line for line in ps.splitlines() if (str(S/'browsers') in line and '--remote-debugging-pipe' in line) or (str(S/'public/home/.local/lib') in line and '/autobyteus-nfs ' in line)]
assert not owned
for role in ('server','client'):
 d=json.loads((E/f'public-{role}-browser.json').read_text())
 for entry in d['browserProcesses']:
  pid=int(entry.split()[0]);assert subprocess.run(['kill','-0',str(pid)],capture_output=True).returncode!=0
for f in ('publish-current.py','resume-current.py','collect-and-verify.py','finish-docs.py'):
 if (S/f).exists():shutil.copyfile(S/f,E/f)
removed=[]
for rel in ('browser-tools','browsers','npm-cache','home','tmp','public','role-server','role-client','role-server-attempt1','final-inspection/candidate','publication-receipt-attempt1','publication-final-receipt.zip'):
 p=S/rel
 if p.exists():
  assert p.resolve().is_relative_to(S) and not p.is_symlink()
  if p.is_dir():shutil.rmtree(p)
  else:p.unlink()
 removed.append({'path':str(p),'absent':not p.exists()})
keep=[S/'candidate',S/'final-inspection/payload'];assert all(p.is_dir() for p in keep)
(E/'runtime-cleanup.json').write_text(json.dumps({'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':'Complete for own runtime/smoke/dependencies','ownedProcesses':owned,'removed':removed,'retained':[str(p) for p in keep],'retention':'Required immutable candidate/final payload through receipt and recovery; not running resources','scope':'Only this task0700 root. No user installation/config/storage, credentials/keychain settings, canonical/PM/app/superrepo or inherited candidates altered. Worktree/branches pending safe post-finalization cleanup.'},indent=2)+'\n')
print('Availability docs updated after actual public verification; only own scratch cleaned, candidate/final payload retained')
