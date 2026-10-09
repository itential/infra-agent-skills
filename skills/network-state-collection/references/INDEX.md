# Network State Collection — Platform Index

| Vendor / platform | Directory | Scope | Notes |
|---|---|---|---|
| Cisco pyATS / Genie | [cisco_pyats/](cisco_pyats/procedure.md) | Parse command output, learn feature state, and compare saved network snapshots | Collection and comparison report observed data; they do not diagnose root causes or approve a network change. |
| NAPALM | [napalm/procedure.md](napalm/procedure.md) | Supported read-only driver getters | Driver coverage and empty/error distinctions retained |
| Linux iproute2 | [iproute2/procedure.md](iproute2/procedure.md) | Local link, address and all-table IPv4/IPv6 route reads | No network changes |

The platform reference contains its source citations, execution sequence, tools, and verification.
New platforms require their own procedure and a check of the router's shared claims.
