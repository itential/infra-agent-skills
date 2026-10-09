# GNS3 link lifecycle: bindings

Authenticated GNS3 controller client; paths are relative to the configured controller. This binding covers API v2, not API v3. JSON payloads unless stated otherwise.

| Operation | Binding | Input / result |
|---|---|---|
| Node ports | `GET /v2/projects/{project_id}/nodes/{node_id}` | `ports` includes adapter and port numbers |
| Link list/detail | `GET /v2/projects/{project_id}/links`; `GET /v2/projects/{project_id}/links/{link_id}` | Link data; detail 200 / 400 / 404 |
| Create | `POST /v2/projects/{project_id}/links` | `nodes`: two objects each with `node_id`, `adapter_number`, `port_number`; 201 / 400 |
| Suspend/resume | `PUT /v2/projects/{project_id}/links/{link_id}` | `suspend`: boolean; 201 / 400 |
| Delete | `DELETE /v2/projects/{project_id}/links/{link_id}` | 204 / 400 |


## Sources

- [GNS3 v2 link reference](https://api.gns3.net/en/latest/api/v2/controller/link.html). Retrieved 2026-10-09.
- [Link creation](https://api.gns3.net/en/latest/api/v2/controller/link/projectsprojectidlinks.html). Retrieved 2026-10-09.
- [Link inspection/update/deletion](https://api.gns3.net/en/latest/api/v2/controller/link/projectsprojectidlinkslinkid.html). Retrieved 2026-10-09.
- [Node port schema](https://api.gns3.net/en/latest/api/v2/controller/node/projectsprojectidnodesnodeid.html). Retrieved 2026-10-09.
