# Cisco CML lab lifecycle: bindings

An authenticated, TLS-verifying `virl2_client.ClientLibrary` is available as `client`; `lab`, `node`, and `link` are objects resolved by identifier. Bindings are publisher SDK methods at the cited commit, not NetClaw MCP tool names. Server/SDK compatibility must match the installed release.

| Operation | SDK binding | Result |
|---|---|---|
| Resolve | `client.get_lab_list()`; `client.join_existing_lab(lab_id)` | IDs; Lab |
| Create | `client.create_lab(title=title, description=description)` | Lab with `id` |
| Import | `client.import_lab(topology_yaml, title=title)`; `client.import_lab_from_path(path, title=title)` | Lab; file import may raise `FileNotFoundError` |
| Inspect | `lab.details()`; `lab.state()`; `lab.has_converged()` | Native details/state; boolean |
| Export | `lab.download()` | YAML string |
| Start/stop | `lab.start(wait=True)`; `lab.stop(wait=True)` | Completion or wait/HTTP exception |
| Wipe/delete | `lab.wipe(wait=True)`; `lab.remove()` | Completion or exception |

Missing-ID error: `ValueError("No lab ID returned!")`. Missing labs use `LabNotFound`; convergence exhaustion raises `RuntimeError`. No automatic retry of a mutation is prescribed.


## Sources

- [Cisco CML ClientLibrary documentation and implementation](https://github.com/CiscoDevNet/virl2-client/blob/7ac2c924ccbdc02264578a95327f8a1363172076/virl2_client/virl2_client.py). Retrieved 2026-10-09.
- [Cisco CML Lab documentation and implementation](https://github.com/CiscoDevNet/virl2-client/blob/7ac2c924ccbdc02264578a95327f8a1363172076/virl2_client/models/lab.py). Retrieved 2026-10-09.
