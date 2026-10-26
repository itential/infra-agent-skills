---
name: vpn-tunnel-management
description: Create, read, update, and delete site-to-site VPN tunnel configurations (IPsec/IKE phase 1 and phase 2 parameters where the platform exposes them, tunnel interfaces) on strongSwan, Palo Alto Networks PAN-OS, Juniper SRX (Junos OS), or Cloudflare WAN (GRE and IPsec tunnel objects), and create route-based IPsec VPN tunnels (static or dynamic Virtual Tunnel Interface) on Cisco ASA (create/configure only on ASA; no documented read, update, or delete there). Does not yet cover remote-access VPN profiles or any other platform. Assumes an authenticated client for the target platform's API/CLI is already available; this skill does not provision or authenticate it. See references/INDEX.md for per-platform scope.
argument-hint: "[platform] [action: create_tunnel|read_tunnel|update_tunnel|delete_tunnel; Cisco ASA: create_tunnel only] [tunnel identifier, fields]"
---

# VPN Tunnel Management

Manages site-to-site VPN tunnel configuration on whichever platform the caller is targeting,
following that platform's own documented procedure exactly.

## When to use this skill

- Creating, reading, updating, or deleting a site-to-site tunnel (IPsec/IKE phase 1 and phase 2
  parameters where the platform exposes them, tunnel interface or tunnel object) on a supported
  platform. On Cisco ASA, only creating a route-based
  VTI tunnel (static or dynamic) is covered. Remote-access VPN profiles are not yet covered by any
  listed platform — see Known limitations.

## Universal concepts (shared VPN vocabulary — verified across strongSwan, PAN-OS, Juniper SRX, and Cloudflare WAN)

- **The IPsec platforms checked (strongSwan, PAN-OS, Juniper SRX, Cloudflare WAN) negotiate in two stages**, though the exact labels vary: an IKE-level
  exchange that authenticates the peers and establishes a secure channel (phase 1 / an IKE_SA), and
  a second exchange that negotiates the actual IPsec traffic-protection parameters (phase 2 / a
  CHILD_SA). PAN-OS and Juniper's own documentation use "Phase 1"/"Phase 2" terminology directly;
  strongSwan's documentation and tooling use the RFC 7296 terms IKE_SA/CHILD_SA for the same
  two-stage structure. Treat these as the same underlying concept when translating between a
  platform that says "phase 2" and one that says "CHILD_SA." The Cisco ASA VTI source refers only to
  IKE and IPsec security associations without phase labels; it does not contradict the two-stage
  structure but does not spell it out either.
- **A committed/loaded configuration is not the same fact as an established tunnel**, on the
  platforms checked. Each of those vendors' procedure files distinguishes a configuration-level success
  (commit accepted, `swanctl --load-all` succeeded, `commit` succeeded) from live negotiated state,
  and, where the vendor documents one, has its own separate state-inspection command for the latter (PAN-OS: `show vpn ike-sa`/
  `show vpn ipsec-sa`; Juniper: `show security ike security-associations`/`show security ipsec
  security-associations`; strongSwan: `swanctl --list-sas`; the Cisco ASA VTI source documents none, so its procedure leaves that command unknown). Never report a tunnel as up from
  configuration/commit success alone — confirm with the platform's own state command.
- **Tearing down or deleting a live tunnel/gateway/SA is disruptive on the platforms checked** — it
  drops in-flight traffic through that tunnel. Each vendor file that documents delete/clear/terminate
  operations gates them behind an explicit operator-confirmation step for this reason.
  The Cisco ASA source documents no delete operation; it gates its other
  disruptive actions the same way.
- **Do not assume a specific proposal/algorithm-naming convention, DH-group numbering, or default
  lifetime value is common across platforms.** PAN-OS, strongSwan, and Junos SRX use
  different exact keyword sets for the same underlying algorithms (e.g. PAN-OS's `aes-256-gcm`
  crypto-profile field vs. strongSwan's dash-joined proposal strings vs. Junos's
  `encryption-algorithm` statement using the same literal keyword `aes-256-gcm` in one case but a
  different accepted DH-group list than PAN-OS documents) — always confirm the exact accepted values
  against that platform's own `references/<platform>/` file rather than assuming one platform's list
  transfers to another.
- This skill has no single wire-level standard grounding every platform's configuration syntax the
  way DNS has RFC 1035 — IKEv2 (RFC 7296) grounds the underlying protocol exchange conceptually, but
  each platform's own configuration object model, field names, and CLI/API surface are vendor-
  specific and not standardized. Treat any cross-platform claim beyond the two points above as
  unverified until checked against a specific vendor's own procedure file.

See `references/INDEX.md` for which platforms have a procedure, and each platform file for how it
implements this shape concretely.

## Procedure

1. **Identify the target platform** — from the caller's request or the `platform` argument. Check
   `references/INDEX.md`; if no matching row exists, stop: this skill doesn't cover it yet.
2. **Open `references/<platform>/procedure.md`** and follow it exactly — it contains that platform's
   full operational procedure, error handling, patterns, known limitations, tools, and verification
   checklist.
3. **Report the outcome** using that platform procedure's own status vocabulary — don't normalize it
   away, and don't conflate a tunnel configuration being written with the tunnel actually establishing
   (phase 1/phase 2 negotiation state is a separate fact to confirm from configuration success).

## Known limitations

- Covers strongSwan, Palo Alto Networks PAN-OS, Juniper SRX (Junos OS), Cloudflare WAN (GRE and
  IPsec tunnel objects), and Cisco ASA (VTI creation only) only — see `references/INDEX.md`. A
  platform not listed there needs a new reference file
  before this skill can be used for it.
- Remote-access VPN profiles (GlobalProtect, IKEv2/EAP or XAuth-based remote access, etc.) are not
  covered by any platform currently listed — every reference file here is site-to-site only.
- Does not cover firewall rules permitting the tunnel's traffic — see `firewall-management` for that;
  a tunnel may be correctly configured and still blocked by policy this skill does not manage.

## Contributing to this skill

**`SKILL.md` only changes for two reasons: a bug in the universal concepts/router logic above, or
adding a pointer to a newly-supported platform.** Platform-specific procedure changes — a new error
code, a corrected field, a changed call mechanism detail — belong in that platform's own
`references/<platform>/procedure.md`, never here.

## Tools

Each platform assumes its own authenticated client — see `references/INDEX.md` for which, and that
platform's `procedure.md` for the specific operations.

## Verification checklist

- [ ] Target platform confirmed against `references/INDEX.md` before proceeding
- [ ] That platform's own `procedure.md` was followed, including its own confirmation gates on
      destructive changes (tunnel deletion, which drops active traffic through it)
- [ ] Outcome reported using the platform procedure's own status vocabulary, distinguishing
      configuration success from actual tunnel-up/negotiated state where the platform makes that
      distinction
