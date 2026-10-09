# Google Compute Engine instance lifecycle

Compute Engine MCP applies one requested VM lifecycle operation and verifies its zone-operation result.

Sources: [Compute MCP tool reference](https://docs.cloud.google.com/compute/docs/reference/mcp) and its linked create, delete, start, stop, reset, machine-type and zone-operation schemas, retrieved 2026-10-09. Bindings and source links are in [endpoints.md](endpoints.md).

## Common Sequences

- Create: Identify scope and inputs → Create instance → Track operation → Read instance state.
- Existing instance change: Identify scope and inputs → Read instance state → Change running state or Resize instance → Track operation → Read instance state.
- Delete: Identify scope and inputs → Read instance state → Delete instance → Track operation.

## Identify scope and inputs

The request identifies project, zone and instance name. The current tool schema determines accepted inputs; unknown arguments are not inferred from the broader Compute API. Creation defaults, when used, are explicitly part of the proposed operation. A missing identifier or unsupported option leaves the change unresolved.

## Read instance state

The basic-info read returns identity, status and machine type for the selected VM. Success matches the requested identity and supplies the relevant current state. An absent or failed read is not permission to recreate an existing-name resource. Resize requires an instance already stopped; a preceding stop is a separate gated change.

## Create instance

Before creation, **stop and confirm with the operator before proceeding** with project, zone, name, machine type, image and any accelerator/maintenance settings. The operation returns an operation name; this is acceptance, not a created-and-ready claim. Track operation determines success. The current defaults are the publisher's e2-medium machine type and Debian 12 image family from its Debian image project, unless supplied explicitly.

## Change running state

Before start, stop or reset, **stop and confirm with the operator before proceeding** with the exact VM and requested action. The selected operation returns a zone-operation name; Track operation determines completion. A response error remains a failed request. These methods are marked non-idempotent by the publisher; an ambiguous response requires state/operation inspection before any replay.

## Resize instance

The stopped VM's requested machine type is recorded. Before applying it, **stop and confirm with the operator before proceeding**. The returned operation name is tracked until the documented completion criterion; the subsequent basic-info read confirms the selected machine type. This procedure does not automatically stop or restart the VM around a resize.

## Delete instance

Before deletion, **stop and confirm with the operator before proceeding**, including the intended instance and the platform-specific disk-retention consequences. The narrow MCP schema does not expose retention overrides; their behavior must be resolved from the deployment's Compute guidance before deletion. A returned operation name is not deletion success. Track operation determines completion; no automatic recreation or rollback is promised.

## Track operation

The zone-operation read uses the returned operation name in the same project and zone. Only DONE with no error establishes operation success. Other states remain incomplete; DONE with error remains failed. Error code, location, message, quota details, HTTP error and warnings are retained when returned. Quota or validation failures require resolving the reported condition; no undocumented retry interval or capacity increase is imposed.

## Patterns

Every mutation returns the same kind of operation identifier, while the required inputs differ. Tool-description prose and JSON fields use different spellings in places; the JSON input schema is authoritative.

## Known limitations

Deleting or resetting a VM can have irreversible consequences. This narrow tool reference does not describe a complete rollback or disk-retention policy; unresolved consequences stop the affected change. The completed control-plane operation does not establish guest application health. A stable complete error-code catalogue is not supplied here.

## Tools

| Operation | Purpose | Category |
|---|---|---|
| Read instance / Track operation | Retrieve state and asynchronous outcome | Read |
| Create / Start / Stop / Reset / Resize / Delete | Apply the selected VM lifecycle change | Write |

## Verification checklist

- Project, zone, instance and requested change are explicit.
- Mutation gate and documented preconditions are satisfied.
- Returned operation reaches DONE without error before success is reported.
- Native warnings/errors and relevant read-back state are retained.
