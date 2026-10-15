---
name: ipam-allocation
description: Allocate IP address space (aggregates/prefixes/subnets and individual IP addresses) on a supported IPAM platform — currently NetBox (REST), Infoblox NIOS (WAPI), and SolarWinds IPAM (SOAP/SWIS verb invocation, not REST). Use when an agent needs to reserve network space or assign an IP address, distinct from creating DNS records for that address (see dns-record-management for that). Assumes an authenticated client for the target platform's API is already available; this skill does not provision or authenticate it. Not every platform uses the same call mechanism — check references/INDEX.md before assuming REST.
argument-hint: "[platform] [action: allocate_prefix|allocate_ip|create_subnet|reserve_ip] [parent/subnet, size]"
---

# IPAM Allocation

Allocates network/subnet space and individual IP addresses on whichever IPAM platform the caller is
targeting, following that platform's own documented procedure and call mechanism exactly.

## When to use this skill

- Reserving a new subnet/prefix from an existing address pool, or assigning an available IP address,
  on a supported IPAM platform.
- Not for creating the DNS record that points at an allocated address — see `dns-record-management`
  for that (a separate concept from address-space allocation, even on platforms like Infoblox that offer
  both).

## Universal concepts (shared IPAM vocabulary, not a wire standard)

There is no RFC grounding IPAM allocation the way RFC 1035 grounds DNS — every platform's allocation
model is its own product design. What is genuinely shared:

- **Address space is hierarchical: a parent block is carved into child blocks, which are carved into
  individual addresses.** Every platform in this skill models this, even though the exact terms differ
  (NetBox: aggregate → prefix → IP; Infoblox: network container → network → IP; SolarWinds: subnet →
  IP node).
- **"Available" is often computed, not a stored fact.** Several platforms calculate what's free on the
  fly rather than maintaining a persistent free-list — don't assume a "list available" response is a set
  of real, reservable records; confirm what the specific platform actually guarantees.
- **Allocation and reservation are not always the same operation.** Some platforms allocate
  immediately and permanently on one call; others (SolarWinds) have a distinct, time-boxed reservation
  step before a final commit. Check the target platform's procedure file before assuming either shape.
- **Not every platform's call mechanism is REST.** SolarWinds IPAM is SOAP/verb-invocation
  (`Invoke-SwisVerb`), not HTTP methods — confirm the mechanism in `references/INDEX.md` before assuming
  GET/POST semantics apply.

See `references/INDEX.md` for which platforms have a procedure, and each platform file for how it
implements this shape concretely.

## Procedure

1. **Identify the target platform** — from the caller's request or the `platform` argument. Check
   `references/INDEX.md`; if no matching row exists, stop: this skill doesn't cover it yet.
2. **Open `references/<platform>/procedure.md`** and follow it exactly — it contains that platform's
   full operational procedure, error handling, patterns, known limitations, tools, and verification
   checklist.
3. **Report the outcome** using that platform procedure's own status vocabulary — don't normalize it
   away, and don't conflate a reservation with a final allocation on a platform that distinguishes them.

## Known limitations

- Currently covers NetBox, Infoblox NIOS (allocation only, not DNS records — see
  `dns-record-management` for those), and SolarWinds IPAM. A platform not listed in
  `references/INDEX.md` needs a new reference file before this skill can be used for it.
- Does not cover DHCP scope/lease configuration (see `dhcp-scope-management`), network discovery, or
  DNS record creation on any platform — those are adjacent capabilities, not address-space
  allocation.

## Contributing to this skill

**`SKILL.md` only changes for two reasons: a bug in the universal concepts/router logic above, or
adding a pointer to a newly-supported platform.** Platform-specific procedure changes — a new error
code, a corrected field, a changed call mechanism detail — belong in that platform's own
`references/<platform>/procedure.md`, never here.

## Tools

Each platform assumes its own authenticated client and call mechanism (REST, WAPI, or SOAP/SWIS verb
invocation) — see `references/INDEX.md` for which, and that platform's `procedure.md` for the specific
operations.

## Verification checklist

- [ ] Target platform confirmed against `references/INDEX.md` before proceeding, including its call
      mechanism (REST vs. non-REST)
- [ ] That platform's own `procedure.md` was followed, including its own confirmation/reservation
      semantics — not a generic/improvised sequence
- [ ] Outcome reported using the platform procedure's own status vocabulary
