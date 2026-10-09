# Cisco CML node lifecycle: bindings

An authenticated, TLS-verifying `virl2_client.ClientLibrary` is available as `client`; `lab`, `node`, and `link` are objects resolved by identifier. Bindings are publisher SDK methods at the cited commit, not NetClaw MCP tool names. Server/SDK compatibility must match the installed release.

| Operation | SDK binding | Inputs/result |
|---|---|---|
| Resolve | `lab.nodes()`; `lab.get_node_by_id(node_id)` | Node objects |
| Create | `lab.create_node(label, node_definition, x=0, y=0, populate_interfaces=False, **kwargs)` | Optional `image_definition`, `configuration`, `ram` (MiB), `cpus`; Node |
| Inspect | `node.state`; `node.interfaces()` | Native state; Interface list |
| Console | `node.console_logs(console_id, lines=None)`; `node.console_key(console_number=0)` | Logs; sensitive console key |
| Start/stop/wipe | `node.start(wait=True)`; `node.stop(wait=True)`; `node.wipe(wait=True)` | Completion or exception |
| Remove | `node.remove()` | Completion or exception |


## Sources

- [Cisco CML Node documentation and implementation](https://github.com/CiscoDevNet/virl2-client/blob/7ac2c924ccbdc02264578a95327f8a1363172076/virl2_client/models/node.py). Retrieved 2026-10-09.
- [Cisco CML Lab documentation and implementation](https://github.com/CiscoDevNet/virl2-client/blob/7ac2c924ccbdc02264578a95327f8a1363172076/virl2_client/models/lab.py). Retrieved 2026-10-09.
