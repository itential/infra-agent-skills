---
name: sdwan_policy_management
description: Look up, create, edit, activate, deactivate, and delete a centralized SD-WAN policy on a supported SD-WAN orchestrator — currently Cisco Catalyst SD-WAN Manager (original template-policy model, centralized policy only). The policy assembles existing rule definitions and applies them to site lists; authoring the lists and definitions themselves is out of scope. Orchestrator-level policy, distinct from firewall_management's security rules and vpn_tunnel_management's point-to-point tunnels. Assumes an authenticated client for the target orchestrator's API is already available; this skill does not provision or authenticate it. Check references/INDEX.md for which platforms and operations are covered.
argument-hint: "[platform] [action: read_policy|create_policy|update_policy|activate_policy|deactivate_policy|delete_policy] [policy name or identifier, fields]"
---

# SD-WAN Policy Management

Manages the lifecycle of a centralized SD-WAN policy — create, edit, activate, deactivate, delete — on
whichever orchestrator the caller is targeting, following that platform's own documented procedure
exactly.

## When to use this skill

- Looking up, creating, editing, activating, deactivating, or deleting a centralized policy on a
  supported SD-WAN orchestrator. Which of those actions a platform supports is platform-dependent;
  see `references/INDEX.md`.
- Not for building the lists and rule definitions a policy is assembled from, or for device-level
  (localized) policy applied through device templates; no procedure here covers them yet.
- Not for security rules on a firewall — see `firewall_management`.
- Not for building a point-to-point VPN tunnel on a gateway — see `vpn_tunnel_management`.
- Not for wireless SSID/WLAN management, even where one vendor offers both — see
  `wireless_network_management`.

## Universal concepts (shared SD-WAN vocabulary, not a wire standard)

Only one platform is documented today, so these are claims expected to hold for any orchestrator and
must be re-checked when a second platform is added (`AGENTS.md` rules 4 and 14). Where a platform
differs, its own procedure wins.

- **Saving a policy and putting it into effect are separate states, where the platform separates
  them.** Creating or editing a saved policy does not change network behavior; activation or
  application to the controllers does. Report which state the policy is in.
- **A policy is assembled from reusable pieces and applied to a scope.** Where a platform lets pieces be shared, changing one can change every policy that uses it; check where it is used first.
- **Overlapping scopes can make behavior ambiguous.** Where the same policy type can reach one site by
  more than one route, behavior may be unpredictable and the platform may not warn about it.
- **Activation and deactivation may complete asynchronously.** An accepted request is not a confirmed
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
- Does not cover authoring the lists and rule definitions a policy is assembled from, or localized
  (device-level) policy.

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
      activating, deactivating, or deleting a policy and on editing one that is active
- [ ] Outcome reported using the platform procedure's own status vocabulary
