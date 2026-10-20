# Endpoints — Google Compute Engine instance lifecycle (REST, v1)

Literal wiring layer for `procedure.md`. Operation names in its Tools table map to the calls below.

Sources, all Google Cloud documentation retrieved 2026-10-19 (the cloud.google.com pages redirect to
docs.cloud.google.com):
- "Compute Engine instance life cycle" (docs.cloud.google.com/compute/docs/instances/instance-life-cycle)
- "Stop and start a VM" (docs.cloud.google.com/compute/docs/instances/stop-start-instance)
- "Suspend and resume a VM" (docs.cloud.google.com/compute/docs/instances/suspend-resume-instance)
- "Create and start a VM" (docs.cloud.google.com/compute/docs/instances/create-start-instance)
- "Delete a VM" (docs.cloud.google.com/compute/docs/instances/deleting-instance)
- "Change the machine type of a stopped VM" (docs.cloud.google.com/compute/docs/instances/changing-machine-type-of-stopped-instance)
- "Create disk snapshots" (docs.cloud.google.com/compute/docs/disks/create-snapshots)
- "API requests and responses" (docs.cloud.google.com/compute/docs/api/how-tos/api-requests-responses)

Base: `https://www.googleapis.com/compute/v1`. Placeholders are in braces. Authentication and token
handling are assumed to be supplied by the client (assumption: OAuth bearer credentials; the pages read
did not cover it).

## Writes return an operation

Create, stop, start, delete, and the other writes return an operation object, not the finished result.
Its states are PENDING, RUNNING, DONE; a failure appears in its error field. Poll it with the operation
read, or the wait call (assumption on the routes: `GET .../zones/{zone}/operations/{operation}` and
`POST .../zones/{zone}/operations/{operation}/wait`; the page named the calls but not the routes).

`requestId` is an optional query parameter on write calls. Same id again means one execution. It must be
a valid UUID that is not all zeros, and the platform remembers it for roughly 60 minutes.

## get_instance / list_instances

```
GET /projects/{project}/zones/{zone}/instances/{instance}   (assumption: mirrors the delete route)
GET /projects/{project}/zones/{zone}/instances              (assumption)
```
Returns `status`, machine type, attached disks (with `autoDelete`), and so on. Status values are in
`procedure.md`.

## insert_instance

```
POST /projects/{project}/zones/{zone}/instances?requestId={uuid}
```
Required body fields: `name`, `machineType`, `disks` (including the boot disk), `networkInterfaces`.
The exact value formats for machine type and disk sources were not read; take them from the reference
for the create method.

## stop_instance / start_instance

```
POST /projects/{project}/zones/{zone}/instances/{instance}/stop
POST /projects/{project}/zones/{zone}/instances/{instance}/start
```
Stopped instances read TERMINATED; started ones read RUNNING.

## suspend_instance / resume_instance

```
POST /projects/{project}/zones/{zone}/instances/{instance}/suspend   (assumption: pattern of stop/start)
POST /projects/{project}/zones/{zone}/instances/{instance}/resume    (assumption)
```
The suspend page did not state the routes. Verify against the API reference before use.

## set_machine_type

```
POST /projects/{project}/zones/{zone}/instances/{instance}/setMachineType   (assumption: route inferred from the method name)
```
Body names the new machine type. The instance must be stopped first. The caller needs the permissions to
set the machine type and to start and stop the instance.

## create_disk_snapshot / get_snapshot

```
POST /projects/{project}/global/snapshots   (assumption: the page said "the snapshots collection of the project")
GET  /projects/{project}/global/snapshots/{snapshot}   (assumption)
```
The body names the source disk and an optional name. Needs permission to create snapshots on the project
and on the disk. Snapshot status names beyond UPLOADING were not read.

## delete_instance

```
DELETE /projects/{project}/zones/{zone}/instances/{instance}?requestId={uuid}
```
Disks marked `autoDelete: true` are removed with the instance; the rest stay.
