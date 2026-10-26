# Routing Troubleshooting (BGP) — Vendor Index

One row per supported vendor. Each vendor directory holds its own `procedure.md` — a decision tree
organized by symptom (session down, session flapping, route missing, unexpected best-path), not a
linear operation sequence.

| Vendor / Platform | Directory | Symptoms covered | Notes |
|---|---|---|---|
| Cisco IOS-XE | `cisco-iosxe/` | session_down, unexpected_best_path | Does not cover session_flapping or route_missing — Cisco's troubleshooting tech note and best-path-selection doc do not give enough verified detail for those two; see the file's own "Explicit unknowns" section. Unverified: the IOS-XE command-reference field dictionary for `show ip bgp summary`. |
| Juniper Junos | `juniper-junos/` | session_down, session_flapping | Does not cover route_missing or unexpected_best_path — Junos's own active-route-selection/tie-break and "hidden route" behavior is not documented here; do not substitute another vendor's best-path order for Junos's own, since it is documented as its own process. Confirms the RFC 4271 session-state names are used as-is (Idle/Connect/Active/OpenSent/OpenConfirm/Established) with no naming divergence in Juniper's command references. |
| FRRouting | `frrouting/` | session_down, route_missing, unexpected_best_path | Does not cover session_flapping as its own entry point — FRR's flap-related content (dampening, MED oscillation) is scattered under other topics rather than a dedicated flapping narrative. Sourced from FRR's "latest" docs branch, not pinned to one release — version-sensitive defaults (`bgp ebgp-requires-policy`, `bgp enforce-first-as`, `bgp network import-check`) should be reconfirmed against the caller's actual installed version. FRR's own best-path order diverges from Cisco's by inserting an admin-distance check first (step 0) and an "already-selected external path" stability tiebreaker (step 10) that Cisco's documented order doesn't have — see SKILL.md's "Universal concepts" note on this. |
