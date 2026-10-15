# BlueCat Address Manager (Integrity/DDI) — DNS Record Creation Procedure

Create a DNS resource record (host, CNAME, alias, MX, TXT, or SRV) inside an existing DNS zone on
BlueCat Address Manager, the on-premises DDI (DNS/DHCP/IPAM) appliance that is part of BlueCat's
Integrity product line. Create-only, in an existing zone — does not cover zone/view/configuration
creation, record edit/delete beyond what's noted below, bulk import/export, or IP address block/network
management. Assumes an authenticated REST client against Address Manager's own RESTful v2 API is
already available.

**This is a different BlueCat product from `references/bluecat/` (BlueCat Horizon / DDI
Orchestrator).** Address Manager is Integrity's self-contained, self-hosted DDI engine with its own
data store and its own REST API surface (the v2 REST API, versioned per Address Manager release). Horizon is
a separately-sold, cloud-hosted control plane that sits in front of and governs existing DNS/DHCP/IPAM
systems (which can include Address Manager itself, Active Directory-integrated DNS, BIND, Kea, or
cloud-provider DNS) rather than being one of those systems itself — it does not expose the same
resource model or endpoint set documented here. Confirm which product a request is actually targeting
before picking a procedure file; do not assume they're interchangeable.

Source grounding: BlueCat's own "Address Manager RESTful v2 API Guide" (docs.bluecatnetworks.com,
retrieved 2026-09-29) plus BlueCat's own published product pages distinguishing Address
Manager/Integrity from Horizon. Address Manager also ships an interactive Swagger UI on the appliance
itself (location in `endpoints.md`) that documents the live, version-exact endpoint/schema set — treat
that as the authoritative source for any field this procedure doesn't cover, since the public docs
describe the API's shape and conventions rather than every resource's full schema.

## Operational procedure

1. **Confirm the zone exists** — look up the target zone by name under its parent view/configuration.
   If the zone can't be found, stop and report FAILED with "zone does not exist" — Address Manager's v2
   API expects the zone to already exist and be addressable by its object ID before a record can be
   posted into it (see `endpoints.md`).
2. **Validate the record type** — Address Manager's v2 API exposes resource-record creation for host,
   CNAME, alias, MX, TXT, and SRV records as distinct object subtypes sharing one collection endpoint
   (see `record-fields.md`). If the caller asks for a type outside this set (e.g. raw `NS`, `PTR`,
   `SOA`, or a DNSSEC type), the public API guide does not document a `resourceRecords` path for it —
   stop and report REJECTED_UNSUPPORTED_TYPE rather than guessing at an undocumented shape; those
   record kinds are managed through other, non-resource-record parts of Address Manager's object model
   (zone/network objects) that are outside this procedure's scope.
3. **Build the record payload** — assemble the record object for the chosen type: `name` and `type` are
   always required; the value field depends on type (`addresses` for a host record, `linkedRecordName`
   for CNAME/alias, `text` for TXT, `priority` plus the target for MX/SRV — see `record-fields.md` for
   the exact per-type field). `ttl` is optional and falls back to the zone/record default when omitted.
4. **Create the record** — submit the payload as a POST to the target zone's resource-record collection.
   See `endpoints.md` for the literal call and the object ID-based URI pattern this API uses throughout
   (not name-based).
5. **Confirm creation** — a 201 response carrying the created record object (with its assigned numeric
   `id`) is success. If the calling tool needs a separate confirmation read, GET the record back by its
   returned `id`, or list the zone's resource-record collection and filter by name/type. Report CREATED
   with the record object.
6. **Handle failures verbatim** — a 400 response indicates a malformed request (e.g. an invalid field
   combination for the chosen type), and a 404 means the parent zone ID no longer resolves. Report
   FAILED with the underlying error content rather than normalizing it, since the guide's own error
   schema is generic (`Error` object) and doesn't enumerate every possible validation message.

## Patterns

- **Object-ID addressing throughout.** Unlike some DNS platforms that key records off their name, this
  API's records, zones, views, and configurations are all addressed by an integer `id` assigned at
  creation — a lookup-by-name step (zone, and afterward the record if a separate confirmation read is
  needed) is a normal, expected part of any sequence here, not an extra safety step.
- **Record type is chosen at creation via the payload's `type` field and is not covered by a documented
  in-place type-change path** in the sources reviewed — if a correction of a wrong-type record is
  needed, treat it as delete-then-recreate unless the target instance's own live Swagger doc shows
  otherwise (this differs from `references/bluecat/`'s Horizon procedure, which states this as an
  explicit vendor-documented warning; the Address Manager v2 guide simply doesn't document an update
  path for the `type` field itself, which is a weaker but same-direction signal — verify against the
  live instance if precision matters).

## Known limitations

- Create-only — does not cover zone/view/configuration creation, IP address block/network/DHCP range
  management, bulk import/export, or PTR-from-host auto-generation.
- Only host, CNAME, alias, MX, TXT, and SRV records are confirmed to go through the `resourceRecords`
  collection endpoint documented here. Other record types (NS, PTR, SOA, DNSSEC types, etc.) are not
  documented as available through this same path in the sources reviewed — this is a real coverage gap,
  not an oversight, and should be checked against the target instance's own Swagger doc before assuming
  they're unsupported outright.
- Exact validation-error message text for a duplicate or conflicting record is not enumerated in the
  sources reviewed — don't invent specific error strings; surface the tool's actual response.

## Tools

| Operation | Description | Category |
|---|---|---|
| Zone lookup | Confirm the target zone exists and resolve its object ID | DNS Zones & Records |
| Resource record create | Create a new host/CNAME/alias/MX/TXT/SRV record under a zone | DNS Zones & Records |
| Resource record read | Confirm a created record by its object ID, or list a zone's records | DNS Zones & Records |

## Verification checklist

- [ ] Target zone confirmed to exist and its object ID resolved before attempting the create call
- [ ] Requested record type confirmed to be one of the six documented resource-record subtypes before
      building the payload
- [ ] Per-type required field supplied correctly (`addresses`/`linkedRecordName`/`text`/`priority`+target)
- [ ] Creation confirmed via the 201 response's record object or a follow-up read by the returned `id`
