from common import *
c=json.loads((E/'environment.json').read_text());P=Path(c['S']);R=P/'repo';env=c['envS']
case='S03'
pre=['pnpm','-C','autobyteus-server-ts','exec','vitest','run']
try:
 event(case,'Started','Rerun exact restored replay fixtures first, then full affected suite')
 run('consumer-fixture-confirm',pre+['tests/unit/agent-execution/backends/antigravity/agy-stream-event-converter.test.ts','tests/unit/agent-execution/backends/codex/thread/codex-model-call-timing.test.ts','--maxWorkers=1','--no-watch'],R,env)
 case='S03';event(case,'Started','Broader affected ownership/runtime/path/terminal regression')
 run('consumer-unit-confirm',pre+['tests/unit/agent-execution/backends','tests/unit/agent-execution/services','tests/unit/agent-execution/agent-provider-factory-builder.test.ts','tests/unit/workspaces','tests/unit/services/terminal-streaming','tests/unit/runtime-management/codex','tests/unit/agent-execution/agent-run-manager.test.ts','tests/unit/services/terminal/pty-session-manager.test.ts','--maxWorkers=2','--no-watch'],R,env)
 event(case,'Completed','Affected regression suite passed; live-gated skips retained separately','Pass','consumer-unit-confirm.log; consumer-fixture-confirm.log; fixture-restoration.json')
 case='S04';event(case,'Started','Local socket/inject file and skill API contracts')
 run('consumer-routes',pre+['tests/e2e/file-explorer/workspace-content-rest.e2e.test.ts','tests/e2e/skills/github-skill-sources-graphql.e2e.test.ts','tests/e2e/agent-definitions/agent-package-private-skills.e2e.test.ts','--maxWorkers=1','--no-watch'],R,env)
 event(case,'Completed','Ordinary file/skill local transport and filesystem cases passed','Pass','consumer-routes.log')
 case='S05';event(case,'Started','Current-build run/memory layout/native PTY and WebSocket lifecycle')
 run('consumer-path-pty',pre+['tests/integration/agent-execution/agent-run-manager.integration.test.ts','tests/integration/agent-execution/agent-run-manager.memory-layout.real.integration.test.ts','tests/e2e/terminal/terminal-websocket-lifecycle.e2e.test.ts','--maxWorkers=1','--no-watch'],R,env)
 event(case,'Completed','Local run registration/memory and actual native PTY/WebSocket lifecycle passed','Pass','consumer-path-pty.log')
 case='S06';event(case,'Started','Generic launcher and disabled Guide/localization tests')
 run('consumer-launcher',['python3','-m','unittest','scripts.tests.test_public_docker_launcher_shared_workspace','scripts.tests.test_public_docker_launcher_stop','-v'],R,env)
 run('consumer-guide',['pnpm','-C','autobyteus-web','test:nuxt','components/settings/__tests__/NfsGuideCard.spec.ts','components/settings/__tests__/NodeManager.spec.ts','components/settings/__tests__/DockerNodeStartGuideCard.spec.ts','utils/__tests__/nfsLauncherCommands.spec.ts','--run','--maxWorkers=2'],R,env)
 run('consumer-localization',['pnpm','-C','autobyteus-web','guard:localization-boundary'],R,env)
 run('consumer-web-boundary',['pnpm','-C','autobyteus-web','guard:web-boundary'],R,env)
 event(case,'Completed','Generic launcher and Guide/guards passed; explicit skips in log; carried Guide render inputs verified','Pass','consumer-launcher.log; consumer-guide.log; consumer-localization.log; consumer-web-boundary.log; source-contract-audit.json')
except Exception as e:
 event(case,'Completed',str(e),'Fail','commands.jsonl; latest log')
 raise
