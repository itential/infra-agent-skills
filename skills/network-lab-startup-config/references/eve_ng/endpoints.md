# EVE-NG native configuration export: bindings

An authenticated cookie-backed JSON client for the configured EVE-NG server is already available. Paths are relative to that server; `{lab_path}` is the URL-encoded folder/file path, including `.unl`. No credentials or insecure TLS flags are embedded.

| Operation | Binding | Result |
|---|---|---|
| Inspect | `GET /api/labs/{lab_path}`; `GET /api/labs/{lab_path}/nodes` | Lab/node metadata |
| Export selected node | `GET /api/labs/{lab_path}/nodes/{node_id}/export` | Mutating GET; export message number 80058 |
| Export all nodes | `GET /api/labs/{lab_path}/nodes/export` | Mutating GET; export message number 80057 |


## Sources

- [EVE-NG API guide (version not specified; publisher warns of outdated examples)](https://www.eve-ng.net/index.php/how-to-eve-ng-api/). Retrieved 2026-10-09.
