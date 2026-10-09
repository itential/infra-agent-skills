# GNS3 link lifecycle

Connect, suspend, resume or delete explicitly selected GNS3 v2 links.

## Common Sequences

- Connect: **Inspect endpoints** → **Create link** → **Inspect link**.
- Isolate/restore: **Inspect link** → **Change suspension** → **Inspect link**.
- Disconnect: **Inspect link** → **Delete link**.

### Inspect endpoints

The project’s nodes expose port entries. The two chosen endpoint tuples come from these returned ports, not from guessed interface-name arithmetic. Node lookup 400 is malformed input; 404 is an absent endpoint.

### Create link

Before connecting the endpoints: stop and confirm with the operator before proceeding. Creation returns HTTP 201 and link data. A 400 indicates invalid input; the endpoint identities and available ports must be corrected before another attempt.

### Inspect link

Link list/detail operations return link IDs, connected node/adapter/port tuples and suspension state. Detail retrieval returns 200; 400 indicates invalid input and 404 an absent link.

### Change suspension

Suspending or resuming a link changes traffic delivery: stop and confirm with the operator before proceeding. The documented update returns 201 and the updated link. A 400 means invalid input. Isolating a node requires explicit selection of each affected link; the procedure does not promise transactional all-link changes.

### Delete link

Before removing connectivity: stop and confirm with the operator before proceeding. HTTP 204 confirms deletion. A 400 indicates invalid input. If a connection is lost during mutation, the current link inventory is needed to distinguish an applied change from an unknown result.

## Patterns

Suspension is a link attribute, separate from node runtime suspension. Port tuple identity is retained in the verification evidence.

## Known limitations

No port-name heuristic, automatic node-name matching or fault-injection filter recipe is assumed. Multi-link mutations can be partial.

## Tools

Assumes the authenticated client described in [the bindings](endpoints.md).

| Operation | Description | Category |
|---|---|---|
| Inspect | Retrieve actual node ports and links | Read |
| Create/update | Connect endpoints or set link suspension | Change |
| Delete | Remove selected link | Destructive |

## Verification checklist

- Both endpoint tuples match returned ports.
- Returned link ID and suspension value are recorded.
- Partial multi-link outcomes remain visible.

## Sources

- [GNS3 v2 link reference](https://api.gns3.net/en/latest/api/v2/controller/link.html). Retrieved 2026-10-09.
- [Link creation](https://api.gns3.net/en/latest/api/v2/controller/link/projectsprojectidlinks.html). Retrieved 2026-10-09.
- [Link inspection/update/deletion](https://api.gns3.net/en/latest/api/v2/controller/link/projectsprojectidlinkslinkid.html). Retrieved 2026-10-09.
- [Node port schema](https://api.gns3.net/en/latest/api/v2/controller/node/projectsprojectidnodesnodeid.html). Retrieved 2026-10-09.
