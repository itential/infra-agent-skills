# GNS3 project snapshots: bindings

Authenticated GNS3 controller client; paths are relative to the configured controller. This binding covers API v2, not API v3. JSON payloads unless stated otherwise.

| Operation | Binding | Input / result |
|---|---|---|
| List/create | `GET /v2/projects/{project_id}/snapshots`; `POST /v2/projects/{project_id}/snapshots` | Create body `name`; create 201 / 404; list 200 / 404 |
| Restore | `POST /v2/projects/{project_id}/snapshots/{snapshot_id}/restore` | 201 project object / 404 |
| Delete | `DELETE /v2/projects/{project_id}/snapshots/{snapshot_id}` | 204 / 404 |

Created object fields: `snapshot_id`, `project_id`, `name`, `created_at` (UTC timestamp). A published output label calls `name` the project name, while the input names the snapshot; the returned field is preserved without inventing a second field.


## Sources

- [GNS3 v2 snapshot reference](https://api.gns3.net/en/latest/api/v2/controller/snapshot.html). Retrieved 2026-10-09.
- [projectsprojectidsnapshots](https://api.gns3.net/en/latest/api/v2/controller/snapshot/projectsprojectidsnapshots.html). Retrieved 2026-10-09.
- [projectsprojectidsnapshotssnapshotid](https://api.gns3.net/en/latest/api/v2/controller/snapshot/projectsprojectidsnapshotssnapshotid.html). Retrieved 2026-10-09.
- [projectsprojectidsnapshotssnapshotidrestore](https://api.gns3.net/en/latest/api/v2/controller/snapshot/projectsprojectidsnapshotssnapshotidrestore.html). Retrieved 2026-10-09.
