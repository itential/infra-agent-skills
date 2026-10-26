---
name: sdwan-policy-management
description: Look up, create, edit, put into effect (activate, or bind to sites), take out of effect, and delete a centralized SD-WAN policy on a supported SD-WAN orchestrator — currently Cisco Catalyst SD-WAN Manager (original template-policy model, centralized policy only) and Palo Alto Networks Prisma SD-WAN (stacked path and QoS policy). A policy is assembled from reusable pieces and applied to sites; which pieces this skill authors and which must already exist depends on the platform (see references/INDEX.md). Orchestrator-level policy, distinct from firewall-management's security rules and vpn-tunnel-management's point-to-point tunnels. Assumes an authenticated client for the target orchestrator's API is already available; this skill does not provision or authenticate it. Check references/INDEX.md for which platforms and operations are covered.
argument-hint: "[platform] [action: read_policy|create_policy|update_policy|activate_policy|deactivate_policy|delete_policy] [policy name or identifier, fields]"
---

# SD-WAN Policy Management

Manages the lifecycle of a centralized SD-WAN policy — create, edit, put into or out of effect, delete —
on whichever orchestrator the caller is targeting, following that platform's own documented procedure
exactly.

## When to use this skill

- Looking up, creating, editing, putting into effect (activating, or binding to sites), taking out of
  effect, or deleting a centralized policy on a supported SD-WAN orchestrator. Which of those actions
  a platform supports is platform-dependent; see `references/INDEX.md`.
- Not for building the reusable inputs a platform's policy refers to (lists, prefixes, applications,
  and similar) where that platform's procedure does not cover them, or for device-level (localized)
  policy; see `references/INDEX.md` for what each platform's procedure covers.
- Not for security rules on a firewall — see `firewall-management`.
- Not for building a point-to-point VPN tunnel on a gateway — see `vpn-tunnel-management`.
- Not for wireless SSID/WLAN management, even where one vendor offers both — see
  `wireless-network-management`.

## Universal concepts (shared SD-WAN vocabulary, not a wire standard)

These claims were checked against both documented platforms and do not extend automatically to a platform not listed in `references/INDEX.md`. Where a platform differs, its own procedure wins.

- **Saving a policy and putting it into effect may be separate states.** Where a platform separates
  them, saving or editing does not change network behavior; activation does. Where it does not (a
  policy takes effect once attached to a site), treat an edit to anything already attached as a live
  change. Report which state the policy is in.
- **A policy is assembled from reusable pieces and applied to a scope.** Where a platform lets pieces be shared, changing one can change every policy that uses it; check where it is used first.
- **Overlapping scopes can make behavior ambiguous.** Where the same policy type can reach one site by
  more than one route, behavior may be unpredictable and the platform may not warn about it.
- **Putting a policy into or out of effect may complete asynchronously.** An accepted request is not a confirmed
  outcome; confirm the final state before reporting success.

## Procedure

1. **Identify the target platform** — from the caller's request or the `platform` argument. Check
   `references/INDEX.md`; if no matching row exists, stop: this skill doesn't cover it yet.
2. **Open `references/<platform>/procedure.md`** and follow it exactly — it contains that platform's
   full operational procedure, error handling, patterns, known limitations, tools, and verification
   checklist.
3. **Report the outcome** using that platform procedure's own status vocabulary — don't normalize it
   away.

## Known limitations

- Platform coverage is in `references/INDEX.md`; a platform not listed there needs a new reference
  file before this skill can be used for it.
- Does not cover firewall rules, point-to-point VPN tunnels, or wireless SSID/WLAN management, even
  where the same vendor offers them in one product.
- Does not cover localized (device-level) policy, or authoring the reusable inputs a platform's policy
  refers to where that platform's procedure does not (see `references/INDEX.md`).

## Contributing to this skill

**`SKILL.md` only changes for two reasons: a bug in the universal concepts/router logic above, or
adding a pointer to a newly-supported platform.** Platform-specific procedure changes — a new error
code, a corrected field, a changed API path — belong in that platform's own
`references/<platform>/procedure.md`, never here.

## Tools

Each platform assumes its own authenticated client — see `references/INDEX.md` for which, and that
platform's `procedure.md` for the specific operations.

## Verification checklist

- [ ] Target platform confirmed against `references/INDEX.md` before proceeding
- [ ] That platform's own `procedure.md` was followed, including its own confirmation gates on
      putting a policy into or out of effect, deleting one, and editing one that is in effect
- [ ] Outcome reported using the platform procedure's own status vocabulary
