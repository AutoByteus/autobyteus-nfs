from common import *
c=json.loads((E/'environment.json').read_text());P=Path(c['S']);R=P/'repo';env=c['envS']
with (T/'api-e2e-coverage-investigation.md').open('a') as f:f.write('''
## S06 prerequisite correction
Initial Guide command collected no tests: all4 suites could not resolve .nuxt/tsconfig.json. Root TESTING.md lines70–73 explicitly requires nuxt prepare, which the API runner omitted. API-owned setup error, not a Guide/product assertion failure. Run documented pnpm -C autobyteus-web exec nuxt prepare in own archive, then exact same4 suites and guards. Preserve consumer-guide.log; no source/test/config changes.
''')
with (E/'attempts.md').open('a') as f:f.write('- S06 Guide initial4 suites collected zero tests due missing .nuxt/tsconfig.json. API omitted documented nuxt prepare. Restored prerequisite using project command; original consumer-guide.log kept, rerun consumer-guide-confirm.log, no test assertion/config edit.\n')
event('S06','Started','Correct API omission of documented Nuxt prepare before exact suite rerun')
try:
 run('consumer-nuxt-prepare',['pnpm','-C','autobyteus-web','exec','nuxt','prepare'],R,env)
 run('consumer-guide-confirm',['pnpm','-C','autobyteus-web','test:nuxt','components/settings/__tests__/NfsGuideCard.spec.ts','components/settings/__tests__/NodeManager.spec.ts','components/settings/__tests__/DockerNodeStartGuideCard.spec.ts','utils/__tests__/nfsLauncherCommands.spec.ts','--run','--maxWorkers=2'],R,env)
 run('consumer-localization',['pnpm','-C','autobyteus-web','guard:localization-boundary'],R,env)
 run('consumer-web-boundary',['pnpm','-C','autobyteus-web','guard:web-boundary'],R,env)
 event('S06','Completed','Generic launcher green; after documented Nuxt preparation all4 Guide suites and both guards passed; no product/test edit','Pass','consumer-guide-confirm.log; consumer-nuxt-prepare.log; consumer-launcher.log; consumer-localization.log; consumer-web-boundary.log')
except Exception as e:
 event('S06','Completed',str(e),'Fail','commands.jsonl; latest log');raise
