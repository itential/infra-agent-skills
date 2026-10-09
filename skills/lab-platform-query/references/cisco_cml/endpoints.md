# Cisco CML controller inspection: bindings

Cisco SDK bindings on authenticated `client`:

- `client.get_system_health()` → dictionary.
- `client.get_system_stats()` → dictionary.
- `client.licensing.status()` → dictionary.
- `client.definitions.node_definitions()` → list of definition dictionaries.

No field names or resource limits absent from the returned version's schema are assumed. Transport/HTTP failures remain the client’s exception/response; no fixed automatic retry budget is documented here.

## Sources

- [Cisco controller SDK](https://github.com/CiscoDevNet/virl2-client/blob/7ac2c924ccbdc02264578a95327f8a1363172076/virl2_client/virl2_client.py). Retrieved 2026-10-09.
- [Cisco licensing SDK](https://github.com/CiscoDevNet/virl2-client/blob/7ac2c924ccbdc02264578a95327f8a1363172076/virl2_client/models/licensing.py). Retrieved 2026-10-09.
- [Cisco definition SDK](https://github.com/CiscoDevNet/virl2-client/blob/7ac2c924ccbdc02264578a95327f8a1363172076/virl2_client/models/node_image_definition.py). Retrieved 2026-10-09.
