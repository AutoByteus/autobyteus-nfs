# API-03 preparation/attempts — current source deeea2f, 2026-10-24

1. Initial SSH bootstrap exited255 before a reliable SSH-ready check; stderr was not retained, so no exact transport cause asserted. Follow-up TCP22 succeeded and bootstrap/key authentication succeeded. No product invoked during this preparation.
2. First browser harness rejected its own process inventory before launching the product. Setting HOME/TMPDIR only in Chromium child environment does not control Playwright's parent-created profile path. Browser closed; no native dashboard/root state created. Original failure JSON/console retained. Correct invocation also sets private HOME/TMPDIR on the Node runner, satisfying the planned owned-profile inventory assertion; no product/assertion change.

3. Second attempt transferred the PTY harness under `pty.py`, shadowing Python stdlib pty before any product launch. Renamed only owned guest harness to driver.py; retained exact traceback. No product state was created; no product/assertion change.

4. Third attempt submitted a chooser path while its initial async listing had not completed; final DOM showed the initial home listing, not the requested child. Exact native trace/DOM retained; no storage plan applied. Normal journey now waits for initial chooser readiness. This does not establish whether early-paste UX is correct; a separate focused user-timing probe will decide after the ordinary flow. Cleanup handler initially could not click Stop behind the modal; exact idle dashboard PID1469 received normal TERM, helper drained, inventory empty. Handler now closes the chooser before Stop.

Follow-up: API07 used normal native key typing80ms/key and actual unmodified responses, reproducing the chooser input overwrite. Waiting for readiness in the successful API03 path isolates the ordinary settled-selection journey; it is not a product fix or a waiver. API07 is the separate failing case.
