# Interface / Link Troubleshooting — Vendor Index

One row per supported vendor. Each vendor directory holds its own `procedure.md` — a decision tree
organized by symptom (interface down, flapping, high errors/discards, duplex/speed mismatch, no link
light), not a linear operation sequence.

| Vendor / Platform | Directory | Symptoms covered | Notes |
|---|---|---|---|
| Cisco IOS-XE | `cisco-ios-xe/` | interface_down, flapping, high_errors, duplex_mismatch, no_link | Best-sourced of the vendors in this skill — errdisable causes/recovery and the duplex-mismatch/CRC guidance are grounded in Cisco's own pages. Field-by-field prose definitions for every `show interfaces` counter are not documented in the sources (only field names from sample output are); flagged inline. |
| Juniper Junos | `juniper-junos/` | interface_down, flapping, no_link (partial); high_errors and duplex_mismatch are minimal read-and-compare entries | Damping-interfaces behavior (including the documented caveat that Junos does not distinguish "down from suppression" vs. "down for real" in its state display) is the strongest-confirmed part. No Junos-specific duplex-mismatch or full error-counter-field documentation is available from the sources — do not assume Cisco's or Arista's documented behavior carries over. |
| Arista EOS | `arista-eos/` | interface_down, flapping (partial), high_errors (partial), duplex_mismatch (partial), no_link | Link Fault Signaling's documented behavior/actions are confirmed; its exact CLI and Dynamic Link Flap Damping's mechanism/defaults are unverified. Standard interface error-counter field names are unverified — high_errors intentionally avoids asserting unconfirmed field names. |
| FRRouting | `frrouting/` | interface_down, no_link (partial); flapping is observation-only; high_errors and duplex_mismatch are explicit not-documented entries | Linux hosts running zebra; FRR reads kernel interface state and documents no physical-layer diagnostics, error counters, or negotiation display. Covers administrative shutdown, `link-detect` (Linux, `IFF_RUNNING` only), and `protodown` on VRRP Backup routers. Field list of `show interface` is unverified. Behavior varies by FRR release; confirm with `show version`. FRRouting also has its own, separate directory under `routing-troubleshooting`. |

FRRouting documents no interface counters or physical-layer causes; its `protodown` state is a documented, intended condition on a VRRP Backup router, not a fault.
