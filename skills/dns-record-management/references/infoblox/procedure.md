# Infoblox NIOS — DNS Record Management Procedure (WAPI)

Create, read, update, or delete a DNS record in Infoblox NIOS — A, AAAA, CNAME, MX, TXT, and PTR —
through the NIOS Web API (WAPI). Every WAPI object (a DNS record included) is addressed by an opaque,
server-issued object reference (`_ref`) rather than by any caller-chosen key, so every write after the
first read/create in a sequence is anchored to that reference, not to the record's own name/value
fields. Assumes an authenticated WAPI client (HTTP Basic credentials for a NIOS administrator with DNS
record read/write permission on the target view) against a reachable Grid Master or Grid Master
Candidate is already available.

Source: Infoblox NIOS WAPI 9.x Reference Guide (Infoblox's own official WAPI reference document, hosted
at docs.infoblox.com) — the introduction, transport/authentication, object-reference model, and
GET/POST/PUT/DELETE method sections, retrieved 2026-09-29. Per-record-type field names (which fields
each record object exposes, and which of them are mandatory on creation) were cross-checked against
Infoblox's own generated WAPI object-schema documentation for WAPI version 2.13.7 (the same schema a
Grid Master itself serves per object type), read through a third-party-hosted mirror of that
generated output because the official PDF reference spreads its object pages across 800+ pages.
Both sources describe the same underlying generated WAPI schema rather than two independent opinions,
and nothing in the cross-check contradicted the official reference guide's own general method/object
model.

## Operational procedure

### 1. Know the addressing model before doing anything else

A record is never addressed by name+type+value once it exists — it is addressed by its `_ref`, a
string that encodes the object's WAPI type, an opaque internal identifier, and (for object types that
have one) a human-readable name component the server includes for convenience only. The server ignores
that trailing name component on input; only the opaque identifier portion matters. This means:

- **Create** returns a `_ref` — capture and keep it if the caller needs to read, update, or delete the
  record again without re-searching for it.
- **Read/update/delete** an existing record either by an already-known `_ref`, or by first searching
  (a filtered read) to obtain the `_ref`, then acting on that reference.
- Never construct a `_ref` by hand from a record's name/value fields — it is opaque and server-issued;
  guessing one is not a supported operation.

### 2. Build the record payload for the requested type

Assemble only the fields relevant to the record type being created or changed; unsupplied optional
fields keep the server's own defaults (view defaults to the Grid's default DNS view if omitted; TTL is
inherited from the zone unless explicitly overridden — see step 3).

- **A** — `name` (owner FQDN) and `ipv4addr` (the address) are mandatory; `view` selects the DNS view
  (defaults to the default view if omitted, and cannot be changed on an existing record — treat a view
  change as delete-then-recreate, see step 7).
- **AAAA** — `name` and `ipv6addr` are mandatory; `view` behaves the same as for A.
- **CNAME** — `name` (the alias) and `canonical` (the target FQDN the alias resolves through) are
  mandatory; `view` behaves the same as for A. Per RFC 1035 §3.6.2 (also enforced by NIOS itself), a
  name that already holds a CNAME cannot simultaneously hold any other record type, and vice versa —
  expect a rejection if a caller's name+view combination already has a conflicting record. See
  `SKILL.md`'s "Universal concepts" for the RFC-level statement of this rule.
- **MX** — `name` (the domain the mail is addressed to), `mail_exchanger` (the receiving mail server's
  FQDN), and `preference` (an integer 0–65535; lower value means higher priority) are all mandatory;
  `view` behaves the same as for A.
- **TXT** — `name` and `text` (the text payload) are mandatory; `view` behaves the same as for A. If the
  text payload itself needs to contain a quote character, follow NIOS's own quoting convention for the
  `text` field's contents rather than assuming no escaping is needed.
- **PTR** — `ptrdname` (the FQDN the pointer resolves to) is always mandatory. Exactly one of
  `ipv4addr` or `ipv6addr` is mandatory, matching whichever address family the reverse zone belongs to
  — never supply both. `name` is only meaningful (and only required) when the PTR record is being
  created in a forward-mapping zone; in the ordinary case of a PTR living in a reverse zone
  (`in-addr.arpa` for IPv4, `ip6.arpa` for IPv6), omit `name` and let the server derive the record's
  placement from the address itself. `view` behaves the same as for A.

Every type above also accepts, optionally: `ttl` (paired with a `use_ttl` boolean — see step 3),
`comment` (free-text, not used in resolution), and `disable` (boolean; a disabled record is retained
but not served in DNS responses).

### 3. TTL is opt-in per record, not just a value

Setting `ttl` alone is not sufficient — the record also carries a `use_ttl` flag, and only when that
flag is true does the record's own `ttl` value override the zone's inherited TTL. Supplying `ttl` in the
same create/update call implicitly sets `use_ttl` to true unless that same call also explicitly sets
`use_ttl` to false — so a plain "set TTL to N" request normally needs no separate `use_ttl` field, but a
caller intentionally reverting to zone-inherited TTL should send `use_ttl: false` explicitly (with or
without a stale `ttl` value, since it is ignored while `use_ttl` is false).

### 4. Search for a record (read, or the lookup step before update/delete)

Issue a filtered read against the record's WAPI object type (`record:a`, `record:aaaa`, `record:cname`,
`record:mx`, `record:txt`, or `record:ptr`) with one or more field=value conditions — typically `name`
plus `view`, and the type-specific value field (`ipv4addr`, `ipv6addr`, `canonical`, `mail_exchanger`,
`text`, or `ptrdname`) when narrowing to one exact record. Conditions are combined with AND; an exact
match is used unless a search modifier is applied (case-insensitive, negation, unanchored regex, or
`<`/`>` comparison — see `endpoints.md` for the modifier characters). A search with no matches returns
an empty result, not an error — report `NOT_FOUND` rather than treating it as a failure. Request only
the fields the caller actually needs via the return-fields option, to keep the response minimal; the
object's `_ref` is always included in the result regardless of which return fields were requested.

### 5. Create a record

Submit the payload from step 2 as a new object of the matching WAPI type. All fields the object type
requires must be present; anything not supplied takes the server's documented default. On success, the
newly created object's `_ref` is returned — capture it. If the caller needs to confirm the values the
server actually stored (some fields can be normalized or defaulted server-side), request specific
return fields on the same create call rather than issuing a separate read.

**If a record with an equivalent identity already exists** (same name/type/view, or in PTR's case the
same address+view), the server rejects the create as a data conflict — treat this as `ALREADY_EXISTS`
rather than a generic failure; do not retry the same create call unchanged. See `endpoints.md`'s error
section for what's confirmed about this response shape and what remains unconfirmed (an exact error
string is not documented in the sources).

### 6. Confirm before a destructive or already-live change

Before an update that changes a record already resolving in production, or before any delete, **stop
and confirm with the operator** — state the record's type, current values, the `_ref` being acted on,
and (for update) the new values being applied. This applies regardless of how the `_ref` was obtained
(directly supplied vs. found via step 4's search).

### 7. Update a record

Submit only the fields being changed, addressed by the record's `_ref` (from a prior create or from
step 4's search) — fields not included in the update request are left unchanged, with one documented
exception: a use-flag-paired field (see step 3) that is written without also specifying its use flag
will implicitly set that use flag to true. A record's `view` cannot be changed via update — if the
caller actually needs to move a record to a different view, treat it as delete-then-recreate (with the
confirmation gate from step 6 applying to the delete half). On success, the object's `_ref` is returned
again — it may differ from the `_ref` that was passed in if the update changed something the reference
itself encodes (e.g. the name component); use the returned `_ref` for any further operations on this
record, not the one that was passed in.

### 8. Delete a record

Submit a delete addressed by the record's `_ref` — no body is used or needed. On success, the deleted
object's `_ref` is returned as confirmation. This step always needs step 6's confirmation gate.

### 9. Handle documented error classes

- **400 (Bad Request)** — malformed request syntax, or a data conflict evaluated server-side (this is
  the class a duplicate-object create falls into, along with other validation failures such as an
  invalid CNAME/other-record-type collision). The response body is JSON regardless of what output
  format was requested, and always carries an `Error` field (a type plus an explanation), a symbolic
  `code`, and a `text` explanation — surface `text` to the operator rather than just the HTTP status.
- **404 (Not Found)** — only returned when addressing a specific object by `_ref` that no longer
  exists; a filtered search that matches nothing returns 200 with an empty result, not a 404 (see step
  4).
- **500 (Server Error)** — not caused by anything in the request; the source notes this class of error
  may be safely retried once, and if it persists it reflects an appliance-side condition worth
  escalating rather than something fixable by changing the request.

## Patterns

- **`_ref` is the unit of state, not the record's own fields.** Two calls that specify the exact same
  name/type/value can still refer to different underlying objects over time if one was deleted and
  recreated — re-resolve a `_ref` via search (step 4) rather than assuming a previously captured one is
  still valid, once a meaningful amount of time or intervening activity has passed.
- **Use-flag pairing (`ttl`/`use_ttl`) is a recurring shape** in NIOS objects generally, not unique to
  DNS records — treat any other field with a `use_<field>` counterpart the same way (writing the
  value field alone implicitly turns the flag on).
- **PTR is the one type here with a conditional required-field set** — `ptrdname` plus exactly one of
  `ipv4addr`/`ipv6addr` always; `name` only inside a forward-mapping zone. Every other type in this
  skill's scope has a fixed required-field set.

## Known limitations

- Scope is exactly six record types — A, AAAA, CNAME, MX, TXT, PTR. NS and DHCP Fixed Address handling
  are out of scope; WAPI supports them through the
  same general object model (`record:ns`, `fixedaddress`).
- View cannot be changed on an existing record via update (step 7) — only via delete-and-recreate,
  which is destructive and needs the confirmation gate from step 6.
- The exact wire-level string(s) NIOS uses to signal "object already exists" on a duplicate create are
  unverified in the sources (see step 5 and `endpoints.md`) — treat any 400
  response whose `text` field describes a conflicting/duplicate object as `ALREADY_EXISTS`, and verify
  the precise string against the target Grid Master's actual behavior before relying on string-matching
  it in an automated pipeline.
- Zone creation, view creation, and Grid/member-level DNS configuration are out of scope — this
  procedure assumes the target zone and view already exist.

## Tools

Every operation maps to the NIOS WAPI's generic GET/POST/PUT/DELETE methods against a record object
type or object reference — see `endpoints.md` for the literal request/response shape.

| Operation | Description | Category |
|---|---|---|
| Search/read `record:a`, `record:aaaa`, `record:cname`, `record:mx`, `record:txt`, `record:ptr` | Find a record by field conditions, or read one directly by `_ref` | DNS Records |
| Create `record:a`, `record:aaaa`, `record:cname`, `record:mx`, `record:txt`, `record:ptr` | Create a new record of the given type | DNS Records |
| Update by `_ref` | Change one or more fields on an existing record | DNS Records |
| Delete by `_ref` | Remove an existing record | DNS Records |

## Verification checklist

- [ ] Record type's mandatory fields were all supplied (see step 2's per-type list, including PTR's
      conditional `name` requirement)
- [ ] A `_ref` was captured from create, or resolved via search, before any read/update/delete
- [ ] `ttl` and `use_ttl` were set together deliberately, not left to an accidental implicit `use_ttl`
      flip (step 3)
- [ ] A view change was recognized as delete-then-recreate, not attempted as a plain update (step 7)
- [ ] Destructive/live-affecting update and every delete had operator confirmation before submission
      (step 6)
- [ ] A duplicate-object rejection on create was reported as `ALREADY_EXISTS`, not `FAILED`
- [ ] An empty search result was reported as `NOT_FOUND`, not treated as an error
