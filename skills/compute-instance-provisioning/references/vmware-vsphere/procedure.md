# VMware vSphere — Virtual Machine Lifecycle

Create, read, power-control, resize (CPU and memory), and delete a virtual machine through the vSphere
Automation REST API on vCenter. Clusters, datastores, networks, content libraries, and permissions are
out of scope except where a step must reference one.

Source status: the Broadcom developer portal pages for the VM operations returned only navigation or an
"API details page unavailable" notice when retrieved on 2026-10-19, apart from a thin read of the create
operation (guest operating system and placement are required). Everything below that is marked
(secondary) comes from the VMware vSphere Automation OpenAPI definition curated in the `itential/assets`
repository (`VMware/vSphere/OpenAPIs/vmware_vsphere_automation-latest.json`), which is a trimmed copy of
the vendor's own API definition, not the vendor's published page. Redo those facts against the portal
once it renders. Do not treat them as verified.

Assumes an authenticated vCenter API session is available. This file does not cover login.

## Common Sequences

Steps marked (gated) contain an operator confirmation.

- **Create a VM:** *Read an existing VM* (name free) → *Create* (gated) → *Power on* (gated) → *Wait for
  the expected state*.
- **Start or stop:** *Read an existing VM* → *Power on* (gated) or *Power off* (gated) or *Shut down the
  guest* (gated) → *Wait for the expected state*.
- **Reset or suspend:** *Read an existing VM* → *Reset* (gated) or *Suspend* (gated) → *Wait for the
  expected state*.
- **Resize:** *Read an existing VM* → *Change CPU or memory* (gated) → (if the platform requires it,
  *Power off* (gated) first and *Power on* (gated) after) → *Wait for the expected state*.
- **Decommission:** *Read an existing VM* → *Power off* (gated) → *Delete* (gated) → *Wait for the
  expected state*.

## Status vocabulary

| Status | Meaning |
|---|---|
| FOUND / NOT_FOUND | A read matched or did not match |
| CREATED, POWERED_ON, POWERED_OFF, SUSPENDED, RESET, RESIZED, DELETED | The expected state was read back |
| GUEST_SHUTDOWN_REQUESTED | The guest was asked to shut down; this call returns at once and gives no completion (see *Shut down the guest*) |
| REJECTED_NOT_ALLOWED | The VM's current power state does not permit the call; nothing changed |
| NOT_COVERED | The operation has no counterpart in the API definition reviewed (snapshot and revert) |
| DECLINED | The operator did not confirm |
| TIMED_OUT | The expected state was not reached within the operator's time limit |
| FAILED | The platform returned an error. Include its code and message |

## Operations

### Read an existing VM

Binds to: get_vm, list_vms, get_vm_power, get_guest_power, get_cpu, get_memory.

- Power states (secondary): POWERED_OFF, POWERED_ON, SUSPENDED. The power read may also report whether the
  last power-off was clean, useful for spotting a crash.
- The guest has its own state (secondary): RUNNING, SHUTTING_DOWN, RESETTING, STANDBY, NOT_RUNNING,
  UNAVAILABLE, plus a flag saying whether the guest is ready for soft power operations.
- Read CPU count, cores per socket, memory size, and the hot-add and hot-remove flags before any resize.
- A list read returns at most 4000 visible VMs; filter rather than listing everything (secondary).
- Success: FOUND with these facts.

### Create

Binds to: create_vm.

The guest operating system type and a placement (folder, resource pool, and host or cluster, plus a
datastore) are required by the documented operation. Check that each referenced object exists first;
creating those objects is out of scope.

**Stop and confirm with the operator before creating:** state name, guest OS, placement, CPU, memory, disk,
and network. The caller needs create-inventory permission on the folder and assign-to-pool permission on
the resource pool (secondary).

- No idempotency token is documented for this call: do not blindly retry after a timeout; read first to see
  whether the VM exists, or you may create a duplicate.
- A new VM starts powered off (assumption: not stated in the pages read); power on is a separate gated step.
- Success: CREATED once the VM can be read. If the operator declines, report DECLINED.

### Power on

Binds to: power_start.

**Stop and confirm with the operator before powering on.** Valid from powered-off or suspended (secondary).
Success: POWERED_ON on a read-back. If already on, the platform answers with an already-in-desired-state
error (secondary); report it as evidence, not as a failure of the VM.

### Power off

Binds to: power_stop.

**Stop and confirm with the operator before powering off.** This is a hard power-off of the virtual
machine, not a clean shutdown: the guest gets no chance to flush. Prefer *Shut down the guest* when the
guest is ready for soft operations. Valid from powered-on or suspended (secondary); an already powered-off
VM returns an already-in-desired-state error (secondary). Success: POWERED_OFF.

### Shut down the guest

Binds to: guest_power_shutdown, get_guest_power.

**Stop and confirm with the operator before shutting down.** Asks the guest operating system to shut down
cleanly. The call returns immediately without waiting (secondary). Read the guest power flag first: if it
says the guest is not ready for soft operations, fall back to *Power off* only with a further confirmation.
Success: after the call, read until the VM power state is POWERED_OFF; until then report
GUEST_SHUTDOWN_REQUESTED. A guest reboot and a guest standby call exist with the same shape (secondary).

### Reset

Binds to: power_reset.

**Stop and confirm with the operator before resetting.** It is a hard reset of a powered-on VM
(secondary). Success: read back POWERED_ON.

### Suspend

Binds to: power_suspend.

**Stop and confirm with the operator before suspending.** Valid from powered-on (secondary). Success:
SUSPENDED.

### Change CPU or memory

Binds to: update_cpu, update_memory.

**Stop and confirm with the operator before changing hardware,** naming old and new values.

- While the VM runs, CPU count may only go up if hot add is enabled, and only go down if hot remove is
  enabled. Memory may change while running only if hot add is enabled, and then within the increment and
  limit reported by the memory read (secondary).
- Enabling or disabling hot add itself requires the VM to be powered off (secondary).
- Otherwise the VM must be powered off. Take it through *Power off* (preferably the clean path) and
  *Power on* with their own confirmations.
- The CPU count must be a multiple of cores per socket, and the allowed range depends on the guest OS and
  hardware version (secondary).
- A refused change returns a not-allowed-in-current-state or invalid-argument error (secondary): report
  REJECTED_NOT_ALLOWED with it.
- Success: RESIZED once a read shows the new values. Disk resize, adding adapters, and NIC changes are
  separate hardware operations not carried out here.

### Snapshot and revert

Not covered. The API definition reviewed (secondary) lists no VM snapshot or revert operation, and the
portal pages could not be read to confirm. Report NOT_COVERED. Do not substitute a clone or a template
deployment, which are different objects.

### Delete

Binds to: delete_vm.

Preconditions: the VM is powered off. Deleting a running VM is rejected with a not-allowed-in-current-state
error (secondary).

**Stop and confirm with the operator before deleting.** Deletion cannot be undone. Disks that were
detached earlier keep their backing files, and a disk-detach call does not delete the file (secondary);
the documentation read does not say which disk files are removed with the VM, so tell the operator that
this is unverified and have them check the datastore afterward.

- Success: DELETED once a read returns not found. If the operator declines, report DECLINED.

### Wait for the expected state

Binds to: get_vm_power, get_guest_power, get_vm.

The documentation read does not say whether the operations above finish before they return, other than
the guest calls (which do not). Read the power state after every write until it matches the target.

| Operation | Success read |
|---|---|
| Power on, Reset | POWERED_ON |
| Power off, Guest shutdown | POWERED_OFF |
| Suspend | SUSPENDED |
| Create | VM readable |
| Delete | VM read returns not found |

No poll interval or timeout is documented. Use backoff, report TIMED_OUT after the operator's limit.

## Patterns

- **Hard versus clean.** Power off and reset act on the virtual machine; only the guest calls ask the
  operating system. The two families are not interchangeable.
- **Powered off first.** Delete needs it, and hardware changes need it unless hot add or hot remove is on.
- **No idempotency token.** Read before retrying a create.
- **Identifiers are platform-assigned.** Look a VM up by filter or name, never assume a name is unique
  (assumption: the platform does not guarantee it).

## Known limitations

- Covers the VM lifecycle only; clusters, datastores, networks, content libraries, clone and template
  deployment, and permissions are not covered.
- No snapshot or revert operation is documented in the sources.
- Much of the detail is secondary-source; see the note at the top.
- The session and credential model are not defined here.
- **Deleting a VM cannot be undone.**

## Tools

| Operation | Description | Category |
|---|---|---|
| get_vm, list_vms | Read VMs | Read |
| get_vm_power, get_guest_power | Read power states | Read |
| get_cpu, get_memory | Read hardware settings | Read |
| create_vm | Create a VM | Write (gated) |
| power_start, power_stop, power_reset, power_suspend | Power control of the VM | Write (gated) |
| guest_power_shutdown | Ask the guest to shut down | Write (gated) |
| update_cpu, update_memory | Change CPU or memory | Write (gated) |
| delete_vm | Delete a VM | Write (gated) |

## Verification checklist

- [ ] The vCenter and the VM identifier match the target
- [ ] The VM and its power state were read before any change
- [ ] The operator confirmed before every create, power change, reset, hardware change, and delete
- [ ] The operator was told which operations are hard (power off, reset) versus clean (guest calls)
- [ ] A resize used hot add or remove only when the flags allowed it; otherwise the VM was powered off first
- [ ] A delete happened only after power-off and told the operator that disk-file handling is unverified
- [ ] Every write was followed by a read that reached the target, or ended in TIMED_OUT or FAILED
- [ ] No snapshot or revert was offered; NOT_COVERED was reported if asked
