# Juniper Junos — Interface / Link Troubleshooting Decision Tree

Read-only diagnosis of physical/logical interface and link problems on Junos devices, organized by
symptom. Follow the entry point matching the observed symptom.

Source: Junos "Interfaces Fundamentals" documentation set, retrieved 2026-09-17:
- "Damping Interfaces" (physical-interface flap damping).
- "Physical Interfaces" (physical interface properties, including unidirectional-interface
  behavior and the interfaces that report FEC statistics).
- "Device Interfaces" (interface naming convention and a reference to `show interfaces terse`).

Not documented in the sources: a complete, field-by-field dictionary for `show interfaces` /
`show interfaces extensive` output. Where a specific counter name is unverified, the file says so
rather than inventing one — treat any such gap as a required live check against current Junos
documentation or the device's own command help before relying on a field name not named here.

## Naming convention (needed to read every check below)

Junos physical interface names follow the pattern `type-fpc/pic/port`, optionally with a
`:channel` suffix for channelized interfaces and a `.logical-unit` suffix for a logical unit on
that physical interface (for example `ge-1/0/0.1` for logical unit 1 on the Gigabit Ethernet port
in FPC slot 1, PIC 0, port 0). Every command below takes this same interface-name form.

## Entry point: interface_down

1. Run `show interfaces terse` to get a quick per-interface view of administrative and link state
   across the box, or `show interfaces <name>` for one interface's full detail.
2. Junos documentation draws a distinction between an interface being administratively disabled
   (an explicit configuration state) and its physical/operational link state being down for a
   different reason — confirm which of the two applies before proceeding, since the remedy differs:
   an administratively disabled interface needs the operator to decide whether to re-enable it,
   while an operationally down interface needs investigation into why.
3. If the interface is administratively enabled but the operational/link state is still down, treat
   this as a physical-layer question and continue to the no_link entry point below.
4. Junos's damping feature (documented in full under the flapping entry point) can also present as
   an interface reporting down when it has actually been temporarily suppressed after repeated
   transitions rather than being down for a fresh reason — if damping is configured on this
   interface, check the flapping entry point before concluding this is a first-time-down event.

## Entry point: flapping

1. Junos ships a documented interface-damping feature specifically to reduce how often a flapping
   physical interface's transitions get advertised further into the routing system, which makes it
   the first thing to check when an interface is reported as repeatedly transitioning.
2. Two damping mechanisms exist in Junos's own configuration model: a straightforward hold-time
   method (separate configurable delays before advertising a transition to up and to down, specified
   in milliseconds, with damping effectively off by default at a 0 ms hold time), and an exponential
   -backoff method modeled on route-flap damping (a per-flap penalty that decays over a configurable
   half-life, with configurable suppress and reuse penalty thresholds and a maximum suppression
   time). Unverified: Junos's default numeric values for the backoff method's half-life, suppress
   threshold, and reuse threshold. Do not assume a specific default; check the device's active
   configuration or current Junos documentation instead of guessing.
3. Check whether damping is configured on the interface in question, and if so, check its damping
   state (surfaced in the "Damping" field within `show interfaces extensive`'s output for that
   interface). A documented and important caveat: Junos's own interface state display does not
   distinguish, at the point you look, whether the interface is down because it is being actively
   suppressed by damping versus down for an unrelated, fresh reason — so seeing "down" while damping
   is configured is not on its own proof of which situation applies; the flap history and damping
   state together are the actual evidence, not the top-level up/down state alone.
4. If damping is not configured, or is configured but not currently suppressing the interface, the
   sources give no further Junos-specific list of documented flap root causes beyond what a
   physical-layer investigation (cabling, transceiver, remote-end behavior) would already cover.
   Report that as an explicit gap rather than fabricating a Junos-specific cause list.

## Entry point: high_errors

1. Unverified: a specific, named set of Junos `show interfaces`/`show interfaces extensive`
   error-counter fields (for example whether Junos labels a given counter "framing errors" versus
   some other name). Rather than inventing field names, run `show interfaces extensive <name>` and
   read whatever error/discard counters that platform's output actually shows, and cross-reference
   the exact field names against the device's own documentation or command help before drawing a
   conclusion from a field not named here.
2. The one specific documented counter is the FEC (forward error
   correction) statistics Junos documents for interfaces that support it — visible via `show
   interfaces <name>`. A climbing pre-FEC or post-FEC error count on an interface that supports FEC
   is evidence of a degrading physical/optical signal on that link, worth checking before assuming a
   purely logical-layer cause.
3. Report the literal counter values read, and explicitly flag if the sources give no documented
   likely-cause mapping for the specific counter observed — don't present a diagnosis the
   documentation doesn't support.

## Entry point: duplex_mismatch

Not documented in the sources: Junos-specific duplex-mismatch troubleshooting (the source pages
cover damping, physical-interface properties, and naming, not duplex negotiation). Do not assume
Junos's duplex/speed reporting or auto-negotiation conventions mirror Cisco's `a-`-prefix
convention documented in the Cisco IOS-XE file in this same skill — that convention is unverified
for Junos. This entry point therefore stops at: read the interface's configured and negotiated
speed/duplex from `show interfaces <name>`, compare against the remote end by the same means, and
flag the cause-mapping guidance as an explicit gap rather than reusing another vendor's documented
behavior.

## Entry point: no_link

1. Run `show interfaces terse` or `show interfaces <name>` and read the reported link state.
2. Junos documents a specific, narrow behavior for unidirectional interfaces (interfaces configured
   to only transmit or only receive) worth ruling in or out if the platform/interface in question
   supports that mode: a transmit-only interface is documented as always reporting operationally up
   regardless of the actual remote-end state, while a receive-only interface's operational status is
   documented as depending only on locally-detected faults, independent of what the remote end is
   doing. If this interface is configured as unidirectional, its up/down reporting does not mean what
   it would for a normal bidirectional interface — confirm this configuration before trusting the
   reported state at face value.
3. For interfaces using an encapsulation that runs keepalives (Junos documentation names HDLC and
   PPP encapsulation specifically), the line-protocol-level state is influenced by keepalive
   exchange with the remote end — a link with no physical signal problem can still show a
   protocol-level down state if keepalives aren't being exchanged, which is a different condition
   from a physical no-link-light situation and worth distinguishing before concluding it's a cabling
   or optics fault.
4. Not documented in the sources, beyond the two behaviors above: a Junos-specific physical-layer
   fault list (transceiver diagnostics, optical power readings, etc.). Flag that as an explicit gap
   rather than inventing platform-specific guidance.

## Known gaps in this vendor's coverage

- No field-by-field dictionary for `show interfaces` / `show interfaces extensive` output is
  available from the sources, so high_errors and duplex_mismatch above are intentionally
  conservative; verify counter names against the device's own command reference.
- No Junos-specific duplex-mismatch documentation was available, so the duplex_mismatch entry point
  is a minimal read-and-compare, not a decision tree built on confirmed Junos guidance.
