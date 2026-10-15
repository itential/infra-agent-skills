# Endpoints — Azure DNS Record Set Create/Update/Delete

Literal wiring layer, quoted from the Azure DNS REST API reference (api-version 2018-05-01). `SKILL.md`
steps reference these by name; bind them to whatever ARM-authenticated REST client/adapter is assumed
available (see `requires_tool`/`assumed_tool` in `SKILL.md` frontmatter).

Source is the Portal's own underlying resource — the Portal doc itself gives no literal API call; the
REST shape below is the secondary source used to fill that gap.

## Create or Update a Record Set

```
PUT https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/dnsZones/{zoneName}/{recordType}/{relativeRecordSetName}?api-version=2018-05-01
```

Path parameters:
- `subscriptionId`, `resourceGroupName` — target Azure subscription/resource group.
- `zoneName` — "The name of the DNS zone (without a terminating dot)."
- `recordType` — one of `A`, `AAAA`, `CAA`, `CNAME`, `MX`, `NS`, `PTR`, `SOA`, `SRV`, `TXT`. "Record
  sets of type SOA can be updated but not created (they are created when the DNS zone is created)."
- `relativeRecordSetName` — "The name of the record set, relative to the name of the zone." Use `@`
  for the zone apex.

Request headers (optional, both control overwrite behavior):
- `If-Match: <etag>` — "Specify the last-seen etag value to prevent accidentally overwriting any
  concurrent changes." Omit to always overwrite.
- `If-None-Match: *` — "Set to '*' to allow a new record set to be created, but to prevent updating an
  existing record set." This is the literal mechanism for a create-only (never-overwrite) call.

Request body: `{ "properties": { "TTL": <seconds>, "<type-specific-field>": ... } }` — see
`references/record-fields.md` for the exact per-type field name and shape.

**Success:**
- `200 OK` — "The record set has been updated." Body: `RecordSet` object (includes `etag`, `id`,
  `properties.fqdn`).
- `201 Created` — "The record set has been created." Same body shape.

**Failure:** any other status code returns a `CloudError` body: `{ "error": { "code", "message",
"target", "details": [] } }`. No specific error codes/strings are enumerated in this reference page —
report the tool's actual `error.code`/`error.message` verbatim rather than pattern-matching against an
invented one (this is a genuine documented gap, not an extraction miss).

## Delete a Record Set

Not shown in the fetched REST reference page (only Create-Or-Update was retrieved per this skill's
scope). The Portal procedure's own delete flow (trash icon →
confirm the name matches → Yes) is the authoritative sequence for this skill; if wiring to the REST
API directly, the standard ARM DNS `RecordSets - Delete` operation (`DELETE` on the same path as
above) is the documented counterpart per Azure's own REST API index, but its exact response codes were
not retrieved as part of this skill's build — confirm against the live REST reference before relying
on it unmodified.

## Documented restrictions to enforce before calling Create-or-Update

- **CNAME:** at most one record in the set (`CNAMERecord` is a single object, not an array, in the
  schema itself).
- **Any record set type:** at most 20 records per set (Portal doc, verbatim: "You can add up to 20
  records to any record set"); no two identical records in one set.
- **SOA at zone apex (`relativeRecordSetName = "@"`):** cannot create/delete records within it (it's
  managed by the zone itself); can update any SOA field except `host` and the record set's own `TTL`.
- **NS at zone apex (`relativeRecordSetName = "@"`):** can add additional `nsdname` entries and modify
  TTL/metadata; cannot remove or modify the Azure-DNS-assigned name server entries that were
  pre-populated at zone creation. Non-apex NS record sets (child-zone delegations) have no such
  restriction.
- **Locked resources:** "If an IP address associated with a recordset is locked you must remove the
  lock prior to deleting the recordset" (verbatim, portal doc) — check for an Azure resource lock
  before attempting a delete if the record is associated with a locked resource.
