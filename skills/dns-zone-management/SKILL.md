---
name: dns-zone-management
description: Create, read, update, and delete a DNS zone — including its SOA/NS configuration and subdomain delegation, where the platform documents them — on AWS Route 53, Cloudflare, or PowerDNS Authoritative Server. Distinct from dns-record-management, which manages individual records inside a zone and assumes the zone already exists; this skill is the zone-level lifecycle those record operations depend on. Assumes an authenticated API client for the target platform (Route 53 API, Cloudflare API Token, or PowerDNS X-API-Key) is already available; this skill does not provision or authenticate it. See references/INDEX.md for the current vendor list.
argument-hint: "[platform] [action: create_zone|read_zone|update_zone|delete_zone|delegate_subdomain] [zone name, fields]"
---

# DNS Zone Management

Manages DNS zone lifecycle — creation, SOA/NS configuration, subdomain delegation, deletion — on
whichever DNS platform the caller is targeting, following that platform's own documented procedure
exactly.

## When to use this skill

- Creating, reading, updating, or deleting a zone, or delegating a subdomain to another set of
  nameservers, on a supported platform.
- Not for creating/updating/deleting an individual record inside a zone that already exists — see
  `dns-record-management` for that. This skill's job ends where a zone exists and is correctly
  configured; record-level content inside it is the other skill's concern.

## Universal concepts (verified across the vendors actually listed below)

This skill has no single wire-level standard grounding zone lifecycle the way `dns-record-management`
can cite RFC 1035/2136/1123 for individual record semantics — zone creation, deletion, and SOA/NS
handling are managed very differently by each platform below, and only the following has actually been
verified true across all three currently listed:

- **Creating a zone does not immediately make it authoritative for the domain.** Every platform below
  requires a separate, external step (an NS delegation change at a registrar or a parent zone) before
  the new zone actually serves traffic for that name — a successful create call is not itself "the
  domain now resolves via this zone."
- **Zone deletion is treated as destructive and effectively irreversible in this skill's own
  procedures**, even though the vendors differ on whether they document a hard precondition for it
  (Route 53 explicitly requires the zone hold only its default records first and states deletion can't
  be undone; no equivalent explicit precondition or "can't be undone" statement appears in the sources for
  Cloudflare or PowerDNS) — every platform
  procedure below still gates deletion on operator confirmation regardless, since the absence of a
  documented safeguard on some platforms is a reason for more caution, not less.
- **SOA/NS auto-generation on zone creation is a real behavior on some, not all, platforms** — Route 53
  and PowerDNS both auto-generate an SOA and NS record set from caller input at creation time; no caller-facing SOA record
  is documented in the sources for Cloudflare's zone API (Cloudflare
  manages its own zone metadata differently) — do not assume every platform in this skill has an
  SOA/NS pair the same way `dns-record-management` assumes for individual zones.

See `references/INDEX.md` for which platforms have a procedure, and each platform file for how it
implements zone lifecycle concretely — including where a platform's own behavior further narrows or
contradicts a generalization above.

## Procedure

1. **Identify the target platform** — from the caller's request or the `platform` argument. Check
   `references/INDEX.md`; if no matching row exists, stop: this skill doesn't cover it yet.
2. **Open `references/<platform>/procedure.md`** and follow it exactly — it contains that platform's
   full operational procedure, error handling, patterns, known limitations, tools, and verification
   checklist.
3. **Report the outcome** using that platform procedure's own status vocabulary — don't normalize it
   away.

## Known limitations

- Platform coverage is exactly the three vendors in `references/INDEX.md` (AWS Route 53, Cloudflare,
  PowerDNS Authoritative Server) — a platform not listed there needs a new reference file before this
  skill can be used for it.
- Does not cover individual record management inside an existing zone — see `dns-record-management`
  for that.
- Subdomain delegation is only documented in depth for the case where the parent domain's authority is
  hosted elsewhere and a subdomain is being handed to one of these platforms — see each platform's own
  `procedure.md` for exactly which delegation shapes are documented versus flagged as unconfirmed.

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
      destructive changes (zone deletion, which removes every record inside it)
- [ ] Outcome reported using the platform procedure's own status vocabulary
