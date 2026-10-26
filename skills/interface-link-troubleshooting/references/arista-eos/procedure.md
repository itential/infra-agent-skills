# Arista EOS — Interface / Link Troubleshooting Decision Tree

Read-only diagnosis of physical/logical interface and link problems on Arista EOS devices,
organized by symptom. Follow the entry point matching the observed symptom.

Source: Arista EOS User Manual 4.36.2F, "Ethernet Ports" chapter, and the EOS 4.36.2F TOI
(Transfer of Information) index, retrieved 2026-09-17.

Two EOS features referenced below are documented by name only: Dynamic Link Flap Damping, and the
exact CLI for Link Fault Signaling. Their mechanism, parameters, and CLI are unverified. Each gap is
flagged at the relevant entry point rather than filled with invented detail.

## Entry point: interface_down

1. Run `show interfaces status` for a per-port summary, or `show interface <name>` (the manual's
   singular command form) for one interface's full detail.
2. Read the reported Status column. The manual's documented status values include `connected`,
   `disabled`, and `notconnect`. A `disabled` status corresponds to the port having been
   administratively shut down in configuration — confirm with the operator whether that's
   intentional before treating it as a fault.
3. A `notconnect` status means EOS is not detecting a connected link partner — treat this as a
   physical-layer question and move to the no_link entry point below rather than assuming a
   configuration cause.
4. If status reads `connected` but the caller still expected different behavior (e.g. no traffic
   passing despite an up port), that's outside this interface_down entry point — check high_errors
   or hand off to a higher-layer troubleshooting skill, since EOS reporting the port as connected
   means the link-layer state itself is not the down condition being asked about.

## Entry point: flapping

1. EOS documents a feature named Dynamic Link Flap Damping, listed in the Ethernet Ports chapter
   under a section on displaying interface interactions. Unverified: its mechanism, default
   parameters, and the CLI used to view or configure it. Do not invent EOS damping default values or
   command syntax: if flap damping is suspected, check the device's current documentation or command
   help rather than carrying over another vendor's damping behavior, including Juniper Junos's
   damping model.
2. Without damping-specific detail, check `show interface <name>` for repeated state transitions
   and cross-reference the high_errors entry point's guidance on FCS/symbol errors, since Link Fault
   Signaling (documented below) ties elevated FCS/symbol error rates to automatic interface actions
   that could plausibly present as flapping if it's configured to disable the interface repeatedly
   rather than just log or fault.
3. Not documented in the sources: a further EOS-specific list of flap root causes beyond the above.
   Report that as an explicit gap rather than fabricating one.

## Entry point: high_errors

1. Unverified: the exact field names EOS uses in its interface error-counter display. Do not assert
   specific EOS counter field names (e.g. a specific "FCS errors" or "alignment errors" column name)
   as vendor documentation. Check the device's own command output or help for the fields actually
   present on the platform and release in use.
2. Link Fault Signaling (LFS) is documented in detail. EOS documents LFS as a way for a port to
   signal a detected link fault to its remote peer over the same link that's experiencing the
   problem, working between the local and remote "reconciliation sublayer" on each end. LFS is
   documented as monitoring FCS and symbol error rates against a configurable threshold, and — once
   that threshold is exceeded — as being able to take one of three documented actions: disable the
   interface for the fault condition, generate a log message, or generate a link fault signal toward
   the peer. Which of these three is configured determines whether a high-FCS/symbol-error condition
   on this platform will present as a logged event, an automatically disabled port, or a signal that
   propagates to the remote end. Check the interface's LFS configuration before assuming the counters
   alone explain the observed symptom. Unverified: the exact CLI; check current EOS documentation or
   the device's command reference.
3. A drop-counter view is documented as `show hardware counter drop`, which reports ASIC-level drop
   conditions (the manual's own example is a "ReassemblyErrors" counter, for frames exceeding the
   interface's MRU). This is a different, chip-level counter set from whatever the platform's
   standard interface error-counter display uses, so don't conflate a nonzero value here with the
   interface-level error counters without checking which counter set actually shows the condition
   being investigated.
4. For an interface using an optical transceiver, `show transceiver status interface <name>` reports
   module presence, alarm/fault state, data-path state, and RX/TX signal-quality metrics including
   pre-FEC and post-FEC bit-error-rate — a degrading pre-FEC or post-FEC BER is evidence of an
   optical/physical-layer problem worth checking before assuming a purely logical cause.
5. Report the literal values read from whichever of the above commands was actually run, and flag
   explicitly if the platform's specific error-counter field names don't match anything this
   procedure names, rather than forcing an unconfirmed field name onto the observed output.

## Entry point: duplex_mismatch

1. Run `show interfaces status` and read the Duplex and Speed columns for the interface, and
   `show interface <name>` for the full detail view, which the manual documents as including
   duplex/speed settings and auto-negotiation status.
2. Compare the local side's duplex/speed and auto-negotiation status against the remote side's,
   obtained the same way on the remote device. Unverified: whether EOS uses the "value with an `a-`
   prefix means auto-negotiated" display convention documented for Cisco IOS-XE. Do not assume it
   carries over; read whatever auto-negotiation indicator the platform's own output actually shows.
3. Not documented in the sources: EOS-specific signs of a duplex mismatch (e.g. a specific syslog
   message name, or which counters climb on which side). Flag that as an explicit gap. Treat a
   mismatch found in step 2 as sufficient evidence on its own (both sides must agree for the link to
   function correctly), and don't assume any of Cisco's documented signs (runts, a specific
   `%CDP`-style message) apply here without separately confirming EOS documents the same behavior.

## Entry point: no_link

1. Run `show interfaces status` and read the Status column; a `notconnect` value is EOS's documented
   status for no link partner detected.
2. For an interface using a pluggable optical transceiver, `show transceiver status interface
   <name>` is the documented way to check whether the module itself reports as present and
   operational, including any alarm/fault conditions — check this before assuming a bad cable, since
   the manual documents this command specifically for module-level presence/fault/signal-quality
   reporting.
3. Not documented in the sources: a further EOS-specific breakdown of no-link-light causes beyond
   the transceiver-status check above. Treat any conclusion beyond "no link partner detected, and
   transceiver status is/isn't reporting a fault" as needing additional platform-specific
   verification.

## Known gaps in this vendor's coverage

- Dynamic Link Flap Damping is documented by name only; its mechanism, defaults, and CLI are
  unverified, so the flapping entry point above is intentionally conservative.
- The exact CLI to view or configure Link Fault Signaling is unverified; only its documented
  behavior and the three actions it can take are known.
- No field-by-field dictionary for the platform's standard interface error-counter command is
  available from the sources, so high_errors above deliberately avoids asserting specific counter
  field names beyond `show hardware counter drop`'s one documented example and the transceiver BER
  fields.
- No EOS-specific duplex-mismatch documentation was available, so duplex_mismatch above is thinner
  than the Cisco IOS-XE file in this same skill and should not be assumed to share Cisco's documented
  behavior.
