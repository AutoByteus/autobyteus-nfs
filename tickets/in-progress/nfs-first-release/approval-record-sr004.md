# SR004 / R3 approval — release before field testing

Task autobyteus-nfs-3 / nfs-first-release. Date2026-10-18. **Approved**.

Source: Delivery's `delivery-evidence/dr-003/user-publish-first-direction.json`, direct user conversation after being informed that candidate builds succeeded but independent/physical test hosts were unavailable.

> please publish first, then we could test. and if we found problem, then we fix

> create one official signed release first. please

This explicitly approves changed sequencing, not physical testing/user verification. R3 changes REQ003/007/008/009 and AC002/005/007/008, related BEH002/004/006 and SCN002–005/007 plus new SCN008. Normal v0.1.0/four build targets and signed Mac/Accepted notarization remain. No beta, fake qualifiedTargets/userVerified, old API promotion, live storage mutation or unsigned shortcut.

Solution Designer has reviewed the current qualification/metadata/installer/publisher path and approves within-direction implementation details: release-authorized installability distinct from deferred field validation, fresh current-source release checks, explicit postpublication test/fix custody. Supplement `postpublication-testing-plan.md` defines only the deferred scope/ownership, not execution or another prerequisite. No repeated questionnaire is needed.

User informed in Solution Designer conversation2026-10-18: “I’ll record your ‘publish first, test afterward’ direction and revise the release gates accordingly. Signing, notarization, artifact integrity, and host-data protections will remain mandatory; physical and user testing will be marked deferred, not passed.”

Prior R2/SR002 preserved in Git and `evidence/release-first/sr004/prior-requirements-doc.md`. It no longer controls prepublication physical/user requirements. Runtime safety/identity/signing constraints it preserved still apply. Current executable gate is unchanged until implementation; this approval does not authorize manually bypassing it.
