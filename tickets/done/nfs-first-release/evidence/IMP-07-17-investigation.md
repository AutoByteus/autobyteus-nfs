# IMP-07-17 — Controlled diagnosis and bounded correction

Command/step: inspect DR011 receipts/current signer and installed codesign manual;
execute IMP-07-01/02/03 native probes (scripts beside results).
Input commit: 79e35392bfe4f795464fecd8c034670b622c1684.
Environment/date: macOS26.5.2 build25F84 arm64, /bin/bash3.2.57,
/usr/bin/openssl LibreSSL3.3.6; 2026-10-19.

## Observed, not inferred

DR011 actual hosted run39210821088/1 at main72b8a4 failed both Mac targets with
sign/exit1/cleanupcomplete/unclassified. Exact raw codesign output no longer
exists: cleanup removed the private capture as required. This receipt cannot
prove the previous failure's cause. Notary did not run. Prior CRR009/010/API005
remain exact-input successful prepublication evidence; no product Pass is inferred.

The historical superrepo comparison IMP-06-18 identified explicit temporary
keychain search-list membership as a difference. Instead of shipping another
pattern-only increment or guessing a credential failure, this round tested that
specific lookup boundary with real local security/codesign commands and newly
generated disposable inputs. No real signing identity/P12/password was read or
exported, no trust store changed, no Apple timestamp/notary call or release action.

- IMP-07-01: security create-keychain succeeded and created the exact supplied
  signing.keychain-db path (no extra -db suffix), but did NOT insert it into the
  user search list. An intentionally missing identity produced exit1 and exactly
  the identity-prefixed `no identity found` form. This form was unrecognized by
  IR006's binary-prefixed error map. The own binary copy remained unchanged.
- IMP-07-02: a newly generated self-signed code-signing identity was imported and
  partitioned with the production's narrow flags. Without membership, explicit
  codesign --keychain still returned identity-prefixed no-identity/exit1. Prepending
  only that owned keychain to the original list yielded sign0 and strict verify0.
- IMP-07-03 repeated this as A/B/A: original membership → failure1; owned+original
  → sign0, strict verify0 and runtime flag present; remove owned membership again
  → same lookup failure1. Explicit security find-identity (without -v) saw the
  synthetic identity throughout. The -v query correctly did NOT report this
  untrusted synthetic identity as a valid Developer ID. This limitation matters:
  the probe is a controlled lookup reproduction, not the entire hosted pipeline.
- All probes restored the byte-identical original search list, deleted their
  owned keychains and removed their scratch. Only structured booleans/exits left
  the probe; no generated private key, P12 or raw command output was retained.

The synthetic probe used --timestamp=none solely to prevent an Apple network
request with a throwaway identity. Production still requires --timestamp,
Developer ID/team validation, strict verification, hardened runtime and Accepted
notary. There is no ad-hoc/self-signed production path or fallback.

## Evidence-based repair and limits

The demonstrated local defect is missing owned-keychain membership in codesign's
lookup context. The repair prepends only the newly created temporary keychain to
the captured original list before identity validation/signing. Original entries,
order and exact cleanup restoration stay intact; no default-keychain change,
-A permission, trust override, intermediate import, credential replacement,
retry or signature-policy weakening. A configuration-command failure preserves
its exit and stops before signing. The fixed diagnostic vocabulary additionally
recognizes only the exact identity-prefixed literal actually observed above;
unknown or ambiguous output remains unclassified and all raw output private.

This is not a claim that either hosted Mac emitted that literal or that DR011's
original cause is conclusively identified. The new current-source hosted path
must establish both real imported Developer ID operations and both Accepted
notary receipts. A current candidate/readiness is needed because the signer is
production-hashed. Delivery owns that later staging/publication. A continued
failure requires its actual current controlled observation, not relabelling old
receipts or speculative secret reprovision. All six secrets remain provisioned.

## Primary contract context

The installed codesign(1) --keychain section distinguishes explicit identity
selection from the normal chain search list; the observed lookup behavior above
is stronger evidence for this environment than assuming create-keychain adds
membership. The historical exact action source also explicitly configures the
list: https://github.com/Apple-Actions/import-codesign-certs/blob/63fff01cd422d4b7b855d40ca1e9d34d2de9427d/src/security.ts
No assertion of latest superrepo/Action hosted success, and its broader -A/list
replacement, disabled timestamp or raw-output handling is not copied.
