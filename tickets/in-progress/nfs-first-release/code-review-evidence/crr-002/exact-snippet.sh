set -euo pipefail
python3() { printf "COMMAND_ENTERED\n"; printf "<%s>\n" "$@"; }
args=()
if [[ "$MODE" == fresh ]]; then args+=(--qualified --candidate work/candidate); fi
python3 packaging/release.py --tag "$TAG" --engine-image "$image" --engine-manifest work/candidate/engine/engine-manifest.json --engine-artifacts work/candidate/engine --target "$TARGET" --output cmd/autobyteus-nfs/release.json "${args[@]}"
