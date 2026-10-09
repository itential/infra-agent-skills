# EVE-NG topology inventory and network creation

Inspect topology endpoints and create a virtual network in an existing EVE-NG lab.

## Common Sequences

- Inspect: **Read topology** → **Read endpoint mappings**.
- Add a network: **Read network types** → **Create network** → **Read topology**.

### Read topology

The publisher returns the lab topology and network inventory, including network identifiers and types. At each operation, the publisher’s response envelope carries a code, status and message. Unauthorized with code 400 indicates an expired session; 401 requires login. Forbidden/403 means insufficient permission. Other 4xx failures require request correction; 5xx errors are reported as server failures. Neither an HTTP response alone nor a message substring replaces the envelope’s outcome.

### Read endpoint mappings

The endpoint collection describes Ethernet networks and serial endpoints. A selected node’s interfaces identify its actual mapping. These are observations, not permission to infer an undocumented connection-write request. Error handling follows **Read topology**.

### Read network types

The supported network-type catalogue supplies the type for creation. A type absent from the catalogue is not replaced with a guessed alias. Error handling follows **Read topology**.

### Create network

Creation supplies the selected network type and requested name/layout. Before changing the lab: stop and confirm with the operator before proceeding. The guide’s network-created success envelope and subsequent network inventory identify the new object. Error handling follows **Read topology**.

## Patterns

Network inventory, serial endpoints and per-node interfaces are different collections. An empty topology does not imply a missing lab.

## Known limitations

The publisher examples disable TLS certificate verification for Pro and show default credentials. Those are unsafe client examples, not requirements of this procedure; an authenticated client with certificate validation is assumed. The publisher warns that some examples are outdated. The installed version’s returned object schema takes precedence; unknown mutation parameters require platform-specific guidance. The public guide does not provide a complete interface-attachment or network-deletion operation. Those mutations are explicitly unsupported here pending installed-version primary documentation.

## Tools

Assumes the authenticated client described in [the bindings](endpoints.md).

| Operation | Description | Category |
|---|---|---|
| Read topology/types | Retrieve networks, types and topology | Read |
| Read endpoint mappings | Retrieve node interfaces and serial endpoints | Read |
| Create network | Add a virtual network of an advertised type | Change |

## Verification checklist

- Network type comes from the platform catalogue.
- The created network appears in the lab’s network inventory.
- Interface-write/deletion semantics are not guessed.

## Sources

- [EVE-NG API guide (version not specified; publisher warns of outdated examples)](https://www.eve-ng.net/index.php/how-to-eve-ng-api/). Retrieved 2026-10-09.
