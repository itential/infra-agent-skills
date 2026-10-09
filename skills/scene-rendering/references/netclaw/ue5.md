# NetClaw Unreal topology scene

Create a static scene from explicitly supplied topology using the pinned renderer and a compatible Unreal Editor MCP server.

## Common Sequences

- Static render: **Resolve editor tools** → **Prepare supplied model** → **Render once** → **Inspect render result**.

### Resolve editor tools

Epic's Unreal MCP documentation describes the experimental Editor plugin and tool discovery. The server address is the configured address reported by the running Editor, not an assumed port. The publisher client initializes a session and discovers toolsets/schemas. This pinned renderer expects specific actor, primitive, object, and material tool contracts. If discovery does not match those contracts, this procedure is unsupported for that Editor version; no guessed alias or replacement call is used. Session or discovery errors end the operation before mutation. Epic documents serial Editor execution, so calls are not overlapped.

### Prepare supplied model

The renderer consumes device and link records. Explicit device types and states are prerequisites: the parser otherwise infers types from names and defaults missing state to healthy. Those defaults are not evidence about a network. Links and interface evidence describe the supplied snapshot. The selected Editor scene must be an approved destination for adding these objects.

### Render once

Rendering creates scene actors and may create/apply materials: stop and confirm with the operator before proceeding. This scope explicitly disables clearing existing actors and changing lighting. The publisher executes device, interface, link, and label creation in sequence. Failed device/link/interface creation contributes errors, and an exception can leave a partially changed scene. A failed or timed-out call does not authorize an automatic retry or the publisher's alternate fast-render fallback.

### Inspect render result

The result contains a native success flag, device/link counts, error list, and duration. Publisher limitation: individual creation errors can coexist with a true success flag, and some label/material results are not included in that flag. Counts and errors therefore remain visible in the outcome; a true flag alone is not evidence of a complete scene. Zero created devices for a nonempty input is a native failure. No automatic cleanup is part of this procedure.

## Patterns

The renderer maintains local actor state. Rendering into an already populated scene is not documented as idempotent. A partial scene persists after many failure paths.

## Known limitations

Only one static render is covered. No live refresh, incident coloration, ping overlays, role inference, actor clearing, lighting setup, or automatic fallback. Compatibility with an arbitrary Unreal release is not established by the NetClaw README.

## Tools

Assumes the authenticated client described in [the bindings](ue5-endpoints.md).

| Operation | Description | Category |
|---|---|---|
| Discover Editor tools | Initialize session and inspect available schemas | Read |
| Render topology | Add supplied topology actors to the selected scene | Change |
| Inspect result | Read native counts, errors and success flag | Read |

## Verification checklist

- Installed tool contracts match the pinned renderer before mutation.
- Explicit device types/states prevent unsupported inference.
- Actor creation had operator confirmation.
- Counts and all recorded errors accompany the native flag; partial results are not hidden.

## Sources

- [renderer.py](https://github.com/automateyournetwork/netclaw/blob/95bb17e27a6a2538fcb0168d0b1d0ab5bbe34692/workspace/skills/ue5-network-viz/renderer.py). Retrieved 2026-10-09.
- [ue5_mcp_client.py](https://github.com/automateyournetwork/netclaw/blob/95bb17e27a6a2538fcb0168d0b1d0ab5bbe34692/workspace/skills/ue5-network-viz/ue5_mcp_client.py). Retrieved 2026-10-09.
- [actors.py](https://github.com/automateyournetwork/netclaw/blob/95bb17e27a6a2538fcb0168d0b1d0ab5bbe34692/workspace/skills/ue5-network-viz/actors.py). Retrieved 2026-10-09.
- [Epic Unreal MCP in Unreal Editor](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-mcp-in-unreal-editor). Retrieved 2026-10-09.
