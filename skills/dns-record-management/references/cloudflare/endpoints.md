# Endpoints — Cloudflare DNS Record Creation

Literal wiring layer. `SKILL.md` steps reference these by name; bind them to whatever REST client/
adapter is assumed available (see `requires_tool`/`assumed_tool` in `SKILL.md` frontmatter).

## Find the target zone

No separate "look up zone" call is described on the create-records how-to page itself. In practice this
is `GET /zones?name={zone_name}` against the Cloudflare API (or the dashboard's own zone list) to
resolve a zone name to its `zone_id`, which the create call requires as a path parameter. Not verbatim
from the primary how-to source — standard Cloudflare API usage, confirm `zone_id` resolution against the
target account before scripting.

## Create DNS Record

**Method/path (verbatim from the Cloudflare API reference):**

```
POST /zones/{zone_id}/dns_records
```

**Request body fields — core (all types):**
- `type` (required) — record type, e.g. `A`, `AAAA`, `CNAME`, `MX`, `TXT`, `NS`, `SRV`, `CAA`, `PTR`.
- `name` (required) — complete DNS record name including the zone name, in Punycode.
- `ttl` (optional) — integer seconds, `1` = automatic ("Auto"). See `references/record-fields.md` for
  the full allowed range and the proxied-record TTL lock.
- `proxied` (optional, boolean) — only meaningful for `A`, `AAAA`, `CNAME`. See
  `references/record-fields.md` for the proxied/DNS-only semantics.
- `comment` (optional) — reference-only string, plan-dependent max length.
- `tags` (optional) — reference-only array, Pro/Business/Enterprise only.

**Request body fields — per record type:** see `references/record-fields.md` for the full
type-by-type breakdown (`content` vs `data` object, which fields are required per type).

**Success:** HTTP 2xx with response body `{"success": true, "result": {<created record object>}, ...}`.
Treat `success: true` with a `result` object containing an `id` as the pass criterion.

**Failure:** `{"success": false, "errors": [...]}`. The sources retrieved for this skill do not document
exact error strings/codes for common failure modes (duplicate record, invalid `content` for the given
`type`, name/type collision). Do not fabricate a specific error string — surface the tool's actual
`errors` array verbatim.

**Documented structural constraints (not per-call errors, but will cause a create call to fail):**
- "A/AAAA records cannot exist on the same name as CNAME records."
- "NS records cannot exist on the same name as any other record type."
- `CNAME` `content` must differ from the record's own `name` (Cloudflare rejects a CNAME pointing to
  itself).
- Cloudflare "may prevent proxying certain CNAME records to avoid misconfigurations" — exact validation
  rule/error text not given in the sources retrieved.
- `A`/`AAAA` `content` cannot be a Cloudflare-owned IP address (documented as a content restriction, not
  as a named error).

**Authentication/authorization:** Cloudflare API token (Bearer) scoped with Zone-level DNS write access.
Dashboard convention for this scope is commonly labeled "Zone → DNS → Edit" in the token-creation UI —
this label was not independently confirmed; confirm against the target account's own "List permission
groups" API response or token-creation screen if precision matters.

## Confirm Record Created

No separate "confirm" call is documented beyond the create call's own response. If the calling tool
needs a separate confirmation read: `GET /zones/{zone_id}/dns_records?type={type}&name={name}` filtered
to the created record, or `GET /zones/{zone_id}/dns_records/{id}` using the `id` returned by the create
call.

## Dashboard equivalent (for context — this skill targets the API, not manual dashboard clicks)

1. Go to the zone's **DNS Records** page.
2. Select **Add record**.
3. Choose a record **Type**.
4. Complete the required fields (vary per record type — see `references/record-fields.md`).
5. Select **Save**.
