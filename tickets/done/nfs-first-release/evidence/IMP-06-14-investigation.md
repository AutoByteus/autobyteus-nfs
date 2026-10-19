# IMP-06-14 — Codesign boundary investigation

- Step: inspect actual DR009 receipts/production command, installed codesign/security contracts and primary Apple/GitHub guidance.
- Input commit: b279d556e2c0f5e90ca24b61c7e67bc809644947; failed published-source run at f830c50bf1238270343afce151dd05b65b10237a.
- Environment/date: local Darwin arm64, read-only documentation and supplied Delivery evidence; 2026-10-19.

## Established evidence

DR009 `delivery-evidence/dr-009/signing-artifact-receipts.json` has matching
arm64/amd64 sanitized failure members: sign / exit1 / cleanup complete. The
normal strict command sequence reached codesign after import, partition-list and
selected-identity checks. It never reached notary. No raw codesign diagnostic was
retained. Therefore it would be false to identify an app-password, chain, ACL,
keychain lock or timestamp-service root cause from that receipt alone.

DR007's local existing-identity development build was Accepted by Apple. It did
not exercise hosted P12 import/temporary keychain or final Intel signing. Its
signed diagnostic and all API candidates are preserved untouched. Implementation
neither exports credentials nor changes the user's keychain/trust settings.

## Dependency contracts, not proof of this hosted cause

[Apple DTS](https://developer.apple.com/forums/thread/712005) explains that code
signing failures depend on the execution context and identity/key access; one
internal-component diagnostic has several possible causes. It describes separate
unlock, ACL and trust investigations. The current script already unlocks, grants
codesign import access and sets a partition list. Do not infer which failed from
successful setup commands alone, or change trust settings speculatively.

The installed `codesign(1)` manual distinguishes selected identity lookup via
--keychain from certificate-chain lookup via the normal search list.
[GitHub's runner guide](https://docs.github.com/en/actions/how-tos/deploy/deploy-to-third-party-platforms/sign-xcode-applications)
shows a temporary keychain lifecycle. Neither proves that an omitted explicit
search-list update caused this run's failure. No speculative keychain/search-list
or intermediate-certificate change is made in this round.

Read-only `security error -2070 -25308 -25293 -25300 -67818 -67820` and
`security error -67885` map fixed
OSStatus values to internal-component, interaction, authentication, missing-item,
expired, revoked and timestamp-unavailable messages. These are observation labels, not a credential
verdict. A failure category only narrows the next investigation.

## Bounded next correction

Capture only the existing codesign command's output in mode0600 owned transient
scratch, classify exact known lines to a fixed vocabulary, and delete capture in
existing cleanup. No output excerpt, identity, account, argument or private file
leaves this boundary. Parser reads at most64KiB+1; unknown/ambiguous/too-large or
undecodable/parser-failure results remain nonzero with the original codesign exit.
Success is still judged by command/strict signature/notary checks, not text.

Actual hosted root cause remains unresolved. This round repairs the remaining
diagnosability gap only. Normal targeted review/current API/new complete candidate
and Delivery-owned authorized hosted continuation are needed to obtain the actual
category (or signing success). Do not mark DR009 resolved or API004 current for
these production changes. If the next real observation establishes a code defect,
return that exact evidence for its minimal repair; no fallback or gate relaxation.
