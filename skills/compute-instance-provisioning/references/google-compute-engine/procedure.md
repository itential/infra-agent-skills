# Google Compute Engine — Instance Lifecycle

Create, read, stop, start, suspend, resume, resize (machine type), back up the disks of, and delete a
Compute Engine virtual machine instance. Networks, disks as standalone objects, images as a catalog,
managed instance groups, and IAM are out of scope except where a step below must read or set one on
the instance.

Written against the Compute Engine documentation pages listed in `endpoints.md` (instance life cycle,
stop and start, suspend and resume, create, delete, change machine type, create disk snapshots, API
requests and operations), retrieved 2026-10-19. Where a page was too thin to settle a detail, this file
says so instead of filling the gap.

Assumes an authenticated client for the target project is available. An instance belongs to one zone, so
every call names the project and the zone that hold it.

## Common Sequences

Steps marked (gated) contain an operator confirmation.

- **Create an instance:** *Read an existing instance* (to confirm the name is free) → *Create* (gated) →
  *Wait for the expected state*.
- **Stop or start:** *Read an existing instance* → *Stop* (gated) or *Start* (gated) → *Wait for the expected state*.
- **Suspend or resume:** *Read an existing instance* → *Suspend* (gated) or *Resume* (gated) → *Wait for
  the expected state*.
- **Resize:** *Read an existing instance* → *Stop* (gated) → *Change the machine type* (gated) → *Start*
  (gated) → *Wait for the expected state*.
- **Back up the disks:** *Read an existing instance* → *Snapshot a disk* → *Wait for the expected state*.
- **Decommission:** *Read an existing instance* → *Snapshot a disk* if anything must survive → *Delete*
  (gated) → *Wait for the expected state*.

## Status vocabulary

Every operation ends with exactly one of these. Report it with the evidence (state read, error).

| Status | Meaning |
|---|---|
| FOUND / NOT_FOUND | A read matched or did not match |
| CREATED, STARTED, STOPPED, SUSPENDED, RESUMED, RESIZED, DELETED | The expected state was read back after the call |
| SNAPSHOT_REQUESTED | The snapshot request completed; the snapshot's own readiness is a separate read (see *Snapshot a disk*) |
| REJECTED_INELIGIBLE | The instance cannot take the change in place (Local SSD, group member, and so on); nothing was changed |
| DECLINED | The operator did not confirm |
| TIMED_OUT | The expected state was not reached within the operator's time limit (the documentation gives none) |
| FAILED | The platform returned an error, or the operation finished with an error. Include the message |

## Operations

### Read an existing instance

Binds to: get_instance, list_instances.

Do this before any change to an existing instance. Its status decides what is allowed.

- Instance statuses (from the instance life cycle page): PENDING (only for queued flex-start capacity
  and standalone TPU hosts), PROVISIONING, STAGING, RUNNING, PENDING_STOP (graceful shutdown phase, where
  enabled), STOPPING, TERMINATED, SUSPENDING, SUSPENDED, REPAIRING. In this platform TERMINATED means
  stopped and still present; it is not deletion.
- Allowed moves per the page: from RUNNING to stopping, suspending, or repair; from TERMINATED to start
  or delete; from SUSPENDED to resume or delete.
- Record the machine type, each attached disk with its auto-delete setting, and whether the instance is a
  member of a managed instance group (both limit later steps).
- Success: FOUND with those facts.

### Create

Binds to: insert_instance.

Preconditions: a name, a machine type, a boot disk definition, and at least one network interface
definition are all required by the documented request.

**Stop and confirm with the operator before creating:** the instance bills for compute from the moment it
runs. State project, zone, name, machine type, boot disk source, and network.

- Include a request identifier (a UUID) so a retry of the same request does not create a second instance.
  Reusing one with different parameters is not documented; use a new one for a changed request.
- The call returns an operation, not a finished instance (see *Wait for the expected state*).
- Success: CREATED once status reads RUNNING. A failing operation carries an error field: report FAILED
  with it.
- If the operator declines, report DECLINED and make no call.

### Wait for the expected state

Binds to: get_operation, wait_operation, get_instance.

Every write returns an operation. Poll it (or use the wait call), then confirm with an instance read.

| Operation | Operation ends | Instance state to read |
|---|---|---|
| Create, Start, Resume | DONE without an error | RUNNING (passes through PROVISIONING and STAGING) |
| Stop | DONE without an error | TERMINATED (passes through STOPPING) |
| Suspend | DONE without an error | SUSPENDED (passes through SUSPENDING) |
| Delete | DONE without an error | The instance read returns not found |
| Snapshot | DONE without an error | See *Snapshot a disk* for the snapshot's own state |

- Operation states are PENDING, RUNNING, DONE. The error field on the operation, not the DONE state,
  tells failure.
- The documentation gives no poll interval or timeout. Use backoff, and report TIMED_OUT after the
  operator's limit; if none was set, ask for one.
- REPAIRING means the platform is repairing the instance; report it as evidence and do not act on it.

### Stop

Binds to: stop_instance.

**Stop and confirm with the operator before stopping:** the guest is shut down, its memory contents are
lost (suspend keeps them), and the workload goes down. Shutdown scripts in the guest must finish first, so
the stop can take a while.

- Disks, configuration, internal and external addresses that are reserved, MAC addresses, and metadata are
  kept. Compute charges stop; disks, disk snapshots, and external addresses still bill while stopped.
- Success: STOPPED once status reads TERMINATED.
- If the operator declines, report DECLINED and make no call.

### Start

Binds to: start_instance.

**Stop and confirm with the operator before starting:** compute billing resumes. Valid from TERMINATED.
Success: STARTED once status reads RUNNING. If the operator declines, report DECLINED.

### Suspend

Binds to: suspend_instance.

**Stop and confirm with the operator before suspending:** workloads freeze, and the memory contents are
saved to disk storage, which needs storage quota. Documented limits: memory up to 208 GB, no GPUs or TPUs
attached, no bare metal, no Confidential VMs. A suspended instance reverts to TERMINATED after 60 days.

- The page did not give the exact route; see the assumption in `endpoints.md`.
- Success: SUSPENDED once status reads SUSPENDED. If the operator declines, report DECLINED.

### Resume

Binds to: resume_instance.

**Stop and confirm with the operator before resuming.** Valid from SUSPENDED. Success: RESUMED once status
reads RUNNING. If the operator declines, report DECLINED.

### Change the machine type

Binds to: set_machine_type.

Preconditions: the instance is TERMINATED (stop it first with the gate above).

- Not eligible for this method: instances with Local SSD attached, members of a managed instance group,
  bare metal instances, and moves between certain older machine series (the page names first to third
  generation). Report REJECTED_INELIGIBLE with the reason and change nothing; the page points to other
  procedures that this file does not carry out.
- The caller needs permission to set the machine type and to start and stop the instance.

**Stop and confirm with the operator before changing the type:** state the old and new type and that the
instance will be started again afterward only on a further confirmation.

- Success: RESIZED once a read shows the new machine type; then follow *Start*.
- If the operator declines, report DECLINED and make no call.

### Snapshot a disk

Binds to: create_disk_snapshot, get_snapshot.

Compute Engine snapshots are of disks, not of the whole machine. A snapshot can be taken while the disk is
attached to a running instance. For consistency, the documentation advises pausing the application first
and resuming it only once the snapshot reaches the UPLOADING state.

- A snapshot restores into a new disk, not in place: **there is no documented revert of an instance to a
  snapshot.** Do not offer one.
- Snapshot the boot disk and every data disk that matters; each is a separate call.
- Success: SNAPSHOT_REQUESTED once the operation finishes. The documented status names beyond UPLOADING
  were not read; read the snapshot and report its state as evidence (assumption: a ready state exists
  and must be reached before the snapshot is relied on).

### Delete

Binds to: delete_instance.

Preconditions: the instance exists and the caller has delete permission. An instance in a managed instance
group with autoscaling may be replaced automatically; resize the group or change the autoscaler first.

**Stop and confirm with the operator before deleting.** Deletion cannot be undone. List every attached
disk with its auto-delete setting: disks set to auto-delete are removed with the instance, the others
remain and keep billing.

- Success: DELETED once the operation is DONE without error and a read returns not found.
- If the operator declines, report DECLINED and make no call.

## Patterns

- **Accepted is not done.** Writes return an operation; read the operation and the instance.
- **TERMINATED is not deleted.** A stopped instance still exists and its disks and reserved addresses
  still bill.
- **Idempotent create.** Supply a request identifier on create. The platform tracks it for about an hour
  (treat the figure as approximate), and it must be a valid, non-zero UUID.
- **Resize is a stop-change-start cycle,** so budget downtime and gate it once with the operator.
- **Suspend keeps memory, stop does not.** Choose by whether the workload can restart cold.

## Known limitations

- Covers the instance lifecycle only; networks, standalone disks, images as a catalog, instance templates,
  managed instance groups, and IAM are not covered.
- Machine type changes that fall outside the eligibility above are only named, not carried out.
- The credential model and the choice of API endpoint are not defined here.
- **Deleting an instance cannot be undone.** Disks marked auto-delete go with it.

## Tools

| Operation | Description | Category |
|---|---|---|
| get_instance | Read one instance and its status | Read |
| list_instances | Read instances in a zone | Read |
| get_operation | Read an operation's state and error | Read |
| wait_operation | Block until an operation is done | Read |
| get_snapshot | Read a snapshot | Read |
| insert_instance | Create an instance | Write (gated) |
| stop_instance | Stop an instance | Write (gated) |
| start_instance | Start a stopped instance | Write (gated) |
| suspend_instance | Suspend an instance | Write (gated) |
| resume_instance | Resume a suspended instance | Write (gated) |
| set_machine_type | Change the machine type of a stopped instance | Write (gated) |
| create_disk_snapshot | Snapshot a disk | Write (no effect on the instance) |
| delete_instance | Delete an instance | Write (gated) |

## Verification checklist

- [ ] Project and zone match the instance being acted on
- [ ] An existing instance was read before any change (status, disks and auto-delete, group membership)
- [ ] The operator confirmed before every create, stop, start, suspend, resume, type change, and delete
- [ ] A create carried a request identifier
- [ ] A resize was stopped first, checked for ineligibility (Local SSD, group, bare metal), and ended running
- [ ] Every write was followed by an operation read and an instance read, or ended in TIMED_OUT or FAILED
- [ ] A delete confirmation listed each disk's auto-delete value
