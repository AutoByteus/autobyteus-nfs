# IMP-04 | native owned-guest protocol/privilege proof, not storage acceptance.
# Run as guest admin via an allocated SSH terminal. Binary is current task build.
import os,sys,subprocess,json,hashlib,time,select,pathlib
binary=str(pathlib.Path.home()/'dashboard-probe/autobyteus-nfs')
is_mac=sys.platform=='darwin';store='/Library/Application Support/AutoByteusNFS' if is_mac else '/var/lib/autobyteus-nfs';installed='/Library/AutoByteusNFS/libexec/autobyteus-nfs' if is_mac else '/usr/libexec/autobyteus-nfs/autobyteus-nfs'
result={'id':'IMP-04','date':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'platform':subprocess.check_output(['uname','-a'],text=True).strip(),'binarySha256':hashlib.sha256(pathlib.Path(binary).read_bytes()).hexdigest(),'cases':[]}
def cmd(args):
 r=subprocess.run(args,capture_output=True,text=True);return {'argv':args,'exit':r.returncode,'stdout':r.stdout,'stderr':r.stderr}
def receive(p):
 ready,_,_=select.select([p.stdout],[],[],15);assert ready,'private reply timeout'
 line=p.stdout.readline();assert line,'helper exited without reply';return json.loads(line)
def start():
 p=subprocess.Popen(['/usr/bin/sudo','--',binary,'internal-install','internal-dashboard-helper','client'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=sys.stderr,text=True,bufsize=1)
 hello=receive(p);assert hello['kind']=='hello' and hello['data']['digest']==result['binarySha256'] and hello['data']['role']=='client',hello;return p
seq=0
def request(p,kind,payload):
 global seq;seq+=1;p.stdin.write(json.dumps({'version':1,'id':seq,'kind':kind,'payload':payload})+'\n');p.stdin.flush();return receive(p)
def close(p):
 p.stdin.close();p.wait(timeout=15);p.stdout.close()
try:
 result['before']=cmd(['/usr/bin/sudo','--','/usr/bin/test','!','-e',store]);assert result['before']['exit']==0,'refuse nonempty guest baseline'
 p=start();reply=request(p,'inspect',{});assert reply['data']['state']=='empty',reply;result['cases'].append({'name':'actual-sudo-install-private-pipes-same-digest','result':'Pass','helloDigest':result['binarySha256'],'configuration':reply['data']})
 connection={'storageId':'11111111-1111-4111-8111-111111111111','endpoint':'192.168.64.2','export':'/owned-test-source','protocol':'3','mountRoot':'/Volumes/nfs-dashboard-privilege-proof'}
 review=request(p,'beginClient',{'connection':json.dumps(connection)});assert not review.get('error'),review;lease=review['data']['leaseId']
 busy=cmd(['/usr/bin/sudo','--',installed,'status']);assert busy['exit']!=0 and 'another administrative operation' in busy['stderr'],busy
 declined=request(p,'commit',{'leaseId':lease,'consent':False,'drained':False});assert declined.get('error') and not declined['error']['effectsMayHaveStarted'],declined
 cancel=request(p,'cancelReview',{'leaseId':lease});assert not cancel.get('error'),cancel
 replay=request(p,'commit',{'leaseId':lease,'consent':True,'drained':False});assert replay.get('error') and not replay['error']['effectsMayHaveStarted'],replay
 result['cases'].append({'name':'real-plan-lock-consent-cancel-replay-no-apply','result':'Pass','busy':busy,'review':review,'declined':declined,'replay':replay})
 close(p)
 # A still-running old parent must not start probes after installed bytes change.
 p=start();mutated=pathlib.Path.home()/'dashboard-probe/changed';mutated.write_bytes(pathlib.Path(binary).read_bytes()+b'changed-identity-control')
 assert cmd(['/usr/bin/sudo','--','/bin/cp',str(mutated),installed])['exit']==0
 changed=request(p,'inspect',{});assert changed.get('error') and 'binary changed' in changed['error']['detail'],changed
 close(p);assert cmd(['/usr/bin/sudo','--','/bin/cp',binary,installed])['exit']==0
 result['cases'].append({'name':'installed-identity-drift-refused','result':'Pass','reply':changed})
 # Close output during a held review; the next response must EPIPE, then drain/cancel.
 p=start();review=request(p,'beginClient',{'connection':json.dumps(connection)});assert not review.get('error');p.stdout.close();seq+=1;p.stdin.write(json.dumps({'version':1,'id':seq,'kind':'inspect','payload':{}})+'\n');p.stdin.flush();code=p.wait(timeout=15);p.stdin.close()
 assert code!=0;free=cmd(['/usr/bin/sudo','--',installed,'status']);assert 'another administrative operation' not in free['stderr'];result['cases'].append({'name':'root-broken-output-releases-review-lock','result':'Pass','helperExit':code,'subsequentStatus':free})
 p=start();p.stdin.write('{"version":1,"id":1,"kind":"inspect","payload":{"uid":0}}\n');p.stdin.flush();p.wait(timeout=15);assert p.returncode!=0;p.stdin.close();p.stdout.close();result['cases'].append({'name':'forged-identity-refused-before-dispatch','result':'Pass'})
 denied=cmd(['/usr/bin/sudo','--','/usr/bin/sudo','-u','nobody','--','/usr/bin/sudo','-n','--',binary,'internal-install','internal-dashboard-helper','client']);assert denied['exit']!=0;result['cases'].append({'name':'OS-denied-user-no-helper','result':'Pass','observation':denied})
 listing=cmd(['/usr/bin/sudo','--','/bin/ls','-la',store]);result['privateState']=listing;assert 'attachment.json' not in listing['stdout'] and 'pending-setup.json' not in listing['stdout']
 result['result']='Pass'
except Exception as ex:result['result']='Fail';result['error']=repr(ex);raise
finally:
 pathlib.Path.home().joinpath('dashboard-probe/result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
