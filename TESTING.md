# Testing AutoByteus NFS

## Prerequisites and local checks

From this repository root, use Go (go.mod minimum 1.25.0; CI pins 1.27.2), Python3
stdlib and Bash on Linux or macOS. Go tests require Python3 for the bootstrap
permission fixture. No Node/pnpm, AutoByteus checkout, Go replace or sibling
module is needed. Install toolchains outside the source tree or in owned scratch.

```sh
go test -race ./...
go vet ./...
go build -o out/autobyteus-nfs ./cmd/autobyteus-nfs
out/autobyteus-nfs version
python3 -m unittest discover -s scripts/tests -p 'test_nfs_*.py' -v
bash -n scripts/public/nfs/install.sh
python3 packaging/release.py --source-hash
```

With actionlint installed, run `actionlint .github/workflows/*.yml` for workflow
syntax. Python workflow fixtures check a deliberate boolean subset, not hosted
Actions. The placeholder installer and `python3 packaging/release.py
--check-publish` must refuse while the lock is unqualified; refusal is expected,
not a working public install command.

Use `CGO_ENABLED=0 GOOS=<darwin|linux> GOARCH=<arm64|amd64> go build -o
<owned-output> ./cmd/autobyteus-nfs` for compilation. Cross-compiled tests/binaries
are not runtime qualification. `-race` needs a matching native compiler; do not
silently drop it and claim race coverage.

## Evidence layers and isolation

Unit/fixture checks exercise temporary files and doubled command/Docker
boundaries. The native Mac source test reads diskutil for its own test directory;
it does not reboot or qualify NFS. The installer Python suite's Go-child mode is
covered by TestBootstrapDirectoryModes, and explicitly skips without that child
when run alone; container-host skip is intentional. Record skips, not Pass.

Run extraction checks in an independent source archive/clone with a private
HOME/TMPDIR and no sibling checkout. Keep current candidate source/commit,
commands, logs, platform and tool versions in ticket evidence. Build outputs,
engine bundles, generated release metadata and caches belong to owned scratch;
never use old builds as proof of current source or commit these generated inputs.
Preserve unowned files and stop/remove only processes and scratch you created.

Ordinary development checks need no root, mounts/exports, live Docker nodes,
provider credentials, user app data, or published release. Do not invoke installed
create/connect/reconnect/detach as a test. A necessary live integration campaign
requires separately scoped, test-owned resources and authorization; neither a
passing fixture nor this repository extraction authorizes one.

Packaging checks may copy an exact retained engine candidate read-only into own
scratch and freshly verify it with packaging/engine/manifest.py. Distinguish actual
arm64 artifact checks from synthetic both-architecture controls; never invent an
amd64 artifact or reuse old source qualification. No engine rebuild is needed
when unchanged verified artifacts suffice. Distribution gates are in
[packaging/RELEASE.md](packaging/RELEASE.md).

When updating a producer contract, compare the consumer snapshot with
`git show <recorded-producer-commit>:testdata/attachment.json`, then run actual Go
producer and app-owned TS parser/launcher checks. Keep both commits/hashes in the
paired evidence. Each repository's ordinary tests run offline on its own fixture.
Consumer checks and their tooling live in the app repository, not this one.

Fix demonstrated in-scope failures; disclose failed attempts and environmental
limits. New behavior/design needs return to its owner. Do not silently weaken
checks or reopen unrelated completed filesystem/editor work. No test result is
user verification, physical/platform qualification or release authorization.
