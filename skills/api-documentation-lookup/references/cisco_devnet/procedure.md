# Cisco API documentation retrieval

Find Cisco Meraki or Catalyst Center API documentation through Cisco DevNet Content Search MCP.

Source: CiscoDevNet [Content Search MCP README](https://github.com/CiscoDevNet/devnet-content-search-mcp/blob/main/README.md), current main, retrieved 2026-10-09. Concrete tool identifiers, parameters and response fields are in [endpoints.md](endpoints.md).

## Common Sequences

- Find an operation by purpose: Select product and search → Retrieve matching documentation → Inspect returned API evidence.
- Resolve a known Meraki operation: Select exact operation ID → Retrieve matching documentation → Inspect returned API evidence.

### Select product and search

A keyword search selects the Meraki or Catalyst Center search operation and a nonempty keyword. The API-only option narrows the results to API material; leaving it unset allows the broader documentation search. The requested result count follows that operation's published schema rather than assuming both products have identical limits.

### Select exact operation ID

A known Meraki operation identifier uses the dedicated exact-identifier lookup. The publisher does not document an equivalent Catalyst Center identifier tool in this interface. A human-readable title is not substituted for an API operation identifier.

### Retrieve matching documentation

The selected search returns documentation records and an error indicator. A successful response with no matches is an empty search, not proof that the product lacks the capability; the publisher suggests broader keywords or synonyms. A missing-keyword error requires the required argument. Rate-limit errors require waiting and fewer requests; the source specifies no universal delay. Authentication failures require valid DevNet credentials and organizational access. An unavailable search service remains unavailable and can be escalated to Cisco DevNet support. A connection failure requires correcting the MCP connection or network access.

### Inspect returned API evidence

The returned title, product metadata, documentation link and API-specific fields establish which operation matched. Where present, the embedded API specification supplies the documented parameters, request body and responses. Success is the requested documentation record with its provenance and applicable product; a missing schema or absent version remains an explicit gap. Retrieving a mutation's documentation does not execute or authorize that mutation.

## Patterns

- Keyword lookup and exact Meraki operation-ID lookup have different parameter names and purposes.
- API-only filtering changes the kinds of documents returned, not the controller's authorization.

## Known limitations

- Search relevance does not establish that a particular controller release supports the operation; returned version information governs applicability.
- The publisher does not state a Catalyst Center default/result-count bound in this README. The live tool schema is required before relying on one.
- No controller configuration, test execution or data-plane validation occurs here.

## Tools

| Operation | Description | Category |
|---|---|---|
| Search Meraki documentation | Retrieve keyword-matched Meraki material | Read |
| Search Catalyst Center documentation | Retrieve keyword-matched Catalyst Center material | Read |
| Resolve Meraki operation ID | Retrieve a known API operation's documentation | Read |

## Verification checklist

- Product, search kind and required argument match the request.
- Error responses remain distinct from empty successful searches.
- Returned documentation links and operation identifiers accompany the evidence.
- Missing version/schema information is explicit and no retrieved API was executed.
