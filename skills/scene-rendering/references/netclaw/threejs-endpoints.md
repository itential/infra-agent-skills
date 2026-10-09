# NetClaw Three.js topology scene: bindings

The pinned skill directory is already available on the Python module path. No package installation is part of this procedure.

| Operation | Binding | Contract |
|---|---|---|
| Model | `topology_model.TopologySnapshot(snapshot_id, source_kind, source_label, devices=..., links=...)` | Use `Device`, `Interface`, `Link`, `LinkEndpoint` from the same module; explicit roles/states; `real_stencil_mode=False` |
| Validate | `snapshot.validate()` | Returns `None` or raises `ValueError` for parent/endpoint mismatch |
| Build payload | `scene_builder.build_scene_payload(snapshot)` | Dictionary with devices, links, legend, source metadata |
| Build HTML | `html_template.render_html(payload)` | HTML string; trusted `source_label` required |
| Write | `output.write_scene(html, snapshot.snapshot_id)` | `Path` beneath `workspace/output/threejs-network-viz`; `topology-{UTC seconds}-{sanitized ID}.html` |
| Open | `output.open_in_browser(path)` | Returns `None`; no render acknowledgement |

Model field names and types are defined by the pinned `topology_model.py`; supplied interfaces use `parent_hostname`, and link endpoints use `hostname` plus optional `interface_name`. No secret-bearing metadata is required.


## Sources

- [topology_model.py](https://github.com/automateyournetwork/netclaw/blob/95bb17e27a6a2538fcb0168d0b1d0ab5bbe34692/workspace/skills/threejs-network-viz/topology_model.py). Retrieved 2026-10-09.
- [scene_builder.py](https://github.com/automateyournetwork/netclaw/blob/95bb17e27a6a2538fcb0168d0b1d0ab5bbe34692/workspace/skills/threejs-network-viz/scene_builder.py). Retrieved 2026-10-09.
- [html_template.py](https://github.com/automateyournetwork/netclaw/blob/95bb17e27a6a2538fcb0168d0b1d0ab5bbe34692/workspace/skills/threejs-network-viz/html_template.py). Retrieved 2026-10-09.
- [output.py](https://github.com/automateyournetwork/netclaw/blob/95bb17e27a6a2538fcb0168d0b1d0ab5bbe34692/workspace/skills/threejs-network-viz/output.py). Retrieved 2026-10-09.
