# Redfish hardware state collection

Collect the state exposed by a Redfish service without invoking management actions.

## Common Sequences

- System observation: **Discover** → **Read system**.
- Component investigation: **Discover** → **Read system** → **Read chassis and sensors** → **Read firmware and logs**.

### Discover

The service root establishes the Redfish service and links to available resource collections. Collection members and continuation links are followed using the returned resource identities; a system ID is not assumed to be a fixed number. Authentication failure means the service did not accept the credentials; authorization failure means access is denied or credentials require change. Neither provides a host-power verdict. A transport/TLS failure leaves service access unresolved.

### Read system

The selected ComputerSystem resource supplies reported power state, local health and health rollup where implemented. Reported On means power is on; it does not establish OS boot or application availability. Off remains the service's reported off state. Transitional and absent/null values retain their native meaning rather than being coerced to On/Off. Resource health and dependent-resource health rollup are recorded separately.

### Read chassis and sensors

The selected system's linked chassis and available thermal, power, sensor and component resources provide reported readings, units, thresholds and status. Returned links determine whether the service uses legacy thermal/power resources or newer subsystem resources. Missing or unavailable resources are coverage gaps. Threshold comparison uses the actual schema's fields and units; there is no universal temperature or power threshold in this procedure.

Health rollup need not equal the worst child health: redundancy and platform architecture can change the rollup. A healthy aggregate therefore does not overwrite a returned component warning or critical state.

### Read firmware and logs

The manager resources expose controller identity and firmware version where supported. The update service's firmware-inventory collection supplies software-inventory records; absence or an empty collection is not proof that no firmware exists. Log-service collections are resolved from the selected system/chassis/manager, then their entry collections are read with pagination. Entries retain timestamp, severity, message and registry identifiers where present. Empty logs establish only that no entries were returned.

Every read uses the common error handling: malformed requests remain invalid; an absent resource remains not found; an unacceptable representation requires a supported representation; service/internal errors leave the affected read incomplete. Extended error messages and resolution information are preserved. No automatic power cycle, log clearing or firmware change is a recovery action.

## Patterns

The resource graph and schema annotations determine interpretation. A chassis, manager and computer system can represent different views of related hardware; their identifiers are not interchangeable.

## Known limitations

Grounded in Redfish specification 1.22.2 and resource guide 2025.1. OEM extensions require the OEM documentation. Log completeness, sensor support and firmware coverage vary by implementation. A BMC observation is not an in-band reachability test.

## Tools

Assumes the authenticated client described in [the bindings](endpoints.md).

| Operation | Description | Category |
|---|---|---|
| Discover | Read service and collection links | Hardware management read |
| Read system/chassis | Collect power, health and sensor state | Hardware management read |
| Read firmware/logs | Retrieve manager, firmware and event records | Hardware management read |

## Verification checklist

- Endpoint and resource identities are resolved.
- All available continuation links were followed or a partial result is declared.
- Power, resource health, rollup and OS availability remain distinct.
- Missing data and native extended errors remain visible.
- No management action was invoked.

## Sources

- [Redfish specification 1.22.2](https://www.dmtf.org/sites/default/files/standards/documents/DSP0266_1.22.2.html). Retrieved 2026-10-09.
- [Redfish resource/schema guide 2025.1](https://redfish.dmtf.org/schemas/DSP2046_2025.1.html). Retrieved 2026-10-09.
