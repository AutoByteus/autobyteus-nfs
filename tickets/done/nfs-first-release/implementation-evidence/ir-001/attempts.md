# IR-001 local attempts and limits

- Initial read of a guessed shared skill path failed; authoritative skill-relative
  `references/design-principles.md` was then read. No product operation involved.
- `python-attempt-1.log`: 27 collected, 3 errors/1 skip. Old source-identity tests
  imported removed facade implementation globals after ownership extraction.
  Updated them to the identity owner, retained semantic mutation/refusal controls;
  no compatibility exports were added. The shell command tailed the log and thus
  returned0 although unittest failed; the raw FAILED result remains authoritative.
- `python-attempt-2.log`: 30 tests, 1 Go-child-only skip, green at that intermediate
  input. Added publication/alias/actual-workflow controls afterward; later logs own
  current results. Duplicate ZIP warning is intentional negative-fixture input.
- `native-attempt-1/`: independent source was incorrectly placed below macOS
  `/private/var/folders`. Source-binding tests correctly rejected that ephemeral
  source location. Race suite failed (other6packages passed); vet/build/version and
  four cross-builds completed. No guard or runtime source was changed. Current
  rerun uses owned APFS development directory outside the forbidden source roots.
- `linux-attempt-1/`: Ubuntu24.04 arm64 container used a Docker Desktop host bind
  for source/HOME/TMPDIR. Python38 passed with3 explicit container/Go-child skips,
  but native administrative flock fixture detected non-native bind-lock behavior;
  Go platform suite failed. No skip or production relaxation. Retry extracts
  read-only input archives into the guest filesystem, with nonroot guest-owned
  HOME/TMPDIR/cache. Original container removed by its owned cleanup.
- Synthetic both-arch engine/OCI/signing/evidence fixtures are NOT real engine,
  Apple, user, physical or publication proof. No retained historical engine input
  was used or modified. No actual GitHub write/signing secret/hosted run performed.

- `linux-attempt-2/`: nonroot guest-filesystem Python38 (3 expected skips), all7 Go
  race packages, vet/build/version passed. The real skopeo1.13.3 OCI-archive source
  reader then attempted chown of root-owned tar directories and failed. Implemented
  the design-permitted owned OCI layout transport: validate full graph, copy exact
  index/blob bytes without adopting tar ownership, then preserve-digests copy.
  No root workaround, image rebuild, conversion or runtime change. Final transport
  check re-executes that actual path; original failure is retained.

- `native-attempt-2/`, `mutations-attempt-1/`, `linux-attempt-3/` retain successful
  intermediate snapshots. Final current runs repeat native14checkgroups, Linux
  checks/real OCI transport and all6 mutations after the final changes. The final
  native copy and Linux input archive are byte-identical to final-source-inputs.
- `final-check-delta.json` and `python-final.log` are intermediate receipts despite
  their original filenames. Current final-checks.json/checks-result.json/python.log
  and linux-checks-result.json supersede them; no deleted or rewritten failure.
