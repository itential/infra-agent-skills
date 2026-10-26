# Endpoints — Infoblox NIOS WAPI DNS Record Management

Literal wiring layer for each capability named in `procedure.md`. General URL shape, method semantics,
search-modifier characters, and error-body shape are drawn from Infoblox's own official WAPI 9.x
Reference Guide (docs.infoblox.com), retrieved 2026-09-29. Per-type required/optional field names were
cross-checked against Infoblox's own generated WAPI object-schema output for WAPI version 2.13.7 (see
`procedure.md`'s source note for how that cross-check was done and why it's flagged separately).

## Base URL and versioning

All calls are `https://<Grid Master host>/wapi/v<major>.<minor>/<path>` — the version segment (e.g.
`v2.13`) pins the WAPI protocol version, which is versioned independently of the NIOS release itself.
Confirm the actual supported version against the target Grid Master rather than assuming one; a client
using an older major.minor than the Grid Master supports still behaves correctly (the server preserves
older-version behavior), but mixing versions across calls in the same session is not supported.

## Authentication

HTTP Basic authentication (NIOS administrator username/password) on every request, or certificate-based
authentication. For repeated calls in the same session, the session cookie (`ibapauth`) returned after
the first authenticated call may be reused instead of resending Basic credentials each time; invalidate
it with `POST /wapi/v<version>/logout` when the session is done.

## Object reference (`_ref`) model

Every create/read/update/delete response includes (or, for update/delete, directly returns) a `_ref`
string for the object — an opaque, server-generated identifier plus WAPI type, optionally followed by a
human-readable name component the server appends for convenience only. Treat the whole string as opaque
input for later calls; do not parse or reconstruct it.

## Search modifiers (GET/search only)

Appended directly to a field name in a query condition (`field<modifier>=value`):

| Modifier | Meaning |
|---|---|
| `!` | Negates the condition |
| `:` | Case-insensitive string match |
| `~` | Regular-expression match (unanchored) |
| `<` | Less-than-or-equal comparison |
| `>` | Greater-than-or-equal comparison |

Only one of `<`, `>`, or `~` may be used in a single condition. No modifier means an exact match.
Multiple field conditions in one request are combined with AND.

## Return fields and pagination (GET/search only)

- `_return_fields=<comma-separated field list>` — return exactly these fields (plus `_ref`, always
  included) instead of the object type's default field set.
- `_return_fields+=<comma-separated field list>` — return these fields in addition to the default set.
- `_max_results=<N>` — cap the number of objects returned; if omitted, the server errors if the match
  count would exceed 1000 objects (equivalent to an implicit `_max_results=-1000`; a negative value
  means "error if more than |N| results," a positive value means "silently truncate to N").
- `_paging=1` (with `_max_results` also set) starts a paged search; the response includes
  `next_page_id` when more pages remain — pass that value back as `_page_id` on the next request against
  the same search to continue.

## A Record

- **Search** — `GET /wapi/v<version>/record:a?name=<owner_fqdn>&view=<dns_view>&_return_fields=name,ipv4addr,view`
- **Create** — `POST /wapi/v<version>/record:a`
  Body (JSON, default content type): `{"name": "<owner_fqdn>", "ipv4addr": "<ipv4_address>", "view": "<dns_view>"}`
  Optional: `ttl` (integer seconds), `use_ttl` (boolean), `comment` (string), `disable` (boolean).
- **Read by reference** — `GET /wapi/v<version>/<_ref>`
- **Update** — `PUT /wapi/v<version>/<_ref>` with a body containing only the fields to change.
- **Delete** — `DELETE /wapi/v<version>/<_ref>` (no body).

## AAAA Record

- **Search** — `GET /wapi/v<version>/record:aaaa?name=<owner_fqdn>&view=<dns_view>&_return_fields=name,ipv6addr,view`
- **Create** — `POST /wapi/v<version>/record:aaaa`
  Body: `{"name": "<owner_fqdn>", "ipv6addr": "<ipv6_address>", "view": "<dns_view>"}`
  Optional fields same set as A (`ttl`, `use_ttl`, `comment`, `disable`).
- **Read/Update/Delete** — same `_ref`-addressed pattern as A.

## CNAME Record

- **Search** — `GET /wapi/v<version>/record:cname?name=<alias_fqdn>&view=<dns_view>&_return_fields=name,canonical,view`
- **Create** — `POST /wapi/v<version>/record:cname`
  Body: `{"name": "<alias_fqdn>", "canonical": "<target_fqdn>", "view": "<dns_view>"}`
  Optional: `ttl`, `use_ttl`, `comment`, `disable`.
- **Read/Update/Delete** — same `_ref`-addressed pattern as A.

## MX Record

- **Search** — `GET /wapi/v<version>/record:mx?name=<domain_fqdn>&view=<dns_view>&_return_fields=name,mail_exchanger,preference,view`
- **Create** — `POST /wapi/v<version>/record:mx`
  Body: `{"name": "<domain_fqdn>", "mail_exchanger": "<mail_server_fqdn>", "preference": <0-65535>, "view": "<dns_view>"}`
  Optional: `ttl`, `use_ttl`, `comment`, `disable`.
- **Read/Update/Delete** — same `_ref`-addressed pattern as A.

## TXT Record

- **Search** — `GET /wapi/v<version>/record:txt?name=<owner_fqdn>&view=<dns_view>&_return_fields=name,text,view`
- **Create** — `POST /wapi/v<version>/record:txt`
  Body: `{"name": "<owner_fqdn>", "text": "<text_payload>", "view": "<dns_view>"}`
  Optional: `ttl`, `use_ttl`, `comment`, `disable`.
- **Read/Update/Delete** — same `_ref`-addressed pattern as A.

## PTR Record

- **Search (IPv4)** — `GET /wapi/v<version>/record:ptr?ipv4addr=<ipv4_address>&view=<dns_view>&_return_fields=ptrdname,ipv4addr,view`
- **Search (IPv6)** — `GET /wapi/v<version>/record:ptr?ipv6addr=<ipv6_address>&view=<dns_view>&_return_fields=ptrdname,ipv6addr,view`
- **Create (reverse zone, ordinary case)** — `POST /wapi/v<version>/record:ptr`
  Body (IPv4): `{"ptrdname": "<target_fqdn>", "ipv4addr": "<ipv4_address>", "view": "<dns_view>"}`
  Body (IPv6): `{"ptrdname": "<target_fqdn>", "ipv6addr": "<ipv6_address>", "view": "<dns_view>"}`
  Supply exactly one of `ipv4addr`/`ipv6addr`, never both.
- **Create (forward-mapping zone only)** — same body plus `name`, per `procedure.md` step 2.
  Optional in all cases: `ttl`, `use_ttl`, `comment`, `disable`.
- **Read/Update/Delete** — same `_ref`-addressed pattern as A.

## Method return shapes

- **POST (create)**: `201` on success. Returns the created object's `_ref` as a bare string by default.
  Passing `_return_fields`/`_return_fields+` on the same call returns the full object (with those
  fields) instead of just the reference string.
- **PUT (update)**: `200` on success. Returns the (possibly changed) `_ref` as a bare string, or the
  full object if `_return_fields`/`_return_fields+` was supplied.
- **DELETE**: `200` on success. Returns the deleted object's `_ref` as a bare string. No request body is
  used; there are no DELETE-specific query options for these record types.
- **GET (search by objtype)**: `200` with a JSON list (empty list if no matches — this is not an error).
- **GET (read by `_ref`)**: `200` with the single object, or `404` if that reference no longer exists.

## Error handling

All errors return HTTP status `400` or higher, with a JSON body regardless of the requested output
format. The body always includes:

| Field | Meaning |
|---|---|
| `Error` | Error type, followed by an explanation after a colon |
| `code` | A symbolic error code |
| `text` | A plain-language explanation of the error |
| `trace` | Debug trace, only present if server-side debugging is enabled |

Status-code classes:

- **400** — malformed request syntax, or a data-conflict/validation failure evaluated server-side. A
  duplicate-object create (same identity already exists) falls in this class; so does an illegal
  CNAME/other-record-type collision at the same name. **The exact `code`/`text` string NIOS uses
  specifically for "object already exists" was not confirmed against the sources** —
  pattern-match on the `text` field describing a conflicting/duplicate object as a heuristic, and verify
  the precise string against the target Grid Master before relying on it in an automated pipeline (see
  `procedure.md`'s Known limitations).
- **404** — the object referenced by a direct `_ref` GET no longer exists. Does not apply to a
  zero-match search by object type, which returns `200` with an empty list.
- **500** — server-side error unrelated to the request content; safe to retry once per the source's own
  guidance, but a persistent 500 indicates an appliance-side condition to escalate rather than a
  request to keep modifying.
