# Cisco CML controller inspection

Read CML controller and catalogue state without changing it.

## Common Sequences

- Platform inspection: **Read controller** → **Read licensing** → **Read definitions**.

### Read controller

The health and resource-statistics operations return the controller's current JSON objects. Native fields and status are retained. Permission/transport/HTTP failure leaves that read incomplete rather than supplying zero utilization. No fixed health schema beyond the returned controller version is assumed.

### Read licensing

The licensing status read returns current licensing configuration/status. A returned licensing error is not automatically repaired by registration or renewal. A specific node allowance is reported only when present in the actual response.

### Read definitions

The node-definition catalogue returns available definitions and their native properties. Definition requirements are not substituted with NetClaw's fixed RAM/CPU table. The observed data can support an operator's separate capacity decision; it does not guarantee that a planned lab will fit.

## Patterns

Licensing, resource utilization and available node definitions are separate observations. Missing data in one is not completed from another.

## Known limitations

No license registration, image upload, maintenance-mode change, host admission or automatic RAM multiplier is included. SDK methods return server objects; an exhaustive version-independent field schema is unverified.

## Tools

Assumes the authenticated client described in [the bindings](endpoints.md).

| Operation | Description | Category |
|---|---|---|
| Controller health/statistics | Read controller observations | Platform read |
| Licensing status | Read current licensing state | Platform read |
| Node definitions | Read available simulation templates | Catalogue read |

## Verification checklist

- Each requested read has native data or an explicit error.
- Fields are reported without invented capacity thresholds.
- No licensing or controller mutation occurred.

## Sources

- [Cisco controller SDK](https://github.com/CiscoDevNet/virl2-client/blob/7ac2c924ccbdc02264578a95327f8a1363172076/virl2_client/virl2_client.py). Retrieved 2026-10-09.
- [Cisco licensing SDK](https://github.com/CiscoDevNet/virl2-client/blob/7ac2c924ccbdc02264578a95327f8a1363172076/virl2_client/models/licensing.py). Retrieved 2026-10-09.
- [Cisco definition SDK](https://github.com/CiscoDevNet/virl2-client/blob/7ac2c924ccbdc02264578a95327f8a1363172076/virl2_client/models/node_image_definition.py). Retrieved 2026-10-09.
