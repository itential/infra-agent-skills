# BlueCat Horizon / DDI Orchestrator — DNS Record Creation Procedure

Create a DNS resource record (A, AAAA, CNAME, TXT, MX, NS, PTR, SRV, and other non-read-only types) in
an existing zone on BlueCat Horizon / DDI Orchestrator. Create-only, in an existing zone — does not
cover zone creation, record edit/delete, bulk import/export, or reverse-record (PTR-from-A)
auto-generation. Assumes an authenticated REST client against the DDI Orchestrator API (DNS record
create + read on the target zone) is already available.

Scope note: covers creating one DNS resource record via BlueCat Horizon's underlying DDI Orchestrator
API. The Horizon User Guide's own "Creating DNS records" page documents the web UI flow, not a REST
schema — the API field names and the record-object schema here are drawn from DDI Orchestrator's own
REST API guide and Ansible module reference, which document the same underlying `dnsRecord` object.
Facts taken from that secondary path are noted as such throughout; if you have access to the
target instance's own live API doc (`/mmws/api/doc`, or Horizon's Administration → API documentation),
verify field names and the exact response schema against it before relying on this unmodified in
production.

## Operational procedure

1. **Confirm the zone exists** — look up the target zone. If it cannot be found, stop and report FAILED
   with "zone does not exist" rather than attempting to create the record — BlueCat requires the zone
   to already exist and be accessible (see `endpoints.md`).
2. **Validate the record type** — check the requested type against the read-only list in
   `record-fields.md` (`ALIAS`, `DLV`, `DNSKEY`, `NSEC`, `NSEC3`, `NSEC3PARAM`, `RRSIG`). If it's one of
   these, stop and report REJECTED_READONLY_TYPE — do not attempt the create call.
3. **Build the record payload** — assemble the `dnsRecord` object: name, type, data, plus TTL if
   supplied (uses the zone/record default if omitted). For MX, SRV, NAPTR, CAA, CERT, HINFO, TLSA, the
   value is a space-separated sub-field list (see `record-fields.md` for what's documented and what
   isn't about sub-field order — confirm against the target instance if precision matters). A comment is
   valid only on records in static zones — omit it for dynamic (AD-integrated) zones. **Important:** once
   created, the record's type can never be changed — if this call is actually a correction of a previous
   wrong-type record, delete the old record first rather than trying to update it (see `endpoints.md` for
   the verbatim BlueCat warning).
4. **Create the record** — submit the payload against the target zone. See `endpoints.md` for the
   literal call.
5. **Confirm creation** — treat a 2xx response carrying the created record object as success. If the
   calling tool needs a separate confirmation read, GET the record back by name/type in the same zone.
   Report CREATED with the record object.
6. **Handle failures verbatim** — the sources for this skill do not document a specific duplicate-record
   or validation-error response (see `endpoints.md`). If the create call fails for any reason other than
   the read-only-type check in step 2, report FAILED with the underlying tool's actual error response
   rather than guessing at a cause.

## Patterns

- **Type is immutable once created.** There is no "change the type" update path — a wrong-type record
  is always delete-and-recreate, never an in-place fix.

## Known limitations

- Create-only — does not cover zone creation, record edit/delete, bulk import/export, or PTR-from-A
  auto-generation.
- Read-only record types (`ALIAS`, `DLV`, `DNSKEY`, `NSEC`, `NSEC3`, `NSEC3PARAM`, `RRSIG`) cannot be
  created through this API at all.
- Field names and the response schema here are drawn from a secondary source (DDI Orchestrator's own
  REST/Ansible references), not BlueCat's Horizon User Guide directly — verify against the target
  instance's live API doc before relying on this unmodified in production.

## Tools

| Operation | Description | Category |
|---|---|---|
| Zone lookup | Confirm the target zone exists and is accessible | DNS Zones |
| `dnsRecord` create | Create a new DNS resource record in a zone | DNS Records |
| `dnsRecord` read | Confirm a created record by name/type (or re-check before a correction) | DNS Records |

## Verification checklist

- [ ] Target zone confirmed to exist before attempting the create call
- [ ] Requested type checked against the read-only list before building the payload
- [ ] Comment omitted for dynamic (AD-integrated) zones
- [ ] Creation confirmed via the create response or a follow-up read by name/type
