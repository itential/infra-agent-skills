# GNS3 node lifecycle: bindings

Authenticated GNS3 controller client; paths are relative to the configured controller. This binding covers API v2, not API v3. JSON payloads unless stated otherwise.

| Operation | Binding | Inputs / result |
|---|---|---|
| Discover | `GET /v2/templates`; `GET /v2/computes` | Available templates/computes |
| Create from template | `POST /v2/projects/{project_id}/templates/{template_id}` | Required integer `x`, `y`; optional `name`, `compute_id`; 201 / 404 |
| List/inspect | `GET /v2/projects/{project_id}/nodes`; `GET /v2/projects/{project_id}/nodes/{node_id}` | `node_id`, `status`, `ports`, `console`, `console_host`, `console_type`; detail 200 / 400 / 404 |
| Runtime action | `POST /v2/projects/{project_id}/nodes/{node_id}/{action}` | `action` is `start`, `stop`, `suspend`, `reload`; 200 / 400 / 404 |
| All-node action | `POST /v2/projects/{project_id}/nodes/{action}` | Same actions; 204 / 400 / 404 |
| Delete | `DELETE /v2/projects/{project_id}/nodes/{node_id}` | 204 / 400 / 404 / 409 |

Console wildcard values are `0.0.0.0` and `::`; they are listen addresses, not remote destinations.


## Sources

- [GNS3 v2 node reference](https://api.gns3.net/en/latest/api/v2/controller/node.html). Retrieved 2026-10-09.
- [Template instantiation](https://api.gns3.net/en/latest/api/v2/controller/template/projectsprojectidtemplatestemplateid.html). Retrieved 2026-10-09.
- [Template catalogue](https://api.gns3.net/en/latest/api/v2/controller/template/templates.html). Retrieved 2026-10-09.
- [Compute catalogue](https://api.gns3.net/en/latest/api/v2/controller/compute/computes.html). Retrieved 2026-10-09.
