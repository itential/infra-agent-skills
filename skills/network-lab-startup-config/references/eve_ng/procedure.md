# EVE-NG native configuration export

Export supported node startup configuration into its EVE-NG lab file.

## Common Sequences

- Export: **Inspect** → **Export**.
- Export all nodes: **Inspect** all selected nodes → **Export** with explicit whole-lab scope.

### Inspect

Lab metadata and node inventory resolve the exact file and node scope. At each operation, the publisher’s response envelope carries a code, status and message. Unauthorized with code 400 indicates an expired session; 401 requires login. Forbidden/403 means insufficient permission. Other 4xx failures require request correction; 5xx errors are reported as server failures. Neither an HTTP response alone nor a message substring replaces the envelope’s outcome.

### Export

Native export saves startup configuration into the lab file and can overwrite a stored version: stop and confirm with the operator before proceeding. The publisher provides selected-node and whole-lab variants. A success envelope with the corresponding export message confirms the API operation. Failures follow **Inspect**; unsupported node extraction remains a platform error and is not replaced with arbitrary guest CLI commands.

## Patterns

The API guide’s single-node export paragraph mistakenly says “wiped”; its route and surrounding description specify export. This procedure follows the export operation, not that wording defect. Exported startup content can be loaded after a later node wipe/start.

## Known limitations

The publisher examples disable TLS certificate verification for Pro and show default credentials. Those are unsafe client examples, not requirements of this procedure; an authenticated client with certificate validation is assumed. The publisher warns that some examples are outdated. The installed version’s returned object schema takes precedence; unknown mutation parameters require platform-specific guidance. Direct reads/writes of embedded lab-file configuration, clearing only a startup fragment, and archive configuration manipulation are not covered by this API page. An export acknowledgement does not prove byte-for-byte contents because a corresponding readback operation is not documented here.

## Tools

Assumes the authenticated client described in [the bindings](endpoints.md).

| Operation | Description | Category |
|---|---|---|
| Inspect | Resolve lab and node identity | Read |
| Export | Save selected startup configuration into the lab | Change |

## Verification checklist

- Node versus whole-lab scope is explicit.
- The native export result is retained.
- No unsupported content-readback claim is made.

## Sources

- [EVE-NG API guide (version not specified; publisher warns of outdated examples)](https://www.eve-ng.net/index.php/how-to-eve-ng-api/). Retrieved 2026-10-09.
