# IMP-16 — CR-001/API-F001 focused local-fix plan

2026-10-24, input4abea65b / unchanged product5f8cabf, R1/SR001 + SR003/ARCH002,
Large/High. Read current TESTING.md, CRR002 and API07 reproduction/settled control.
Only the ordinary chooser's path edit ownership and its durable browser coverage
are in scope; no backend, privilege, storage, schema or release change.

1. Build existing rootless tagged Go preview from an independent source copy.
2. Add actual-UI regression reproducing API07's enabled-field typing across initial
   directory completion. Hold only an actual HTTP response until keyboard prefix
   entry; release while edit is active and type suffix. No wait-until-settled before
   typing. Verify original source fails. Also cover delayed initial POST response.
3. Move input assignment to explicit list/navigation initiation, not background
   result rendering. Keep typed draft and explicit List/parent/child/selection coherent.
4. Run both browser engines/narrow+desktop, settled typing/manual List, parent,
   child, selection and error controls. Run unchanged normal UI flows and focused
   dashboard race/vet, static-embedding/source-hash Python checks. Reuse unchanged
   native/admin/API scoped results; do not repeat a storage campaign for frontend JS.
5. Inspect rendered output, preserve red/green receipts, remove only owned scratch,
   append IR002 and return through fresh targeted source-review route.

Root-protocol/clipboard doubles and response scheduling are explicitly test-only.
Actual local HTTP and embedded UI execute. This is not native NFS or API acceptance.
