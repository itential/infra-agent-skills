# NetBox stored record query

NetBox REST reads retrieve selected device, interface, cable, site, IP address, prefix and VLAN records and their documented fields.

Source: [NetBox REST API](https://netboxlabs.com/docs/netbox/integrations/rest-api/), current documentation, retrieved 2026-10-09. Authentication and literal query bindings are in [endpoints.md](endpoints.md).

## Common Sequences

- Find records: Discover collection → Filter and page records → Read identified record.
- Read known identifier: Discover collection → Read identified record.

## Discover collection

The API root and installed interactive API documentation identify available applications, model collections and supported query parameters. Success identifies the requested collection and its schema. The token version determines its authorization header; current v2 tokens differ from legacy v1 tokens. A missing collection or incompatible schema stops that query instead of borrowing a field or path from a different release.

## Filter and page records

The collection query uses filters published for that model and version. Success returns a count and a page of results with next/previous links. Following the returned next link preserves the query until no further page remains. Page size is deployment-limited; this procedure does not disable that limit. A complete empty result is distinct from an authorization or query error.

The missing-credentials condition is a forbidden response; the configured authentication is checked before retrying. Other validation, permission and server errors retain their response details. The cited overview does not give an exhaustive error catalogue for every model; endpoint-specific documentation governs unlisted failures. No error is converted into an empty inventory.

## Read identified record

The detail operation uses the record's returned URL or its documented identifier route. Success returns the selected object's identifier and its fields. More than one matching search result remains a collection; it is not automatically reduced to the first result. An absent record is reported as absent for that instance and identifier. NetBox related objects use brief representations; child collections are not included merely because a parent object was retrieved.

## Patterns

Filters and related-object schemas are platform/version specific. A recorded interface administrative state is not equivalent to an observed operational link state. Comparing intended and observed data requires a separately specified mapping; this read procedure does not infer one.

## Known limitations

Only the listed model families are in scope. Stored data cannot establish present device reachability. Custom fields, namespace/VRF relationships and tenant-specific extensions follow the installed schema rather than assumed global field names. No inventory mutation, drift severity policy or ticket workflow is performed.

## Tools

| Operation | Purpose | Category |
|---|---|---|
| Discover collection | Read API root and installed model contract | Read |
| Filter and page records | Retrieve scoped model collections | Read |
| Read identified record | Retrieve one stored object | Read |

## Verification checklist

- Instance, model and API version match the request.
- Model filters come from that instance's documented contract.
- Returned identifiers and pagination completeness are preserved.
- Stored state is distinguished from live observations and errors from empty results.
