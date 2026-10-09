# NetClaw Canvas envelope construction

Construct one A2UI payload using the publisher’s envelope builder, without collecting data or sending it to a UI.

## Common Sequences

- Payload: **Select supplied content** → **Build envelope** → **Inspect result**.
- Unavailable content: **Select supplied content** → **Build error envelope** → **Inspect result**.

### Select supplied content

The publisher registers seven component names, listed in the bindings. This procedure accepts already supplied component content, scope, warnings, and source records; it does not derive severity, health, approvals, or topology. The builder does not reject unknown component names or validate a component's content, so registration and compatible content are prerequisites rather than properties of a successful return.

### Build envelope

The normal builder returns a JSON-compatible object with a versioned Canvas envelope, component name, generated ID, timestamp, and the supplied content. Source records preserve whether each input was available, partial, or unavailable. The implementation also writes a local console/in-memory audit entry; that side effect does not establish a durable GAIT record. A module or serialization error leaves no usable envelope.

### Build error envelope

The error builder returns an error-card with a message and suggested next step. This is an unavailable visualization result, not a successful rendering. Suggestions are caller-supplied text, not authority to perform external actions.

### Inspect result

The returned envelope identifies the intended component and carries the supplied content and source metadata. Its creation is the terminal outcome here; there is no display acknowledgement in this API. The publisher's separate status helper uses only source-status flags: no sources or all unavailable yields failed; a mixed unavailable/partial set yields degraded; otherwise it yields complete. It does not inspect content correctness.

## Patterns

The envelope builder passes content through. Missing source metadata cannot be repaired by assigning a success label. The error envelope has a different property set from a normal envelope.

## Known limitations

The implementation is a payload builder, not a browser renderer. Its generated identifier uses ordinary pseudo-random values and is not an authentication token. No durable audit persistence or frontend compatibility is established by these functions.

## Tools

Assumes the authenticated client described in [the bindings](endpoints.md).

| Operation | Description | Category |
|---|---|---|
| Build envelope | Package supplied visualization content | Local transformation |
| Build error envelope | Package an unavailable-content result | Local transformation |
| Inspect source status | Summarize supplied availability flags | Local read |

## Verification checklist

- The component is one of the published registrations.
- Content and source status remain faithful to the supplied evidence.
- A constructed JSON payload is not reported as a displayed visualization.

## Sources

- [NetClaw Canvas envelope implementation](https://github.com/automateyournetwork/netclaw/blob/95bb17e27a6a2538fcb0168d0b1d0ab5bbe34692/workspace/skills/canvas-network-viz/lib/a2ui-renderer.js). Retrieved 2026-10-09.
- [Local audit implementation](https://github.com/automateyournetwork/netclaw/blob/95bb17e27a6a2538fcb0168d0b1d0ab5bbe34692/workspace/skills/canvas-network-viz/lib/gait-logger.js). Retrieved 2026-10-09.
