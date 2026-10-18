set -euo pipefail
image=$(python3 packaging/release.py --operation oci --directory work/candidate/engine.oci.tar | python3 -c 'import json,sys; print("ghcr.io/autobyteus/autobyteus-nfs@"+json.load(sys.stdin)["index"])')
# Keep the array nonempty for Mac system Bash 3.2 under nounset.
args=(--tag "$TAG" --engine-image "$image" --engine-manifest work/candidate/engine/engine-manifest.json --engine-artifacts work/candidate/engine --target "$TARGET" --output cmd/autobyteus-nfs/release.json)
if [[ "$MODE" == fresh ]]; then args+=(--qualified --candidate work/candidate); fi
python3 packaging/release.py "${args[@]}"
