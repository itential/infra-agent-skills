# NAPALM normalized device reads

Collect supported normalized facts using the selected NAPALM driver.

## Common Sequences

- Device collection: **Resolve driver** → **Open session** → **Collect selected getters** → **Close session**.

### Resolve driver

The requested OS maps to a driver in the publisher's support matrix. Getter support is checked independently for that driver; transport support is not proof that every getter exists. The device identity and requested getter list are explicit. Unsupported drivers or methods remain unsupported rather than returning an invented empty structure.

### Open session

The driver receives the target and externally supplied credentials. Connection success establishes a session, not network health. Driver-specific transport/authentication failures stop this device's collection. TLS/SSH trust and required device features follow the selected driver's documented options; no universal secure default is asserted.

### Collect selected getters

The requested read methods return their documented structures. Facts include identity/version/interface names; interface reads distinguish administrative and operational state; counters, addresses, neighbors, environment and route state retain their native schemas and units. A method-not-implemented error is a coverage gap. A failed read is not an empty successful observation. Configuration retrieval and BGP configuration are outside this subset because they can expose secrets.

### Close session

The driver closes its connection after collection, including the failure path. Output associates each requested getter with returned data or its failure. Close failure is reported separately from already collected data.

## Patterns

A common getter name does not guarantee equal implementation coverage. The support matrix and returned field semantics remain driver-specific.

## Known limitations

No configuration load, commit, rollback, arbitrary CLI, connectivity probe or NetClaw ownership/policy wrapper is included. Native getter structures do not provide the wrapper’s available/gap_reason envelope.

## Tools

Assumes the authenticated client described in [the bindings](endpoints.md).

| Operation | Description | Category |
|---|---|---|
| Open/close driver | Establish and release the supported device connection | Transport |
| Read getters | Retrieve selected normalized operational data | Device read |

## Verification checklist

- Driver and each requested getter are supported.
- Device identity and getter names accompany results.
- Unsupported/failed reads remain visible.
- Session cleanup is accounted for.

## Sources

- [NAPALM driver reference](https://napalm.readthedocs.io/en/latest/base.html). Retrieved 2026-10-09.
- [NAPALM support matrix](https://napalm.readthedocs.io/en/latest/support/index.html). Retrieved 2026-10-09.
- [NAPALM connection lifecycle example](https://napalm.readthedocs.io/en/latest/tutorials/changing_the_config.html). Retrieved 2026-10-09.
