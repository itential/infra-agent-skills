# Juniper Junos — BGP Troubleshooting Decision Tree

Covers `session_down` and `session_flapping`. Does not cover `route_missing` or `unexpected_best_path` — Junos's own active-route-selection tie-break order and its "hidden route" concept are not documented here; another vendor's algorithm is not reused and none is invented.

Sources (2026-09-17): Juniper's own published command references for
`show bgp summary` (juniper.net/documentation/us/en/software/junos/bgp/topics/ref/command/
show-bgp-summary.html) and `show bgp neighbor` (…/show-bgp-neighbor.html). Both are Juniper's
current documentation site, not a mirror or third party.

## Read-only checks this file relies on

- `show bgp summary` — one line per peer: peer address, peer AS, inbound/outbound packet counters,
  outbound queue depth, flap count, time since the last Established/non-Established transition, and
  a state/route-count field.
- `show bgp neighbor [<neighbor-address>]` — full per-peer detail, including current state, prior
  state, the most recent protocol event, the most recent error, session duration, and flap count.

## Entry point: session_down

A peer that never reaches Established, or one whose state needs to be characterized before deciding
what to check next.

1. Run `show bgp summary`. The documented state field reports one of the RFC 4271 state names
   (Idle, Connect, Active, OpenSent, OpenConfirm) while the session is not yet Established; once
   Established, Junos repurposes that same column position to report route counts instead of a
   state word — so a numeric-looking value there means the session for that peer IS up, and this
   is not a session_down case for that peer.
2. Run `show bgp neighbor <neighbor-address>` for the peer that isn't reaching Established, and read
   the **State** field together with **Last state** and **Last event**:
   - **Idle** — Junos's own documentation describes this as the initial stage, awaiting a Start
     event. The documentation does not enumerate specific configuration mistakes that leave a
     peer stuck here; report the state and the **Last error** field's value rather than guessing
     at a cause.
   - **Connect** — awaiting completion of the underlying transport (TCP) handshake.
   - **Active** — Junos is itself initiating a new connection attempt (per the source's own
     wording, this is the stage where the router is actively trying to establish transport,
     distinct from passively waiting).
   - **OpenSent** — the local side has sent its OPEN message and is waiting on the peer's OPEN in
     return.
   - **OpenConfirm** — an OPEN was received from the peer and acknowledged; the session is waiting
     on a KEEPALIVE (or a NOTIFICATION) before moving to Established.
   Junos's own documented state names match RFC 4271's set exactly here — no naming divergence was
   found for the state names themselves in the documentation (see SKILL.md's "Universal
   concepts" note on this — Junos is confirmed-consistent with the RFC's state vocabulary, at least
   for this command's output).
3. Check the **Last error** field. Documented values include "None", "Hold Time Expired", "Finite
   State Machine Error", and "Cease" — report whichever literal value is present. The documentation documents what these values mean at a vocabulary level (a hold-timer expiry, an internal
   state-machine violation, or a Cease notification) but does not give a further structured
   breakdown of every root cause behind each — treat further root-causing as "consult
   platform-specific guidance" beyond reporting the literal error string and the state history
   (**Last state**, **Last event**) as evidence.
4. If the evidence doesn't resolve to one of the above, report the full literal `show bgp neighbor`
   output as the evidence and note this vendor's documentation doesn't go further for this
   specific combination of fields.

## Entry point: session_flapping

A peer that reaches Established but does not stay there — repeated transitions.

1. Run `show bgp summary` and read the **Flaps** field for the peer — this is Junos's running count
   of how many times that session has dropped and come back up. A non-zero and climbing value
   confirms this is genuinely a flapping session rather than a one-time drop; note the count as part
   of the reported evidence.
2. Run `show bgp neighbor <neighbor-address>` and read **Number of flaps** (the same counter at
   per-peer detail level) together with **Last event** and **Last error**, using the same field
   vocabulary as the session_down branch above (Idle/Connect/Active/OpenSent/OpenConfirm/
   Established for state; Open/RecvOpen/KeepAlive/RecvKeepAlive/RecvUpdate/ConnectRetry/HoldTime/
   Closed for the last event; None/Hold Time Expired/Finite State Machine Error/Cease for the last
   error).
3. Report the diagnosis as the literal **Last error** value plus the **Last event** immediately
   preceding it (e.g. a **Last error** of "Hold Time Expired" following a **Last event** of
   "HoldTime" points at the session missing its negotiated keepalive cadence, whereas a **Last
   error** of "Cease" points at a deliberate teardown rather than a timer problem) — report both
   fields together, not the error alone, since the source documents them as separate fields for a
   reason.
4. The documentation does not give a structured list of underlying causes behind repeated
   Hold-Time-Expired or Cease events (e.g. it doesn't say "check CPU load" or "check policer drops"
   as Junos-documented remediation for this). Report the evidence and flag further root-causing as
   an explicit unknown — "consult platform-specific guidance" — rather than asserting a cause this
   source doesn't state.

## Explicit unknowns for this vendor (do not fill from general knowledge or another vendor)

- Not documented: a Junos-specific active-route-selection tie-break order — do not borrow
  Cisco's or FRR's ordering and present it as Junos's; Junos is documented to implement its own
  route-selection process and the exact tie-break sequence must come from a Junos source directly.
- Not documented: Junos "hidden" routes (routes present in the table but not active) — this is a real gap for the `route_missing` symptom category specifically,
  since a Junos-hidden route is a plausible real-world cause of "the route I expect isn't there."
- Not documented: a structured list of session-establishment root causes (AS mismatch, authentication mismatch, address-family mismatch, TCP port reachability) from Junos's own troubleshooting guidance — the two sources used here are command/field references, not a troubleshooting narrative page.
