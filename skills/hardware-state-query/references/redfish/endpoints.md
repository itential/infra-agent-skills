# Redfish hardware state collection: bindings

An authenticated Redfish HTTP client uses the operator-selected HTTPS service. Resource links are resolved on that service; credentials are not forwarded to arbitrary destinations.

| Operation | Literal binding | Relevant response fields |
|---|---|---|
| Discover service | `GET /redfish/v1/` | `RedfishVersion`, `Systems`, `Chassis`, `Managers`, `UpdateService`, `@odata.id` |
| Read collection/resource | `GET {returned-resource-uri}` | `Members`, `Members@odata.nextLink`, `@odata.type` |
| Read system | `GET {selected-system-uri}` | `PowerState`, `Status.Health`, `Status.HealthRollup`, `ProcessorSummary`, `MemorySummary`, `Links.Chassis` |
| Read chassis | `GET {selected-chassis-uri}` | `Thermal`, `Power`, `ThermalSubsystem`, `PowerSubsystem`, `Sensors` as present |
| Read manager | `GET {selected-manager-uri}` | `FirmwareVersion`, `Status`, `LogServices` |
| Read firmware inventory | `GET {UpdateService.FirmwareInventory.@odata.id}` after reading UpdateService | SoftwareInventory members, `Version`, `Status` |
| Read log entries | `GET {LogService.Entries.@odata.id}` after reading LogService | `Created`, `Severity`, `Message`, `MessageId`, `MessageArgs` as present |

Successful reads normally return 200 and the requested representation. Relevant error statuses: 400 invalid request; 401 missing/invalid authentication; 403 insufficient permission or required credential change; 404 unavailable URI; 405 unsupported method; 406 unsupported representation; 500 internal service failure; 503 temporarily unavailable. Redfish extended errors appear under `error`, including `code`, `message` and `@Message.ExtendedInfo`. Native Health values are `OK`, `Warning`, `Critical`; an omitted/null property is not `OK`.

## Sources

- [Redfish specification 1.22.2](https://www.dmtf.org/sites/default/files/standards/documents/DSP0266_1.22.2.html). Retrieved 2026-10-09.
- [Redfish resource/schema guide 2025.1](https://redfish.dmtf.org/schemas/DSP2046_2025.1.html). Retrieved 2026-10-09.
