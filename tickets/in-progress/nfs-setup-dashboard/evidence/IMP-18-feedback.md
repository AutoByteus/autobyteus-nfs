# IMP-18 — IR002 chooser feedback, 2026-10-24

Commit7b0577a4f2637ddf12a74a0156e4243a41a3719c. macOS26.5.2arm64,
Go1.27.2 tagged preview from independent owned source; Playwright1.64.1,
Chromium156.0.8078.4 and WebKit27.2. Same private HOME/TMP/cache/scratch as IMP16.

Read API07's actual native-key failure/control and current production. Added a
rootless actual-UI regression in `internal/dashboard/__tests__/chooser.cjs`,
invoked by existing browser.cjs. Actual local Go HTTP/readDirectories and embedded
assets execute; only one actual response's delivery is held to deterministically
cross the user's keyboard prefix/suffix. Response content/status are not forged.
The root-protocol and clipboard doubles remain explicitly separate from native
NFS. No sudo, VM, installer, storage, user browser profile or OS clipboard touched.

**Red**: original4abea65b product plus the new regression, chooser-poll/Chromium1280,
exit1: `background listing replaced the active draft`. Actual field becomes the
whole listing path instead of the typed prefix. Exact assertion and screenshot
are IMP-17-red/result.json and the companion PNG/log. This is the supplied API07
behavior reproduced cheaply; original API native evidence is unchanged.

**Green**: same regression after7b0577a4, **16/16 cases Pass**: eight normal
server/client controls plus eight chooser cases (POST and GET completion across
active typing, each at1280/390 on both engines). Focus remains on the input;
remaining keys append to the retained prefix. Settled typing, exact explicit List,
parent/child navigation, selected source, reopening, missing-directory error and
correction all pass. An unlisted draft cannot silently select a previous listing.
No browser page errors or horizontal overflow; Stop drains the rootless fixture.
Result and PNGs are IMP-18-green/. Every fixture/context is closed and removed.

Inspected Chromium390 and WebKit390 chooser-poll images directly: label/input,
List folders, directory rows, parent/selection buttons, focus ring and manual-path
hint fit the modal. The long path uses normal input scrolling, not corrupted text;
full value and caret behavior are asserted by the real browser interaction. No
CSS/layout redesign or backend policy adjustment was needed.

IMP19 focused race/vet and2 embedding/hash Python tests pass. Initial IMP19 command
used malformed `-timeout90s`; Go reported no Go files/setup failure before tests.
Raw attempt1 remains failed. Corrected only the harness to `-timeout 90s`; current
source unchanged and dashboard race passed. Vet/Python also rerun green. No native
storage/API/field acceptance is inferred. API-REV-001 remains its own Fail81.43
until affected validation; scoped passing native checks are not reopened.
