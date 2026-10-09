# EVE-NG lab lifecycle

Discover, create, inspect, operate or delete an EVE-NG lab using its published API.

## Common Sequences

- Discover/create: **Discover** → **Create** if requested → **Inspect**.
- Run/stop: **Inspect** → **Operate nodes** → **Inspect**.
- Remove: **Inspect** → **Delete**.

### Discover

Folder listing returns separate lab and folder collections. Lab paths, rather than guessed UUID endpoints, identify the selected file. System status and the current authenticated-user record provide platform/session context. At each operation, the publisher’s response envelope carries a code, status and message. Unauthorized with code 400 indicates an expired session; 401 requires login. Forbidden/403 means insufficient permission. Other 4xx failures require request correction; 5xx errors are reported as server failures. Neither an HTTP response alone nor a message substring replaces the envelope’s outcome.

### Create

Lab creation uses the requested folder, name and metadata. Before writing the lab file: stop and confirm with the operator before proceeding. The documented result has code 200 and success status with the lab-created message. Folder discovery supplies the created path for inspection. Error handling follows **Discover**.

### Inspect

Lab retrieval returns code 200, success and lab metadata. Node inventory supplies runtime state for the lab; metadata existence alone does not mean nodes are running. Error handling follows **Discover**.

### Operate nodes

The publisher provides whole-lab node start and stop operations. Each changes live simulation state: stop and confirm with the operator before proceeding. The response’s success/failure envelope and subsequent node inventory are retained. A node-start failure remains a failure even when a client received a response; error handling follows **Discover**.

### Delete

Lab deletion removes the selected file: stop and confirm with the operator before proceeding. Code 200, success and the lab-deleted message are the documented result. Error handling follows **Discover**; unknown deletion errors are not treated as already absent.

## Patterns

One account supports one active login location according to the guide; a second login can invalidate the first. Path encoding preserves folder boundaries and filename identity.

## Known limitations

The publisher examples disable TLS certificate verification for Pro and show default credentials. Those are unsafe client examples, not requirements of this procedure; an authenticated client with certificate validation is assumed. The publisher warns that some examples are outdated. The installed version’s returned object schema takes precedence; unknown mutation parameters require platform-specific guidance. Portable archive import/export is not specified in the cited API guide and is not covered.

## Tools

Assumes the authenticated client described in [the bindings](endpoints.md).

| Operation | Description | Category |
|---|---|---|
| Discover/inspect | Read folder, lab, node, session and system data | Read |
| Create/start/stop | Create a lab or control its nodes | Change |
| Delete | Remove the selected lab | Destructive |

## Verification checklist

- The exact lab file path is retained.
- Success is checked in the response envelope.
- Node runtime state is not inferred from lab metadata.
- Session failures are distinguished from operation failure.

## Sources

- [EVE-NG API guide (version not specified; publisher warns of outdated examples)](https://www.eve-ng.net/index.php/how-to-eve-ng-api/). Retrieved 2026-10-09.
