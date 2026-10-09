# Panorama managed-firewall observations

Discover managed firewalls and retrieve a selected firewall's system information through Panorama.

Sources: Palo Alto Networks current API Usage Guide [query a managed firewall](https://docs.paloaltonetworks.com/ngfw/api/pan-os-xml-api-use-cases/query-a-firewall-from-panorama-api), [request structure](https://docs.paloaltonetworks.com/ngfw/api/getting-started/structure-of-a-pan-os-xml-api-request), [error codes](https://docs.paloaltonetworks.com/ngfw/api/getting-started/pan-os-xml-api-error-codes), retrieved 2026-10-09. The authenticated XML API bindings are in [endpoints.md](endpoints.md).

1. **Read managed devices.** The operational query returns either all managed firewalls or only connected firewalls. Success is a successful XML response containing device records and their serial identifiers. A missing/disconnected device is not silently replaced with another target.
2. **Select returned serial identifiers.** The publisher's workflow carries the serial value from each requested device into the subsequent query. The serial selects the firewall behind Panorama; an address or display name is not substituted for it.
3. **Read selected firewall system information.** The system-information query includes the chosen target serial. Success is a successful response containing that firewall's system information, including reported identity, serial, model and software data. The same read is repeated for each explicitly selected serial, preserving individual failures.

For each read: missing/illegal parameters or unknown/invalid commands require correction; malformed XML requires rebuilding valid XML; invalid or incomplete object selectors require correcting scope. Missing and nonunique objects remain explicit failures. Authentication/role denial requires valid access, and an operation denied on the current device state is not bypassed. Internal errors are escalated to vendor support; a timed-out session remains failed and needs valid session access. A reference-count deletion error or another mutation-specific error on this read-only sequence indicates the wrong operation binding and stops the sequence. Exact codes are in the endpoint error table.

## Patterns

- The management connection terminates on Panorama while the target serial selects the managed firewall.
- HTTP completion alone is insufficient; XML response status determines operation success.

## Known limitations

- Device groups, templates, security/NAT policy searches, commits, policy-hit evidence and traffic reachability are outside this subset.
- The publisher's illustrative managed-device XML has malformed entry markup and inconsistent example serial values. Those examples are not copied; the live response's serial element supplies the target.
- No automatic retry count is specified by these sources.

## Tools

| Operation | Description | Category |
|---|---|---|
| Read managed devices | Retrieve all or connected managed-firewall records | Read |
| Read targeted system information | Query a selected firewall through Panorama | Read |

## Verification checklist

- All-versus-connected discovery matches the requested coverage.
- Targets come from returned serial identifiers.
- Each system read returned successful XML and the intended firewall identity.
- Individual errors remain visible and no policy reachability verdict is inferred.
