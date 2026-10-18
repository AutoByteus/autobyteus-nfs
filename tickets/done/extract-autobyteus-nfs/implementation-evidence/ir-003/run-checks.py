from pathlib import Path
import subprocess,tempfile,shutil,json,hashlib,time
E=Path(__file__).resolve().parent
S=Path('/Users/normy/autobyteus_org/autobyteus-worktrees/extract-autobyteus-nfs')
P=Path(tempfile.mkdtemp(prefix='nfs-extract-ir003-',dir='/Users/normy/autobyteus_org'))
(E/'scratch-path.txt').write_text(str(P)+'\n');R=P/'repo';R.mkdir()
fixtures={x['path'] for x in json.loads((E.parent.parent/'evidence/api-e2e/api-rev-001/fixture-restoration.json').read_text())['files']}
inputs=[]
for rel in subprocess.check_output(['git','-C',str(S),'ls-files','-z']).decode().split('\0'):
 if not rel or (rel.startswith('tickets/') and rel not in fixtures):continue
 f=S/rel
 if not f.is_file():continue
 d=R/rel;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,d)
 inputs.append(dict(path=rel,sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
for d in ['home','tmp']:(P/d).mkdir()
env={'PATH':'/Users/normy/.nvm/versions/node/v22.21.1/bin:/opt/homebrew/bin:/usr/bin:/bin','HOME':str(P/'home'),'TMPDIR':str(P/'tmp'),'CI':'true','COREPACK_ENABLE_DOWNLOAD_PROMPT':'0'}
(E/'check-environment.json').write_text(json.dumps(dict(scratch=str(P),env=env,source_head=subprocess.check_output(['git','-C',str(S),'rev-parse','HEAD'],text=True).strip(),input_count=len(inputs),fixtures=sorted(fixtures)),indent=2)+'\n')
(E/'source-inputs.json').write_text(json.dumps(inputs,indent=2)+'\n')
checks=[
 ('install',['pnpm','install','--frozen-lockfile']),
 ('build',['pnpm','-C','autobyteus-server-ts','test:integration:prepare']),
 ('typecheck',['pnpm','-C','autobyteus-server-ts','typecheck']),
 ('unit',['pnpm','-C','autobyteus-server-ts','exec','vitest','run','tests/unit/agent-execution','tests/unit/workspaces','tests/unit/services/terminal-streaming','tests/unit/services/terminal/pty-session-manager.test.ts','tests/unit/runtime-management/codex','tests/unit/agent-memory','tests/unit/skill-update-notices','--maxWorkers=2','--no-watch']),
 ('integration',['pnpm','-C','autobyteus-server-ts','exec','vitest','run','tests/integration/application-backend/brief-package-team-prompt.integration.test.ts','tests/integration/skill-update-notices','--maxWorkers=1','--no-watch']),
 ('core-units',['pnpm','-C','autobyteus-ts','exec','vitest','run','tests/unit/agent/platform-input-preface-memory.test.ts','tests/unit/agent/loop/llm-response-stream-collector.test.ts','tests/unit/agent/pipelines/llm-response-pipeline.test.ts','--maxWorkers=2','--no-watch']),
 ('nuxt-prepare',['pnpm','-C','autobyteus-web','exec','nuxt','prepare']),
 ('guide',['pnpm','-C','autobyteus-web','test:nuxt','components/settings/__tests__/NfsGuideCard.spec.ts','components/settings/__tests__/NodeManager.spec.ts','components/settings/__tests__/DockerNodeStartGuideCard.spec.ts','utils/__tests__/nfsLauncherCommands.spec.ts','--run','--maxWorkers=2']),
 ('localization',['pnpm','-C','autobyteus-web','guard:localization-boundary']),
 ('web-boundary',['pnpm','-C','autobyteus-web','guard:web-boundary']),
 ('launcher',['python3','-m','unittest','scripts.tests.test_public_docker_launcher_shared_workspace','scripts.tests.test_public_docker_launcher_stop','-v']),
]
out=[]
for name,cmd in checks:
 t=time.time()
 with (E/f'{name}.log').open('w') as log:
  log.write('$ '+' '.join(cmd)+'\n');log.flush()
  r=subprocess.run(cmd,cwd=R,env=env,stdout=log,stderr=subprocess.STDOUT)
 out.append(dict(name=name,command=cmd,exit=r.returncode,seconds=round(time.time()-t,3)))
 (E/'checks-result.json').write_text(json.dumps(out,indent=2)+'\n')
 print(name,r.returncode,flush=True)
 if r.returncode:break
mismatches=[v['path'] for v in inputs if (S/v['path']).read_bytes()!=(R/v['path']).read_bytes()]
(E/'input-integrity.json').write_text(json.dumps(dict(files=len(inputs),mismatches=mismatches),indent=2)+'\n')
assert not mismatches
raise SystemExit(any(c['exit'] for c in out))
