# gtrace IP metadata lookup

Collect the requested metadata for a parsed IP address.

## Common Sequences

- Enrich an address: **Validate address** → **Read metadata** → **Report provenance and gaps**.

### Validate address

Each selected lookup parses the supplied IPv4/IPv6 literal. Invalid input produces an address error rather than a hostname search. The tools do not require raw-socket privileges.

### Read metadata

ASN lookup returns available network/organization, prefix, country and registry context. Geographic lookup returns available city, region, country, coordinates and timezone. Reverse lookup returns resolver-derived hostname information. The requested operations are independent: failure of one does not turn another's data into a complete record. Provider/resolver failure remains a lookup error.

### Report provenance and gaps

The result identifies the input address, lookup types and returned values, with any missing/error result explicitly retained. Native JSON output is available when requested. A registry/network record, geographic database value and PTR name are separate metadata sources, not authentication of the host or proof of its current physical location.

## Patterns

Lookups can succeed independently and can disagree in geographic or naming context. The procedure reports each returned value with its lookup type.

## Known limitations

Provider freshness and location accuracy are not universally documented. No universal ASN-to-organization ownership conclusion or security reputation is inferred.

## Tools

Assumes the authenticated client described in [the bindings](endpoints.md).

| Operation | Description | Category |
|---|---|---|
| ASN lookup | Read registry/network metadata | Public metadata read |
| Geographic lookup | Read geographic metadata | Public metadata read |
| Reverse DNS | Read resolver hostname result | DNS read |

## Verification checklist

- The input is a valid IP literal.
- Requested lookup results and failures are separate.
- Values remain attributed metadata, not verified host identity.

## Sources

- [gtrace lookup tool schemas](https://github.com/hervehildenbrand/gtrace/blob/db04fd53e5a2a54c0fa0288543d619b9ece7d0c2/internal/mcp/server.go). Retrieved 2026-10-09.
- [gtrace lookup implementations](https://github.com/hervehildenbrand/gtrace/blob/db04fd53e5a2a54c0fa0288543d619b9ece7d0c2/internal/mcp/handlers.go). Retrieved 2026-10-09.
