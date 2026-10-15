# FRRouting — BGP Troubleshooting Decision Tree

Covers `session_down`, `route_missing`, and `unexpected_best_path`. Does not yet cover
`session_flapping` as its own entry point — the consulted source discusses flap-related mechanisms
(dampening, MED-driven oscillation) as side notes under other topics rather than as a dedicated
flapping-diagnosis narrative, so a dedicated flapping entry point is left for a follow-up pass rather
than assembled from those side notes.

Source consulted (2026-09-17): the official FRRouting documentation's BGP chapter,
docs.frrouting.org/en/latest/bgp.html ("latest" branch — not pinned to a specific FRR release; a
caller should confirm the installed FRR version's docs match before treating version-sensitive
defaults below, like `bgp ebgp-requires-policy` or `bgp enforce-first-as`, as certainly on/off for
their install).

## Read-only checks this file relies on

- `show bgp summary` — one line per peer, including session status and a "(Policy)" marker
  appended when `bgp ebgp-requires-policy` is configured and one direction (inbound or outbound) has
  no route-map/filter attached.
- `show bgp neighbors [<neighbor-address>] [json]` — full per-neighbor detail; the `json` form
  (optionally `json brief`) returns a structured object per neighbor.
- `show bgp <prefix>` / `show ip bgp <prefix>` — candidate paths toward a prefix, used for the
  unexpected_best_path branch.

## Entry point: session_down

1. Run `show bgp summary`. If the peer's session isn't shown as established, note whether a
   "(Policy)" marker is present — if `bgp ebgp-requires-policy` is enabled and either the inbound or
   outbound policy for that peer is missing, FRR's own documentation states routes still aren't
   accepted or announced even once the session itself is up; don't mistake a policy-driven
   no-routes-flowing condition for a session-establishment failure — check state first, policy
   marker second.
2. If the session genuinely isn't reaching Established, run `show bgp neighbors <neighbor-address>`
   and check for the specific, named failure conditions the source documents:
   - **No configured remote AS.** The source states FRR's own daemon reports this directly — its
     documented complaint text is "can't find neighbor 10.0.0.1" (substituting the real address).
     If this message appears, the neighbor statement itself is incomplete, not a wire-level problem.
   - **Capability mismatch.** The source states that when the two sides have no capabilities in
     common, FRR sends an Unsupported Capability notification and resets the connection — check
     whether the peer's advertised capabilities (address families in particular) actually overlap
     with what's configured locally.
   - **`bgp enforce-first-as` violation.** This check defaults to enabled per the source; for an
     eBGP peer, the first segment of the received AS_PATH must equal the peer's configured remote
     AS, or FRR denies the session. If the peer is inserting a different AS first (e.g. behind
     another router), this is the documented cause to check.
   - **eBGP peer not directly connected.** The source describes a connected-check that fails when an
     eBGP peer's address isn't on a directly attached interface; the documented resolution is
     configuring `disable-connected-check` on that neighbor, but only after confirming this is an
     intentional multihop design rather than a routing mistake.
   - **eBGP peer more than one hop away.** Separately from the above, the source states
     `ebgp-multihop` must be configured on the neighbor for a genuinely multihop eBGP session, or the
     session won't come up at all.
   - **Peer address only reachable via the default route.** The source notes that if the peer's
     address isn't itself present in the RIB and is only reachable through a default route, the
     `ip nht resolve-via-default` setting is required for FRR's next-hop tracking to consider the
     peer reachable.
3. If none of the above named conditions match, report the literal `show bgp neighbors` output
   (particularly `lastResetDueTo` if using the JSON form) as the evidence, and note that the
   consulted source doesn't enumerate further causes beyond these — treat anything else as
   "consult platform-specific guidance."

## Entry point: route_missing

Used when a route the caller expects to see (either received from a peer or originated locally) is
absent from the BGP table.

1. First determine whether the missing route is meant to be locally originated or received from a
   peer — the documented causes differ.
2. **Locally originated route missing:** the source documents that with `bgp network import-check`
   (on by default in the documented version line), a `network` statement only originates a prefix
   into BGP if that same prefix already exists in the RIB from some other source (interface route,
   static route, IGP, etc.) — a `network` statement alone, with no matching RIB entry, will not
   produce a BGP route. Confirm the underlying RIB entry exists first.
3. **Locally originated aggregate missing:** the source states that an aggregate can only be
   advertised if at least one more-specific (longer) prefix contributing to it is already present in
   the BGP table — an aggregate with no qualifying contributor won't appear. Separately, if
   `aggregate-address ... summary-only` is configured, the source states the more-specific
   contributing routes are intentionally suppressed from advertisement (by design, not a fault) —
   if the caller expected to see the specific rather than the aggregate, this is the documented
   cause.
4. **Received route missing (present on the peer, not appearing locally):** check for
   `bgp ebgp-requires-policy` first, per the session_down branch's step 1 — the source states that
   without an inbound policy configured under that setting, no routes are accepted from the peer at
   all, regardless of session state. This is the one route-missing cause this source documents with
   a specific, named mechanism; the source consulted this pass does not give a further structured
   list of other inbound-filtering or prefix-limit causes.
5. Report the diagnosis together with the literal `show bgp summary` policy marker and/or
   `show bgp neighbors` inbound/outbound filter state that supports it, or state explicitly that the
   consulted source doesn't cover the specific pattern observed.

## Entry point: unexpected_best_path

1. Run `show bgp <prefix>` (or `show ip bgp <prefix>`) to list every candidate path FRR holds for
   the prefix, with each path's attributes (weight, local preference, AS_PATH, origin, MED, whether
   eBGP- or iBGP-learned, IGP metric to next hop, router ID, cluster list, peer address).
2. Walk FRR's documented best-path comparison order and identify the first step at which the
   candidate paths actually differ — later steps are irrelevant once an earlier one has decided it.
   In the order the source documents (the source itself numbers its first step 0):
   0. A locally redistributed or aggregated route is preferred over a received BGP path when their
      administrative distances differ.
   1. Higher configured weight wins.
   2. Higher local preference wins.
   3. A route this router originated itself (static, aggregate, or redistributed) is preferred over
      a received one; if `bgp bestpath aigp` is enabled and both candidates carry an AIGP attribute,
      the lower AIGP value is used as a tiebreaker at this step specifically.
   4. Shorter AS_PATH wins.
   5. Lower origin type wins, ranked IGP, then EGP, then Incomplete.
   6. Among paths received from the same neighboring AS, lower MED wins.
   7. A path learned from an eBGP peer is preferred over one learned from any other peer type.
   8. Lower IGP cost to the path's next hop wins.
   9. (Multipath eligibility is evaluated here if multipath is enabled; `bgp bestpath as-path
      multipath-relax` extends multipath eligibility to paths with unequal AS_PATHs. This step
      governs whether multiple paths get installed together, not which single path wins the
      comparison below this point.)
   10. For eBGP paths, the path that is already the current selection is preferred (this
       stability-biased step is skipped if `bgp bestpath compare-routerid` is configured).
   11. Lower router ID wins — using the ORIGINATOR_ID attribute if present (iBGP route-reflection
       case), otherwise the advertising peer's own router ID.
   12. Shorter cluster list wins.
   13. Final tiebreaker: the path received from the peer with the numerically higher transport-layer
       (TCP) address wins.
3. Report the diagnosis as the specific numbered step that broke the tie, the attribute values for
   both the winning path and the path the caller expected, and the literal `show bgp <prefix>` output
   showing them — never report just "step N" without the underlying values.
4. If the paths under comparison came from the same AS and MED-driven oscillation is suspected
   (route reflectors in an iBGP topology repeatedly changing which path is best), the source flags
   this as a known non-transitive-preference edge case and documents `bgp always-compare-med` with
   uniformly configured MED values as its own suggested mitigation — note this as a possibility
   worth reporting if the observed pattern is genuinely unstable (best path changing repeatedly)
   rather than a one-time comparison.

## Explicit unknowns for this vendor (do not fill from general knowledge)

- No dedicated `session_flapping` entry point — see the note at the top of this file.
- No literal route-table status-code legend (e.g. valid/best/internal markers as printed by
  `show bgp`/`show ip bgp`) was obtained from the source this pass — don't assert specific status
  characters as FRR-documented until a page containing that legend is actually reached.
- The exact JSON field key names quoted above for `show bgp neighbors ... json brief` (hostname,
  remoteAs, localAs, lastResetDueTo, status, lastResetTimerMsecs, messageStats, addressFamilyInfo)
  came through an intermediate summarization step rather than a direct read of a raw JSON example in
  the source — treat these as indicative of the shape of the output, not as a verified literal
  schema, until confirmed against a live FRR instance or a raw copy of the doc page.
