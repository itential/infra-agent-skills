# Endpoints — Micetro REST API v2 DNS Record Management

Wiring layer for the operations named in `procedure.md`. Sources (retrieved 2026-10-19): Micetro 25.1
documentation "Micetro REST API" (URL shape, reference format, filter/paging syntax, add/modify/delete
examples) and Micetro's REST API v2 OpenAPI definition (parameters and bodies), **verify against the
target server's own API documentation page**.

## Base URL and authentication

All calls go to `https://<micetro host>/mmws/api/v2/<resource>` (the product also serves plain HTTP,
which the definition marks as not recommended). Authentication options documented: a Micetro session ID
as a bearer token (the session is created through the API's sessions resource, whose request shape was
not read for this file — **unknown**), HTTP Basic with a Micetro user's login name and password, and
Windows NTLM or Kerberos. Keep credentials out of URLs and logs.

## References and conventions

- Object reference format: `<resource>/<number>` (for example `dnsZones/<number>`). A zone name with its
  trailing dot, or a record's own name, may stand in for the number where it is unambiguous.
- For complex objects the documentation recommends a JSON request body rather than query parameters.
- Add/modify examples in the documentation pass JSON in query parameters (`dnsRecord=`, `properties=`);
  the body form below follows the API definition.
- The error body (non-2xx) is JSON with `code` (integer) and `message` (string).

## Operations

| Operation | Request | Success |
|---|---|---|
| List zone records | `GET /dnsZones/{dnsZoneRef}/dnsRecords` | `200`; body has `dnsRecords` (list) and `totalResults` |
| Get record | `GET /dnsRecords/{dnsRecordRef}` | `200` |
| Add record | `POST /dnsZones/{dnsZoneRef}/dnsRecords` | `201`; body is `{"ref": "dnsRecords/<number>"}` |
| Set record properties | `PUT /dnsRecords/{dnsRecordRef}` | `204`, no body |
| Remove record | `DELETE /dnsRecords/{dnsRecordRef}` | `204`, no body |

A bulk-add call exists (`POST /dnsRecords`, body with a `dnsRecords` array and a `dnsZoneRef`) but is not
used by `procedure.md`; its per-record failure behavior is undocumented in the sources.

### List zone records — query options

| Option | Meaning |
|---|---|
| `filter` | Regex-style criteria, form `field=pattern` (documented example: `name=^test.example`) |
| `offset`, `limit` | Paging: first item is offset 0; limit is the page size |
| `sortBy`, `sortOrder` | Field to sort by; order (the documentation example uses `descending`) |
| `targetRef` | Return the page whose first item is that record (overrides `offset` when found) |
| `syncZone` | `true` synchronizes the zone from the DNS server before listing |
| `includeMetaRecords` | `true` also returns control directives and comment lines |
| `hideNonAccessibleHosts` | `true` hides records the caller cannot access |

### Add record — body

```json
{
  "dnsRecord": {
    "name": "<owner name>",
    "type": "<A|AAAA|CNAME|MX|TXT|PTR|SRV>",
    "data": "<value; space-separated for MX and SRV>",
    "ttl": "<optional, e.g. 3600>",
    "comment": "<optional, static zones only>",
    "enabled": true
  },
  "saveComment": "<optional>",
  "placeAfterRef": "<optional record ref>",
  "forceOverrideOfNamingConflictCheck": false
}
```

`dnsRecord.name`, `dnsRecord.type`, and `dnsRecord.data` are required. `dnsRecord.aging` (dynamic
records, AD-integrated zones only) and `dnsRecord.customProperties` exist but are outside this
procedure's scope. Leave `forceOverrideOfNamingConflictCheck` unset or `false` unless the operator
instructs otherwise.

### Set record properties — body

```json
{
  "properties": { "data": "<new value>" },
  "saveComment": "<optional>"
}
```

`properties` is a free-form key/value map. Only `data` is shown in the documented example; other record
fields (`ttl`, `comment`, `enabled`, `name`) are an **assumption** — verify before use. Leave
`deleteUnspecified` unset (default `false`); setting it to `true` clears every property not listed.

### Remove record — query options

| Option | Meaning |
|---|---|
| `saveComment` | Text recorded with the action |
| `forceRemoval` | Forces removal where possible — leave unset unless the operator explicitly asks |
| `objType` | Object type filter; not needed for a record `ref` |

## Record type names relevant here

`A`, `AAAA`, `CNAME`, `MX`, `TXT`, `PTR`, `SRV` (all in the API's record-type list). Read-only or
out-of-scope names in the same list include `ALIAS`, `DNSKEY`, `RRSIG`, `DS`, `SOA`, and `NS`.

## Errors

| Condition | Wire signal | Handling |
|---|---|---|
| Any failure | non-2xx status, JSON `{code, message}` | Surface `message` to the operator |
| Not found / duplicate / validation / permission | **Unknown** — specific statuses and messages not documented in the sources | Do not pattern-match on guessed strings; consult the target server's behavior |
