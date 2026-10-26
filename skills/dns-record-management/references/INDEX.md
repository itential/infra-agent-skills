# DNS Record Management — Vendor Index

One row per supported vendor. Each vendor directory holds its own `procedure.md` (the full step-by-step),
plus wire-level `endpoints.md` and, where the vendor has non-obvious per-type field rules, `record-fields.md`.

| Vendor / Platform | Directory | Scope | Notes |
|---|---|---|---|
| AWS Route 53 | `route53/` | Create/update(upsert)/delete a basic record, with propagation confirmation | Change-batch model, `PENDING`→`INSYNC` polling |
| Azure DNS | `azure/` | Create/update/delete a record **set** (not a single record), add/remove within a set | Record-set (not record) model; zone-apex SOA/NS restrictions |
| Cloudflare | `cloudflare/` | Create a record (create-only) | Proxy-status gate requires operator confirmation |
| Infoblox NIOS | `infoblox/` | Create/read/update/delete A/AAAA/CNAME/MX/TXT/PTR | `_ref`-addressed object model (WAPI); grounded in Infoblox's own official WAPI reference guide, with per-type field names cross-checked against Infoblox's generated WAPI object schema — see `procedure.md` for the one unconfirmed detail (exact duplicate-object error string) |
| BlueCat Horizon / DDI Orchestrator | `bluecat/` | Create a record (create-only) | Record type is immutable once created; field names drawn from a secondary source — verify against the target instance |
| BlueCat Address Manager | `bluecat-address-manager/` | Create host/CNAME/alias/MX/TXT/SRV records (create-only) | A genuinely different BlueCat product from the row above (Address Manager is Integrity's self-hosted DDI engine with its own v2 REST API; Horizon is a separately-sold cloud control plane overlaying existing DNS/DHCP/IPAM systems) — see note below. Object-ID addressed throughout, not name-addressed. |
| PowerDNS Authoritative Server | `powerdns/` | Create/replace/delete an RRset, plus incremental single-record add (`EXTEND`)/remove (`PRUNE`) without touching the rest of the RRset | The only platform here with a native incremental-add/-remove primitive — others require a read-modify-write cycle for the same "add one value to a multi-value record" ask. Also the only platform with in-scope DNSSEC rectification (see note below). |
| Akamai Edge DNS | `akamai-edge-dns/` | Create/read/replace/delete a record set via direct record-set operations (Edge DNS API v2) | Record-set model: no per-value add/remove, replace needs the full array. Change lists, zone lifecycle and DNSSEC not covered. Apex SOA/NS handling, rate limits and ETag requirement are undocumented in the sources used (marked unverified); base path unverified |
| GoDaddy | `godaddy/` | Add, replace (by type+name or by type), delete (by type+name) and read DNS records (Domains API v1) | Type-and-name addressing, no record IDs. NS/SOA cannot be changed through record calls; nameserver changes and replace-all are not covered. Get-records details, TTL-minimum and apex-CNAME rules come from a troubleshooting guide whose v1 applicability is unstated; reference page lists both 200 and 204 for replace |
| Micetro (Men and Mice) | `micetro/` | Create/read/update/delete A/AAAA/CNAME/MX/TXT/PTR/SRV records | REST API; no NS or SOA coverage. Micetro also manages DHCP and IPAM, which are never merged into this skill's DNS reference files. Several details are unverified (TTL inheritance, CNAME/naming conflict enforcement, error strings, CNAME/PTR data format) and marked in `procedure.md`. |

**Not in scope for this skill:** NetBox IPAM (prefix/IP address allocation is a different capability —
see the separate `ipam-allocation` skill, not a DNS vendor variant).

**BlueCat Horizon vs. BlueCat Address Manager:** these are two distinct BlueCat products, not two
names for the same API. Address Manager (`bluecat-address-manager/`) is part of BlueCat's Integrity line — a
self-hosted DDI appliance with its own resource model and REST API rooted at `/api/v2`. Horizon
(`bluecat/`) is a separately-sold, cloud-hosted control plane that overlays and governs existing
DNS/DHCP/IPAM systems (which can include an Address Manager instance, Active Directory-integrated DNS,
BIND, Kea, or cloud DNS) rather than being one of those systems itself. Do not treat one vendor
directory as covering the other.

**DNSSEC scope (PowerDNS):** PowerDNS requires zone rectification after any RRset change on a
DNSSEC-enabled zone. That is a required follow-up step to a record change, so it is in scope, whereas
creating DNSSEC record types (DS/DNSKEY) directly is out of scope on every platform. DNSSEC-related
post-change housekeeping is in scope where a platform's own record-change procedure requires it.

**Apex SOA/NS and record addressing (Akamai Edge DNS, GoDaddy):** Akamai's documentation is silent on apex SOA/NS, so a restriction or auto-management there is not documented. Azure, Akamai, and GoDaddy address grouped records (record sets, type+name groups) rather than single records, so do not assume per-record addressing.

**Apex SOA/NS (Micetro):** Micetro's documentation treats SOA and NS as ordinary record types and states no apex restriction. Apex SOA/NS restrictions apply only where a platform documents them.
