# Cisco CML stored node configuration: bindings

An authenticated, TLS-verifying `virl2_client.ClientLibrary` is available as `client`; `lab`, `node`, and `link` are objects resolved by identifier. Bindings are publisher SDK methods at the cited commit, not NetClaw MCP tool names. Server/SDK compatibility must match the installed release.

| Operation | SDK binding | Input/result |
|---|---|---|
| Resolve/read | `lab.get_node_by_id(node_id)`; `node.configuration`; `node.configuration_files` | Main string; named-file list |
| Replace | `node.configuration = value` | String, `{"name": filename, "content": text}`, list of those dictionaries, or `None` |
| Extract | `node.extract_configuration()`; `lab.sync()` | Completion and refreshed stored configuration |

Unsupported configuration types raise `TypeError` with prefix `Unhandled type:`. The literal main-file name accepted by the SDK is `Main`.


## Sources

- [Cisco CML Node documentation and implementation](https://github.com/CiscoDevNet/virl2-client/blob/7ac2c924ccbdc02264578a95327f8a1363172076/virl2_client/models/node.py). Retrieved 2026-10-09.
