#!/usr/bin/env bash
# Narrow signing boundary; no GitHub/registry effects. Never trace secrets.
set +x
set -euo pipefail
umask 077
[[ $# == 2 ]] || { echo 'Usage: sign-macos.sh BINARY SANITIZED_RECEIPT' >&2; exit 2; }
binary=$1
receipt=$2
for name in CERTIFICATE PASSWORD IDENTITY APPLE_ID APPLE_APP_SPECIFIC_PASSWORD APPLE_TEAM_ID; do
  value=${!name:-}
  [[ -n "$value" && "$value" != REPLACE_ME_BEFORE_RELEASE ]] || { echo "Missing/placeholder signing input: $name" >&2; exit 1; }
done
unset value
[[ "$IDENTITY" == 'Developer ID Application: '*" ($APPLE_TEAM_ID)" ]] || { echo 'Selected identity/team is not Developer ID Application' >&2; exit 1; }
scratch=$(mktemp -d "${RUNNER_TEMP:?}/nfs-signing.XXXXXXXX")
keychain="$scratch/signing.keychain-db"
cleanup() {
  code=$?
  trap - EXIT
  if [[ -f "$scratch/search.json" ]]; then
    python3 - "$scratch/search.json" <<'PY' || code=1
import json, subprocess, sys
subprocess.run(['security','list-keychains','-d','user','-s',*json.load(open(sys.argv[1]))], check=True, stdout=subprocess.DEVNULL)
PY
  fi
  if [[ -e "$keychain" ]]; then security delete-keychain "$keychain" >/dev/null 2>&1 || code=1; fi
  rm -rf -- "$scratch"
  exit "$code"
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
security list-keychains -d user | python3 -c 'import json,shlex,sys; json.dump(shlex.split(sys.stdin.read()),sys.stdout)' > "$scratch/search.json"
# Python's strict decoder rejects truncated/invalid certificate input; mode0600.
printf '%s' "$CERTIFICATE" | python3 -c 'import base64,sys; open(sys.argv[1],"xb").write(base64.b64decode(sys.stdin.buffer.read(),validate=True))' "$scratch/certificate.p12"
unset CERTIFICATE
keychain_password=$(openssl rand -hex 32)
security create-keychain -p "$keychain_password" "$keychain" >/dev/null
security unlock-keychain -p "$keychain_password" "$keychain" >/dev/null
security import "$scratch/certificate.p12" -k "$keychain" -P "$PASSWORD" -T /usr/bin/codesign > "$scratch/import.log" 2>&1
unset PASSWORD
security set-key-partition-list -S apple-tool:,apple:,codesign: -s -k "$keychain_password" "$keychain" > "$scratch/partition.log" 2>&1
unset keychain_password
security find-identity -v -p codesigning "$keychain" > "$scratch/identities.txt"
python3 - "$scratch/identities.txt" <<'PY'
import os, sys
assert '"'+os.environ['IDENTITY']+'"' in open(sys.argv[1]).read(), 'Selected signing identity unavailable'
PY
codesign --force --timestamp --options runtime --keychain "$keychain" --sign "$IDENTITY" "$binary" > "$scratch/sign.log" 2>&1
codesign --verify --strict --verbose=2 "$binary" > "$scratch/verify.log" 2>&1
codesign -d --verbose=4 "$binary" > "$scratch/details.txt" 2>&1
python3 - "$scratch/details.txt" <<'PY'
import os, sys
s=open(sys.argv[1]).read().splitlines()
assert 'TeamIdentifier='+os.environ['APPLE_TEAM_ID'] in s, 'Signed team differs'
assert 'Authority='+os.environ['IDENTITY'] in s, 'Signed identity differs'
assert any('runtime' in x and 'flags=' in x for x in s), 'Hardened runtime missing'
assert any(x.startswith('Timestamp=') for x in s), 'Secure timestamp missing'
PY
ditto -c -k --keepParent "$binary" "$scratch/notarize.zip"
notary_exit=0
xcrun notarytool submit "$scratch/notarize.zip" --apple-id "$APPLE_ID" --password "$APPLE_APP_SPECIFIC_PASSWORD" --team-id "$APPLE_TEAM_ID" --wait --output-format json > "$scratch/notary.json" 2> "$scratch/notary-error.log" || notary_exit=$?
python3 - "$scratch/notary.json" "$binary" "$receipt" <<'PY'
import hashlib, json, os, re, sys
r=json.load(open(sys.argv[1]))
assert r.get('status') in ('Accepted', 'Invalid', 'Rejected', 'In Progress'), 'Unknown notary status'
assert re.fullmatch(r'[a-fA-F0-9-]{36}', r['id']), 'Notary submission identity missing'
result={'status':r['status'],'submissionId':r['id'],'teamId':os.environ['APPLE_TEAM_ID'],
        'binarySha256':hashlib.sha256(open(sys.argv[2],'rb').read()).hexdigest()}
with open(sys.argv[3],'x') as f: json.dump(result,f,indent=2);f.write('\n')
print('Notary status: '+r['status']+'; submission: '+r['id'])
assert r['status'] == 'Accepted', 'Notarization not Accepted'
PY
[[ "$notary_exit" == 0 ]] || { echo 'Notary command failed' >&2; exit 1; }
# A standalone binary cannot be stapled. Downloaded online verification is separate.
