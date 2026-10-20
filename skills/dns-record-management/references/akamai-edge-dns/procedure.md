# Akamai Edge DNS — DNS Record Set Procedure

Create, read, replace (update), or delete a record set (all values sharing one name and type) in an existing
Akamai Edge DNS zone through the Edge DNS API v2, using the direct record-set operations. Assumes an
authenticated API client for the target account (EdgeGrid-signed requests with an API client holding
read-write access to the "DNS—Zone Record Management" permission) is already available. Does not cover zone
creation or deletion, change lists (batched edits), zone versions or reactivation, DNSSEC, zone transfers,
or bulk record-set calls.

Sources (retrieved 2026-10-19), all from Akamai's TechDocs Edge DNS reference: "Create a record set",
"Replace a record set", "Get a record set", "Delete a record set", "Use change lists", "Definitions of the
activationState", "Get started". Details marked (unverified) were not confirmed on the vendor reference pages and need checking there.

## Model

The unit of change is the **record set**: one name, one type, one TTL, and an array of values. There is no
per-value add or remove; adding or removing one value means reading the set and replacing it with the
modified array. Direct operations take effect on the network right after the call completes, whereas change
lists batch edits until submitted; this procedure uses direct operations only.

## Common Sequences

- **Create a record set:** confirm the zone (step 1) → validate values and check CNAME exclusivity
  (steps 3-4) → create (step 5) → verify (step 7).
- **Change a record set or add/remove one value:** confirm the zone (step 1) → read the set (step 2) →
  build the full desired array (step 3) → replace (step 5) → verify (step 7).
- **Remove a record set:** read the set (step 2) → operator confirmation and delete (step 5) → verify
  absence (step 7).

## Operational procedure

1. **Confirm the zone** — the zone must already exist and be reachable with the credentials. A 404 naming
   the zone means it is missing or not visible to the account; stop and report FAILED. Multi-account users
   may need the account-switch parameter (see `endpoints.md`).
2. **Read the current record set** (skip for a plain create of a new name) — a 404 means the set does not
   exist. Keep the returned values; replace needs the full desired array.
3. **Validate the type and values** — each value is a string in zone-file (RFC 1035 master file) rdata
   format, one string per record. TTL is an integer of 0 or more. Build the complete array for the
   desired end state. SOA and NS record-set handling at the zone apex is not stated in the sources:
   (unverified) consult platform-specific guidance before touching them and treat them as out of scope here.
4. **Check CNAME exclusivity** — a CNAME cannot coexist with other types at the same name (RFC 1035
   §3.6.2). Read the name's existing types first; on a conflict stop and report REJECTED_STRUCTURAL_CONFLICT.
5. **Apply the change**
   - Create: submit the name, type, TTL and values. Success is HTTP 201 with the created record set.
     A 409 means the record set already exists; report ALREADY_EXISTS and offer replace instead.
   - Replace (update): name and type in the body must match an existing record set. Success is HTTP 200
     returning the replaced set. A 404 means it does not exist; report NOT_FOUND.
   - Delete: **stop and confirm with the operator before proceeding** — it removes the whole record set
     (every value), and the sources document no undo for it. Success is HTTP 204 with an empty body.
6. **Handle concurrency and validation errors** — a 412 means the optimistic-concurrency tag sent with the
   request no longer matches the current state; re-read and retry only after rechecking the desired end
   state. 400 or 422 means invalid fields or values (for example a TTL out of range); report the error
   body and do not retry unchanged. 415 means the content type was not JSON. 401 means missing or invalid
   credentials. Errors use the RFC 7807 problem-details shape.
7. **Verify** — read the record set back and compare name, type, TTL and values with the intended state.
   The zone's activation state moves from PENDING to ACTIVE as the change propagates; whether record-set
   responses expose it is not stated (unverified), so check the zone's state through the vendor's zone
   read if propagation confirmation is required.

## Patterns

- **Replace is all-or-nothing for the set.** Omitting a value from the submitted array removes it. To add
  one value to a multi-value set, read, append, then replace.
- **Create versus replace are different calls.** Create fails with 409 on an existing set, and replace fails
  with 404 on a missing one; neither acts as an upsert.
- **Mixing direct operations with change lists is risky.** A pending change list is tied to the zone
  version it started from and goes stale (409) once another version activates, so avoid direct edits
  while a change list is in flight.

## Known limitations

- Rate limits are not stated in the sources used: (unverified) on an HTTP 429, back off and honor any
  `Retry-After` header.
- Whether the 412 concurrency tag is mandatory or optional on these operations is not stated
  (unverified); send it when the client has one from a prior read.
- Delete is irreversible per the sources consulted; no restore procedure was found for a deleted set.
- Zone-apex SOA/NS handling is undocumented in the sources used (see step 3).

## Tools

| Operation | Description | Category |
|---|---|---|
| Get record set | Read one record set by zone, name and type | DNS Records |
| Create record set | Create a new record set | DNS Records |
| Replace record set | Replace an existing record set's TTL and values | DNS Records |
| Delete record set | Delete a record set and all its values | DNS Records |
| Get zone | Read the zone and its activation state (for existence and propagation checks) | DNS Zones |

## Verification checklist

- [ ] Zone confirmed to exist before any write
- [ ] CNAME exclusivity checked against the name's existing types
- [ ] Replace body carried the complete desired value array
- [ ] Delete confirmed with the operator before submission
- [ ] Record set read back and matched the intended state
