# Cisco NSO device and service queries

Read NSO-maintained device data and discover deployed service instances without changing configuration.

Sources: [publisher MCP server](https://github.com/NSO-developer/cisco-nso-mcp-server/blob/main/cisco_nso_mcp_server/server.py), [device helpers](https://github.com/NSO-developer/cisco-nso-mcp-server/blob/main/cisco_nso_mcp_server/services/devices.py), [service helpers](https://github.com/NSO-developer/cisco-nso-mcp-server/blob/main/cisco_nso_mcp_server/services/services.py), and [NSO 6.5 lifecycle operations](https://nso-docs.cisco.com/guides/nso-6.5/operation-and-usage/operations/lifecycle-operations), retrieved 2026-10-09. MCP bindings are in [endpoints.md](endpoints.md).

## Common Sequences

- Device inspection: Discover groups/drivers → Read device records → Check synchronization.
- Stored-configuration inspection: Check synchronization → Read device configuration.
- Service inventory: Discover service types → Read service instances.

### Discover groups/drivers

The group and driver-list reads return the NSO data for available device groups and NED identifiers. Successful empty data is distinct from an embedded error: these helpers can return an empty list alongside error status. Group membership supplies names for subsequent reads; driver identifiers do not prove a particular device is onboarded.

### Read device records

An explicit NSO device name selects its platform, stored configuration, or state record. Success is the native requested record; platform data contains the platform name/version/model supported by the device driver. The source does not define a universal serial-number or interface-counter schema. Missing names and read failures return error status/messages and are not empty successful records. A configuration response can contain sensitive settings; the outcome preserves only the requested evidence, without copying unrelated credentials into reports.

### Check synchronization

The device check compares NSO's synchronization information with the device using its driver-specific mechanism. The native synchronization result is retained. Device synchronization is not the service-specific consistency check and may not disclose a full configuration difference; no automatic remediation follows a mismatch. Failed checks remain failures, not out-of-sync verdicts inferred from transport errors.

### Discover service types

The service-type read returns the types actually present on this NSO instance. Empty results with error status are failures. Returned model identifiers, including namespace information, supply the type for the next operation; generic service names from examples are not substitutes.

### Read service instances

The selected service type addresses its instance collection. Success is the returned model-specific service data. The publisher requires a service-type parameter and returns an explicit error if missing or if the request fails. The response does not guarantee a universal affected-device list, deployment status, or service health field; only fields actually established by that service model support those conclusions.

## Patterns

- The MCP inputs nest device/service fields inside a parameter object; flattened examples do not match the current implementation.
- Helpers return errors as ordinary objects. A successful tool transport is insufficient without checking the result status.
- Device state, stored configuration and service-instance data each retain their provenance.

## Known limitations

- The MCP surface supplies discovery and reads, not service create/delete/redeploy operations.
- Service-specific health checks and relationship schemas require the applicable package documentation.
- The publisher's connection defaults include unencrypted local HTTP and example administrator credentials. An authenticated deployment with appropriate transport protection is a prerequisite; those defaults are not suitable production credentials.

## Tools

| Operation | Description | Category |
|---|---|---|
| Read device groups | Return NSO group membership | Inventory |
| Read driver identifiers | Return available NED IDs | Inventory |
| Read device platform | Return driver-supported platform information | Read |
| Read device configuration | Return NSO's stored configuration | Read |
| Read device state | Return device state through NSO | Read |
| Check device synchronization | Return native synchronization result | Validation |
| Discover service types | Return installed service type identifiers | Inventory |
| Read service instances | Return instances of a specified type | Read |

## Verification checklist

- Device names and namespaced service types came from the intended NSO instance.
- Embedded error results were not mistaken for successful empty collections.
- Synchronization results remain distinct from service health and full configuration comparisons.
- Model-dependent fields and incomplete coverage remain explicit.
