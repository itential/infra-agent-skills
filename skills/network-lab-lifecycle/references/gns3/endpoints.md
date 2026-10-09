# GNS3 project lifecycle: bindings

Authenticated GNS3 controller client; paths below are relative to the configured controller. Scope is API v2 (published 2.2 documentation), not API v3. JSON bodies except archive transfer. No default credentials are supplied.

| Operation | Binding | Input / result |
|---|---|---|
| List/create | `GET /v2/projects`; `POST /v2/projects` | Create body `name`; optional documented `project_id`, `path`, `auto_open`, `auto_close`, `auto_start`; 201 / 409 |
| Inspect/delete | `GET /v2/projects/{project_id}`; `DELETE /v2/projects/{project_id}` | 200 / 404; delete 204 / 404 |
| Open/close | `POST /v2/projects/{project_id}/open`; `POST /v2/projects/{project_id}/close` | Open 201 / 404; close 204 / 404 |
| Duplicate | `POST /v2/projects/{project_id}/duplicate` | Body `name`; optional `reset_mac_addresses`; 201 / 403 / 404 |
| Export | `GET /v2/projects/{project_id}/export` | 200 archive / 404 |
| Import | `POST /v2/projects/{project_id}/import` | Portable archive; content type and collision behavior unverified; 200 / 403 |


## Sources

- [GNS3 v2 Project reference](https://api.gns3.net/en/latest/api/v2/controller/project.html). Retrieved 2026-10-09.
- [projects](https://api.gns3.net/en/latest/api/v2/controller/project/projects.html). Retrieved 2026-10-09.
- [projectsprojectid](https://api.gns3.net/en/latest/api/v2/controller/project/projectsprojectid.html). Retrieved 2026-10-09.
- [projectsprojectidopen](https://api.gns3.net/en/latest/api/v2/controller/project/projectsprojectidopen.html). Retrieved 2026-10-09.
- [projectsprojectidclose](https://api.gns3.net/en/latest/api/v2/controller/project/projectsprojectidclose.html). Retrieved 2026-10-09.
- [projectsprojectidduplicate](https://api.gns3.net/en/latest/api/v2/controller/project/projectsprojectidduplicate.html). Retrieved 2026-10-09.
- [projectsprojectidexport](https://api.gns3.net/en/latest/api/v2/controller/project/projectsprojectidexport.html). Retrieved 2026-10-09.
- [projectsprojectidimport](https://api.gns3.net/en/latest/api/v2/controller/project/projectsprojectidimport.html). Retrieved 2026-10-09.
