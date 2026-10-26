# DHCP Scope Management — Vendor Index

One row per supported vendor. Each vendor directory holds its own `procedure.md` (the full step-by-step),
plus wire-level `endpoints.md`.

| Vendor / Platform | Directory | Scope | Notes |
|---|---|---|---|
| Infoblox NIOS | `infoblox/` | Create/update/delete a DHCP `range` inside an existing network, exclude specific addresses, create/update/delete a `fixedaddress` client reservation — via WAPI | REST-like WAPI. Also appears in `ipam-allocation`'s `INDEX.md` (`infoblox/` there covers network/IP allocation as inventory only) — the two Infoblox directories are deliberately separate procedures; do not merge them. Sourced from a third-party WAPI-doc mirror (Infoblox's own docs require an authenticated Grid Master session) — re-verify field names against the target Grid Master's WAPI version before automating. |
| ISC Kea | `isc-kea/` | Create/update(full or delta)/delete a DHCPv4 subnet, manage shared networks, create/get/update/delete a host reservation — via the Kea Control Agent's `subnet_cmds`/`host_cmds` hook command API | JSON-over-HTTP command/response envelope (`command`/`service`/`arguments` request; `result`/`text`/`arguments` response) — not literal HTTP method+path semantics the way REST is; see `procedure.md`'s own note that the same result code means different things across different commands. Does not appear in `ipam-allocation` (Kea isn't covered there). DHCPv4-primary; IPv6 command names exist but weren't independently verified. |
| Microsoft DHCP Server | `microsoft-dhcp/` | Create/update/delete an IPv4 scope, create/delete a client reservation — via the `DhcpServer` PowerShell module | **CLI/cmdlet-driven, not REST** — no `endpoints.md`; CLI syntax stays inline in `procedure.md`. Does not appear in `ipam-allocation` (not covered there). IPv4-only; the parallel `*Dhcpv6*` cmdlet family is not covered. |

There is no single wire standard grounding DHCP scope/lease management across vendors — RFC 2131
defines the DHCP protocol clients and servers speak on the wire, but says nothing about how an
operator's management API/CLI should represent a scope or reservation as a configuration object;
each platform above designed that management surface independently (NIOS's `range`/`fixedaddress`
objects, Kea's `subnet_cmds`/`host_cmds` command API, Windows's `DhcpServer` cmdlet family).
`SKILL.md`'s "Universal concepts" section reflects that: it states only the handful of structural
claims genuinely verified across all three platforms above (see that section's own citation of which
vendor confirmed each claim), not an assumed DHCP-wide standard.

**A genuinely different call mechanism, as in `ipam-allocation`:** Infoblox NIOS is REST-like WAPI,
Kea is a JSON command/response envelope over HTTP (not literal HTTP-method-per-operation semantics),
and Microsoft DHCP Server is PowerShell/CIM cmdlets with no wire-level API surface documented here at
all. `SKILL.md`'s "Tools" section and this table state the mechanism per-platform rather than
assuming REST.
