# Endpoints — BlueCat Address Manager DNS Record Creation

Literal wiring layer. `procedure.md` steps reference these by name; bind them to whatever REST client/
adapter is assumed available.

Base path: Address Manager's RESTful v2 API is rooted at `/api/v2` on the appliance
(`https://<address-manager-host>:<port>/api/v2/...`). The interactive Swagger UI for the exact
version running on a given appliance lives at `http(s)://<host>/api/docs` — treat that as the
authoritative field/response reference for the live instance; this file reflects BlueCat's publicly
published v2 API guide.

## Authentication

BlueCat's own v2 API guide states the RESTful v2 API accepts both the Basic and Bearer HTTP
authentication schemes. The guide does not specify which credential (login password vs. a
separately-issued API token) each scheme expects — confirm against the target instance's own
`/api/docs` Swagger UI before hardcoding a scheme or credential shape.

## Find the target zone

```
GET /api/v2/zones?filter=name:eq('<zone-name>')
```

Returns the matching zone object(s), including the zone's `id`, which subsequent calls need. If no
match, report the zone as not found (see `procedure.md` step 1).

## Create a resource record

```
POST /api/v2/zones/{id}/resourceRecords
```

`{id}` is the target zone's object ID from the lookup above. Request body is a single resource-record
object; the required/optional fields differ by chosen `type` — see `record-fields.md`.

**Success:** HTTP 201, body is the created resource-record object including its newly assigned integer
`id`.

**Documented failure responses:**
- 400 — malformed request (body content violates the schema/validation rules for the chosen type)
- 401 — authentication failed
- 404 — the parent zone ID does not resolve to an existing zone

The response body for 400/401/404 is a generic error object; the guide does not enumerate specific
error-message text per validation failure — surface whatever the instance actually returns rather than
guessing at a message.

## Read a resource record back

```
GET /api/v2/resourceRecords/{id}
```

Use the `id` returned from the create call. Alternatively, list a zone's records and filter by name and
type:

```
GET /api/v2/zones/{id}/resourceRecords?filter=name:eq('<record-name>')
```

## Update a resource record

```
PUT /api/v2/resourceRecords/{id}
```

Full-object replace, same schema as create. No separate endpoint or field is documented in the sources
reviewed for changing only the `type` of an existing record in place — see `procedure.md`'s Patterns
section for how to treat a type-correction request.

## Delete a resource record

```
DELETE /api/v2/resourceRecords/{id}
```

**Success:** HTTP 204, empty body. This is a destructive, hard-to-reverse action — get explicit
operator confirmation before issuing this call, the same as any delete on a live DNS zone.
