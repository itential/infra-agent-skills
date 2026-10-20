---
name: firewall-management
description: Create, read, update, and delete firewall security policy objects (rules, address/service objects, NAT rules) on a supported firewall platform — currently Palo Alto Networks PAN-OS/Panorama (REST API), Fortinet FortiOS/FortiGate (CLI), Cisco ASA (CLI, with limited confirmed REST coverage), Juniper SRX/Junos OS (CLI), Fortinet FortiManager (JSON-RPC, central policy packages), WatchGuard Firebox (WatchGuard Cloud REST API), and AWS Network Firewall (rule groups and policies via API). Assumes an authenticated client for the target platform's API/CLI is already available; this skill does not provision or authenticate it. Does not cover Cisco FTD/FMC (not yet researched).
argument-hint: "[platform] [action: create_rule|read_rule|update_rule|delete_rule|create_object] [rule/object identifier, fields]"
---

# Firewall Management

Manages firewall security policy objects — rules, address/service objects, NAT rules — on whichever
firewall platform the caller is targeting, following that platform's own documented procedure exactly.

## When to use this skill

- Creating, reading, updating, or deleting a firewall rule, address/service object, or NAT rule on a
  supported platform.
- Not for web application firewall (WAF) rules, rate-limit rules, or managed-ruleset bindings — see
  `waf-management` for that. A platform may offer both network-layer and application-layer
  protection under one product line; this skill covers only the network-layer rule/object model.

## Universal concepts (shared firewall vocabulary, not a wire standard)

There is no wire-level standard behind firewall rule/object management the way DNS has RFC 1035 —
every claim below was checked against the vendors currently listed in `references/INDEX.md`
(PAN-OS, FortiOS, Cisco ASA, Juniper SRX, FortiManager, WatchGuard Firebox, AWS Network Firewall)
and holds as stated; it is not assumed to extend automatically to a platform not yet added.

- **A rule matches traffic by referencing named objects (addresses, and where the platform defines
  them, services), rather than embedding raw values inline.** PAN-OS, FortiOS, Cisco ASA, Juniper SRX,
  FortiManager and WatchGuard model an address as its own named object that a rule references by
  name — read or confirm an object's current definition separately from the rule. AWS Network
  Firewall is the exception: it has no address objects, so check its procedure.
- **Deleting an object or rule that something else still depends on is not something to assume the
  platform blocks for you.** Enforcement varies and is partial at best. PAN-OS, FortiOS, Cisco ASA,
  FortiManager and WatchGuard procedures found no platform-enforced reference check preventing
  deletion of an in-use object or rule (ASA's docs explicitly note this for network-service
  objects). Juniper SRX documents some commit-time enforcement for specific cases only, and AWS
  Network Firewall rejects deleting something still in use. Treat "check for existing references
  before deleting" as this skill's own discipline in every vendor procedure, not a safety net the
  platform itself is confirmed to provide.
- **How a write becomes "live" varies by vendor and is not safe to assume uniform.** PAN-OS and
  Juniper SRX have a documented candidate/commit model where nothing takes effect until a separate
  commit step. FortiManager and WatchGuard stage changes centrally and need a separate push to the
  devices. Cisco ASA's REST API is documented as writing only to the running configuration,
  requiring a separate persist step to survive a reload. AWS Network Firewall applies writes
  without a commit step, but check its procedure for how changes propagate. Whether FortiOS's and
  ASA's CLI writes apply immediately was not independently confirmed. Don't assume "the write call
  returned success" means "this is now enforced" — check each vendor's own procedure for what
  apply/commit/persist step (if any) it requires.
- **NAT is not modeled the same way across vendors — don't assume a shared shape.** PAN-OS treats
  NAT rules as their own separate rule family (parallel to security rules); FortiOS's VIP table
  covers destination NAT specifically, separate from its firewall-policy table and from source NAT
  (configured differently, at the policy level); Cisco ASA nests static/auto NAT as a subcommand
  inside the network object it translates, not as an independent rule list; Juniper SRX keeps NAT in
  its own rule sets, separate from security policies. NAT modeling for FortiManager, WatchGuard and
  AWS Network Firewall was not confirmed. Confirm the target vendor's own NAT model before assuming
  any of these shapes carries over to another platform.

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

- Covers PAN-OS/Panorama, FortiOS/FortiGate, Cisco ASA, Juniper SRX, FortiManager, WatchGuard Firebox and AWS Network Firewall only — see
  `references/INDEX.md` for exactly what's confirmed for each. A platform not listed there (including
  Cisco FTD/FMC) needs a new reference file before this skill can be used for it.
- Each vendor file also carries its own gaps (e.g. PAN-OS's NAT-rule REST path, FortiOS's REST API
  surface, ASA's FTD/FMC distinction) — check that vendor's own Known limitations before assuming
  full coverage of every operation named in this skill's description.

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
      destructive changes (rule/object deletion, NAT rule removal)
- [ ] Outcome reported using the platform procedure's own status vocabulary
