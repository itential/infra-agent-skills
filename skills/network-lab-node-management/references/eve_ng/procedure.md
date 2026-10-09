# EVE-NG node lifecycle

Create, inspect, start, stop or wipe an EVE-NG node.

## Common Sequences

- Add: **Discover** → **Create** → **Inspect**.
- Operate: **Inspect** → **Start or stop** → **Inspect**.
- Reset: **Inspect** → **Wipe** → **Inspect**.

### Discover

Template listing and template details provide supported images and node settings. Selected template/image values come from that response rather than fixed NetClaw image names. At each operation, the publisher’s response envelope carries a code, status and message. Unauthorized with code 400 indicates an expired session; 401 requires login. Forbidden/403 means insufficient permission. Other 4xx failures require request correction; 5xx errors are reported as server failures. Neither an HTTP response alone nor a message substring replaces the envelope’s outcome.

### Create

Creation supplies node type and template plus the selected image, resources and layout. Before allocating a node: stop and confirm with the operator before proceeding. The guide’s node-created success result includes its numeric identifier. IOL port-group counts differ from QEMU interface counts; the selected template’s schema determines the inputs. Error handling follows **Discover**.

### Inspect

Node list/details return the node identity, runtime status, image, template and console URL. Console URLs and guest output are restricted to the authorized consumer. The interface operation supplies actual interface identifiers. Error handling follows **Discover**.

### Start or stop

Before changing node runtime state: stop and confirm with the operator before proceeding. The selected-node operation returns a success or failure envelope. The failure named **Node start failed** in the bindings remains a failed start. Subsequent node inspection supplies runtime evidence; no fixed boot-delay guarantee is asserted. Error handling follows **Discover**.

### Wipe

The publisher removes node user configuration and rebuilds the node from its image on a subsequent start: stop and confirm with the operator before proceeding. The wipe success envelope confirms the action. An exported startup configuration in the lab may be loaded after that wipe, so wipe is not a guarantee that every stored copy of configuration was erased. Error handling follows **Discover**.

## Patterns

Several lifecycle actions are mutating reads at the HTTP layer. Wipe removes runtime state; a previously exported configuration is a separate stored artifact.

## Known limitations

The publisher examples disable TLS certificate verification for Pro and show default credentials. Those are unsafe client examples, not requirements of this procedure; an authenticated client with certificate validation is assumed. The publisher warns that some examples are outdated. The installed version’s returned object schema takes precedence; unknown mutation parameters require platform-specific guidance. Node deletion is not documented in this public API page and is outside this reference.

## Tools

Assumes the authenticated client described in [the bindings](endpoints.md).

| Operation | Description | Category |
|---|---|---|
| Discover/inspect | Read templates, images, node state and interfaces | Read |
| Create/start/stop | Allocate or control a node | Change |
| Wipe | Clear node runtime configuration | Destructive |

## Verification checklist

- Template/image and node ID match the request.
- The envelope’s native result is retained.
- Wipe does not imply exported startup data was erased.
- Failed start is not replaced with a readiness claim.

## Sources

- [EVE-NG API guide (version not specified; publisher warns of outdated examples)](https://www.eve-ng.net/index.php/how-to-eve-ng-api/). Retrieved 2026-10-09.
