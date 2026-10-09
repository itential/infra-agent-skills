# Google Cloud compute inventory query

Google Cloud's Resource Manager and Compute Engine MCP services return selected project and compute records.

Sources: [Compute MCP reference](https://docs.cloud.google.com/compute/docs/reference/mcp), [instance list](https://docs.cloud.google.com/compute/docs/reference/mcp/tools_list/list_instances), [instance detail](https://docs.cloud.google.com/compute/docs/reference/mcp/tools_list/get_instance_basic_info), and [project search](https://docs.cloud.google.com/resource-manager/reference/mcp/search_projects), retrieved 2026-10-09. Bindings are in [endpoints.md](endpoints.md).

## Common Sequences

- VM inventory: Discover projects → Inspect tool contract → List resources → Read selected resource → Read attached disks.
- Group/template inspection: Discover projects → Inspect tool contract → List resources → Read selected resource → Read group members or template properties.
- Capacity records: Discover projects → Inspect tool contract → List reservations or commitments → Read selected resource → Read commitment reservations.

## Discover projects

Project search returns projects visible to the authenticated caller, with continuation when needed. An empty query can discover all visible projects. Multiple search fields match any field, not all fields. Success identifies the requested project ID; permissions can limit the visible set. Pagination continues using the returned token before claiming completeness.

## Inspect tool contract

The current tool schema determines required project, zone or region and any resource name. Zonal inventory is not automatically project-wide. Commitments are regional; templates, snapshots and images use their documented project scope. Missing or unauthorized scopes remain explicit instead of being substituted with defaults.

## List resources

The selected collection read returns native records and the operation's paging metadata. Instance listing requires both project and zone and returns basic information. Success preserves record identities and native statuses. A returned continuation token is supplied on the next same-scope read; an absent token establishes the last page for that operation. Other collections follow their own discovered contracts. Query/permission errors remain distinct from empty data.

## Read selected resource

Detail reads return the selected instance, disk, managed group, reservation, commitment or template. Success requires the expected name/ID and documented fields. The basic instance schema contains identity, status, machine type, creation time and accelerators; it does not contain the IP/network-interface details claimed by the source skill. Disk performance configuration describes provisioned settings, not observed throughput.

## Read attached disks / Read group members or template properties / Read commitment reservations

The matching relationship query returns the disks attached to one instance, managed instances of one group, template properties, or reservations linked to one commitment. Success retains the parent identifier and returned resource identities. Template service accounts, metadata and disk details can include sensitive configuration; output is limited to requested evidence. A relationship-read error is not proof of no attached resources.

## Patterns

The publisher's prose sometimes uses snake_case while its JSON schema uses camelCase; the JSON schema determines actual request members. A machine/accelerator catalogue describes offerings, not a guarantee that requested capacity can be allocated. Reservation and commitment records do not themselves establish realized utilization or savings.

## Known limitations

No stable exhaustive tool error list is published by the overview. Native authentication, permission, validation and service errors remain visible and require their operation-specific guidance. Current schemas govern optional filters and paging; no source-wrapper filter is assumed. Mutating Compute operations are outside this read capability.

## Tools

| Operation | Purpose | Category |
|---|---|---|
| Discover projects | Identify visible project IDs | Read |
| Inspect tool contract | Identify required scope and response | Read |
| List/read resources | Retrieve compute, storage and capacity records | Read |
| Read resource relationships | Retrieve attached disks, group members and linked reservations | Read |

## Verification checklist

- Project and zone/region scope match the requested resource family.
- Native identities, states and continuation metadata are preserved.
- Basic instance fields are not expanded with invented network details.
- Provisioned settings are not reported as measured usage or assured capacity.
