# Endpoints — VMware vSphere VM lifecycle (Automation REST API)

Literal wiring layer for `procedure.md`.

Source: the VMware vSphere Automation OpenAPI definition as trimmed in the `itential/assets` repository
(`VMware/vSphere/OpenAPIs/vmware_vsphere_automation-latest.json`), reviewed 2026-10-19. This is a
**secondary source**: the vendor's own portal pages (developer.broadcom.com, vSphere Automation API,
vCenter VM) could not be read on that date. Every route and error below is therefore unverified against
the primary documentation. That copy lists one server form, `https://{host}/api`, and one session-token
(API-key style) scheme.

Paths are relative to `/api`. `{vm}` is the VM identifier.

## Reads

```
GET /vcenter/vm                        list (at most 4000 visible VMs, filterable)
GET /vcenter/vm/{vm}                   one VM
GET /vcenter/vm/{vm}/power             power state (POWERED_OFF | POWERED_ON | SUSPENDED), clean power-off flag
GET /vcenter/vm/{vm}/guest/power       guest state (RUNNING | SHUTTING_DOWN | RESETTING | STANDBY | NOT_RUNNING | UNAVAILABLE), operations_ready
GET /vcenter/vm/{vm}/hardware/cpu      count, cores_per_socket, hot_add_enabled, hot_remove_enabled
GET /vcenter/vm/{vm}/hardware/memory   size_MiB, hot_add_enabled, hot_add_increment_size_MiB, hot_add_limit_MiB
```

## create_vm

```
POST /vcenter/vm
```
Body: a create spec whose only required field in the definition is the guest OS type. A placement spec
(folder, resource pool, host or cluster, datastore) is documented as needed by the create-page read and
the permission text. Other fields were not reviewed.

## Power

```
POST /vcenter/vm/{vm}/power?action=start      from powered-off or suspended
POST /vcenter/vm/{vm}/power?action=stop       hard power-off; 400 if already off
POST /vcenter/vm/{vm}/power?action=reset      powered-on VM
POST /vcenter/vm/{vm}/power?action=suspend    powered-on VM
POST /vcenter/vm/{vm}/guest/power?action=shutdown   clean shutdown request, returns at once
POST /vcenter/vm/{vm}/guest/power?action=reboot     clean reboot request, returns at once
POST /vcenter/vm/{vm}/guest/power?action=standby    suspend request to the guest
```
Error classes seen in the definition: already-in-desired-state (400), not-allowed-in-current-state (400),
unauthenticated (401), unauthorized (403). Exact error type names beyond these were not recorded.

## update_cpu / update_memory

```
PATCH /vcenter/vm/{vm}/hardware/cpu       { count, cores_per_socket, hot_add_enabled, hot_remove_enabled }
PATCH /vcenter/vm/{vm}/hardware/memory    { size_MiB, hot_add_enabled }
```
Fields left out stay unchanged. Memory change while running needs hot add on and must fit the reported
increment and limit. Changing a hot-add flag needs the VM powered off. A bad value returns invalid-argument;
a wrong power state returns not-allowed-in-current-state.

## delete_vm

```
DELETE /vcenter/vm/{vm}
```
400 not-allowed-in-current-state if the VM is powered on. Requires the delete-inventory privilege.
