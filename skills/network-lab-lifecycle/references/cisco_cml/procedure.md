# Cisco CML lab lifecycle

Manage CML labs using Cisco’s Python client.

## Common Sequences

- Create/import: **Resolve or create** → **Inspect**.
- Operate: **Inspect** → **Start or stop** → **Inspect**.
- Remove: **Inspect** → **Start or stop** (stop) → **Wipe** → **Delete**.

### Resolve or create

The client lists accessible lab IDs and joins the exact selected lab. Creation returns a lab object with an ID; importing YAML also returns a lab object. Before creation or import: stop and confirm with the operator before proceeding. Missing local import files fail before upload; a response without an ID raises the missing-ID error in the bindings. No creation success is inferred from that error.

### Inspect

Lab details and the native state describe the selected lab. YAML export returns a string representation; it is a topology/configuration export, not a saved running VM memory image. A copy can be created by exporting and importing into a new lab, with the creation gate above.

### Start or stop

Starting/stopping changes all nodes and links: stop and confirm with the operator before proceeding. The publisher client can wait for convergence and query native lab state. A start request alone does not establish that every guest is configured. A transport or HTTP failure remains a failed operation; the SDK does not supply a universal retry rule. A missing lab/node/interface is a resolution failure, not permission to recreate it. A convergence wait that raises a runtime error is incomplete, not successful.

### Wipe

Wiping clears node/link runtime state: stop and confirm with the operator before proceeding. The client can wait for convergence; the native state and details remain the outcome evidence. Stored topology export does not preserve running disks.

### Delete

The publisher requires the lab to be stopped and wiped first. Deletion is irreversible: stop and confirm with the operator before proceeding. Successful removal makes the local lab object stale; subsequent operations must resolve a current object. HTTP failure is not deletion success.

## Patterns

Lab removal has explicit stopped-and-wiped prerequisites. A client-side local list is not the same operation as retrieving the server’s current accessible labs.

## Known limitations

Client behavior is pinned to the cited publisher commit. The publisher does not document a universal ready-within-N-seconds guarantee; no NetClaw boot-time estimate is retained.

## Tools

Assumes the authenticated client described in [the bindings](endpoints.md).

| Operation | Description | Category |
|---|---|---|
| Resolve/inspect/export | Read server lab identity, state, details or YAML | Read |
| Create/import/start/stop | Manage selected lab lifecycle | Change |
| Wipe/delete | Clear runtime state or remove lab | Destructive |

## Verification checklist

- The exact server lab ID is retained.
- Native state and convergence result are reported separately.
- Delete follows successful stop and wipe.
- Missing-ID, stale-object, and wait failures are not hidden.

## Sources

- [Cisco CML ClientLibrary documentation and implementation](https://github.com/CiscoDevNet/virl2-client/blob/7ac2c924ccbdc02264578a95327f8a1363172076/virl2_client/virl2_client.py). Retrieved 2026-10-09.
- [Cisco CML Lab documentation and implementation](https://github.com/CiscoDevNet/virl2-client/blob/7ac2c924ccbdc02264578a95327f8a1363172076/virl2_client/models/lab.py). Retrieved 2026-10-09.
