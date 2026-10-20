---
name: dns-record-management
description: Create, update, or delete a DNS record (A, AAAA, CNAME, MX, TXT, NS, SOA, PTR, SRV, CAA) on a supported DNS platform — AWS Route 53, Azure DNS, Cloudflare, Infoblox NIOS, BlueCat Horizon/DDI Orchestrator, BlueCat Address Manager, PowerDNS Authoritative Server, Akamai Edge DNS, GoDaddy, or Micetro — following RFC 1035/2136/1123 semantics and each platform's documented procedure. Use when a DNS record must be created, changed, or removed on one of these platforms. Assumes an authenticated API/WAPI client for the target platform is already available; this skill does not provision or authenticate that client. Does not cover DNS zone creation/deletion (see dns-zone-management), alias/traffic-routing record types (Route 53 alias records, Azure targetResource), creating DNSSEC record types directly (DS/DNSKEY), or NetBox IPAM (a separate capability — see references/INDEX.md). DNSSEC post-change housekeeping a platform requires (e.g. PowerDNS zone rectification) is in scope where its procedure documents it.
argument-hint: "[platform] [action] [record_name] [record_type] [values...]"
---

# DNS Record Management

Creates, updates, or deletes a DNS record on one of the supported platforms, honoring both the universal
RFC-level record semantics (`references/rfc1035-1123-extract.md`) and that platform's own documented
procedure, field rules, and restrictions (`references/<platform>/procedure.md`).

## When to use this skill

- A DNS record (A/AAAA/CNAME/MX/TXT/NS/SOA/PTR/SRV/CAA) needs to be created, updated, or deleted on
  Route 53, Azure DNS, Cloudflare, Infoblox NIOS, BlueCat Horizon/DDI Orchestrator, BlueCat Address
  Manager, PowerDNS, Akamai Edge DNS, GoDaddy, or Micetro.
- Not for creating the zone itself — see `dns-zone-management` for zone creation, SOA/NS
  configuration, and subdomain delegation. Also not for alias/traffic-routing record types, creating
  DNSSEC record types directly, or IP address space allocation (that's IPAM, not DNS record
  management — see `references/INDEX.md`).

## Universal concepts (apply regardless of platform)

- **CNAME exclusivity** (RFC 1035 §3.6.2): a name holding a CNAME cannot hold any other record type at
  the same node. Several platforms enforce this as a structural conflict check before create.
- **Zone-apex SOA/NS are not ordinary records.** Where a platform documents it, it restricts, auto-manages,
  or excludes caller-driven changes to the apex SOA/NS set; where its docs are silent, treat them as not
  ordinary records anyway and consult platform-specific guidance.
- **TTL governs resolver caching** (RFC 1035 §3.2.1) — platforms may enforce a minimum, a range, or
  a fixed value under certain conditions, so check the platform's own TTL rules.
- **A destructive or already-resolving change needs operator confirmation before submission** — every
  platform procedure below has this gate built into its own steps; never skip it because "the API call
  would succeed."

See `references/rfc1035-1123-extract.md` for the full grounding (record type definitions, which concepts
are RFC-derived vs. platform-specific).

## Procedure

1. **Identify the target platform** — from the caller's request or the `platform` argument. If it isn't
   one of the platforms in `references/INDEX.md`, stop: this skill doesn't cover it, and does not
   improvise a generic procedure for an unsupported platform.
2. **Open `references/<platform>/procedure.md`** and follow it exactly — it contains that platform's
   full operational procedure, error handling, patterns, known limitations, tools, and verification
   checklist. This file is intentionally the router; the real steps live per platform because the
   platforms genuinely do not share one procedure (see `references/INDEX.md` for why, e.g. per-record versus grouped record-set addressing).
3. **Report the outcome** using that platform procedure's own status vocabulary (e.g. `SUCCESS`,
   `CREATED`, `ALREADY_EXISTS`, `REJECTED_*`, `FAILED`) — don't normalize it away.

## Known limitations

- Does not cover DNS zone creation — every platform procedure assumes the zone already exists (except
  where a platform's own procedure documents zone creation as a directly-related prerequisite step,
  e.g. PowerDNS).
- Does not cover alias/traffic-routing record types (Route 53 alias records, Azure `targetResource`) or
  creating DNSSEC record types directly (DS/DNSKEY) — out of scope on every platform that offers them.
  DNSSEC-related post-change housekeeping a platform's own procedure requires (e.g. PowerDNS zone
  rectification) is in scope, since it's a documented follow-up step to a record change, not a record
  type being created.
- Does not cover NetBox or other IPAM (IP address space allocation) — see `references/INDEX.md`.
- Platform coverage is exactly the ten vendors in `references/INDEX.md` — a platform not listed there
  needs a new `references/<platform>/procedure.md` before this skill can be used for it.

## Contributing to this skill

**`SKILL.md` itself should only ever change for two reasons: a bug in the universal concepts/router
logic above, or adding a pointer to a newly-supported platform.** Platform-specific procedure changes —
a new error code, a corrected field name, a changed API path — belong in that platform's own
`references/<platform>/procedure.md` and `endpoints.md`, never here. If you're about to add vendor-
specific detail to this file, put it in the platform's reference file instead.

## Tools

Each platform assumes its own authenticated client (REST API, WAPI) — see `references/INDEX.md` for
which, and that platform's `procedure.md` for the specific operations/mechanisms.

## Verification checklist

- [ ] Target platform confirmed against `references/INDEX.md` before proceeding
- [ ] That platform's own `procedure.md` was followed, including its own confirmation gates and error
      handling — not a generic/improvised sequence
- [ ] Outcome reported using the platform procedure's own status vocabulary
