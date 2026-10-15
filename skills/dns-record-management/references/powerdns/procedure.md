# PowerDNS Authoritative Server — DNS Record Management Procedure

Create, update (including add/remove a single record without touching the rest of an RRset), and
delete DNS records in a PowerDNS Authoritative Server zone, via the PowerDNS HTTP API's Zones
resource. Covers RRset management within an existing zone — zone creation/deletion and DNSSEC
enablement are covered as prerequisites/adjacent operations, not this skill's primary focus (see Known
limitations for the full zone-lifecycle boundary). Assumes an authenticated HTTP API client against
the target PowerDNS Authoritative Server (an `X-API-Key` header value already available) is already
available to the calling agent.

## Operational procedure

### Common Sequences

**Create or fully replace a record (the common "set this record to these values" ask):**
1. Modify RRsets with `changetype: REPLACE` and the full desired `records` array — REPLACE
   overwrites the entire RRset for that name+type, not just adds to it.

**Add one record to an existing RRset without disturbing other records already there (e.g. add a
second MX host or a second A record, leaving existing ones intact):**
1. Modify RRsets with `changetype: EXTEND` and exactly one record — PowerDNS adds it to the RRset only
   if not already present, without touching other records in that RRset. **This is the documented,
   correct way to do an incremental add** — no read-then-append-then-resubmit cycle needed, unlike
   platforms without this primitive (see Patterns).

**Remove one record from an RRset without deleting the whole RRset:**
1. Modify RRsets with `changetype: PRUNE` and exactly one record — removes it from the RRset if
   present, leaving other records in that RRset untouched.

**Delete an entire RRset (all records of a given name+type):**
1. Modify RRsets with `changetype: DELETE` and an empty `records` array.

If a caller's ask doesn't match one of these shapes, use the individual capability sections directly.

### Modify RRsets (create/update/delete records)

A single call can carry multiple RRset operations in one `rrsets` array — each entry independently
specifies its own `changetype`, so a create, an extend, and a delete can all be submitted together
against the same zone in one request if the caller's task calls for it.

Each RRset entry requires: `name` (fully-qualified, trailing dot — e.g. `test.example.org.`), `type`
(e.g. `A`, `MX`, `TXT`), and `changetype` (`REPLACE`, `DELETE`, `EXTEND`, or `PRUNE`).

- **`REPLACE`**: requires `ttl` and the full `records` array (each record: `content`, `disabled`).
  Overwrites the entire RRset — any existing records for this name+type not included in this array are
  removed.
- **`DELETE`**: `records` must be empty, and `ttl` must **not** be included — the source is explicit
  both are documented constraints, not just conventions.
- **`EXTEND`**: exactly one record in `records`; adds it if not already present. Optional
  `write_unchanged` (boolean) controls whether a database write happens even when the record was
  already present (i.e. the operation was a no-op) — set this if the caller's downstream tooling needs
  to observe a write event even on a no-op extend.
- **`PRUNE`**: exactly one record in `records`; removes it if present. Same `write_unchanged` option as
  EXTEND.

Optional on any RRset entry: `comments` (array of `{content, account, modified_at}` — an audit trail
attached to the RRset itself, not the zone).

**Never send `serial` or `notified_serial` in the request body** — the source states plainly these
"MUST NOT be sent in client bodies." They're server-managed; PowerDNS increments the zone serial
automatically on a successful RRset change.

Confirm success: `204 No Content`. A validation failure (e.g. `records` non-empty on a `DELETE`, more
than one record on an `EXTEND`/`PRUNE`) returns an error body `{"error": "...", "errors": ["..."]}` —
report the actual error text, don't guess at the cause from the status code alone.

### Confirm before a destructive or overwriting change

If the operation is a `DELETE`, a `PRUNE` removing a record still in active use, or a `REPLACE`
against a name+type that already resolves in production, **stop and confirm with the operator before
proceeding** — this affects live DNS resolution, the same discipline this skill applies on every
platform. State the zone, RRset name/type, the operation, and (for REPLACE) the full set of values
being written, since REPLACE silently drops anything not included.

### Rectify a Zone (DNSSEC-enabled zones only)

DNSSEC-enabled zones need rectification after an RRset change for DNSSEC signing data to stay
consistent. Two paths: set `api_rectify: true` on the zone (at creation or update) so PowerDNS
rectifies automatically after each API-driven change, or call the rectify operation explicitly.
**The explicit rectify call fails on slave zones and on zones without DNSSEC enabled** — don't call it
reflexively after every change on every zone; confirm the zone is a DNSSEC-enabled primary/native zone
first, or rely on `api_rectify` instead of manual calls.

## Patterns

- **EXTEND/PRUNE solve the "add one record to a multi-value RRset" problem natively — no read-modify-
  write cycle required.** Other platforms in this skill (Azure DNS in particular) have no equivalent
  and must read the current record set, append/remove client-side, and resubmit the full array.
  PowerDNS's EXTEND/PRUNE changetypes do this server-side in one call — prefer them over a manual
  REPLACE-with-read-first cycle whenever the ask is "add/remove one value, leave the rest alone."
- **REPLACE is a full overwrite, not a merge.** Submitting a REPLACE with only the new value(s) silently
  drops every existing record for that name+type not included in the call — this is the same
  "don't build arrays with `$var` refs, build the full array explicitly" discipline that matters
  elsewhere; always confirm what the current RRset contains before REPLACE-ing it, unless the intent
  really is a full overwrite.
- **DNSSEC rectification is a real post-change requirement, not optional housekeeping, but only on
  DNSSEC zones.** Calling rectify on a non-DNSSEC or slave zone fails outright — check zone type/DNSSEC
  status before deciding whether this step applies at all.

## Known limitations

- Covers RRset create/update/delete within an existing zone (REPLACE/DELETE/EXTEND/PRUNE) and DNSSEC
  rectification — does not cover zone creation/deletion in depth (only referenced as a prerequisite),
  zone transfer/AXFR operations, NOTIFY, or metadata management beyond `api_rectify` and the DNSSEC-
  related metadata keys mentioned in Rectify a Zone.
- **A `REPLACE` against a name+type already resolving in production is hard to reverse** — PowerDNS
  keeps no undo for a completed RRset change; reversal means resubmitting the prior values, and only if
  they were captured beforehand. This is why the confirmation gate above exists.
- `EXTEND`/`PRUNE` accept exactly one record each — attempting to submit more than one in the same
  RRset entry is a validation error, not silently handled by processing only the first.
- The explicit rectify endpoint's slave-zone/non-DNSSEC failure is a hard constraint, not a warning —
  don't call it as a defensive "just in case" step on every zone.

## Tools

Every operation below maps to the PowerDNS Authoritative Server HTTP API — see `endpoints.md` for the
literal request/response shape.

| Operation | Description | Category |
|---|---|---|
| Modify RRsets (PATCH zone) | Create, replace, delete, extend, or prune one or more RRsets in one call | Record Management |
| Retrieve Zone | Read a zone's current RRsets and metadata | Record Management |
| Rectify Zone | Recompute DNSSEC ordering/signing data after a change (DNSSEC zones only) | DNSSEC |

## Verification checklist

- [ ] The correct `changetype` was chosen deliberately — REPLACE only when a full overwrite is
      actually intended, EXTEND/PRUNE for a single-record add/remove that must leave the rest of the
      RRset untouched
- [ ] Neither `serial` nor `notified_serial` was included in any request body
- [ ] DELETE operations carried an empty `records` array and omitted `ttl`; EXTEND/PRUNE carried
      exactly one record
- [ ] A destructive/overwriting change (DELETE, PRUNE of an in-use record, or REPLACE against a
      resolving name+type) was confirmed with the operator before submission
- [ ] Rectification was only attempted against a confirmed DNSSEC-enabled primary/native zone, or
      handled automatically via `api_rectify` instead of a manual call
