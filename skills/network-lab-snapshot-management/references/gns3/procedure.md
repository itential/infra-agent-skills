# GNS3 project snapshots

Manage project snapshots through the documented GNS3 v2 snapshot API.

## Common Sequences

- Create: **List** → **Create** → **List**.
- Restore: **List** → **Restore**.
- Remove: **List** → **Delete** → **List**.

### List

The project snapshot catalogue returns HTTP 200 with snapshot IDs, names and creation times. A 404 means the project is absent. Names alone do not replace the selected snapshot ID.

### Create

Snapshot creation writes persisted project data: stop and confirm with the operator before proceeding. A requested name produces HTTP 201 and a snapshot object with its ID and UTC creation timestamp. A 404 means project resolution failed.

### Restore

Restoration replaces current project state: stop and confirm with the operator before proceeding. HTTP 201 and the returned project object confirm the API’s restore operation. A 404 means the project or snapshot is absent. The cited endpoint does not define automatic stopping or snapshot runtime-memory contents; those details require installed-version guidance before a running project can be restored safely.

### Delete

Deleting a snapshot removes it from disk: stop and confirm with the operator before proceeding. HTTP 204 confirms deletion. A 404 means project or snapshot is already absent; the result remains distinguishable from a new deletion.

## Patterns

The returned snapshot ID is the restore/delete selector. Restoration success does not prove guest protocol convergence or application recovery.

## Known limitations

Snapshot coverage, quiescing requirements, automatic node-stop behavior and cross-version portability are not specified by the endpoint reference. They are explicit unknowns, not inherited promises from NetClaw.

## Tools

Assumes the authenticated client described in [the bindings](endpoints.md).

| Operation | Description | Category |
|---|---|---|
| List | Read snapshot identities and timestamps | Read |
| Create | Persist a snapshot of the selected project | Change |
| Restore/delete | Replace project state or remove snapshot | Destructive |

## Verification checklist

- Snapshot and project IDs match the operator’s selection.
- Creation records the returned ID and timestamp.
- Restore records the returned project and native API result.
- Unknown running-state safety is resolved before restore.

## Sources

- [GNS3 v2 snapshot reference](https://api.gns3.net/en/latest/api/v2/controller/snapshot.html). Retrieved 2026-10-09.
- [projectsprojectidsnapshots](https://api.gns3.net/en/latest/api/v2/controller/snapshot/projectsprojectidsnapshots.html). Retrieved 2026-10-09.
- [projectsprojectidsnapshotssnapshotid](https://api.gns3.net/en/latest/api/v2/controller/snapshot/projectsprojectidsnapshotssnapshotid.html). Retrieved 2026-10-09.
- [projectsprojectidsnapshotssnapshotidrestore](https://api.gns3.net/en/latest/api/v2/controller/snapshot/projectsprojectidsnapshotssnapshotidrestore.html). Retrieved 2026-10-09.
