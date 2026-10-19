# IMP-07-20 — Evidence metadata notes

Step: evidence audit; source3f67e36193c246ca08b49cda818be5c0f94eba51;
Darwin arm64; 2026-10-19.

No unexpected failing product check in this round. Native missing-membership
failures and fixture mutants/original-code failure are intentional controls.
The preliminary focus log reports the then-HEAD79e3539 but exercised the dirty
signer/test bytes later committed unchanged as3f67e36; a footer and result field
explicitly clarify that distinction. The final full run is committed3f67e36.

Two copied runner JSON check-ID labels were corrected to match their filenames
(IMP-07-15 copy, IMP-07-16 cleanup); commands, inputs and observed values were
unchanged. The runner source now emits those labels. This bookkeeping correction
is not a rerun or a product change. Final full-run results replace the preliminary
summary; the preliminary focus result is retained separately as IMP-07-04.

All controlled native probes restored the exact original search list and removed
owned keychains/private inputs. Final fixture runner removed its independent
source/HOME/TMP. No candidate, user credential, canonical checkout, PM data or
other owner's evidence was modified. Ignored worktree caches are not treated as
disposable or included in the commit. No source push/hosted dispatch/release.
