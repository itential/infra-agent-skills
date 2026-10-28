# VPN Tunnel Management — Vendor Index

One row per supported vendor/platform. Each vendor directory holds its own `procedure.md` (the full
step-by-step) plus a companion field-reference file (`endpoints.md` for REST/API-driven platforms, or
a descriptively-named field-reference file for CLI-driven platforms).

| Vendor / Platform | Directory | Scope | Notes |
|---|---|---|---|
| strongSwan | `strongswan/` | Site-to-site (and host-to-host) IPsec/IKE tunnel via `swanctl`/`swanctl.conf`, current control interface | CLI/config-driven, no `endpoints.md`. Does not cover the legacy `ipsec.conf`/`starter`/`stroke` toolchain, EAP/XAuth remote-access profiles, or PKI/certificate provisioning. |
| Palo Alto Networks | `paloalto-panos/` | Route-based (and policy-based Proxy-ID) site-to-site IPsec VPN: IKE Gateway, IKE/IPSec Crypto Profiles, IPsec Tunnel object, tunnel interface | `endpoints.md` documents field names/option lists; procedure covers web UI/XML API/CLI generically. Does not cover GlobalProtect remote access, certificate/PKI lifecycle, or security-policy/NAT configuration. |
| Juniper SRX (Junos OS) | `juniper-srx/` | Route-based, autokey-IKE site-to-site IPsec VPN: IKE/IPsec proposal, policy, gateway, VPN object, `st0` tunnel interface | CLI-driven; companion file is `ike-ipsec-proposal-fields.md`. Does not cover policy-based VPN, remote-access/dial-up VPN, Auto Discovery VPN, or hub-and-spoke NHTB. |
| Cisco ASA | `cisco-asa/` | Route-based IPsec VPN via static or dynamic Virtual Tunnel Interface (VTI): IPsec proposal/transform set, IPsec profile, tunnel interface or virtual template + tunnel-group attachment. **Create/configure only** — the source documents no read, update, or delete | CLI-driven, no `endpoints.md`; literal ASA commands are inline in `procedure.md`. The source gives no verification commands. Does not cover policy-based (crypto map) VPN, remote access, IP SLA tracking, or the peer's configuration. |
| Cloudflare WAN | `cloudflare-wan/` | List, read, create, update, and delete GRE and IPsec tunnel objects against Cloudflare's anycast endpoints; generate or set an IPsec pre-shared key; per-tunnel health-check settings, reading tunnel health by data center, and a symptom-to-fix table for unhealthy tunnels | REST, with `endpoints.md`. The tunnel object holds no IKE or Child SA parameters: those are chosen on the customer router from Cloudflare's supported set. GRE tunnels are unencrypted and have no negotiation. Cloudflare is the IKE responder only. Does not cover BGP settings, static routes, Network Interconnect, tunnel health alerts, or traffic analytics. Separate from Cloudflare's entries under other skills. Rate limits and API error codes are undocumented. |

Cloudflare WAN GRE tunnels have no encryption or negotiation, and its IPsec tunnel object carries no IKE or Child SA parameters (the customer router's configuration carries them). The two-stage and phase 1/phase 2 vocabulary applies to its IPsec tunnels only.
