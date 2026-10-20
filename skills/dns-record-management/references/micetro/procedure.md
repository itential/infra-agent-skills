# Micetro — DNS Record Management Procedure (REST API v2)

Create, read, update, or delete a DNS record in Micetro (Men&Mice, now part of BlueCat) — A, AAAA, CNAME,
MX, TXT, PTR, and SRV — through the Micetro REST API, version 2. Micetro manages records inside a DNS
zone it already knows about; every record is addressed by a server-issued object reference (`ref`)
after creation, and a record's type and data travel as plain fields (type name, plus a single `data`
string), not as per-type objects. Assumes an authenticated REST client for a Micetro user with DNS
write permission on the target zone is already available; this skill does not create sessions or
credentials.

Sources (retrieved 2026-10-19):
- Micetro 25.1 documentation, "Micetro REST API" (docs.menandmice.com) — object references, URL
  addressing, filter/pagination syntax, the add/modify/delete examples.
- Micetro 25.1 documentation, "DNS Resource Records" — record-type immutability, supported types.
- Micetro 25.1 documentation, "AWS and Azure ALIAS records in Micetro" — read-only ALIAS type.
- Micetro 11.0 documentation, `mm_dnsrecord` Ansible module page — data format for multi-field types,
  static-zone-only comments, apex/relative naming.
- BlueCat blog, "Ultimate Guide to the Micetro REST API" — worked TXT create example and the 201
  success response (secondary; not a product manual).
- Micetro's REST API v2 OpenAPI definition (the document the product itself serves from its own
  API documentation page): request/response schemas and parameters. **Verify field names against the target server's own API documentation page
  before automating.**

The product documentation reads for this pass say little about validation behavior (naming conflicts,
apex handling, TTL inheritance, error strings). Those items are marked **unknown** below rather than
guessed.

## Common Sequences

- **Create a record:** resolve the zone (step 1) → look for an existing record (step 3) → build the
  payload (step 2) → create (step 4).
- **Change a record:** search for the record to obtain its `ref` (step 3) → confirmation gate (step 5)
  → update (step 6).
- **Remove a record:** search for the record to obtain its `ref` (step 3) → confirmation gate (step 5)
  → delete (step 7).
- **Change a record's type:** not an update — delete the old record and create a new one (step 2's
  type rule), with the step 5 gate applying to the delete.

## Operational procedure

### 1. Identify the zone and the addressing model

A zone is referenced either by its server-issued reference (`dnsZones/<number>`) or by its zone name,
which in Micetro always carries a trailing dot (for example `example.com.`) and may be used in place of
the numeric reference where it is unambiguous. Record names may be given partially qualified
(relative to the zone) or fully qualified. Records themselves are addressed by `dnsRecords/<number>`
references; the documentation also shows a record being addressed by its own name, but that form only
works when exactly one record has that name — **always act on the numeric `ref` obtained from a read**,
because a name can match several records (different types or data).

If the same zone name exists on more than one DNS server or view, the zone name alone may be ambiguous
— use the zone's `ref` (obtainable by listing zones) in that case. (Assumption: derived from the
documented "where unambiguous" wording; the exact ambiguity error is not documented in the sources
read.)

### 2. Build the record payload

A record carries these fields. `name`, `type`, and `data` are mandatory on creation:

- `name` — owner name, partial or fully qualified.
- `type` — one of the record type names Micetro accepts (this skill covers A, AAAA, CNAME, MX, TXT, PTR,
  SRV). **The type cannot be changed after the record is saved** — the product documentation says so
  explicitly, so a wrong type means delete-and-recreate.
- `data` — the record's value as one string. Types with several value fields (MX, SRV) use a
  space-separated list, in the standard RFC field order: MX is preference then mail host; SRV is
  priority, weight, port, then target host. Single-value types carry just the value: an address for
  A/AAAA, free text for TXT. For CNAME and PTR the value is the target name (Assumption: not spelled
  out in the sources read; consistent with the other types — confirm against the target server).
- `ttl` — optional, as a string. Micetro accepts shorthand durations (seconds, minutes, hours, days,
  weeks). **Unknown:** whether an omitted TTL inherits the zone default — the sources read do not say;
  supply `ttl` explicitly when the TTL matters.
- `comment` — optional free text. Only records in static zones can carry a comment.
- `enabled` — optional boolean; defaults to enabled. A disabled record is kept but not served.
- `aging` — optional; a non-zero value creates a dynamic record and is meaningful only in Active
  Directory-integrated zones. Leave unset for ordinary records.

Create-time options (outside the record itself): a save-comment string recorded with the action, a
placement reference to insert after an existing record, and a flag to override the naming-conflict
check **if that check is enabled in the server's system settings**. Do not set the override flag unless
the operator explicitly asks for it.

### 3. Search for a record (read, or lookup before update/delete)

List the records of the target zone, narrowing with the filter option (a regex-style `field=pattern`
expression, for example on `name`), then match type and data on the result to pick the exact record.
The result includes the record's `ref`, `name`, `type`, `ttl`, `data`, `comment`, `enabled`, and zone
reference, plus a total count. Use offset/limit to page through large zones. Two options matter:

- The listing normally reflects Micetro's own copy of the zone; an option to synchronize the zone from
  the DNS server first exists for cases where the server may have changed out-of-band.
- Control directives and comment lines are excluded unless explicitly requested — do not request them
  for ordinary record lookups.

An empty result is not an error — report `NOT_FOUND`. A record can also be read directly by its `ref`.

### 4. Create a record

Submit the payload from step 2 to the target zone. Success is a "created" response whose body carries
the new record's `ref` — capture it. Creating a second record with the same name and type but different
data is ordinary DNS (a multi-value record set); creating an exact duplicate, or a name that violates
the CNAME exclusivity rule (see `SKILL.md`), may be rejected. **Unknown:** the exact error text for
either case, and whether CNAME exclusivity is enforced at all — the documentation only shows an optional
naming-conflict check controlled by system settings. Treat any rejection whose message describes a
conflict or duplicate as `ALREADY_EXISTS`, and independently check before creating that no CNAME and no
other type already share the target name (a search on that name in step 3 covers this).

### 5. Confirm before a destructive or already-live change

Before any update that changes a record already resolving in production, and before every delete,
**stop and confirm with the operator**: state the record's name, type, current data, the `ref` being
acted on, and (for update) the new values. This applies however the `ref` was obtained. Deleting
a record is not reversible through the API; recreating it requires submitting the full payload again.

### 6. Update a record

Submit the changed values for the record's `ref` as a property set. The documented example changes the
record's `data`. (Assumption: other fields — `ttl`, `comment`, `enabled`, `name` — are accepted through
the same property set; the sources read show only `data`. Verify the others against the target server
before relying on them.) An option to clear properties not explicitly listed exists on the property-set
call — leave it unset, so unlisted fields stay as they are. Success is a "no content" response with no
body; confirm the change with a read (step 3) rather than expecting the new values in the response.

A record's type cannot be changed (step 2). The documentation for Micetro's Ansible modules adds that
multiple records sharing a name make in-place change ambiguous there and recommends add-then-remove; the
REST property-set call targets one `ref`, so this limitation applies to tooling that matches by name,
not to a `ref`-addressed update.

### 7. Delete a record

Submit a delete for the record's `ref`. Options exist to attach a save-comment to the action and to
force removal where the server would otherwise refuse; **do not use the force option** unless the
operator explicitly asks for it, since the sources read do not document what a refusal protects. Success
is a "no content" response; confirm with a search (step 3) that the record is gone. Always preceded by
step 5's confirmation.

### 8. Handle error responses

Failed calls return a non-2xx status with a JSON body carrying a numeric `code` and a text `message`
(per the API definition); surface `message` to the operator. **Unknown:** the specific status codes and
messages for not-found, duplicate, validation, permission, and unreachable-DNS-server failures — the
sources read list only the success codes. Do not retry a write unchanged after a conflict-style
rejection; for a server-side failure, consult platform-specific guidance rather than assuming a retry
is safe.

## Patterns

- **Numeric `ref` over names.** Name-addressing exists but is only safe when unique; searching first and
  acting on the `ref` removes the ambiguity (step 1).
- **Dynamic DNS zones.** Records written with a non-zero aging value are dynamic records in AD-integrated
  zones; ordinary automation should never set it, and should treat existing dynamic records as owned by
  the directory service.
- **Read-only types.** ALIAS records (synchronized from AWS and Azure) are read-only in Micetro, and the
  DNSSEC-generated types (such as DNSKEY and RRSIG) are listed as read-only too; none of them can be
  created or edited through this procedure.
- **Zone synchronization.** The listing normally reflects Micetro's view of the zone; if records may
  have been changed directly on the DNS server, use the synchronize option on the search (step 3)
  before concluding a record is absent.

## Known limitations

- Scope is A, AAAA, CNAME, MX, TXT, PTR, and SRV records. NS and SOA records, including at the zone
  apex, are not covered: Micetro lists them as ordinary record types, but the sources read give no apex
  rules, so they are left to platform-specific guidance. CAA and the other multi-field types are
  excluded because their field layouts were not confirmed.
- Zone creation, DNS server and view management, and DHCP/IPAM objects are out of scope; the zone must
  already exist. Micetro's DHCP and IPAM functions belong to other capabilities and are never merged
  into this directory.
- A record's type cannot be changed (step 2).
- Delete cannot be undone through the API (step 5).
- TTL inheritance, naming-conflict enforcement, apex behavior, and exact error strings are
  undocumented in the sources read (marked **unknown** above).
- Only the REST API v2 is covered, not Micetro's Management Console, command-line interface, or
  automation modules.

## Tools

| Operation | Description | Category |
|---|---|---|
| List zone records | Search a zone's records with a filter, paging, and optional sync | DNS Records |
| Get record | Read one record by `ref` | DNS Records |
| Add record | Create one record in a zone | DNS Records |
| Set record properties | Change fields of an existing record by `ref` | DNS Records |
| Remove record | Delete one record by `ref` | DNS Records |

## Verification checklist

- [ ] Zone identified (by `ref` where the name could be ambiguous) and record `name`, `type`, `data` all supplied
- [ ] Type was chosen deliberately — it cannot be edited afterward
- [ ] A search for the target name ran first, so no CNAME/other-type clash or exact duplicate was created
- [ ] `ttl` was set explicitly when it mattered (inheritance undocumented)
- [ ] The record's numeric `ref` was captured from create, or resolved by search, before update/delete
- [ ] Every delete, and every live-affecting update, had operator confirmation first; force and
      naming-conflict override options were left unset
- [ ] Outcome confirmed by a follow-up read, since update and delete return no body
- [ ] An empty search was reported `NOT_FOUND`, not an error
