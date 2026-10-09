# PeeringDB network and presence lookup

Read a network's published registration and its exchange/facility presence from PeeringDB.

## Common Sequences

- Network context: **Find network** → **Read network presence**.

### Find network

An ASN-filtered network collection returns an array of matching records. Success is a network record whose ASN matches the request, retaining its PeeringDB identifier. Empty data means no visible matching record. Anonymous access can hide contact information; authentication uses an API key for the authorized view.

### Read network presence

A detail read of the returned network identifier expands related sets to the explicitly selected depth. Network-at-exchange and network-at-facility relationships provide published presence evidence. Success is the selected network and returned related records, not proof of an established BGP session. Separate relationship collection reads can use the selected network identifier, bounded by limit/skip, when expanded data is insufficient.

The API's data array is retained even for a single object. Authentication failure with deprecated Basic credentials requires the documented API-key method, not repeated Basic attempts. Other error status/message data remains a failure; permission-filtered or truncated results do not establish global absence. The sources do not provide one fixed retry budget; throttling retains any response guidance.

## Patterns

The API specification distinguishes expansion defaults for collections and single-object reads. This procedure supplies an explicit depth instead of relying on the inconsistent defaults in the HOWTO. The documentation still contains older Basic-auth URL examples despite stating that Basic authentication is rejected; those examples are not followed.

## Known limitations

No record edits, private-contact access beyond the client's permissions, peering negotiation or operational session verification is included.

Sources: [PeeringDB API specification](https://docs.peeringdb.com/api_specs/) and [search/API HOWTO](https://docs.peeringdb.com/howto/search/), retrieved 2026-10-09. Bindings: [endpoints](endpoints.md).

## Tools

| Operation | Purpose | Category |
|---|---|---|
| Find network | Read a network by ASN | Read |
| Read network presence | Read published exchange/facility associations | Read |

## Verification checklist

- ASN and returned network ID match.
- Explicit expansion depth and collection bounds are recorded.
- Published presence is distinguished from live peering.
- Restricted/missing data and native errors are preserved.
