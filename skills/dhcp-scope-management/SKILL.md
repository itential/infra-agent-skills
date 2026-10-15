---
name: dhcp-scope-management
description: Create, read, update, and delete a DHCP scope/subnet and its lease reservations — currently Infoblox NIOS (WAPI range/fixedaddress objects), ISC Kea (Control Agent subnet_cmds/host_cmds hook commands), and Microsoft Windows Server DHCP Server (DhcpServer PowerShell module). Distinct from ipam-allocation, which reserves address space and IPs as inventory records; this skill manages the DHCP service configuration that actually leases addresses to clients from that space. Assumes an authenticated/permitted client for the target platform (WAPI session, Control Agent HTTP access, or a PowerShell session with the DhcpServer module) is already available; this skill does not provision or authenticate it. Not every platform uses the same call mechanism — check references/INDEX.md before assuming REST.
argument-hint: "[platform] [action: create_scope|read_scope|update_scope|delete_scope|create_reservation|delete_reservation] [scope/reservation identifier, fields]"
---

# DHCP Scope Management

Manages DHCP scope/subnet configuration and lease reservations on whichever DHCP platform the caller
is targeting, following that platform's own documented procedure exactly.

## When to use this skill

- Creating, reading, updating, or deleting a DHCP scope/subnet, or creating/deleting a lease
  reservation for a specific client, on a supported platform.
- Not for reserving IP address space or an individual IP as an inventory record — see
  `ipam-allocation` for that. A platform like Infoblox may expose both concerns through related
  objects, but allocating the address as inventory and configuring DHCP to actually lease it are
  different operations; this skill is only the latter.

## Universal concepts (shared DHCP vocabulary, not a wire standard)

There is no wire standard grounding *management-API* shape here the way RFC 1035/2136/1123 ground
DNS — RFC 2131 defines the DHCP protocol itself (what a client and server exchange on the wire), not
how a vendor's own API/CLI should represent scope or reservation configuration. Every platform below
designed that management surface independently. What is verified true across all three platforms
currently covered (Infoblox NIOS, ISC Kea, Microsoft DHCP Server — see `references/INDEX.md`):

- **A scope/subnet's address-space definition and its DHCP-service configuration are handled as
  distinct concerns from address-space allocation as inventory**, even on a platform that also does
  IPAM. Infoblox's `range` object is separate from its `network` object; Kea's `subnet_cmds` operate
  on service configuration, not an inventory record; Windows's scope cmdlets have no IPAM-inventory
  counterpart at all in this module. This is the basis for this skill's own boundary with
  `ipam-allocation` — see "When to use this skill" above.
- **A lease reservation ties a specific client identifier (most commonly a MAC address, though every
  platform here also supports at least one alternate identifier type) to a specific address, and is a
  distinct object from the scope/subnet it lives in.** Infoblox's `fixedaddress`, Kea's host
  reservations, and Windows's `DhcpServerv4Reservation` are all separate create/read/update/delete
  operations from their platform's own scope object, not a field on the scope itself.
- **Updating a scope/subnet's core configuration is not a full-replace operation by default on every
  platform — this is NOT a safe generalization, it's flagged here specifically because it does NOT
  hold universally.** Kea's plain `subnet4-update` fully overwrites the subnet (anything omitted is
  removed); Infoblox's range/fixedaddress updates and Microsoft's `Set-DhcpServerv4Scope` both change
  only the fields explicitly supplied. Confirm the target platform's own update semantics in its
  `procedure.md` before assuming either behavior.
- **Deleting a scope/subnet does not, by itself, guarantee cleanup of the leases or reservations
  issued under it** on at least one platform (Kea's `subnet4-del` explicitly does not remove
  associated leases/reservations, per its own documentation) — this was not independently confirmed
  either way for Infoblox or Microsoft in this pass, so treat "does deletion clean up dependents" as
  a per-platform question to check, not an assumed yes/no, before relying on it in an automated flow.
- **Deleting a scope/subnet or a reservation that may be actively in use is treated as a
  confirmation-gated action in every platform's own procedure file here** — not because of a shared
  vendor guarantee, but because this repo's own authoring rule (`AGENTS.md` rule 7) requires it
  regardless of what the vendor's API itself enforces.

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

- Currently covers Infoblox NIOS, ISC Kea, and Microsoft DHCP Server — see `references/INDEX.md`. A
  platform not listed there needs a new reference file before this skill can be used for it.
- Does not cover IP address space allocation as an inventory record — see `ipam-allocation` for that.
- Does not cover DHCPv6, DHCP failover-partner relationship setup, or lease-level management
  independent of scope/reservation configuration — see each platform's own `procedure.md` for the
  specifics of what its file does and doesn't address.

## Contributing to this skill

**`SKILL.md` only changes for two reasons: a bug in the universal concepts/router logic above, or
adding a pointer to a newly-supported platform.** Platform-specific procedure changes — a new error
code, a corrected field, a changed call mechanism detail — belong in that platform's own
`references/<platform>/procedure.md`, never here.

## Tools

Each platform assumes its own authenticated/permitted client and call mechanism (WAPI, a JSON
command/response envelope over HTTP, or PowerShell/CIM cmdlets — not all of them REST) — see
`references/INDEX.md` for which, and that platform's `procedure.md` for the specific operations.

## Verification checklist

- [ ] Target platform confirmed against `references/INDEX.md` before proceeding, including its call
      mechanism (REST-like WAPI, JSON command envelope, or PowerShell/CIM — not all are REST)
- [ ] That platform's own `procedure.md` was followed, including its own confirmation gates on
      destructive changes (scope deletion, which affects every active lease under it)
- [ ] Outcome reported using the platform procedure's own status vocabulary
