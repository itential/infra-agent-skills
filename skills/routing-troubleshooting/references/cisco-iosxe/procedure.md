# Cisco IOS-XE — BGP Troubleshooting Decision Tree

Covers `session_down` and `unexpected_best_path`. Does not cover `session_flapping` or `route_missing` — Cisco's published guidance does not give enough verified detail for those two categories to write a reliable decision tree, and general BGP knowledge is not substituted.

Sources (2026-09-17): Cisco's public "Troubleshooting BGP" tech note
(cisco.com/en/US/tech/tk365/technologies_tech_note09186a008009478a.shtml) and Cisco's public
"BGP Best Path Selection Algorithm" document
(cisco.com/c/en/us/support/docs/ip/border-gateway-protocol-bgp/13753-25.html). Both are Cisco's own
published guidance, not third-party summaries. Unverified: the exact `show ip bgp summary` column dictionary from the IOS-XE command reference — see the explicit unknown below.

## Read-only checks this file relies on

- `show ip bgp summary` — one-line-per-neighbor view; the last column reads either a session state
  word (before Established) or a received-prefix count (once Established).
- `show ip bgp neighbors [<neighbor-address>]` — full per-neighbor detail, including the session
  state, counters, and the reason the last session ended.
- `show ip bgp [<prefix>] [longer-prefixes]` — the BGP table view used to see every candidate path
  toward a prefix and which one is marked as the selected/best path.

## Entry point: session_down

A peer that never reaches Established.

1. Run `show ip bgp summary` for the neighbor in question. If the state column shows anything other
   than a prefix count, the session has not reached Established — proceed to step 2. If it shows a
   number, the session IS established and this is not a session_down case (recheck the symptom
   category).
2. Run `show ip bgp neighbors <neighbor-address>` and read the reported session state:
   - **Idle** — the process is not attempting a connection. The source material does not give a
     structured breakdown of every cause of a stuck Idle state; treat this as "consult
     platform-specific guidance / verify the neighbor statement and any administrative shutdown of
     the peer" rather than a single known cause.
   - **Active** or **Connect** — a TCP-level connection attempt is in progress but not completing.
     The source's own troubleshooting guidance for this stage centers on reachability: confirm IP
     connectivity to the peer address exists at all, and check for a path MTU problem along the way
     (the source's own worked example uses `ping <peer-address> size 1400 df-bit` to test for MTU
     black-holing). Interface flapping toward the peer is called out explicitly as a trigger: by
     default, "BGP resets the neighborship if the link used in order to reach the neighbor goes
     down" — if the underlying interface/link is unstable, the session will not stabilize until that
     is fixed; the documented knob to decouple session state from link transitions is
     `no bgp fast-external-fallover` (this changes reset behavior, it does not fix a genuinely down
     link).
   - **OpenSent** / **OpenConfirm** — an OPEN message has gone out and the session is stuck waiting
     on the peer's response or acknowledgment. The documentation does not give a structured
     breakdown of causes at this specific stage; report the state and treat root-causing it further
     as an explicit unknown for this vendor file rather than guessing (e.g. do not assert AS-number
     mismatch, hold-time mismatch, or authentication mismatch as Cisco-documented causes — none of those is confirmed in the Cisco sources used here, despite being common real-world BGP failure modes).
3. If the neighbor detail output shows a recent teardown, check the reported reason. The source
   material's own logged examples for a session that came up and then dropped are the
   `BGP_SESSION-5-ADJCHANGE` messages "Peer closed the session" and "Unknown path error" — report
   whichever string actually appears rather than assuming a cause; the source does not decode what
   drove "Unknown path error" any further.
4. If nothing above explains the stuck state, report the observed state plus the literal
   `show ip bgp neighbors` output as the evidence, and note that this vendor's documentation
   don't go further for this state combination — "consult platform-specific guidance" rather than
   inventing a cause.

## Entry point: unexpected_best_path

Used when a prefix has more than one candidate path and the one actually marked best/selected isn't
the one expected.

1. Run `show ip bgp <prefix> longer-prefixes` (or `show ip bgp <prefix>`) to list every path IOS-XE
   currently holds toward the prefix, together with its attributes (weight, local preference,
   AS_PATH, origin, MED, next hop, whether it's marked eBGP/iBGP).
2. First rule out a path being excluded from consideration entirely rather than merely losing a
   tie-break. The documentation calls out three conditions under which a path won't carry the
   "valid" marker and is therefore skipped over during best-path evaluation: the path is marked
   "not synchronized" (a legacy IGP-synchronization requirement — note this may not apply to a
   modern configuration where synchronization is disabled, which is the common default; treat
   "not synchronized" appearing on a valid path as worth investigating rather than assuming it's
   always the cause), the path's next hop is not reachable through the IGP/RIB, or the path is
   marked "(received-only)," meaning an inbound policy accepted the path onto the router but blocked
   it from being used or re-advertised.
3. If every candidate path is valid, walk the vendor's documented best-path order and find the first
   criterion where the candidates actually differ — that is the deciding factor, and everything
   after it in the list is irrelevant to this particular decision. In the order this source
   documents it:
   1. Highest weight wins.
   2. Highest local preference wins.
   3. A path this router itself originated (via a `network` statement or an aggregate) is preferred
      over a received path.
   4. Shortest AS_PATH wins.
   5. Lowest origin type wins, ranked IGP, then EGP, then Incomplete.
   6. Lowest MED wins (only a meaningful tiebreaker between paths from the same neighboring AS).
   7. An eBGP-learned path is preferred over an iBGP-learned path.
   8. Lowest IGP metric to the path's next hop wins.
   9. (Multipath eligibility is evaluated here if multipath is configured — this determines whether
      more than one path gets installed, not which single path is "best" for tie-breaking purposes
      below this point.)
   10. The path that has been up the longest (received first) wins, when comparing external paths.
   11. Lowest BGP router ID wins.
   12. Shortest cluster list wins.
   13. Lowest neighbor (peer) address wins — final tiebreaker.
4. Report the diagnosis as: which numbered criterion above actually broke the tie, the attribute
   values for the winning and (at minimum) the expected path side by side, and the literal
   `show ip bgp` output that shows them — never report "criterion N wins" without also showing the
   underlying attribute values that made it true.
5. If the caller's expected path was excluded at step 2 (marked invalid) rather than losing a
   tie-break at step 3, report that as the diagnosis instead — it's a different cause requiring a
   different fix (fixing reachability or policy, not attribute tuning).

## Explicit unknowns for this vendor (do not fill from general knowledge)

- Not documented: a primary-source breakdown of `session_flapping` causes (a session that reaches Established repeatedly but doesn't stay there).
- Not documented: a primary-source breakdown of `route_missing` beyond the single documented check in
  step "verify the network statement" for locally-originated prefixes — a received prefix that
  simply never shows up (filtered inbound, maximum-prefix limit, etc.) is not covered.
- The exact column-by-column field dictionary for `show ip bgp summary` (Neighbor, AS, message
  counters, table version, queue depths, up/down time, and the shared state/prefix-count column)
  is Unverified against the Cisco command reference, despite being stable, widely-documented output across IOS-XE releases. Treat the column names used above as indicative rather than verified.
