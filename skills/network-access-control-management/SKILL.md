---
name: network-access-control-management
description: Register, quarantine, release, and remove network endpoints, assign them to groups or profiles, and read their session state on a supported network access control (NAC/AAA) platform. Port- and network-level admission, distinct from zero-trust-access-policy-management's application-access policy. Assumes an authenticated client for the target platform's API is already available; this skill does not provision or authenticate it. No vendor coverage yet — see references/INDEX.md.
argument-hint: "[platform] [action: read_endpoint|register_endpoint|assign_group|quarantine|release|delete_endpoint|read_session] [endpoint identifier, fields]"
---

# Network Access Control Management

Manages endpoint admission on whichever network access control platform the caller is targeting —
registering, quarantining, releasing, and removing endpoints and their group or profile
assignment — following that platform's own documented procedure exactly.

## When to use this skill

- Reading, registering, assigning to a group or profile, quarantining, releasing, or
  deleting an endpoint, or reading its session state, on a supported NAC/AAA platform.
- Not for application-access or internet-access policy in a cloud security service — see
  `zero-trust-access-policy-management`.
- Not for network-layer firewall rules — see `firewall-management`.
- Not for address assignment — see `dhcp-scope-management` and `ipam-allocation`.

## Universal concepts (shared NAC/AAA vocabulary, not a wire standard)

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
- Does not cover firewall rules, address assignment, or cloud application-access policy.
- Authorization-policy rule authoring (the conditions that decide admission) is out of scope until a
  platform procedure documents it as its own distinct, gated procedure.

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
      quarantine of a live endpoint, endpoint deletion, and group changes that alter existing access
- [ ] Outcome reported using the platform procedure's own status vocabulary
