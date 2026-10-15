# Azure DNS — Record Set Management Procedure

Create, add a record to, update, or delete a DNS record set (A, AAAA, CNAME, MX, NS, PTR, SRV, TXT, CAA)
in an existing Azure DNS zone. Covers standard (non-alias) record sets in an existing zone only — DNS
zone creation, alias record sets (`targetResource`), and the DS/NAPTR/TLSA record types are out of scope.
Assumes an ARM-authenticated REST client against the Azure DNS management API
(`Microsoft.Network/dnsZones/*` record-set read/write) is already available.

Note the vocabulary difference from most other DNS platforms: Azure operates on a **record set** (one or
more values of the same name+type, e.g. two MX hosts in one set), not a single record — several steps
below exist specifically because of that.

## Operational procedure

### Common Sequences

1. **Point a new hostname at an IP address (the common "add an A record" ask):** Confirm the zone
   exists and the name isn't already in use for that type → **Create or Update a Record Set** with
   action CREATE, type A, one `ipv4Address` value → **Confirm the Result**.
2. **Add a second value to an existing record set (e.g. a second MX host, another TXT string):**
   **Create or Update a Record Set** with action ADD_RECORD — read the current record set first,
   append the new value to the type's record array, and submit the full updated set (Azure has no
   separate "append" call; see that section's ADD_RECORD note) → **Confirm the Result**.
3. **Retire a hostname entirely:** **Check Zone-Apex Restrictions** to confirm the target isn't the
   protected apex SOA/NS set → confirm with the operator → **Delete a Record Set**.

### Create or Update a Record Set

1. **Confirm the zone exists** — the target zone must already exist in the given resource group; this
   skill does not create zones (out of scope).
2. **Check type-specific restrictions before building the payload** (see `endpoints.md` for full
   detail):
   - CNAME: the record set may hold only one record — reject a request to add a second value; a
     correction requires replacing the single `cname` value, not appending.
   - Any type: reject a request that would exceed 20 records in the set, or that duplicates an existing
     identical record in the set.
   - SOA: cannot be created (only updated — it's auto-created with the zone); at the zone apex
     (`relative_record_set_name = "@"`), `host` and the record set's own TTL cannot be changed — reject
     an update attempting either.
   - NS at the zone apex: additional `nsdname` entries may be added and TTL/metadata modified, but the
     pre-populated Azure DNS name server entries cannot be removed or modified — reject a request that
     would alter or drop any of them. Non-apex NS record sets have no such restriction.
3. **Confirm before overwriting or deleting production resolution** — if this is an UPDATE/CREATE
   against a name+type that already resolves, **stop and confirm with the operator** before proceeding,
   stating the zone, record set name, type, and the values being changed.
4. **Build the request** — TTL plus the caller-supplied type-specific field values for the record(s)
   being added/set, using the exact field names from `record-fields.md` for the record type (e.g.
   `ARecords[].ipv4Address`, `CNAMERecord.cname`, `MXRecords[].preference`/`exchange`). For ADD_RECORD,
   first read the current record set and append the new entry to the existing array — there is no
   separate "add one record" API call; the full desired array is submitted each time. If the caller
   supplied the record set's current `etag` (to guard against overwriting a concurrent change), set
   `If-Match` to it; use `If-None-Match: *` if the caller wants the call to fail rather than overwrite an
   existing record set.
5. **Submit the call** — see `endpoints.md` § "Create or Update a Record Set" for the literal call.
   Treat `200 OK` as UPDATED and `201 Created` as CREATED, both carrying the resulting `RecordSet`
   object.
6. **Handle failures** — any other status returns a `CloudError` (`error.code`/`error.message`). No
   specific error codes are documented on the source reference page — report the tool's actual error
   verbatim as FAILED rather than guessing at a cause (see `endpoints.md`).

### Delete a Record Set

1. **Check zone-apex restrictions first** (see below) — the SOA and NS record sets at the zone apex
   (`relative_record_set_name = "@"`) cannot be deleted; they are removed automatically only when the
   zone itself is deleted. Reject a delete request against either, reporting which restriction applied.
2. **Check for a resource lock** — if an IP address or resource associated with the record set is
   locked, the lock must be removed before the record set can be deleted (documented restriction — see
   `endpoints.md`). Report this to the operator rather than attempting to force it.
3. **Confirm before deleting** — always confirm with the operator before a delete call: state the zone,
   record set name, and type being removed.
4. **Delete the record set** — see `endpoints.md` § "Delete a Record Set." Report DELETED on success.

Note: removing a single record from a multi-record set (leaving other records in place) is not a delete
of the record set — it's an UPDATE that resubmits the set's array without that entry. "Removing the last
record from a record set doesn't delete the record set" (source, verbatim) — an explicit delete call is
still required to remove the now-empty set, if that's the intended outcome.

### Check Zone-Apex Restrictions

Applies whenever `relative_record_set_name = "@"`:
- **SOA:** records cannot be added to or removed from the apex SOA set. Any update may change any SOA
  field except `host` and the record set's own TTL.
- **NS:** additional name servers may be added, and TTL/metadata modified — but the Azure-DNS-assigned
  name server entries already present cannot be removed or modified. This restriction applies only at
  the zone apex; NS record sets elsewhere in the zone (child-zone delegation) have no such restriction.
- Neither the apex SOA nor apex NS record set can be deleted directly — both are removed automatically
  only when the zone itself is deleted.

### Confirm the Result

- **CREATE/UPDATE:** confirm the response's `RecordSet.properties` reflects the submitted values (TTL
  and type-specific fields) and note `properties.fqdn` and `etag` for the report.
- **DELETE:** confirm a subsequent list/get against the record set returns not-found.
- **Rejected on a documented restriction:** no call was submitted — report which restriction applied.

## Patterns

- **Adding a record is always a full-array resubmit.** There's no incremental "append one value" call —
  ADD_RECORD reads the current set and resubmits the whole array with the new entry appended.
- **Removing the last record ≠ deleting the set.** An empty record set still exists until an explicit
  delete call removes it.

## Known limitations

- Covers standard (non-alias) record sets in an existing zone only — DNS zone creation, alias record
  sets (`targetResource`), and DS/NAPTR/TLSA record types are out of scope.
- The zone-apex SOA and NS record sets can never be deleted — only edited within documented limits — so
  "delete" isn't a universal operation across every record set in a zone.
- **Any DELETE, and any UPDATE/CREATE against a name+type that already resolves in production, is hard
  to reverse** — Azure DNS keeps no undo/rollback for a completed change. Reversal is only possible via
  an inverse call (recreate with original values, remove an added record, revert a field) and only if
  those prior values were captured beforehand. This is why the confirm-before-overwriting step exists.

## Tools

Every operation below maps to the Azure Resource Manager DNS API (management.azure.com, api-version
2018-05-01) — see `endpoints.md` for the literal request/response shape.

| Operation | Description | Category |
|---|---|---|
| `RecordSets - Create Or Update` | Create, update, or add/remove a record within a record set | Record Set Management |
| `RecordSets - Delete` | Delete a record set (subject to zone-apex restrictions) | Record Set Management |
| `RecordSets - Get` | Read a record set's current state (used before ADD_RECORD, and to confirm results) | Record Set Management |

## Verification checklist

- [ ] Type-specific restrictions (CNAME single-record, 20-record cap, SOA/NS zone-apex rules) were
      checked before submitting, not discovered from a rejected call
- [ ] Confirmed with the operator before any delete, or any create/update against a name+type that
      already resolves in production
- [ ] For ADD_RECORD: the full updated array was submitted, not just the new entry
- [ ] Result confirmed via the response object (CREATE/UPDATE) or a follow-up not-found read (DELETE)
