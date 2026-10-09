# GNS3 project lifecycle

Manage project containers through the documented GNS3 v2 controller API.

## Common Sequences

- Create a usable project: **Resolve or create** → **Open or close** → **Inspect**.
- Copy a project: **Inspect** → **Copy or archive** → **Inspect** the returned project.
- Remove a project: **Inspect** → **Delete**.

### Resolve or create

The project catalogue returns IDs and names. Creation uses the requested name and returns HTTP 201 with a project ID. Repository gate for server creation: stop and confirm with the operator before proceeding. A conflict (409) means a project already exists; the existing project must be resolved rather than blindly recreated.

### Inspect

Project retrieval returns HTTP 200 with project data, including its `opened` or `closed` state. A missing project (404) ends this branch with a not-found result.

### Open or close

Before opening a project with automatic node start enabled, or closing an active project: stop and confirm with the operator before proceeding. Opening returns 201; closing returns 204. The subsequent inspection reports the resulting project state. A 404 means the project no longer resolves. The close documentation lists an output schema despite its 204 response; no response body is required for success.

### Copy or archive

Duplication takes the existing project and a destination name; before creating the copy, stop and confirm with the operator before proceeding. HTTP 201 returns the copied project. A 403 means duplication is restricted to the local server; a 404 means the source is absent.

Export returns the portable archive with HTTP 200; a 404 means the project is absent. Import replaces/creates the selected destination from an archive: stop and confirm with the operator before proceeding. HTTP 200 returns the imported project; a 403 means import is forbidden. The published endpoint page does not define upload content type or collision semantics; import is blocked until the installed server's archive-upload contract is verified.

### Delete

Deletion removes the project from disk: stop and confirm with the operator before proceeding. HTTP 204 confirms deletion. A 404 means the target is already absent and must be reported as such, not as a new deletion.

## Patterns

Opening can start nodes when the project’s automatic-start property is enabled. Duplication has a documented local-server restriction. Names are presentation values; the controller’s IDs select objects.

## Known limitations

Import payload transport is explicitly unverified in the cited page. No image redistribution rights, complete snapshot semantics, or GNS3 v3 compatibility are implied.

## Tools

Assumes the authenticated client described in [the bindings](endpoints.md).

| Operation | Description | Category |
|---|---|---|
| Resolve/inspect | Retrieve project catalogue or details | Read |
| Create/open/close/copy | Manage a project container | Change |
| Export/import | Transfer a portable archive | Read/change |
| Delete | Remove the project from disk | Destructive |

## Verification checklist

- Creation/copy returns the destination project ID.
- The returned project state is reported without claiming guest readiness.
- Delete is distinguished from already absent.
- Archive import is not attempted without verified upload semantics.

## Sources

- [GNS3 v2 Project reference](https://api.gns3.net/en/latest/api/v2/controller/project.html). Retrieved 2026-10-09.
- [projects](https://api.gns3.net/en/latest/api/v2/controller/project/projects.html). Retrieved 2026-10-09.
- [projectsprojectid](https://api.gns3.net/en/latest/api/v2/controller/project/projectsprojectid.html). Retrieved 2026-10-09.
- [projectsprojectidopen](https://api.gns3.net/en/latest/api/v2/controller/project/projectsprojectidopen.html). Retrieved 2026-10-09.
- [projectsprojectidclose](https://api.gns3.net/en/latest/api/v2/controller/project/projectsprojectidclose.html). Retrieved 2026-10-09.
- [projectsprojectidduplicate](https://api.gns3.net/en/latest/api/v2/controller/project/projectsprojectidduplicate.html). Retrieved 2026-10-09.
- [projectsprojectidexport](https://api.gns3.net/en/latest/api/v2/controller/project/projectsprojectidexport.html). Retrieved 2026-10-09.
- [projectsprojectidimport](https://api.gns3.net/en/latest/api/v2/controller/project/projectsprojectidimport.html). Retrieved 2026-10-09.
