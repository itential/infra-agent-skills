# EVE-NG topology inventory and network creation: bindings

An authenticated cookie-backed JSON client for the configured EVE-NG server is already available. Paths are relative to that server; `{lab_path}` is the URL-encoded folder/file path, including `.unl`. No credentials or insecure TLS flags are embedded.

| Operation | Binding | Input/result |
|---|---|---|
| Topology | `GET /api/labs/{lab_path}/topology` | Topology data |
| Networks | `GET /api/labs/{lab_path}/networks`; `GET /api/labs/{lab_path}/networks/{network_id}` | Network IDs and metadata |
| Endpoints | `GET /api/labs/{lab_path}/links`; `GET /api/labs/{lab_path}/nodes/{node_id}/interfaces` | Ethernet networks, serial endpoints, interface mapping |
| Types | `GET /api/list/networks` | Available network types |
| Create | `POST /api/labs/{lab_path}/networks` | Required `type`; optional `name`, `left`, `top`; returned success envelope |


## Sources

- [EVE-NG API guide (version not specified; publisher warns of outdated examples)](https://www.eve-ng.net/index.php/how-to-eve-ng-api/). Retrieved 2026-10-09.
