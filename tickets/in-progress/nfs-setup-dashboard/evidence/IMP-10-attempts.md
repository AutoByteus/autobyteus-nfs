# IMP-10 — Owned Mac preparation and attempts

2026-10-24; production5f8cabf, exact development Darwinarm64 SHA86bff169…e8e1;
owned Tart Tahoe26.6.2arm64. Full source/build identity in IMP-06-current-native-build.json.

1. Preparation used `/usr/bin/test`, which is absent on this Mac image (exit127).
   It did not establish empty state. Subsequent actual authorization/metadata and
   failed-attempt root-path listing established no prior NFS installation.
2. First driver used nohup but retained the SSH controlling terminal. Its proposed
   no-TTY subprocess correctly launched a dashboard instead of returning refusal.
   Inspection showed ordinary PID798 only, no root NFS state/helper/mount. Sent
   TERM to that exact owned idle dashboard (normal graceful stop), reaped it and
   the driver; raw failed result retained in IMP-10-attempt1/. Corrected the
   *harness* to start command controls and the outer driver in new sessions;
   actual UI still uses pty.fork to establish its intended terminal. No product fix.
3. Actual Mac client plan/consent reached mount_nfs, but both guests could not ARP
   one another on default Apple shared NAT. Host bridge100 READ ONLY inspection
   showed PRIVATE members; host ip.forwarding was already1. No host configuration
   changed. Added only owned guest peer-specific routes via their existing
   192.168.64.1 gateway. The first Mac ping still selected an earlier failed scoped
   neighbor route; removed ONLY that guest's failed neighbor192.168.64.8. Actual
   route lookup then selected the gateway and2/2 peer pings succeeded. Linux route
   is peer192.168.64.2/32 via gateway. Both routes are test-owned and will disappear
   with guest cleanup. No host bridge/firewall/sysctl change, public forwarding,
   product fallback, private-state edit or forced mount cancellation. Pending
   admitted mount was left to complete normally after reachability restoration.

This is owned test-network preparation, not physical/LAN or field qualification.
It establishes no protocol failure or product acceptance by itself. Network read,
route commands, outputs and preserved pending intent are in IMP-10-network-* and
IMP-10-guest-route-* logs. Final journey result is recorded separately.
