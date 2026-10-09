# RIPE Atlas probe and anchor inventory

Read existing RIPE Atlas probe counts and anchor records without creating measurements.

## Common Sequences

- Probe availability evidence: **Read probe inventory** for the selected ASN/country/status.
- Anchor evidence: **Read anchors** → retain each anchor's associated probe identity and status fields.

### Read probe inventory

The probe collection is filtered by the requested ASN, country, public/anchor attributes or numeric status. Success is the returned count and result page. The count describes the filtered collection, not only the current page. Continuation links are followed when records, rather than only the count, are requested. Non-public probes can expose basic metadata while hiding operational details; hidden fields remain unknown.

### Read anchors

The anchor collection accepts IPv4/IPv6 ASN and country filters plus active/public/retirement filters. Success is a count and anchor records containing their identities and associated probe IDs. Continuation links supply further pages. Active, disabled and permanently decommissioned are distinct filters; they are not collapsed to one state.

The documented successful response is a JSON collection with count and results. The consulted operation references do not enumerate a complete error contract; failed responses retain native status/body. A failure is not a zero probe count. No fixed polling/retry interval is asserted.

## Patterns

A connected probe count is inventory evidence, not a measurement of the requested target. ASN fields for IPv4 and IPv6 can differ. Anchor records and the probes hosted on them have distinct identifiers.

## Known limitations

No measurement creation, probe control, private-data bypass or reachability conclusion is included.

Sources: RIPE Atlas [probe list](https://atlas.ripe.net/docs/apis/rest-api-reference/probes/probes_list/) and [anchor list](https://atlas.ripe.net/docs/apis/rest-api-reference/anchors/anchors_list/), retrieved 2026-10-09. Bindings: [endpoints](endpoints.md).

## Tools

| Operation | Purpose | Category |
|---|---|---|
| Read probe inventory | Read filtered probe count and records | Read |
| Read anchors | Read anchor records and probe associations | Read |

## Verification checklist

- Filter and count scope are explicit.
- All requested pages were retrieved or marked incomplete.
- Hidden fields remain unknown.
- No inventory count is described as a packet-test result.
