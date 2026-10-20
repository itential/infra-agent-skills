# Endpoints — Morpheus instance lifecycle (REST)

Literal wiring layer for `procedure.md`.

Source: the Morpheus API reference (apidocs.morpheusdata.com), pages "Add an instance"
(/reference/addinstance), "Get an instance" (/reference/getinstance), "Stop an instance"
(/reference/stopinstance), "Start an instance" (/reference/startinstance), "Delete an instance"
(/reference/deleteinstance), "Resize an instance" (/reference/resizeinstance), "Snapshot an instance"
(/reference/snapshotinstance), retrieved 2026-10-19. The pages were read through a summarizing fetch, so
confirm exact field spellings against them before first use. Authentication is a bearer token. The
base URL is the customer's own Morpheus appliance (assumption: paths below are relative to it).

Ids are integers. Success responses carry `success: true`; errors carry a message and may carry a
validation errors object.

```
POST   /api/instances                      create_instance
GET    /api/instances/{id}                 get_instance
GET    /api/instances                      list_instances (assumption: collection read, not fetched)
PUT    /api/instances/{id}/stop            stop_instance
PUT    /api/instances/{id}/start           start_instance
PUT    /api/instances/{id}/resize          resize_instance
PUT    /api/instances/{id}/snapshot        snapshot_instance
DELETE /api/instances/{id}                 delete_instance
```

## create_instance

Body: an `instance` object with `name`, `site` (object with the group `id`), `instanceType` (object with
a `code`), `layout` (object with `id`), and `plan` (object with `id`); a `config` object whose shape
varies by cloud; and optionally `zoneId` (the cloud id), `volumes` (include the root volume), and
`networkInterfaces` (each with a `network.id`). Success returns 200 with the instance.

## stop_instance / start_instance

Query: `server` (boolean; stop defaults to true, start's description says only the service starts unless
it is true). Stop also takes `muteMonitoring` (default false) and `force` (default false, hard power-off).
Success returns 200 with `success: true`.

## resize_instance

Query: `force` (override a snapshot-deletion restriction). Body: `instance` (id and target plan id),
`servicePlanOptions` (CPU cores, cores per socket, memory), `volumes` (grow, size in GB),
`storageControllers`, `deleteOriginalVolumes` (Amazon only), `networkInterfaces`. Returns 200 with the
updated instance.

## snapshot_instance

Body (all optional): `name`, `description`, `memorySnapshot` (VMware and some other types), `forExport`.
Returns success and a list of process ids, one per server.

## delete_instance

Query, all default off except the address release: `preserveVolumes`, `keepBackups`, `removeVolumes`,
`force`, and `releaseFloatingIps` / `releaseEIPs` (default on). Success returns 200 with `success: true`.

## get_instance

Returns the instance with cloud, group, cluster, memory, storage, cores, volumes, interfaces, and status
fields (`status`, `statusDate`, `statusPercent`, `statusEta`). The permitted status values are not given
on the page.
