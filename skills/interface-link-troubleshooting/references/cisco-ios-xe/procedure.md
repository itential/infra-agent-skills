# Cisco IOS-XE — Interface / Link Troubleshooting Decision Tree

Read-only diagnosis of physical/logical interface and link problems on Cisco IOS-XE devices,
organized by symptom. Follow the entry point matching the observed symptom; each branch names the
next check to run and, where the source states one, the documented likely cause.

Sources, retrieved 2026-09-17:
- Cisco IOS Interface and Hardware Component Command Reference, "show interfaces" sample output
  (chapter covering `show hw-module slot tech-support` through `show interfaces vg-anylan`),
  cisco.com.
- Cisco errdisable-recovery support document, cisco.com.
- An older Cisco Ethernet auto-negotiation/duplex-mismatch tech note, cisco.com (still live at
  retrieval time; content style suggests it predates current IOS-XE branding, but it is Cisco's own
  published material and nothing in it is IOS-XE-version-specific).

Not documented in the sources: Cisco's field-by-field prose definitions for every `show interfaces`
counter (only the field *names* appearing in sample output are confirmed). Where this procedure
explains what a counter means, treat that explanation as a reasonable operator-level restatement,
not a vendor definition, and re-verify against current platform documentation before relying on it
for an unfamiliar counter.

## Entry point: interface_down

1. Run `show interfaces <interface> status` (or `show interfaces <interface>` for the full detail
   view) and read the reported state.
2. If the state reads administratively down: the interface has been manually disabled
   (`shutdown` applied in configuration). Documented next step: check the running configuration for
   that interface (`show running-config interface <interface>`) and confirm with the operator
   whether the shutdown is intentional before treating this as a fault.
3. If the state reads `err-disabled`: Cisco's errdisable mechanism has automatically taken the
   port out of service after detecting one of several fault conditions it monitors by default. Run
   `show errdisable recovery` to see which cause is flagged and how much (if any) automatic-recovery
   time remains; `show errdisable detect` shows which causes are currently being monitored. Cisco's
   documented default is that detection for all its built-in causes is active out of the box, while
   the automatic recovery timer itself is off by default (300 seconds when an operator turns it on).
   Documented causes behind an err-disabled state include: a duplex mismatch, an EtherChannel/PAgP/
   DTP negotiation inconsistency between the two ends of a channel, a BPDU Guard trip (a BPDU
   arriving on a port configured not to expect one), a UDLD-detected unidirectional link, a
   late-collision condition, the link-flap detector itself (see the flapping entry point below),
   a port-security violation, an L2TP guard trip, a DHCP-snooping rate-limit violation, an
   unsupported or faulty GBIC/SFP or cable, an ARP-inspection violation, an 802.1X violation, or an
   inline-power fault. Match the specific cause reported by `show errdisable recovery` to this list
   rather than guessing; if the reported cause needs a deeper check (e.g. duplex mismatch), continue
   into the relevant entry point below. To restore the port once the underlying condition is
   resolved, Cisco's documented manual recovery is to enter interface configuration mode and issue
   `shutdown` followed by `no shutdown` — **this is a state change on a live interface; stop and
   confirm with the operator before issuing it**, since it will briefly interrupt anything already
   using the port if traffic resumed on its own.
4. If the state reads up/up but the caller still expected connectivity: this is not an
   interface_down condition by Cisco's own state model — move to the no_link or high_errors entry
   point depending on what the caller actually observed.
5. If neither administratively down nor err-disabled explains it: report the literal state string
   from `show interfaces status` as the evidence. Not documented in the sources: every possible
   down-state string — say so explicitly rather than guessing at an unconfirmed cause.

## Entry point: flapping

1. Run `show interfaces <interface>` and note the "interface resets" counter and, if available,
   a carrier-transitions-style counter in the output — a nonzero and climbing value across repeated
   checks is the evidence of instability, not a single snapshot value.
2. Cisco's errdisable mechanism includes a link-flap detector as one of its default-monitored
   causes (see the interface_down entry point above) — if the interface has already gone to
   `err-disabled` with a flap-related cause, follow that branch instead; `show errdisable
   flap-values` shows the configured flap thresholds that would trigger it.
3. If the interface is still up but its counters show repeated resets rather than a single
   transition, the documented duplex-mismatch and cabling/CRC causes described in the high_errors
   entry point below are common contributors to instability, not just to a static error count —
   cross-check that entry point's evidence (CRC/frame/alignment counters) before concluding the
   cause is something else entirely.
4. Not documented in the sources: a general-purpose "why is this specific interface flapping"
   root-cause list beyond the errdisable flap detector and the duplex/cabling signs covered
   elsewhere. If those don't explain it, say so explicitly as an unresolved cause needing
   platform-specific or hardware-level follow-up rather than inventing one.

## Entry point: high_errors

1. Run `show interfaces <interface>` and read the error counters in the output: input errors (with
   its CRC, frame, overrun, ignored, and abort sub-counts) and output errors (with its collisions
   sub-count), alongside the reliability and load fields.
2. A nonzero and climbing CRC-error count is documented as indicating that frames are arriving with
   a checksum that doesn't match what the receiving side recalculates — Cisco's own guidance
   attributes this to line noise, a transmission problem, or a duplex mismatch between the two ends
   of the link, and separately notes that collisions or a physical/cabling fault are common
   contributors to a high CRC count specifically.
3. A nonzero and climbing frame/alignment-error count is documented as arising from frames with an
   incorrect octet count alongside a bad CRC — attributed to the same duplex-mismatch and physical
   -layer causes as CRC errors, plus (on older shared-media/hub topologies specifically) collisions
   in a shared collision domain; this last cause is unlikely to apply on a modern switched, full
   -duplex network and should be weighted accordingly.
4. If either of the above is climbing, move to the duplex_mismatch entry point to confirm or rule
   out a mismatch as the specific cause before assuming it's a cabling fault (or vice versa).
5. If the errors are output errors/collisions on a link that should be full-duplex with no
   collisions expected, that pattern is itself one of the documented duplex-mismatch signs — see
   the duplex_mismatch entry point.
6. Report the exact counter values read in step 1 as the evidence, not just which category was
   nonzero.

## Entry point: duplex_mismatch

1. Run `show interfaces <interface> status` and read the reported Duplex and Speed columns. Cisco's
   documented convention is that a value prefixed with `a-` (for example `a-full`, `a-100`) means
   that value was reached through auto-negotiation; a value with no `a-` prefix means it was
   statically/manually configured on that side.
2. Compare the local side's negotiated/configured duplex and speed against the remote side's, if the
   remote side's values are obtainable (e.g. via the same command run on the other device, or via
   `show interfaces <interface> capabilities` to see what the local port supports/advertises).
   A mismatch — most commonly one side auto-negotiating and the other statically forced, landing on
   different duplex values — is the documented root cause this entry point exists to confirm.
3. Cisco's documented signs that a duplex mismatch is actually occurring (cross-reference against
   what was found in high_errors): FCS/alignment errors climbing specifically on the side running
   half-duplex, runt frames appearing on the side running full-duplex, and — where CDP is enabled
   between the two devices — a `%CDP-4-DUPLEX_MISMATCH` syslog message on either side, which is a
   direct, named signal worth checking for in the device's logging output before doing the manual
   comparison in step 2.
4. Cisco's documented remedy is to bring both sides into agreement, preferably by enabling
   auto-negotiation on both ends (removing any hard-coded `speed`/`duplex` configuration, or
   explicitly configuring `speed auto`) rather than forcing a matching static value on both sides —
   auto-negotiation on just one side while the other is static is itself the most common way this
   mismatch happens. **Changing an interface's speed/duplex configuration is a configuration change
   with potential to interrupt traffic already flowing over that link; stop and confirm with the
   operator before applying it** — this procedure only diagnoses the mismatch, it does not apply the
   fix itself (see `SKILL.md`'s read-only scope).

## Entry point: no_link

1. Run `show interfaces <interface> status` (or the full `show interfaces <interface>`) and read
   the reported line state together with the Duplex/Speed/Type columns.
2. If the state reads `notconnect` (no physical carrier detected) rather than `err-disabled` or
   administratively down, treat this as a physical-layer problem — no cable seated, a failed cable,
   or an incompatible/faulty transceiver — since neither of those two other states (already covered
   above) applies. Cisco's documented err-disable causes include "incorrect GBIC/SFP or cable" as one
   of its monitored fault conditions, so also check whether errdisable has already flagged that
   specific cause via `show errdisable recovery` before assuming it's purely a cabling issue outside
   the box's own detection.
3. `show interfaces <interface> capabilities` shows what speed/duplex/media types the local port
   itself supports — use it to rule out a transceiver/port mismatch (for example, an installed
   optic the port doesn't support) as the cause before assuming the cable itself is at fault.
4. Not documented in the sources: a further breakdown of no-link-light causes beyond what's
   covered above (administratively down, err-disabled, and a physical/transceiver fault manifesting
   as `notconnect`). If none of these explain the observed state, report the literal reported state
   as evidence and flag that root cause as unresolved by the documented causes rather than guessing
   further.

## Known gaps in this vendor's coverage

- No Cisco field-by-field prose definition of every `show interfaces` counter is available from the
  sources — this file explains counters using the field names Cisco's own sample output confirms
  exist, with operator-level restatements of what each represents; treat as reasonable inference,
  not vendor definition.
- No IOS-XE-current (17.x) command reference distinct from the general IOS Interface and Hardware
  Component Command Reference material above is available from the sources — re-verify command
  availability and output format against the specific IOS-XE release in use before relying on exact
  field layout.
