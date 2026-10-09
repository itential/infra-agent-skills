# Cisco CML link lifecycle: bindings

An authenticated, TLS-verifying `virl2_client.ClientLibrary` is available as `client`; `lab`, `node`, and `link` are objects resolved by identifier. Bindings are publisher SDK methods at the cited commit, not NetClaw MCP tool names. Server/SDK compatibility must match the installed release.

| Operation | SDK binding | Inputs/result |
|---|---|---|
| Inspect | `lab.nodes()`; `lab.interfaces()`; `lab.links()`; `lab.sync()` | Current topology objects |
| Resolve interface | `lab.get_interface_by_id(interface_id)` | Interface or `InterfaceNotFound` |
| Add interface | `lab.create_interface(node, slot=None, wait=True)` | Interface; may fill preceding available slots |
| Connect | `lab.create_link(interface_a, interface_b, wait=True)` | Link |
| Disconnect | `lab.remove_link(link, wait=True)` | Completion or exception |


## Sources

- [Cisco CML Lab documentation and implementation](https://github.com/CiscoDevNet/virl2-client/blob/7ac2c924ccbdc02264578a95327f8a1363172076/virl2_client/models/lab.py). Retrieved 2026-10-09.
