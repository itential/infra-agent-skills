# APIC fabric and managed-object observations

Read ACI system inventory, endpoints, current faults or an explicitly identified managed object through APIC.

Source: Cisco [APIC REST API Configuration Guide, Using the REST API](https://www.cisco.com/c/en/us/td/docs/dcn/aci/apic/all/apic-rest-api-configuration-guide/cisco-apic-rest-api-configuration-guide/m_using_the_rest_api.html), continuously published guide including release-specific query limitations, retrieved 2026-10-09. Wire bindings and publisher error strings are in [endpoints.md](endpoints.md).

## Common Sequences

- Fabric records: Select model and scope → Read systems, endpoints or faults → Complete bounded pages.
- Object evidence: Select model and scope → Read named managed object.

### Select model and scope

The publisher requires the target release's Management Information Model reference to establish valid classes, distinguished names, attributes and access privileges. This procedure binds only the documented system, endpoint, fault and named-object reads. The query's object scope and filters are explicit; no tenant-wide health threshold or unsupported class schema is assumed.

### Read systems, endpoints or faults

The system collection returns controller/spine/leaf system elements with their available identity and role fields. The endpoint collection returns attached endpoint observations including IP/MAC/encapsulation where present. The current-fault collection returns native fault objects; an optional cause filter restricts the result to configuration failures. Success is the returned managed-object collection and count. A cleared or absent fault is not proof of application reachability.

### Complete bounded pages

The query uses a bounded page size and zero-based page numbers. Every page request computes a new result set; pages are not a server-pinned snapshot. Success is the requested coverage with actual response counts, preserving changes or partial coverage during collection. The guide's special log-record pagination rules are outside this current-state procedure.

For the documented destination-unavailable timeout on a read, Cisco recommends three to five retries. A too-large-result error requires a narrower filter, not an unchanged unbounded retry. The corresponding documented query limit is 100,000 objects and a 90-second response allowance; these are APIC-specific limits from this guide, not a general controller rule. Other authentication, authorization, schema or transport errors remain failed reads with their native details.

### Read named managed object

A known distinguished name selects the exact object. The self scope retrieves that object's properties. Where supported, the documented additional-object option includes its health or fault records; absence remains absence, not a synthesized zero score. Success is the intended object's returned distinguished name and properties. The publisher masks password properties in reads; writing a read response back would erase those values, so this observation procedure performs no write-back.

## Patterns

- System nodes, attached endpoints and fault records are different object classes.
- Pagination is recomputed per request and cannot promise a frozen fabric snapshot.
- The guide contains a malformed configuration-failure filter example; the valid equality-filter syntax in its companion example governs this binding.

## Known limitations

- No compliance/health threshold, universal fault severity recommendation, contract analysis or EPG reachability verdict is included.
- Log history, subscriptions and vendor-specific capacity or interface-fault diagnostics require their own procedures.
- Model fields beyond the examples require the deployed release's MIM; no generic field dictionary is invented.

## Tools

| Operation | Description | Category |
|---|---|---|
| Read systems | Retrieve fabric system-element records | Read |
| Read endpoints | Retrieve attached endpoint records | Read |
| Read faults | Retrieve current fault records with an optional cause filter | Read |
| Read named managed object | Retrieve a distinguished object's properties | Read |
| Read collection page | Retrieve the next explicitly scoped page | Read |

## Verification checklist

- Target APIC, model release, class/object and filters are explicit.
- Returned objects retain their native identifiers and properties.
- Query errors remain separate from empty successful results.
- Page coverage and non-snapshot behavior are recorded.
- Masked passwords are neither exposed nor written back.
