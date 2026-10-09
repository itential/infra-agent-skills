# Cisco CML link lifecycle

Connect or disconnect explicitly identified interfaces in a CML lab.

## Common Sequences

- Connect: **Inspect** → **Create interfaces** if needed → **Create link** → **Inspect**.
- Disconnect: **Inspect** → **Remove link** → **Inspect**.

### Inspect

The lab returns nodes, interfaces and links. Resolution uses actual interface IDs from the selected lab. An absent node/interface/link is a selection failure; creation is not inferred as the remedy.

### Create interfaces

The publisher can allocate an interface in the next free slot or populate available slots through a specified slot. Before changing the topology: stop and confirm with the operator before proceeding. The returned interface object supplies its ID and slot. If no requested interface is returned, the client raises an interface-not-found error.

### Create link

The publisher creates a link between two resolved interfaces. Before attaching the link: stop and confirm with the operator before proceeding. The returned link has an ID and the two selected interface objects. Optional convergence waiting may raise a runtime error; that is not successful completion.

### Remove link

Before disconnecting the selected interfaces: stop and confirm with the operator before proceeding. Successful removal removes the link object from the lab. HTTP or transport errors remain failed changes; the current topology must be re-read before deciding what happened.

## Patterns

Explicit interface selection avoids silently choosing a different port. Interface slot creation can allocate several interfaces rather than only one.

## Known limitations

Link conditioning, annotations and image-specific port limits remain outside this procedure. No global rule that every lab must be stopped before every topology edit is asserted.

## Tools

Assumes the authenticated client described in [the bindings](endpoints.md).

| Operation | Description | Category |
|---|---|---|
| Inspect | Retrieve nodes, interfaces, links | Read |
| Create interface/link | Allocate interfaces and connect selected endpoints | Change |
| Remove link | Disconnect selected endpoints | Destructive |

## Verification checklist

- The source and destination interface IDs match the supplied topology.
- Returned link ID is recorded.
- Convergence exceptions and missing objects are preserved.
- A removed link is absent from the refreshed topology.

## Sources

- [Cisco CML Lab documentation and implementation](https://github.com/CiscoDevNet/virl2-client/blob/7ac2c924ccbdc02264578a95327f8a1363172076/virl2_client/models/lab.py). Retrieved 2026-10-09.
