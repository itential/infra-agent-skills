# DNS Zone Management — Vendor Index

One row per supported vendor. Each vendor directory holds its own `procedure.md` (the full step-by-step),
plus wire-level `endpoints.md`.

| Vendor / Platform | Directory | Scope | Notes |
|---|---|---|---|
| AWS Route 53 | `route53/` | Create/read/update(comment)/delete a hosted zone; SOA/NS defaults; subdomain delegation from an externally-hosted parent domain | Also in `dns-record-management`'s INDEX.md (record-level ops there, zone lifecycle here — separate procedures, not merged). Deletion requires the zone reduced to only its default SOA/NS records first, and is documented as irreversible. |
| Cloudflare | `cloudflare/` | Create/read/delete a zone; setup-type selection (full/partial/secondary/internal); full-setup activation flow | Also in `dns-record-management`'s INDEX.md. Exact error list and subdomain-setup compatibility matrix are unverified — see that vendor's `procedure.md` Known limitations before treating as exhaustive. No zone-must-be-empty precondition for delete is documented (contrast with Route 53) — treat as unconfirmed, not as "no such constraint." |
| PowerDNS Authoritative Server | `powerdns/` | Create/read/update/delete a zone; `kind`/`nameservers`/replication-adjacent config; where subdomain delegation fits | Also in `dns-record-management`'s INDEX.md (RRset-level ops there, zone lifecycle here). Full `kind` enum, exact default SOA content, and exact error strings are flagged unconfirmed in that vendor's `procedure.md`. |

**Not covered:** Azure DNS, BlueCat, and Infoblox NIOS have zone-level APIs, but this skill has no
procedure for them; each appears in `dns-record-management`'s vendor set for record operations only.
A platform not listed in the table above needs a procedure before this skill can be used for it.
