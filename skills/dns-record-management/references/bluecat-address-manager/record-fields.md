# Record Field Reference — BlueCat Address Manager Resource Record Object

Field list for the resource-record object accepted by Address Manager's v2 API `resourceRecords`
create/update calls, drawn from BlueCat's own RESTful v2 API guide's resource model.

## Common fields (every type)

| Field | Required | Notes |
|---|---|---|
| `name` | Yes | Record name, relative to the containing zone (not fully qualified). |
| `type` | Yes | One of the six subtypes below. Chosen at creation; no documented in-place change path (see `procedure.md` Patterns). |
| `ttl` | No | Seconds. Falls back to the zone/record default when omitted. |
| `absoluteName` | N/A | Server-computed, read-only; returned on read, never sent on create/update. |
| `id` | N/A | Server-assigned integer, read-only; used to address the record in later calls. |
| `userDefinedFields` | No | Free-form key/value metadata; presence and enforcement depend on the target instance's configured user-defined-field schema. |

## Per-type value field

| Type | Field | Notes |
|---|---|---|
| Host record | `addresses` | Array of one or more IP addresses (IPv4 and/or IPv6) the name resolves to. |
| CNAME record | `linkedRecordName` | The canonical target name this record points to. |
| Alias record | `linkedRecordName` | Same shape as CNAME; Address Manager models alias records as a distinct subtype rather than reusing the CNAME type directly. |
| MX record | `priority` + target | Mail-exchange target plus its numeric priority; both required together. |
| TXT record | `text` | Free-text value. |
| SRV record | `priority` + target | Service-locator target plus its numeric priority; both required together. |

## Record types confirmed available through `resourceRecords`

Host, CNAME, Alias, MX, TXT, SRV — these six are the set confirmed in the public v2 API guide's
resource model.

## Not confirmed through this endpoint

NS, PTR, SOA, and DNSSEC-related record types are not documented as available through the
`resourceRecords` collection in the sources. Address Manager's broader
object model manages some of these through other resource paths (e.g. zone-level SOA/NS settings tied
to the zone object itself rather than a standalone record). Treat a request for one of these as outside
this procedure's confirmed scope — check the target instance's own live Swagger documentation
(`http(s)://<host>/api/docs`) before assuming either way.

## Type immutability

No documented update path changes only a record's `type` field once created — see `procedure.md`'s
Patterns section for how this procedure treats a type-correction request.
