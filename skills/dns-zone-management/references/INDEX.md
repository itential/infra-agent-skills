# DNS Zone Management — Vendor Index

One row per supported vendor. Each vendor directory holds its own `procedure.md` (the full step-by-step),
plus wire-level `endpoints.md`.

| Vendor / Platform | Directory | Scope | Notes |
|---|---|---|---|
| AWS Route 53 | `route53/` | Create/read/update(comment)/delete a hosted zone; SOA/NS defaults; subdomain delegation from an externally-hosted parent domain | Also in `dns-record-management`'s INDEX.md (record-level ops there, zone lifecycle here — separate procedures, not merged). Deletion requires the zone reduced to only its default SOA/NS records first, and is documented as irreversible. |
| Cloudflare | `cloudflare/` | Create/read/delete a zone; setup-type selection (full/partial/secondary/internal); full-setup activation flow | Also in `dns-record-management`'s INDEX.md. Some detail sourced via an LLM-mediated documentation fetch rather than a raw-page read — see that vendor's `procedure.md` Known limitations before treating as exhaustive (exact error list, subdomain-setup compatibility matrix unconfirmed). No documented zone-must-be-empty precondition for delete was found (contrast with Route 53) — treat as unconfirmed, not as "no such constraint." |
| PowerDNS Authoritative Server | `powerdns/` | Create/read/update/delete a zone; `kind`/`nameservers`/replication-adjacent config; where subdomain delegation fits | Also in `dns-record-management`'s INDEX.md (RRset-level ops there, zone lifecycle here). Some detail sourced via an LLM-mediated documentation fetch — full `kind` enum, exact default SOA content, and exact error strings are flagged unconfirmed in that vendor's `procedure.md`. |

**Not yet covered:** Azure DNS and BlueCat both appear in `dns-record-management`'s vendor set but were
not added here in this pass — Azure DNS's zone-level REST API (`Zones - Create Or Update`) was spot-
checked during this research and does look real and well-documented (tags, `zoneType`
Public/Private, `nameServers`/`maxNumberOfRecordSets` in the response), so it's a reasonable next
candidate; it just wasn't carried through to a full procedure/endpoints pair in this pass to keep
depth over breadth. BlueCat and Infoblox NIOS zone-level APIs were not researched at all here.
