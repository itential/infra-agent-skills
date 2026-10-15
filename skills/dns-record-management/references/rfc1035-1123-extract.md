# DNS Record Concepts — RFC Extract

Grounding reference for the record types and terms `SKILL.md` and the per-vendor procedures assume.
Primary sources: RFC 1035 (Domain Names — Implementation and Specification), RFC 2136 (Dynamic Updates
in the Domain Name System), RFC 1123 (Requirements for Internet Hosts), RFC 1183/2782/6844 (RP/AFSDB,
SRV, CAA respectively — the newer record types no vendor here treats as "basic" the same way as A/CNAME).

## Core record types referenced across the vendor procedures

| Type | RFC | Purpose |
|---|---|---|
| A | 1035 §3.4.1 | Maps a name to an IPv4 address. |
| AAAA | 3596 | Maps a name to an IPv6 address. |
| CNAME | 1035 §3.3.1 | Aliases a name to another (canonical) name. A name with a CNAME cannot also hold other record types at the same node (1035 §3.6.2) — this is *the* structural rule behind Cloudflare's and others' "A/AAAA cannot share a name with an existing CNAME" check. |
| MX | 1035 §3.3.9 | Mail exchange, ordered by `preference` (lower value = more preferred). |
| NS | 1035 §3.3.11 | Delegates a subdomain to authoritative name servers. |
| PTR | 1035 §3.3.12 | Reverse-maps an address to a name (in the `in-addr.arpa`/`ip6.arpa` tree). |
| SOA | 1035 §3.3.13 | Zone authority record — one per zone, holds serial/refresh/retry/expire/minimum-TTL. Every vendor here treats SOA specially (auto-created, restricted, or entirely out of scope) rather than as a record a caller creates freely. |
| TXT | 1035 §3.3.14 | Arbitrary text, commonly used for verification tokens and SPF/DKIM/DMARC. |
| SRV | 2782 | Service location: priority/weight/port/target. |
| CAA | 6844 | Constrains which CAs may issue certificates for the name. |

## Universal concepts every vendor procedure builds on

- **A record set at a given name+type is the unit of change** — but what counts as "the record" is not
  uniform: most platforms treat one record = one value, while Azure's record *set* explicitly bundles
  multiple values (e.g. two MX hosts) under one name+type. This is why Azure's procedure has an
  ADD_RECORD path with no equivalent elsewhere.
- **TTL (Time To Live, RFC 1035 §3.2.1)** governs resolver caching duration in seconds. Every vendor here
  accepts a caller-supplied TTL, though enforcement differs (Cloudflare silently overrides TTL to Auto
  when proxying is enabled).
- **Zone delegation (NS) at a zone's apex is structurally different from NS elsewhere** — RFC 1035
  requires the parent zone's own NS set at its apex to reflect the zone's actual authoritative servers.
  This is the root cause of Azure's apex-NS restriction (can't remove the zone's own assigned servers)
  and a general reason every vendor treats apex NS/SOA as special-cased rather than a plain record.
- **DNS updates are not universally transactional** — RFC 2136 (Dynamic Update) describes an update as a
  set of prerequisites + a set of RR changes applied together, which Route 53's all-or-nothing change
  batch mirrors; not every vendor implementation here offers the same atomicity (BlueCat and Infoblox
  create one record per call, with no documented multi-record transaction).

## What is genuinely vendor-specific (not RFC-derived)

None of the following come from the RFCs — they are vendor product decisions, and are documented per
vendor under their own `references/<vendor>/` directory, not here:
- Whether creation is idempotent (Infoblox: yes, by design) or not (others: undocumented duplicate
  behavior).
- API shape (REST route/method, WAPI object-type conventions, ARM record-set schema).
- Extra platform features layered on top of a DNS record (Cloudflare's proxy/CDN routing, Route 53's
  alias records, Azure's `targetResource` alias sets) — RFC 1035 has no concept of any of these.
