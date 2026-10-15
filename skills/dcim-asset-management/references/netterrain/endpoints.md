# Endpoints — NetTerrain WAPI v1 Device & Rack Provisioning

Literal wiring layer. `procedure.md` steps reference these by name; bind them to whatever REST
client/adapter is assumed available. Every path below is relative to a specific NetTerrain instance's
own base URL (e.g. `https://{your-netterrain-host}/wapi/v1/...` — the exact host, port, and any path
prefix are deployment-specific, not fixed).

Sources: Graphical Networks' "Getting Started with REST API" Part 1/2/3 blog series (see
`procedure.md` for full citations), cross-checked against a previously retrieved export of a
NetTerrain instance's own generated WAPI v1 OpenAPI/Swagger definition. Field names, required-field
sets, and response codes below are drawn from that Swagger definition unless noted otherwise; confirm
against the target instance's own live Swagger page, since local customization is possible.

## Authenticate

**Token exchange (required for any write call):**
```
POST /wapi/v1/token
```
Body carries the account's credentials; response includes an `access_token` value. Supply that value
on every subsequent write call as `Authorization: Bearer <access_token>`. This path is documented in
the vendor's blog series but was not present in the Swagger definition consulted (it appears to sit
outside the `/wapi/v1` resource surface that definition describes) — confirm the exact path/response
shape against the target instance.

**Basic auth (read-only, TLS only):** send `Authorization: Basic <base64 credentials>` — vendor
guidance restricts this to `GET` calls made over an encrypted connection; do not use it for
create/update/delete.

**Anti-forgery header (instance-dependent):** if the target instance's own Swagger definition lists a
request-verification header parameter on a write operation, that instance has anti-forgery checking
enabled server-side and the header must be populated with a current value obtained from that instance
(the value is session/instance-specific, never a fixed constant) — treat its presence in the Swagger
definition as the signal to look for, not something to hardcode from this file.

## Device types / rack types (prerequisite lookups)

```
GET /wapi/v1/device_types
GET /wapi/v1/device_types/{id}
GET /wapi/v1/rack_types
GET /wapi/v1/rack_types/{id}
```
List or filter to resolve an existing type record's `href` before creating a device or rack. No
create/update against these collections is in scope for this skill — they're a pre-managed library.

## Racks

```
GET    /wapi/v1/racks                 # list, supports page/per_page/offset, expand, show_child_collections, attribute filters
POST   /wapi/v1/racks                 # create
GET    /wapi/v1/racks/{id}            # read one
PUT    /wapi/v1/racks/{id}            # update
DELETE /wapi/v1/racks/{id}            # delete
```

**Create/update body fields:**
| Field | Required on create | Notes |
|---|---|---|
| `name` | Yes | Rack label |
| `rack_type` | Yes | `{ "href": "<existing rack_types/{id} URL>" }` |
| `base_node.parent_diagram` | Yes | `{ "href": "<existing nodes/{id} URL>" }` — parent location |
| `power` | No | Numeric total power capacity |
| `max_weight` | No | Numeric total weight capacity |
| `href` | Must be absent | Including one on a create body causes a conflict response |

Read-only rollup fields present in responses, never send on write: `power_used`, `weight_used`,
`available_rack_units`.

**Example create body (placeholder values):**
```json
{
  "name": "RACK-EXAMPLE-01",
  "rack_type": { "href": "{base}/wapi/v1/rack_types/1000000000001" },
  "base_node": { "parent_diagram": { "href": "{base}/wapi/v1/nodes/2000000000001" } },
  "power": 5000,
  "max_weight": 900
}
```

**Update body:** same shape, plus the target rack's own `href`; omit fields that aren't changing only
if the target instance's Swagger definition documents partial update — otherwise resend the full set.

**Status codes:** 201 create success; 200 read/update/delete success; 400 malformed/empty body; 404
not found; 409 create body included an `href`; 500 server-side create/update failure.

## Devices

```
GET    /wapi/v1/devices               # list, supports page/per_page/offset, expand, show_child_collections, attribute filters
POST   /wapi/v1/devices               # create
GET    /wapi/v1/devices/{id}          # read one
PUT    /wapi/v1/devices/{id}          # update (includes rack-unit mount/dismount)
DELETE /wapi/v1/devices/{id}          # delete
```

**Create body fields:**
| Field | Required on create | Notes |
|---|---|---|
| `name` | Yes | Device label |
| `device_type` | Yes | `{ "href": "<existing device_types/{id} URL>" }` |
| `parent_rack_container` | One of this or `base_node.parent_diagram` | `{ "href": "<rack container slot URL, e.g. racks/{rack_id}/containers/{slot_n}>" }` |
| `container_position` | With `parent_rack_container` | Numeric rack-unit offset within the rack |
| `base_node.parent_diagram` | One of this or `parent_rack_container` | `{ "href": "<existing nodes/{id} URL>" }` — unmounted placement |
| `peak_power` | No | Numeric |
| `weight` | No | Numeric |
| `status` | No | Free-text operational-state string |
| `href` | Must be absent | Including one on a create body causes a conflict response |

**Example create body — rack-mounted (placeholder values):**
```json
{
  "name": "SW-EXAMPLE-01",
  "device_type": { "href": "{base}/wapi/v1/device_types/1000000000002" },
  "parent_rack_container": { "href": "{base}/wapi/v1/racks/2000000000010/containers/12" },
  "container_position": 12,
  "peak_power": 150,
  "weight": 8,
  "status": "installed"
}
```

**Example create body — unmounted (placeholder values):**
```json
{
  "name": "SPARE-EXAMPLE-01",
  "device_type": { "href": "{base}/wapi/v1/device_types/1000000000002" },
  "base_node": { "parent_diagram": { "href": "{base}/wapi/v1/nodes/2000000000005" } },
  "status": "online"
}
```

**Update body — remount (placeholder values):**
```json
{
  "href": "{base}/wapi/v1/devices/2000000000099",
  "parent_rack_container": { "href": "{base}/wapi/v1/racks/2000000000010/containers/14" },
  "container_position": 14,
  "status": "online"
}
```

**Update body — dismount (placeholder value):**
```json
{
  "href": "{base}/wapi/v1/devices/2000000000099",
  "container_position": -1
}
```

**Status codes:** 201 create success; 200 read/update/delete success; 400 malformed/empty/missing
required field on create (e.g. neither placement supplied — this rejection was inferred from the
required-field description, exact error text not documented in the sources retrieved); 404 not found;
409 create body included an `href`; 500 server-side create/update failure.

## Collection controls (applies to both `/devices` and `/racks`)

| Parameter | Purpose |
|---|---|
| `page`, `per_page`, `offset` | Pagination |
| `expand` | `self` to inline collection items fully; `<child_resource_name>` to also inline a named child resource; `all_children` to inline every child resource recursively |
| `show_child_collections` | When true, unexpanded child collections include basic collection metadata instead of a bare href stub |
| `<attribute>=<value>` | Filter the collection to records matching that attribute, e.g. `?name=SW-EXAMPLE-01` |

List responses carry pagination metadata (`total_pages`, `items_count`, `total_items`), navigation
links (previous/next/first/last), and an items container holding the actual records.
