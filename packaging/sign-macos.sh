#!/usr/bin/env bash
# Narrow signing boundary; no GitHub/registry effects. Never trace secrets.
set +x
set -euo pipefail
umask 077
# Keep a diagnostic-only stderr outside the private command redirection.
exec 3>&2
[[ $# == 2 ]] || { echo 'Usage: sign-macos.sh BINARY SANITIZED_RECEIPT' >&2; exit 2; }
binary=$1
receipt=$2
failure_receipt="${receipt%.json}-failure.json"
stage=validate-inputs
diagnostic=not-collected
scratch=
keychain=
cleanup() {
  code=$?
  trap - EXIT INT TERM
  cleanup_status=complete
  if [[ -n "$scratch" ]]; then
    if [[ -f "$scratch/search.json" ]]; then
      python3 - "$scratch/search.json" >/dev/null 2>&1 <<'PY' || cleanup_status=failed
import json, subprocess, sys
subprocess.run(['security','list-keychains','-d','user','-s',*json.load(open(sys.argv[1]))], check=True, stdout=subprocess.DEVNULL)
PY
    fi
    if [[ -e "$keychain" ]]; then
      security delete-keychain "$keychain" >/dev/null 2>&1 || cleanup_status=failed
    fi
    rm -rf -- "$scratch" >/dev/null 2>&1 || cleanup_status=failed
  fi
  if [[ "$cleanup_status" == failed && "$code" == 0 ]]; then stage=cleanup; code=1; fi
  if [[ "$code" != 0 ]]; then
    # Values are fixed internal stage labels, numeric exit status and a fixed enum.
    # Never include command text/arguments, raw tool output or credential values.
    printf 'Signing failed: stage=%s exit=%s cleanup=%s diagnostic=%s\n' "$stage" "$code" "$cleanup_status" "$diagnostic" >&3
    if ! (set -o noclobber; printf '{"schema":1,"status":"Failed","stage":"%s","exitCode":%s,"cleanup":"%s","diagnostic":"%s"}\n' \
        "$stage" "$code" "$cleanup_status" "$diagnostic" > "$failure_receipt") 2>/dev/null; then
      echo 'Signing failure receipt unavailable (not overwritten)' >&3
    fi
  fi
  exit "$code"
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
sign_and_notarize() {
  for name in CERTIFICATE PASSWORD IDENTITY APPLE_ID APPLE_APP_SPECIFIC_PASSWORD APPLE_TEAM_ID; do
    value=${!name:-}
    [[ -n "$value" && "$value" != REPLACE_ME_BEFORE_RELEASE ]] || exit 1
  done
  unset value
  stage=validate-identity
  [[ "$IDENTITY" == 'Developer ID Application: '*" ($APPLE_TEAM_ID)" ]] || exit 1
  stage=create-scratch
  scratch=$(mktemp -d "${RUNNER_TEMP:?}/nfs-signing.XXXXXXXX")
  keychain="$scratch/signing.keychain-db"
  stage=read-search-list
  security list-keychains -d user | python3 -c 'import json,shlex,sys; json.dump(shlex.split(sys.stdin.read()),sys.stdout)' > "$scratch/search-pending.json"
  mv -- "$scratch/search-pending.json" "$scratch/search.json"
  stage=decode-certificate
  # Python's strict decoder rejects truncated/invalid certificate input; mode0600.
  printf '%s' "$CERTIFICATE" | python3 -c 'import base64,sys; open(sys.argv[1],"xb").write(base64.b64decode(sys.stdin.buffer.read(),validate=True))' "$scratch/certificate.p12"
  unset CERTIFICATE
  stage='keychain-password'
  keychain_password=$(openssl rand -hex 32)
  stage=create-keychain
  security create-keychain -p "$keychain_password" "$keychain"
  stage=unlock-keychain
  security unlock-keychain -p "$keychain_password" "$keychain"
  stage=import-certificate
  security import "$scratch/certificate.p12" -k "$keychain" -P "$PASSWORD" -T /usr/bin/codesign
  unset PASSWORD
  stage=partition-key
  security set-key-partition-list -S apple-tool:,apple:,codesign: -s -k "$keychain_password" "$keychain"
  unset keychain_password
  # Explicit --keychain alone is not sufficient for codesign lookup. Add only
  # this owned keychain, preserving prior entries/order; cleanup restores exactly.
  stage=configure-search-list
  python3 - "$scratch/search.json" "$keychain" <<'PYLIST'
import json, os, sys
prior = json.load(open(sys.argv[1]))
os.execvp('security', ['security', 'list-keychains', '-d', 'user', '-s', sys.argv[2], *prior])
PYLIST
  stage=find-identity
  security find-identity -v -p codesigning "$keychain" > "$scratch/identities.txt"
  stage=validate-identity-available
  python3 - "$scratch/identities.txt" <<'PY'
import os, sys
assert '"'+os.environ['IDENTITY']+'"' in open(sys.argv[1]).read(), 'Selected signing identity unavailable'
PY
  stage=sign
  # Capture only this failing boundary in private scratch, never in an artifact.
  # An if around one external command preserves its status; do not wrap the function.
  if codesign --force --timestamp --options runtime --keychain "$keychain" --sign "$IDENTITY" "$binary" > "$scratch/sign.txt" 2>&1; then
    :
  else
    sign_exit=$?
    diagnostic=$(python3 - "$scratch/sign.txt" "$binary" <<'PYDIAG'
import os, sys
# Fixed observations, not root-cause conclusions. Never emit input or exceptions.
try:
    with open(sys.argv[1], 'rb') as f:
        data = f.read(65537)
    if len(data) > 65536:
        result = 'output-too-large'
    else:
        lines = data.decode('utf-8').splitlines()
        warning = 'Warning: unable to build chain to self-signed root for signer '
        errors = {
            'errSecInternalComponent': 'internal-component',
            'User interaction is not allowed.': 'interaction-not-allowed',
            'The user name or passphrase you entered is not correct.': 'authentication-failed',
            'The specified item could not be found in the keychain.': 'keychain-item-not-found',
            'An expired certificate was detected.': 'certificate-expired',
            'The certificate was revoked.': 'certificate-revoked',
            'The timestamp service is not available.': 'timestamp-unavailable',
        }
        matches = {value for error, value in errors.items() if sys.argv[2]+': '+error in lines}
        if os.environ['IDENTITY']+': no identity found' in lines:
            matches.add('identity-not-found')
        if any(warning+'"'+name+'"' in lines for name in (os.environ['IDENTITY'], '(null)')):
            result = 'chain-build-warning'
        else:
            result = next(iter(matches)) if len(matches) == 1 else 'unclassified'
    print(result)
except (OSError, UnicodeError, KeyError):
    print('unavailable')
PYDIAG
    ) || diagnostic=unavailable
    # Only literal vocabulary can reach public stderr/JSON, even on parser failure.
    case "$diagnostic" in
      chain-build-warning|identity-not-found|internal-component|interaction-not-allowed|authentication-failed|keychain-item-not-found|certificate-expired|certificate-revoked|timestamp-unavailable|unclassified|output-too-large|unavailable) ;;
      *) diagnostic=unavailable ;;
    esac
    exit "$sign_exit"
  fi
  stage=verify-signature
  codesign --verify --strict --verbose=2 "$binary"
  stage=inspect-signature
  codesign -d --verbose=4 "$binary" > "$scratch/details.txt" 2>&1
  stage=validate-signature
  python3 - "$scratch/details.txt" <<'PY'
import os, sys
s=open(sys.argv[1]).read().splitlines()
assert 'TeamIdentifier='+os.environ['APPLE_TEAM_ID'] in s, 'Signed team differs'
assert 'Authority='+os.environ['IDENTITY'] in s, 'Signed identity differs'
assert any('runtime' in x and 'flags=' in x for x in s), 'Hardened runtime missing'
assert any(x.startswith('Timestamp=') for x in s), 'Secure timestamp missing'
PY
  stage=notary-archive
  ditto -c -k --keepParent "$binary" "$scratch/notarize.zip"
  stage=notary-submit
  notary_exit=0
  xcrun notarytool submit "$scratch/notarize.zip" --apple-id "$APPLE_ID" --password "$APPLE_APP_SPECIFIC_PASSWORD" --team-id "$APPLE_TEAM_ID" --wait --output-format json > "$scratch/notary.json" || notary_exit=$?
  stage=notary-receipt
  receipt_exit=0
  python3 - "$scratch/notary.json" "$binary" "$receipt" <<'PY' || receipt_exit=$?
import hashlib, json, os, re, sys
r=json.load(open(sys.argv[1]))
assert r.get('status') in ('Accepted', 'Invalid', 'Rejected', 'In Progress'), 'Unknown notary status'
assert re.fullmatch(r'[a-fA-F0-9-]{36}', r['id']), 'Notary submission identity missing'
result={'status':r['status'],'submissionId':r['id'],'teamId':os.environ['APPLE_TEAM_ID'],
        'binarySha256':hashlib.sha256(open(sys.argv[2],'rb').read()).hexdigest()}
with open(sys.argv[3],'x') as f: json.dump(result,f,indent=2);f.write('\n')
PY
  # Preserve a real notary command failure even if its output cannot form a receipt.
  [[ "$notary_exit" == 0 ]] || { stage=notary-submit; exit "$notary_exit"; }
  [[ "$receipt_exit" == 0 ]] || exit "$receipt_exit"
  stage=notary-accepted
  python3 - "$receipt" <<'PY'
import json, sys
assert json.load(open(sys.argv[1]))['status'] == 'Accepted', 'Notarization not Accepted'
PY
}
# Run as an ordinary simple command, NOT an if/|| predicate (which disables
# errexit within a Bash function). Only controlled diagnostics leave this boundary.
sign_and_notarize >/dev/null 2>&1
# A standalone binary cannot be stapled. Downloaded online verification is separate.
