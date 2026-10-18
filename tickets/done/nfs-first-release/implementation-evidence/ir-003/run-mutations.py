"""Owned local mutation sensitivity checks, not release evidence."""
import json,os,shutil,subprocess
from pathlib import Path
E=Path(__file__).resolve().parent;ROOT=E.parents[4];S=Path((E/'scratch-path.txt').read_text().strip());src=S/'mutation-source'
shutil.copytree(S/'source',src)
env={'PATH':str(S/'go/bin')+':/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin','HOME':str(S/'home'),'TMPDIR':str(S/'tmp'),
     'GOCACHE':str(S/'cache'),'GOMODCACHE':str(S/'modcache'),'GOTOOLCHAIN':'local','PYTHONDONTWRITEBYTECODE':'1'}
py=['/usr/bin/python3','-m','unittest','discover','-s','scripts/tests','-v','-p']
go=['go','test','./internal/cli','-run','TestReleaseAdmissionCurrentSchemaAndClaims','-v']
cases=[
 ('authorization','packaging/release_support/readiness.py',"authorization['requirementsRevision'] == 'R3/SR004'","True",py+['test_nfs_release_records.py']),
 ('source-applicability','packaging/release_support/readiness.py',"record['sourceHash'] == c['sourceHash']","True",py+['test_nfs_release_records.py']),
 ('field-claim','packaging/release_support/readiness.py',"record['fieldValidation'] == i.DEFERRED_FIELD_VALIDATION","True",py+['test_nfs_release_records.py']),
 ('notes-disclosure','packaging/release_support/payload.py',"(assets / 'release-notes.md').read_text() == readiness.release_notes(q)","True",py+['test_nfs_release_records.py']),
 ('provenance-disclosure','packaging/release_support/payload.py',"provenance['fieldValidation'] == q['fieldValidation']","True",py+['test_nfs_release_records.py']),
 ('engine-reset','packaging/engine/manifest.py',"lock['releaseReadiness']=None","pass # omitted readiness invalidation",py+['test_nfs_engine_packaging.py']),
 ('legacy-claim','internal/cli/verify-release.go','decoder.DisallowUnknownFields()','// omitted strict release fields',go),
 ('false-runtime-claim','internal/cli/verify-release.go','manifest.Schema != 2 || manifest.FieldValidation != (setup.FieldValidation{Filesystem: "deferred", User: "deferred"})','false',go),
]
results=[]
for name,file,before,after,args in cases:
 p=src/file;original=p.read_text();assert before in original,(name,before)
 p.write_text(original.replace(before,after))
 try:
  with (E/('mutation-'+name+'.log')).open('w') as log:r=subprocess.run(args,cwd=src,env=env,stdout=log,stderr=subprocess.STDOUT)
  raw=(E/('mutation-'+name+'.log')).read_text()
  detected=r.returncode!=0 and ('FAIL:' in raw or '--- FAIL:' in raw) and 'build failed' not in raw
  results.append({'name':name,'file':file,'command':args,'exitCode':r.returncode,'detectedAssertion':detected});print(results[-1],flush=True)
 finally:p.write_text(original)
(E/'mutations.json').write_text(json.dumps(results,indent=2)+'\n')
assert all(x['detectedAssertion'] for x in results)
