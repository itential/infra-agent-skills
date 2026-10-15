# Endpoint Wiring — Docker Hub Container Workload Deployment

Literal API calls behind each capability named in `docker-hub/procedure.md`. All calls are against
`https://hub.docker.com`, JSON request/response bodies. Source: docs.docker.com "Docker Hub API"
reference (`/reference/api/hub`), version `2-beta`, retrieved 2026-09-29.

## Authenticate — create an access token (current, recommended)

`POST /v2/auth/token`

No auth required to call this endpoint itself. Body:

```json
{"identifier": "myusername", "secret": "dckr_pat_..."}
```

`identifier` — a username (password or personal-access-token login) or an organization name
(organization access token login). `secret` — the corresponding password, PAT, or OAT.

Response `200`: `{"access_token": "<JWT>"}` — documented as expiring in 10 minutes. Use as
`Authorization: Bearer <access_token>` on subsequent calls. Response `401`: authentication failed.

## Authenticate — legacy login (deprecated, do not build new automation against it)

`POST /v2/users/login` — body `{"username", "password"}`, returns `{"token": "<JWT>"}` on `200`, or
`401` with `{"detail": "..."}` (plus an optional `login_2fa_token` if two-factor auth is enabled, to be
completed via `POST /v2/users/2fa-login`). The source explicitly marks this deprecated in favor of
`POST /v2/auth/token` above.

## Create a repository

`POST /v2/namespaces/{namespace}/repositories`

Auth: bearer token. Body:

| Field | Required | Notes |
|---|---|---|
| `name` | yes | 2–255 chars, lowercase alphanumeric plus `.`/`_`/`-` |
| `namespace` | yes | Owning namespace (user or organization) |
| `description` | no | Max 100 chars |
| `full_description` | no | Max 25000 chars |
| `registry` | no | e.g. `docker.io` |
| `is_private` | no | Defaults to `false` (public) |

Response `201`: full `repository_info` object (`name`, `namespace`, `repository_type`, `status`,
`is_private`, `is_automated`, `star_count`, `pull_count`, `last_updated`, `date_registered`,
`permissions` object with `read`/`write`/`admin` booleans, etc.). Errors: `400` bad request, `401`
unauthorized, `403` forbidden, `404` not found, `500` internal error.

## Read / list repositories

- `GET /v2/namespaces/{namespace}/repositories/{repository}` — one repository; same `repository_info`
  shape as create's response. Bearer token optional for a public repository. `401`/`403`/`404`/`500`.
- `HEAD /v2/namespaces/{namespace}/repositories/{repository}` — existence check only, no body.
- `GET /v2/namespaces/{namespace}/repositories` — list within a namespace. Query params: `page`
  (default 1), `page_size` (default 10, max 100), `name` (partial-match filter), `ordering` (one of
  `name`/`-name`/`last_updated`/`-last_updated`/`pull_count`/`-pull_count`). Response `200`:
  `{"count", "next", "previous", "results": [repository_info, ...]}`. Note: an organization-access-token
  caller without the `scope-repository-list` scope is documented to receive a normal `200` containing
  only public repositories, with no indication that private ones were withheld. Errors: `400` invalid
  `ordering` value, `401`, `403`, `404` (page number beyond available results).

## List repository tags

`GET /v2/namespaces/{namespace}/repositories/{repository}/tags`

Auth: bearer token (optional for a public repository). Query params: `page` (default 1), `page_size`
(default 10, max 100). Response `200`: paginated envelope (`count`/`next`/`previous`/`results`) of
`tag` objects (see field table below). Errors: `403` forbidden, `404` not found.

`HEAD` on the same path checks whether the repository has any tags at all (`200` vs `404`, no body).

## Read a single repository tag

`GET /v2/namespaces/{namespace}/repositories/{repository}/tags/{tag}`

Auth: bearer token (optional for a public repository). Response `200`: one `tag` object. Errors: `403`
forbidden, `404` not found.

`HEAD` on the same path checks whether that specific tag exists (`200` vs `404`, no body).

**No `DELETE` is documented on either the collection or single-tag path** — confirmed absent as of
this research (see `procedure.md` step 5).

## `tag` object field reference

| Field | Notes |
|---|---|
| `id` | Integer tag ID |
| `name` | Tag name, e.g. `latest` |
| `full_size` | Compressed size (sum of all layers) of the tagged image |
| `v2` | Whether the tag uses the Registry V2 format |
| `images[]` | One entry per platform variant — see below |
| `creator` / `last_updater` / `last_updater_username` | User IDs/username of who pushed/last updated |
| `last_updated` | ISO-8601 timestamp |
| `tag_last_pulled` / `tag_last_pushed` | ISO-8601 timestamp or `null` |
| `tag_status` | `active` \| `inactive` — whether pushed/pulled in roughly the past month |

Each `images[]` entry: `architecture`, `os`, `os_version`, `os_features`, `variant`, `features`,
`digest`, `size`, `status` (`active`\|`inactive`), `last_pulled`, `last_pushed`.

## Personal access tokens

- `POST /v2/access-tokens` — create. Body: `token_label` (required, 1–100 chars), `scopes` (required
  array — valid values `repo:admin`|`repo:write`|`repo:read`|`repo:public_read`), `expires_at`
  (optional ISO-8601; omitted means no expiration). Response `201`: `accessToken` object including
  `uuid`, `token` (shown in full only at creation), `token_label`, `scopes`, `created_at`,
  `expires_at`, `is_active`. Errors: `400`, `401`.
- `GET /v2/access-tokens` — list. Query params `page`/`page_size` (defaults 1/10). Response `200`:
  paginated envelope plus `active_count`. Errors: `400`, `401`.
- `GET /v2/access-tokens/{uuid}` — read one; `token` field is masked (`"***"`) on read. Errors: `401`,
  `404`.
- `PATCH /v2/access-tokens/{uuid}` — update `token_label` and/or `is_active`. Errors: `400`, `401`.
- `DELETE /v2/access-tokens/{uuid}` — permanent, documented as not reversible. Response `204`. Errors:
  `401`, `404`.

## Rate limiting (applies across this API's own endpoints)

Response headers on every call: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`
(unix timestamp). Exceeding the limit returns `429` with a `Retry-After` header (seconds to wait).
Explicitly documented as separate from Docker Hub's image-pull rate limiting, which applies to the
Engine-side transfer instead (see `docker-engine/endpoints.md`).

## Error response shape

Most endpoints: `{"message": "<string>", "errinfo": null}` — seen values include `"bad request"`,
`"unauthorized"`, `"permission denied"`, `"not found"`, `"conflict"`, `"internal error"`.

Login endpoints specifically: `{"detail": "<string>"}` (e.g. `"Incorrect authentication credentials"`),
with an optional `login_2fa_token` field when two-factor authentication must be completed next.
