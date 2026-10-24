# IMP-06 native preparation / attempts

- First SSH background launch did not survive the short PTY session: the poll
  found no process/result and the intended console file was absent. No product
  success is inferred. Rerun used a detached session (`setsid nohup`) plus a
  two-second launch observation; the public CLI itself obtains its own PTY in
  the Python driver. Original start/poll/console observations retained.
- Second launch completed the bounded Linux native server/control journey.
  Every tested setup operation ran in the owned Ubuntu24.04.5 arm64 guest. The
  guest has no browser opener; the actual public command reported that fact and
  provided its local fallback, used by the driver only inside the guest.
- Both dashboard processes exited0 in the driver's explicit assertions. The
  final `close: null` entries mean already reaped by those assertions, not an
  unobserved exit. Source/marker/mount and installed job are deliberately retained
  for the independent Mac client journey, not claimed cleaned. Helper/UI closed.
  Driver PID2249 is finished. No public release or live-user state was touched.
