# Record Field Reference — Cloudflare DNS Record Object

Full field breakdown for the record object accepted by `POST /zones/{zone_id}/dns_records`, drawn from
the Cloudflare API reference plus the dashboard-facing proxy-status, TTL, and record-attributes pages.

## Core fields (all record types)

| Field | Required | Notes |
|---|---|---|
| `type` | Yes | Record type. See supported types below. |
| `name` | Yes | Complete DNS record name including the zone name, in Punycode. |
| `ttl` | No | Integer seconds. `1` = "Auto." Unproxied: 60–86400s (30s minimum on Enterprise plans). Proxied: locked to Auto (300s), cannot be edited. |
| `proxied` | No | Boolean. Only valid for `A`, `AAAA`, `CNAME` — see "Proxy status" below. |
| `comment` | No | Reference-only note; no effect on DNS resolution. Max 100 chars (Free), 500 chars (Pro/Business/Enterprise). Excludes `\n`/`\r`. One per record. |
| `tags` | No | Reference-only array of `name:value` pairs; no effect on DNS resolution. Pro/Business/Enterprise only (not Free). Tag name: letters/numbers/`-`/`_`, case-insensitive, max 32 chars. Tag value: max 100 chars. Max 20 tags/record. Names prefixed `cf-` are reserved for Cloudflare's own use — do not set manually. |

## Per-type content/data fields

| Type | Content/data field(s) | Notes |
|---|---|---|
| `A` | `content` — valid IPv4 address | Must be your origin server's address; cannot be a Cloudflare-owned IP. Supports `proxied`. |
| `AAAA` | `content` — valid IPv6 address | Same origin-IP restriction as A. Supports `proxied`. |
| `CNAME` | `content` — valid target hostname | Must differ from the record's own `name`. Supports `proxied`; if proxied, the final resolved target must have valid A/AAAA records. Cloudflare may block proxying certain CNAMEs to prevent misconfiguration (exact rule not documented in sources retrieved). |
| `MX` | `content` — mail server hostname; `priority` (number) | `priority` is required for MX. Does not support `proxied`. |
| `TXT` | `content` — one or more quoted text strings | Max 255 bytes per string (documented constraint). Does not support `proxied`. |
| `SRV` | `data` object: `priority`, `weight`, `port`, `target` | Does not support `proxied` (confirmed explicitly in source 3). |
| `CAA` | `data` object: `flags`, `tag`, `value` | Specifies which CAs may issue certs for the domain. Does not support `proxied`. |
| `NS` | `content` — nameserver hostname | Cloudflare supports up to 10 NS records per delegation name; best practice is 7 or fewer. Cannot share a name with any other record type. Does not support `proxied`. |
| `PTR` | `content` — domain name the address points to | Should preferably be added to reverse zones. Does not support `proxied`. |

**Not covered by this skill (create-only, common types above are the scope):** `SOA` (auto-created by
Cloudflare, not user-created), `SVCB`/`HTTPS` (Cloudflare auto-generates these for proxied domains with
HTTP/2 or HTTP/3), `DS`/`DNSKEY` (DNSSEC), and less-common types (`URI`, `NAPTR`, `SSHFP`, `TLSA`,
`SMIMEA`, `CERT`) — the source pages describe these narratively without a create-field table; if a
caller needs one of these, check the Cloudflare API reference for its exact `data`/`content` schema
before extending this skill.

## Settings object (optional, type-dependent)

Available on several types (A, AAAA, CNAME, MX, NS, PTR, TXT per the API reference):
- `ipv4_only` — "When enabled, only A records will be generated." (CNAME flattening related)
- `ipv6_only` — "When enabled, only AAAA records will be generated."
- `flatten_cname` — CNAME flattening at the zone apex (noted for CNAME records).

`A`/`AAAA` also expose `private_routing` (boolean) tied to the Enterprise-only "private network routing"
feature — out of scope for this skill.

## Proxy status semantics (`proxied` field)

- Only `A`, `AAAA`, `CNAME` support `proxied: true`. Setting it on any other type is invalid.
- **Proxied ("orange cloud")**: Cloudflare sits between visitors and the origin — optimizing, caching,
  and protecting traffic. Origin IP is hidden.
- **DNS-only ("grey cloud", `proxied: false`)**: Cloudflare answers with the record's actual
  content/IP and does not route HTTP/HTTPS traffic through its network. This exposes the origin IP to
  anyone who queries the record.
- If multiple records share the same name and any one is proxied, all records at that name are treated
  as proxied.
- Records that exist for non-traffic purposes (e.g. a CNAME used only for domain-ownership verification)
  should NOT be proxied, per Cloudflare's own guidance.
- Proxying is enabled by default for eligible record types during initial domain onboarding — not
  necessarily during ad hoc record creation via this skill (the how-to page does not state a default
  for individually created records; treat `proxied` as an explicit input each time, defaulting to
  `false`/unset unless the caller specifies otherwise).

## TTL semantics

- Unproxied record TTL: 60–86400 seconds (non-Enterprise), 30–86400 seconds (Enterprise). `1`/"Auto" =
  300 seconds.
- Proxied record TTL: fixed at Auto (300 seconds); cannot be set to any other value.
- Longer TTL = better lookup caching, slower propagation of changes. Shorter TTL = opposite tradeoff.
- Client-side DNS caches may hold a record longer than its TTL states — this is a known, stated
  limitation, not a Cloudflare defect.

## Structural constraints (will cause a create call to fail)

- A/AAAA records cannot exist on the same name as a CNAME record.
- NS records cannot exist on the same name as any other record type.
- Maximum wire-format size: 4,096 bytes per record.
- Combined content of multiple records sharing the same name+type: cannot exceed 8,192 characters.
