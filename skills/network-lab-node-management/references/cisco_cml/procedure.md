# Cisco CML node lifecycle

Create, inspect, start, stop, wipe or remove a selected CML node.

## Common Sequences

- Add a node: **Resolve and inspect** → **Create** → **Resolve and inspect**.
- Change runtime state: **Resolve and inspect** → **Start/stop/wipe** → **Resolve and inspect**.
- Remove: **Resolve and inspect** → **Remove**.

### Resolve and inspect

The lab’s node inventory supplies node IDs and definitions. Node objects provide native state, interfaces, console logs, and a console key. A console key is access material and is excluded from general reports. Missing-node or missing-interface errors mean resolution failed. A transport or HTTP failure remains a failed operation; the SDK does not supply a universal retry rule. A missing lab/node/interface is a resolution failure, not permission to recreate it. A convergence wait that raises a runtime error is incomplete, not successful.

### Create

Creation uses the requested label and an installed node definition, with any requested image/configuration overrides. Before allocating the node: stop and confirm with the operator before proceeding. The publisher returns a node object with an ID. Duplicate labels cause a warning in the client, not a uniqueness guarantee; subsequent operations use IDs.

### Start/stop/wipe

Each action changes the node, and wipe clears its disks: stop and confirm with the operator before proceeding. The client’s optional wait checks convergence. After the action, native state is retained as evidence; guest command readiness is not inferred from process state. An exception or exhausted wait remains incomplete.

### Remove

Removal deletes the node from the lab: stop and confirm with the operator before proceeding. The publisher removes the server object and its local representation; a stale node is not reused. Transport/HTTP failure remains a failed removal.

## Patterns

The publisher supports interfaces populated at creation or added later. No fixed boot-time or memory sizing heuristic is added. Console logs can contain sensitive configuration and credentials.

## Known limitations

No guest CLI execution, operating-system commands, arbitrary hardware sizing, or node-definition installation is included.

## Tools

Assumes the authenticated client described in [the bindings](endpoints.md).

| Operation | Description | Category |
|---|---|---|
| Inspect | Resolve node, state, interfaces and console metadata | Read |
| Create | Add a node using an installed definition | Change |
| Start/stop | Change node runtime state | Change |
| Wipe/remove | Erase node disks or remove node | Destructive |

## Verification checklist

- Created node ID and requested definition are retained.
- Native state and convergence result are separate.
- Wipe is explicitly distinguished from stop.
- Console secrets are not placed in reports.

## Sources

- [Cisco CML Node documentation and implementation](https://github.com/CiscoDevNet/virl2-client/blob/7ac2c924ccbdc02264578a95327f8a1363172076/virl2_client/models/node.py). Retrieved 2026-10-09.
- [Cisco CML Lab documentation and implementation](https://github.com/CiscoDevNet/virl2-client/blob/7ac2c924ccbdc02264578a95327f8a1363172076/virl2_client/models/lab.py). Retrieved 2026-10-09.
