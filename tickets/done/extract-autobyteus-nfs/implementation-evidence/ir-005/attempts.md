# IR005 attempts
1. Initial preparation script used E.parents[3] instead of E.parents[4] for N,
   copied ticket files to owned baseline, and failed on missing
   tickets/packaging/release-lock.json before container or tests. Preserved script
   and result in attempt-1. Corrected root; discarded only that wrong owned copy;
   official SHA-verified Go downloads reused.
2. Native Linux baseline hosted-config run expected exit1 and reproduced the
   actual CI errors/panic. This is failure reproduction, not a candidate pass.
3. Corrected native Linux and Darwin checks passed first run. Three mutation
   copies deliberately fail named assertions; no mutation entered source.
