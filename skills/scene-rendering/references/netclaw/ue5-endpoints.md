# NetClaw Unreal topology scene: bindings

An installed pinned NetClaw UE5 renderer and compatible Unreal MCP Editor plugin are prerequisites. The client receives the operator-supplied server address as `url`; no default endpoint is assumed.

| Operation | Binding | Contract |
|---|---|---|
| Session | `async with UE5MCPClient(url=editor_mcp_url) as client` | Initializes MCP session; can raise `UE5MCPError` |
| Discovery | `await client.list_toolsets()`; `await client.describe_toolset(toolset_name)` | Actual toolsets and parameter schemas |
| Render | `await render_topology_from_dict(client, data, clear_existing=False, setup_lighting=False, apply_materials=True)` | `RenderResult(success, devices_rendered, links_rendered, errors, duration_seconds)` |

`data.devices` uses explicit `hostname`, `device_type`, `status`, and optional documented `interfaces`, `model`, `vendor`, `ip_addresses`, `utilization`. `data.links` uses `source_device`, `target_device`, `source_interface`, `target_interface`, explicit `status`, and optional `bandwidth`/`utilization`. The pinned model is authoritative for accepted values; supplied data must match it.

Toolset names are version-specific. The pinned client/actor helpers reference `editor_toolset.toolsets.actor.ActorTools` and related toolsets. Epic's current plugin documentation does not promise those names across releases. Discovery mismatch is an unsupported binding, not permission to invent a replacement.


## Sources

- [renderer.py](https://github.com/automateyournetwork/netclaw/blob/95bb17e27a6a2538fcb0168d0b1d0ab5bbe34692/workspace/skills/ue5-network-viz/renderer.py). Retrieved 2026-10-09.
- [ue5_mcp_client.py](https://github.com/automateyournetwork/netclaw/blob/95bb17e27a6a2538fcb0168d0b1d0ab5bbe34692/workspace/skills/ue5-network-viz/ue5_mcp_client.py). Retrieved 2026-10-09.
- [actors.py](https://github.com/automateyournetwork/netclaw/blob/95bb17e27a6a2538fcb0168d0b1d0ab5bbe34692/workspace/skills/ue5-network-viz/actors.py). Retrieved 2026-10-09.
- [Epic Unreal MCP in Unreal Editor](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-mcp-in-unreal-editor). Retrieved 2026-10-09.
