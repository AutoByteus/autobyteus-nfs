#!/bin/bash
set -eu
R=/home/admin/dashboard-checks
mkdir "$R/final-src"
tar -xzf /home/admin/dashboard-probe/final-check-source.tar.gz -C "$R/final-src"
export HOME="$R/home" TMPDIR="$R/tmp" GOCACHE="$R/cache" GOTOOLCHAIN=local
export PATH="$R/tools/go/bin:/usr/local/bin:/usr/bin:/bin"
cd "$R/final-src"
echo "source=$(git rev-parse HEAD)"; git diff --stat
go version; cc --version | head -1
set +e
go test -race -timeout 120s ./... > "$R/go-final.log" 2>&1; a=$?
go vet ./... > "$R/vet-final.log" 2>&1; b=$?
python3 -m unittest discover -s scripts/tests -p 'test_nfs_*.py' -v > "$R/python-final.log" 2>&1; c=$?
printf '{"raceExit":%s,"vetExit":%s,"pythonExit":%s}\n' "$a" "$b" "$c" > "$R/final-result.json"
cat "$R/final-result.json"
