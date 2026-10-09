# GNS3 node lifecycle

Create nodes from installed templates and control their runtime state through GNS3 v2.

## Common Sequences

- Create: **Discover** → **Create from template** → **Inspect**.
- Operate: **Inspect** → **Change runtime state** → **Inspect**.
- Remove: **Inspect** → **Delete**.

### Discover

The template and compute catalogues identify available resources. The selected project and installed template IDs are inputs to creation; no image or licensed appliance is downloaded by this procedure.

### Create from template

Before allocating a node: stop and confirm with the operator before proceeding. Creation supplies the template, project and requested coordinates; a compute override is available when the template lacks a default compute. HTTP 201 returns the created node. A 404 means project or template resolution failed.

### Inspect

Node details or the project’s node list report identity, ports, console transport and native state (`stopped`, `started`, `suspended`). A malformed lookup (400) must be corrected; an absent node (404) is reported as absent. If the console bind address is a wildcard, the publisher requires the controller connection address instead of the wildcard address.

### Change runtime state

Starting, stopping, suspending or reloading affects node operation: stop and confirm with the operator before proceeding. Single-node actions return HTTP 200; whole-project actions return 204. An invalid action request (400) is corrected without broadening scope; an absent target (404) requires renewed resolution. A successful request is followed by native-state inspection. Emulation process state does not establish guest protocol convergence.

### Delete

Deletion removes the selected node: stop and confirm with the operator before proceeding. HTTP 204 confirms removal; 400 is invalid input, 404 is already absent, and 409 means the node is locked. A locked node is not forcibly unlocked as an implicit recovery.

## Patterns

Template-based creation has its own operation. The read-only template ID returned in node details is not a substitute for the template-create operation.

## Known limitations

GNS3 v2 only. Console metadata retrieval does not authorize arbitrary guest commands. Supported suspension behavior depends on node type; a reported success must not replace state inspection.

## Tools

Assumes the authenticated client described in [the bindings](endpoints.md).

| Operation | Description | Category |
|---|---|---|
| Discover/inspect | Read project, template, compute, node and port identity | Read |
| Create | Instantiate an installed template | Change |
| Runtime action | Start, stop, suspend or reload selected nodes | Change |
| Delete | Remove a selected node | Destructive |

## Verification checklist

- Node ID and selected template/compute are retained.
- Requested single-node versus project-wide scope matches the call.
- Native node state is returned.
- Lock conflicts and absent objects are not silently worked around.

## Sources

- [GNS3 v2 node reference](https://api.gns3.net/en/latest/api/v2/controller/node.html). Retrieved 2026-10-09.
- [Template instantiation](https://api.gns3.net/en/latest/api/v2/controller/template/projectsprojectidtemplatestemplateid.html). Retrieved 2026-10-09.
- [Template catalogue](https://api.gns3.net/en/latest/api/v2/controller/template/templates.html). Retrieved 2026-10-09.
- [Compute catalogue](https://api.gns3.net/en/latest/api/v2/controller/compute/computes.html). Retrieved 2026-10-09.
