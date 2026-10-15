# Endpoint Wiring — Cloudflare DNS Zone Management

Literal API calls behind each capability named in `procedure.md`. All calls are the Cloudflare REST
API (Zones resource), JSON request/response bodies, authenticated with an API Token (`Authorization:
Bearer <token>`) or legacy email+key headers. Source: developers.cloudflare.com API reference,
retrieved 2026-09-17 via an LLM-mediated documentation fetch — treat exact field/error completeness as
provisional and re-check the live OpenAPI/reference page before relying on this as exhaustive (see
`procedure.md`'s Known limitations).

## Create a Zone

Tool hint: Create Zone (Zones resource, create operation).

Literal route: `POST /zones`

Body fields:

| Field | Required | Notes |
|---|---|---|
| `name` | yes | Domain name; standard DNS length limits (253 chars overall, 63 per label). |
| `account.id` | no | Which Cloudflare account owns the zone, if the caller has more than one. |
| `type` | no | One of `full`, `partial`, `secondary`, `internal`. Defaults to `full` if omitted. |

Response: envelope `{success, result, errors[], messages[]}`. `result` (the zone object) includes at
least: `id`, `name`, `status` (`initializing` \| `pending` \| `active` \| `moved`), `name_servers[]`
(Cloudflare-assigned), `original_name_servers[]` (populated once/if Cloudflare detects the domain's
prior nameservers), `created_on`, `activated_on`, `account`, `owner`, `type`.

Errors: general `errors[]` entries in the standard envelope shape (`code` numeric ≥1000, `message`,
optional `documentation_url`, optional `source.pointer`) — no zone-specific error codes were confirmed
as part of this research; report the literal code/message returned rather than mapping it to an
assumed category.

## Read a Zone

Tool hint: Read/Get Zone Details (Zones resource, get-by-id operation).

Literal route: `GET /zones/{zone_id}`

Path parameter: `zone_id` (max 32 chars).

Response: envelope as above; `result` is the same zone object shape as Create.

## Delete a Zone

Tool hint: Delete Zone (Zones resource, delete operation).

Literal route: `DELETE /zones/{zone_id}`

Path parameter: `zone_id` (max 32 chars). Requires Zone Write permission on the token (or legacy
email+key credentials with equivalent access).

Response: envelope `{success, result: {id}, errors[], messages[]}` — `result.id` echoes the deleted
zone's ID.

No documented pre-delete constraint (e.g. requiring the zone to be record-empty first) was confirmed
during this research — see `procedure.md`'s Known limitations.

## Field reference (zone-level fields only)

| Field | Location | Notes |
|---|---|---|
| `name` | Create request | The domain name being onboarded. |
| `account.id` | Create request | Optional; disambiguates which account owns the zone. |
| `type` | Create request, response | `full` \| `partial` \| `secondary` \| `internal`; defaults to `full`. |
| `id` | Response | Zone identifier, max 32 chars, used as `{zone_id}` in read/delete. |
| `status` | Response | `initializing` \| `pending` \| `active` \| `moved`. |
| `name_servers` | Response | Cloudflare-assigned authoritative name servers for the zone. |
| `original_name_servers` | Response | The domain's name servers prior to onboarding, if detected. |
| `created_on` / `activated_on` | Response | Timestamps. |
