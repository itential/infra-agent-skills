---
name: sdwan_policy_management
description: Read, create, update, delete, activate, and deactivate SD-WAN templates, policies, and application/path-steering rules, and read edge and overlay status, through a supported SD-WAN orchestrator. Orchestrator-level policy, distinct from firewall_management's security rules and vpn_tunnel_management's point-to-point tunnels. Assumes an authenticated client for the target platform's API is already available; this skill does not provision or authenticate it. No vendor coverage yet — see references/INDEX.md.
argument-hint: "[platform] [action: read_edge|read_policy|create_policy|update_policy|delete_policy|activate_policy|deactivate_policy] [edge/policy identifier, fields]"
---

# SD-WAN Policy Management

Manages SD-WAN templates, policies, and path/application-steering rules through whichever orchestrator the
caller is targeting, following that platform's own documented procedure exactly.

## When to use this skill

- Reading edge or overlay status, or creating, updating, deleting, activating, or deactivating a
  template, policy, or application/path-steering rule on a supported SD-WAN orchestrator.
- Not for security rules on a firewall — see `firewall_management`.
- Not for building a point-to-point VPN tunnel on a gateway — see `vpn_tunnel_management`.
- Not for wireless SSID/WLAN management, even where one vendor offers both — see
  `wireless_network_management`.

## Universal concepts (shared SD-WAN vocabulary, not a wire standard)

*(To be filled in as vendors are added — see `AGENTS.md` rule 4: only claims verified true across
every vendor actually listed belong here. Do not pre-populate this section with assumptions before
a vendor's real behavior has been checked against them.)*

See `references/INDEX.md` for which platforms have a procedure, and each platform file for how it
implements this shape concretely.

## Procedure

1. **Identify the target platform** — from the caller's request or the `platform` argument. Check
   `references/INDEX.md`; if no matching row exists, stop: this skill doesn't cover it yet.
2. **Open `references/<platform>/procedure.md`** and follow it exactly — it contains that platform's
   full operational procedure, error handling, patterns, known limitations, tools, and verification
   checklist.
3. **Report the outcome** using that platform procedure's own status vocabulary — don't normalize it
   away.

## Known limitations

- No vendor coverage yet — see `references/INDEX.md`. A platform not listed there needs a new
  reference file before this skill can be used for it.
- Does not cover firewall rules, point-to-point VPN tunnels, or wireless SSID/WLAN management, even where the
  same vendor offers them in one product.

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
      deleting a policy or template, and activating or deactivating a policy that applies to live edges
- [ ] Outcome reported using the platform procedure's own status vocabulary
