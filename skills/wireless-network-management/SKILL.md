---
name: wireless-network-management
description: Provision, update, or read SSID/WLAN configuration on a supported wireless-management platform — currently Cisco Meraki (SSID slot configuration, no create endpoint exists), HPE Aruba Networking Central, and Cisco Catalyst Center (async create-and-provision, fabric and non-fabric). Use when an agent needs to provision or inspect a wireless SSID. Assumes an authenticated client for the target platform's API is already available; this skill does not provision or authenticate it. Not every platform supports write operations — check references/INDEX.md before assuming SSID creation is possible on a given platform.
argument-hint: "[platform] [action: list|get|create|update|disable|provision] [ssid/wlan name, fields]"
---

# Wireless Network Management

Provisions, updates, or reads SSID/WLAN configuration on whichever wireless-management platform the
caller is targeting, following that platform's own documented procedure and capability boundaries.

## When to use this skill

- Listing, reading, creating, updating, or disabling an SSID/WLAN on a supported platform.
- Not every platform documents every action as an API route — check `references/INDEX.md` for how each
  platform's operations are bound before promising a specific mechanism.

## Universal concepts (shared wireless-management vocabulary, not a wire standard)

- **"Create an SSID" is not always a distinct operation from "update one."** Meraki has no create
  endpoint at all — every SSID is a pre-provisioned numbered slot configured via the same call used
  for updates. Catalyst Center does have a distinct create call. Confirm which model the target
  platform uses before assuming a REST-conventional POST-to-create exists.
- **Provisioning a live SSID change is a production action, not a preview.** Every platform in this
  skill that supports writes treats a change as taking effect on real infrastructure — there is no
  staging/dry-run step documented for any of them. Confirm with the operator before changing a slot/
  SSID already serving production traffic.
- **PSK/passphrase fields are auth-mode-gated across platforms, not universally settable.** Both
  Meraki (`psk` valid only when `authMode` is `psk`) and Catalyst Center (`passphrase` "only applicable
  for SSID with PERSONAL auth type") enforce this same rule independently — treat it as a pattern to
  expect on a new platform too, not a Meraki-specific quirk.
- **An async write is not complete when the initial call returns.** Where a platform's write is
  asynchronous (Catalyst Center), the initial response is an acceptance, not a completion — always
  poll to a terminal state before reporting success.

See `references/INDEX.md` for which platforms have a procedure, and each platform file for how it
implements this shape concretely.

## Procedure

1. **Identify the target platform** — from the caller's request or the `platform` argument. Check
   `references/INDEX.md`; if no matching row exists, stop: this skill doesn't cover it yet.
2. **Open `references/<platform>/procedure.md`** and follow it exactly — it contains that platform's
   full operational procedure, error handling, patterns, known limitations, tools, and verification
   checklist.
3. **Report the outcome** using that platform procedure's own status/completion vocabulary — for an
   async platform, only after polling confirms a terminal state, not from the initial response.

## Known limitations

- Currently covers Cisco Meraki, HPE Aruba Networking Central, and Cisco Catalyst Center.
  A platform not listed in `references/INDEX.md` needs a new reference file before this skill can be
  used for it.
- Write capability is platform-dependent, not guaranteed — check `references/INDEX.md` before telling
  a caller this skill can provision an SSID on their behalf on every platform equally.
- Does not cover site/group management, RF profile design, AP hardware provisioning, or guest/captive-
  portal configuration in depth — only what each platform's own SSID/WLAN procedure directly covers.

## Contributing to this skill

**`SKILL.md` only changes for two reasons: a bug in the universal concepts/router logic above, or
adding a pointer to a newly-supported platform.** Platform-specific procedure changes belong in that
platform's own `references/<platform>/procedure.md` and `endpoints.md`, never here.

## Tools

Each platform assumes its own authenticated client — see `references/INDEX.md` for which, and that
platform's `procedure.md` for the specific operations.

## Verification checklist

- [ ] Target platform confirmed against `references/INDEX.md` before proceeding, including whether it
      actually supports the requested write operation
- [ ] That platform's own `procedure.md` was followed, including its own confirmation gates and
      completion-polling requirements
- [ ] Outcome reported using the platform procedure's own status vocabulary, only after confirming
      actual completion on async platforms
