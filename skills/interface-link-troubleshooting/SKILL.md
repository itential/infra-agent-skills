---
name: interface-link-troubleshooting
description: Diagnose physical/logical interface and link problems (interface down, flapping, high error/discard counters, duplex/speed mismatch, no link light) by reading interface state and counters on a supported platform, and mapping observed state to the platform's own documented likely causes — currently Cisco IOS-XE, Juniper Junos, and Arista EOS (symptom coverage varies by vendor; see references/INDEX.md). Use when an agent needs to investigate why a link isn't behaving as expected — not for configuring interface settings from scratch (that is a create/update operation with a different shape; this skill is read-only diagnosis). Assumes an authenticated CLI/API session against the target device is already available; this skill does not provision or authenticate it.
argument-hint: "[platform] [symptom: interface_down|flapping|high_errors|duplex_mismatch|no_link] [interface identifier]"
---

# Interface / Link Troubleshooting

Diagnoses physical and logical interface/link problems on whichever platform the caller is targeting,
by reading interface state and counters and mapping them to that platform's own documented likely
causes — not a configuration-change skill.

## Why this skill has a different shape than most others in this repo

This skill is **diagnostic-shaped**, not CRUD-shaped (see `AGENTS.md` rule 2) — the "procedure" is a
decision tree keyed by symptom, and the useful output is a diagnosis plus the literal evidence that
supports it, not a created/updated/deleted record. This skill has no destructive-action confirmation
gates because reading interface state and counters doesn't change anything on the platform. If a
future addition to this skill ever proposes a remediation action (clearing counters, forcing a
speed/duplex setting, administratively flapping the interface), that action needs its own
confirmation gate exactly like any CRUD skill's destructive step.

## When to use this skill

- An interface is down, flapping, showing elevated error/discard counters, suspected of a
  duplex/speed mismatch, or showing no link light, on a supported platform, and the caller needs to
  identify which documented cause applies.
- Not for configuring interface settings (speed, duplex, VLAN membership, description) from scratch —
  that would be a CRUD-shaped configuration capability with its own confirmation-gate requirements,
  separate from this read-only diagnostic one.

## Universal concepts (shared interface-state vocabulary, not a wire standard)

Confirmed against the three platforms currently listed in `references/INDEX.md` (Cisco IOS-XE,
Juniper Junos, Arista EOS) as of the research pass that added them — re-check every claim below
against any newly added vendor before assuming it still holds (`AGENTS.md` rule 4):

- **There is no single wire-level standard grounding interface/link state the way RFC 4271 grounds
  BGP session state, or RFC 1035/2136/1123 ground DNS.** Every platform researched so far defines its
  own state names, its own error-counter field names, and its own documented likely-cause mappings —
  do not assume a counter name, a status string, or a documented cause from one vendor's file applies
  to another's; each vendor's `procedure.md` says explicitly where it could not confirm something
  rather than borrowing another vendor's confirmed behavior.
- **Administratively disabled vs. operationally down is a distinction every platform researched so
  far draws in some form** — an interface an operator has explicitly disabled in configuration is a
  different condition, needing a different response, than one that is enabled but not passing link
  for some other reason. The exact state string and command differ per platform; see each vendor's
  `procedure.md`.
- **Every platform researched so far documents a mechanism, or at least a display artifact, in which
  the interface's reported state does not fully explain why it's in that state** without a further
  check — Cisco's err-disabled state names a specific detected cause that must be read separately
  (`show errdisable recovery`), and Junos's damping feature can make an interface report down without
  its state display distinguishing "suppressed" from "actually down for a new reason." Arista's
  Dynamic Link Flap Damping is confirmed to exist but its detail wasn't retrieved this pass, so it is
  not yet confirmed to share this same caveat — don't assume it does until checked.
- Beyond these, do not assume any specific error-counter name (CRC, FCS, alignment, symbol, etc.),
  duplex/speed auto-negotiation display convention, or documented root-cause list is shared across
  vendors — each is confirmed or explicitly flagged as unconfirmed in that vendor's own file.

See `references/INDEX.md` for which platforms have a procedure, and each platform file for how it
implements this shape concretely.

## Procedure

1. **Identify the target platform** — from the caller's request or the `platform` argument. Check
   `references/INDEX.md`; if no matching row exists, stop: this skill doesn't cover it yet.
2. **Identify the symptom category** — interface down, flapping, high errors/discards, duplex/speed
   mismatch, or no link light. This determines which decision-tree entry point in
   `references/<platform>/procedure.md` to start from; the platform file is organized by symptom, not
   by a linear operation sequence.
3. **Open `references/<platform>/procedure.md`** and follow its decision tree for that symptom exactly
   — it maps each observed state to that platform's own documented likely causes and the next check to
   run.
4. **Report the diagnosis** — which documented cause the evidence points to, the evidence itself (the
   literal command/API output that supports it), and any documented next step the platform's own
   guidance suggests — don't present a diagnosis without the evidence that supports it.

## Known limitations

- Currently covers Cisco IOS-XE, Juniper Junos, and Arista EOS — see `references/INDEX.md` for
  exact symptom-category coverage per vendor (deliberately partial for some). A platform not
  listed there needs a new reference file before this skill can be used for it.
- Read-only diagnosis only. Does not configure, remediate, or reset anything — a caller who needs to
  act on a diagnosis needs a separate configuration-change capability, which may not exist yet in this
  repository.
- Covers physical/logical interface and link-layer symptoms only. A diagnosis that points to a
  routing-layer cause (e.g. a route not propagating because the underlying link is down) should hand
  off to `routing-troubleshooting` rather than this skill trying to cover both layers.

## Contributing to this skill

**`SKILL.md` only changes for two reasons: a bug in the universal concepts/router logic above, or
adding a pointer to a newly-supported platform.** Platform-specific decision-tree content — a new
documented cause, a corrected CLI/API output pattern, a vendor-specific counter name — belongs in
that platform's own `references/<platform>/procedure.md`, never here.

## Tools

Each platform assumes its own authenticated CLI/API session — see `references/INDEX.md` for which,
and that platform's `procedure.md` for the specific read-only checks it uses.

## Verification checklist

- [ ] Target platform confirmed against `references/INDEX.md` before proceeding
- [ ] Symptom category correctly identified before opening the platform's decision tree
- [ ] That platform's own `procedure.md` decision tree was followed for the identified symptom
- [ ] Diagnosis reported together with the literal evidence (command/API output) that supports it —
      never a bare conclusion
- [ ] No configuration change was made — this skill is read-only; anything beyond reading state is
      out of scope here
