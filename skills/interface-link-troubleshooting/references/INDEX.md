# Interface / Link Troubleshooting — Vendor Index

One row per supported vendor. Each vendor directory holds its own `procedure.md` — a decision tree
organized by symptom (interface down, flapping, high errors/discards, duplex/speed mismatch, no link
light), not a linear operation sequence.

| Vendor / Platform | Directory | Symptoms covered | Notes |
|---|---|---|---|
| Cisco IOS-XE | `cisco-ios-xe/` | interface_down, flapping, high_errors, duplex_mismatch, no_link | Strongest-sourced of the three vendors added so far — errdisable causes/recovery and the duplex-mismatch/CRC guidance are both grounded in retrieved Cisco pages. Field-by-field prose definitions for every `show interfaces` counter were not retrieved (only field names from sample output); flagged inline. |
| Juniper Junos | `juniper-junos/` | interface_down, flapping, no_link (partial); high_errors and duplex_mismatch are explicit stubs pending further research | Damping-interfaces behavior (including the documented caveat that Junos does not distinguish "down from suppression" vs. "down for real" in its state display) is the strongest-confirmed part. No Junos-specific duplex-mismatch or full error-counter-field documentation was retrieved this pass — do not assume Cisco's or Arista's documented behavior carries over. |
| Arista EOS | `arista-eos/` | interface_down, flapping (partial), high_errors (partial), duplex_mismatch (partial), no_link | Link Fault Signaling's documented behavior/actions are confirmed; its exact CLI and Dynamic Link Flap Damping's mechanism/defaults were not retrieved. Standard interface error-counter field names were not confirmed (source page returned 403) — high_errors intentionally avoids asserting unconfirmed field names. |
