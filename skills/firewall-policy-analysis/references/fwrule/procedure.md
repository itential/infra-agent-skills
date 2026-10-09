# FWRule candidate overlap analysis

AutomateIP FWRule MCP normalizes supplied firewall policy data and identifies how a candidate intersects that ruleset.

Source: [publisher README](https://github.com/AutomateIP/fwrule-mcp/blob/main/README.md), current main, retrieved 2026-10-09. Bindings and format details are in [endpoints.md](endpoints.md).

## Common Sequences

- Native configuration: Discover formats → Parse policy → Check normalized data → Analyze candidate.
- Already normalized data: Check normalized data → Analyze candidate.

## Discover formats

The supported-vendor query returns vendor identifiers and required configuration formats. The selected parser must match that returned support. An unsupported vendor or version is not silently assigned a similar parser. The current publisher lists FortiOS 6.x–7.x; the older source's 5.x claim and fork-install workaround are not carried forward.

## Parse policy

The parsing operation receives the complete supplied vendor-format policy and any supplied supplemental objects. Success returns normalized rules in the engine's schema. A parse or validation error prevents analysis of that result. The publisher does not enumerate stable error codes; the native error and affected input remain in the outcome.

## Check normalized data

The publisher's inspection stage checks rule counts and address/object resolution against the supplied policy. The rules include their order, enabled state, action, zones, addresses, services and applications. An unexplained count or object mismatch makes the parsed representation unverified. Already structured data can use normalized input directly when its fields and resolved addresses are known; missing data is not invented.

## Analyze candidate

The analysis compares a single candidate with the existing rules, optionally at an explicit insertion position. Native-format and normalized-input modes use the bindings in the companion file. Success returns the engine's overlap findings, including duplicates, shadowing, action conflicts, partial intersections and subset/superset relationships where detected. Findings retain affected rule identities and dimensions from the response. A validation/analysis error is a failed analysis, not a clean policy.

## Patterns

- Order affects shadowing; a proposed insertion position is part of the candidate context.
- Unresolved object references can become an unrestricted match in the publisher's conservative model. This can inflate findings and requires visible uncertainty.
- The publisher warns that parser behavior can change with vendor output formats. A successful parse alone does not validate the representation.

## Known limitations

This is analysis of supplied data, not proof of live forwarding behavior or authorization to deploy. Business approval, cleanup priorities and change-ticket policy are outside scope. No configurations are changed. Batch analysis is a newer publisher operation outside the three-operation source extraction.

## Tools

| Operation | Purpose | Category |
|---|---|---|
| Discover formats | List supported vendor input contracts | Read |
| Parse policy | Normalize supplied configuration | Offline analysis |
| Analyze candidate | Compare candidate against supplied rules | Offline analysis |

## Verification checklist

- Input format and vendor are supported by the selected engine.
- Rule counts and object resolution were checked against the supplied source.
- Candidate placement is retained when supplied.
- Native findings and parser uncertainty are reported without a deployment or approval claim.
