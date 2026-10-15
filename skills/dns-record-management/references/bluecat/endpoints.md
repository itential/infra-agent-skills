# Endpoints — BlueCat Horizon / DDI Orchestrator DNS Record Creation

Literal wiring layer. `SKILL.md` steps reference these by name; bind them to whatever REST client/
adapter is assumed available (see `requires_tool`/`assumed_tool` in `SKILL.md` frontmatter).

## Find the target zone

No single documented "get zone" call was found in the sources retrieved. In practice this is a GET
against the zone collection/reference for the target DNS configuration, filtered by zone name — verify
the exact path against the target instance's own live API doc at `http(s)://<host>/mmws/api/doc`
(Horizon: Administration → API documentation in-product).

## Create DNS Record

**Method/path (verbatim example from the Micetro REST API guide, DDI Orchestrator's underlying
engine):**

```
POST http(s)://<micetro.yourdomain.tld>/mmws/api/dnsZones/{zoneRef}/dnsRecords?dnsRecord={"name":"name","type":"A","data":"1.2.3.4"}
```

The guide recommends putting the object in the request body rather than the query string for anything
beyond the simplest case: `POST /mmws/api/dnsZones/{zoneRef}/dnsRecords` with the `dnsRecord` object as
the JSON body.

`{zoneRef}` is the target zone's reference/name (e.g. `test.menandmice.com.` — note the trailing dot in
the guide's own example).

**Request body fields** (`dnsRecord` object — see `references/record-fields.md` for full field notes):
- `name` (required) — record name, partial or fully qualified
- `type` (required) — one of the 35 supported record types minus the read-only set (see SKILL.md)
- `data` (required) — record data; space-separated list for MX, SRV, NAPTR, CAA, CERT, HINFO, TLSA
- `ttl` (optional) — seconds, or shorthand `1s`/`1m`/`1h`/`1d`/`1w`
- `comment` (optional) — static zones only
- `enabled` (optional) — boolean, defaults to enabled
- `aging` (optional) — AD-integrated dynamic zones only; hours since 1601-01-01 UTC, non-zero marks the
  record dynamic

**Success:** HTTP 2xx with the created `dnsRecord` object (including its assigned reference) in the
response body. Exact status code (200 vs 201) and full response schema are not stated in the sources
retrieved — confirm against the target instance's live API doc.

**Authentication:** Bearer token (JWT, per Horizon's "Obtaining JSON Web Tokens for authentication"),
or `loginName`/`password`/`session` query arguments, or NTLM/Kerberos — per the Micetro REST API guide.

**Documented error conditions:**
- Wrong record type selected at creation time is **not recoverable by editing** — the UI guide states
  verbatim: "If you save a new DNS record with the wrong type, you cannot change the type later. You
  must delete the record and create a new one with the correct type." Treat any "change record type"
  request as: delete + recreate, never an update call.
- No exact duplicate-record or validation-error response body/status code is given in the sources
  retrieved. This is a genuine gap — do not fabricate a specific error string; if the create call
  fails, surface the tool's actual error response verbatim rather than pattern-matching against an
  invented one.

## Confirm Record Created

No explicit "confirm" step is documented beyond the create call's own response returning the created
object. Read back the record (GET on the same `dnsRecords` collection, filtered by `name`/`type`) if
the calling tool needs a separate confirmation read rather than trusting the create response.
