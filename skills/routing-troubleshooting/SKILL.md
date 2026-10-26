---
name: routing-troubleshooting
description: Diagnose BGP session and route-propagation problems (session not establishing, session flapping, expected route missing from the table, unexpected best-path selection) by reading session and route state on a supported routing platform, and mapping observed state to the platform's own documented likely causes. Use when an agent needs to investigate why BGP isn't behaving as expected — not for configuring BGP, static routes, or routing policy from scratch (that is a create/update operation with a different shape; this skill is read-only diagnosis). Assumes an authenticated CLI/API session against the target device or controller is already available; this skill does not provision or authenticate it. No vendor coverage yet — see references/INDEX.md.
argument-hint: "[platform] [symptom: session_down|session_flapping|route_missing|unexpected_best_path] [peer/prefix identifier]"
---

# Routing Troubleshooting (BGP)

Diagnoses BGP session and route-propagation problems on whichever routing platform the caller is
targeting, by reading session/route state and mapping it to that platform's own documented likely
causes — not a configuration-change skill.

## Shape of this skill

This skill is **diagnostic-shaped**: the "procedure" is a decision tree (check session state → if Established, check whether routes are received → if
received, check whether they're best-path selected → …), and the useful output is a diagnosis plus
supporting evidence, not a single created or deleted record. Each `references/<platform>/procedure.md` is a decision tree, and a diagnostic step is complete when the operator or caller knows which documented cause applies, not when platform state changes.

This skill only reads session and route state, so it has **no destructive-action confirmation gates**. It does not clear sessions or reset peers; a remediation *action* of that kind would need its own confirmation gate like any other destructive step.

## When to use this skill

- A BGP session won't establish, is flapping, or a specific prefix is missing/unexpectedly
  not-best-path on a supported platform, and the caller needs to identify which documented cause
  applies.
- Not for configuring BGP neighbors, policies, or static routes from scratch — that would be a
  CRUD-shaped configuration capability with its own confirmation-gate requirements, separate from
  this read-only diagnostic one.

## Universal concepts (shared BGP vocabulary — RFC 4271)

The BGP session state machine's six named states — Idle, Connect, Active, OpenSent, OpenConfirm,
Established — come from RFC 4271, and each vendor's own CLI reports them verbatim: Juniper Junos's `show bgp neighbor` output uses these exact six words for its State/Last state fields, and Cisco IOS-XE and FRRouting use the same vocabulary, though their documentation gives less field-by-field confirmation than Juniper's — see each vendor's own `procedure.md` for exactly what is and isn't verified. Only Established has a consistent, universally-observed second meaning
across all three vendors: once a session reaches Established, the same output field that showed the
state name is commonly repurposed to show a route/prefix count instead (confirmed for both Cisco
IOS-XE's summary-table state/PfxRcd column and Juniper's `show bgp summary` State field) — a numeric
value in that field position is itself evidence the session is up, not evidence of anything about the
state machine itself.

**Not universal — do not assume across vendors:**
- The BGP best-path/route-selection tie-break order is NOT one universal algorithm, even though
  every vendor examined so far implements *some* ordered list of the same broad concepts (weight,
  local preference, AS-path length, origin, MED, eBGP-vs-iBGP, IGP metric, router ID). Cisco IOS-XE
  and FRRouting's own documented orders differ in real, material ways — FRRouting's documented order
  inserts an administrative-distance check before weight (a step Cisco's documented order doesn't
  have at all) and a "prefer the already-selected eBGP path" stability tiebreaker that Cisco's
  documented order also doesn't have. Treat the tie-break order as vendor-specific and always consult
  that vendor's own `procedure.md` rather than assuming one vendor's order generalizes.
- Unverified: Junos's own active-route-selection tie-break order (see `references/juniper-junos/procedure.md`'s explicit-unknowns section); it is not safe to assume it matches either Cisco's or FRR's documented order just because the underlying concepts
  are similar.
- There is no confirmed-universal set of session-establishment root causes (AS mismatch, TCP/179
  reachability, authentication mismatch, hold-time mismatch) across these three vendors' own documentation — each vendor file states which specific causes its own source documents, and none of the three gives a complete list covering all of these common real-world causes. Don't treat a cause documented for
  one vendor as automatically applicable to another without that vendor's own source confirming it.

See `references/INDEX.md` for which platforms have a procedure, and each platform file for how it
implements this shape concretely, including exactly which of the above each vendor's documentation does and doesn't confirm.

## Procedure

1. **Identify the target platform** — from the caller's request or the `platform` argument. Check
   `references/INDEX.md`; if no matching row exists, stop: this skill doesn't cover it yet.
2. **Identify the symptom category** — session not establishing, session flapping, route missing, or
   unexpected best-path selection. This determines which decision-tree entry point in
   `references/<platform>/procedure.md` to start from; the platform file is organized by symptom, not
   by a linear operation sequence.
3. **Open `references/<platform>/procedure.md`** and follow its decision tree for that symptom exactly
   — it maps each observed state to that platform's own documented likely causes and the next check to
   run.
4. **Report the diagnosis** — which documented cause the evidence points to, the evidence itself (the
   literal command/API output that supports it), and any documented next step the platform's own
   guidance suggests (which is often "escalate" or "consult platform-specific guidance," not a fix this
   skill performs) — don't present a diagnosis without the evidence that supports it.

## Known limitations

- No vendor coverage yet — see `references/INDEX.md`. A platform not listed there needs a new
  reference file before this skill can be used for it.
- Read-only diagnosis only. Does not configure, remediate, or reset anything — a caller who needs to
  act on a diagnosis (clear a session, change a policy) needs a separate configuration-change
  capability, which may not exist yet in this repository.
- Covers BGP only. OSPF, IS-IS, or static-route troubleshooting would be a separate capability (or a
  clearly-scoped addition here with its own vendor coverage) — do not silently expand this skill's
  scope to other protocols without treating that as a new-capability-shaped decision.

## Contributing to this skill

**`SKILL.md` only changes for two reasons: a bug in the universal concepts/router logic above, or
adding a pointer to a newly-supported platform.** Platform-specific decision-tree content — a new
documented cause, a corrected CLI/API output pattern, a vendor-specific state name — belongs in that
platform's own `references/<platform>/procedure.md`, never here.

## Tools

Each platform assumes its own authenticated CLI/API session — see `references/INDEX.md` for which,
and that platform's `procedure.md` for the specific read-only checks it uses.

## Verification checklist

- [ ] Target platform confirmed against `references/INDEX.md` before proceeding
- [ ] Symptom category correctly identified before opening the platform's decision tree
- [ ] That platform's own `procedure.md` decision tree was followed for the identified symptom
- [ ] Diagnosis reported together with the literal evidence (command/API output) that supports it —
      never a bare conclusion
- [ ] No configuration change was made — this skill is read-only; anything beyond reading state is out
      of scope here
