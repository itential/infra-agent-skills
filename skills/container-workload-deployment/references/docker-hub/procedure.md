# Docker Hub — Container Workload Deployment Procedure

Covers Docker Hub's own documented v2 REST API (base URL in `endpoints.md`) for authenticating, creating and
browsing repositories, and reading/listing image tags — the registry *metadata* side of getting an
image ready to deploy. Source: docs.docker.com "Docker Hub API" reference (`/reference/api/hub`),
retrieved 2026-09-29.

**Scope boundary with `docker-engine/procedure.md`: Docker Hub's own API does not move image bytes.**
The actual push/pull transfer is a separate, documented Docker Engine operation (pulling an image, or
pushing one — see `docker-engine/procedure.md`/`endpoints.md` for the literal calls), authenticated
with a credential obtained through this file's step 1. This file's job in a deployment workflow is:
authenticate, make sure the target repository exists, and afterward verify what tag actually landed —
not the transfer itself.

## Operational procedure

### 1. Authenticate

Obtain a bearer token before calling any other endpoint below. The currently recommended call is the
access-token endpoint, taking an `identifier` (a username for a password/personal-access-token login,
or an organization name for an organization access token) and a `secret` (the password, PAT, or OAT
itself). The returned `access_token` is a JWT, documented as expiring in 10 minutes — treat it as
short-lived and re-authenticate rather than caching it long-term. Use it as
`Authorization: Bearer <access_token>` on every subsequent call.

A separate, older login endpoint exists and is explicitly marked deprecated in favor of the one above
— don't build new automation against it. If the target account's organization enforces SSO, a plain
password is documented as not accepted at all; a personal access token is required instead.

### 2. Confirm or create the target repository

Before pushing a new image for the first time, check whether the repository already exists (read it
directly, or use the lightweight existence-check form of the same call) rather than assuming create is
safe to call blindly — repository creation isn't documented as idempotent. To create one, supply at
minimum a `name` (2–255 chars, lowercase alphanumeric plus `.`/`_`/`-`, no leading/trailing separator)
and the owning `namespace`; optionally a short `description` (documented max 100 chars), a longer
`full_description` (documented max 25000 chars), and `is_private` (defaults to public/`false` if
omitted — confirm this default is actually what's wanted before creating, since flipping a repository
from public to private later is a separate, more consequential change than setting it correctly at
creation).

### 3. Hand off the actual image transfer to Docker Engine

With a valid bearer token from step 1 (or the underlying username/password/PAT it was derived from,
depending on what the Engine call's `X-Registry-Auth` header expects — see `docker-engine/endpoints.md`
for its exact shape), perform the pull or push through the Docker Engine API. This is a deliberate
routing step, not a gap: Docker Hub's own documented API surface has no image-bytes endpoint to call
instead.

### 4. Verify what actually landed, by listing/reading tags

After a push (or before relying on a pull target), confirm via Docker Hub's own tag endpoints rather
than trusting the Engine-side push response alone — the two are separate systems and a push that the
daemon reports as complete is still worth confirming registry-side for anything automation-critical.
List tags for the repository, or read one specific tag by name, to get back its `full_size`
(compressed size across all layers), per-architecture `images[]` entries (each with `architecture`,
`os`, `digest`, `status` of `active`/`inactive`, `last_pushed`/`last_pulled`), and `tag_status`
(`active`/`inactive` — whether the tag has been pushed to or pulled from in roughly the past month,
per the source's own definition).

### 5. Tag or repository deletion — a confirmed gap, do not fabricate an endpoint

Docker Hub's currently published v2 API reference does not document a delete
operation for an individual tag, nor for a whole repository — only create/list/read operations appear
for both. No endpoint is invented here: if a caller needs to remove a tag or repository, there is no documented REST
endpoint in this file to do it with. The source's own "Resources" section points to a separate,
explicitly experimental Docker Hub CLI tool as the documented alternative — that tool is out of scope
for this API-driven procedure, and its use would need its own confirmation gate if pulled in later,
given deletion is inherently destructive (like any destructive step).

### 6. Handle documented errors

Docker Hub's error responses are a flat JSON object — `{"message": "...", "errinfo": null}` on the
generic error shape used across most endpoints (examples seen: `"bad request"`, `"unauthorized"`,
`"permission denied"`, `"not found"`, `"conflict"`, `"internal error"`), or a `{"detail": "..."}` shape
specifically on the login endpoints. Status codes: `400` malformed request (e.g. an invalid `ordering`
value on a list call), `401` unauthenticated/bad credentials, `403` forbidden (authenticated but not
permitted — note that a namespace list call is documented to silently omit private repositories rather
than erroring when the caller's token lacks the scope to see them, so a `200` with fewer results than
expected can itself be a permissions signal, not just a `403`), `404` not found (including requesting
a list page number beyond the available results), `429` rate limit exceeded (see Patterns), `500`
internal error.

## Patterns

- **Rate limiting is separate from Docker Hub's pull rate limiting.** This API's own limits are
  reported via `X-RateLimit-Limit`/`X-RateLimit-Remaining`/`X-RateLimit-Reset` response headers; a
  `429` response also carries a `Retry-After` header stating how many seconds to wait. The source is
  explicit that this is a different limit from the separate, better-known Docker Hub image-pull rate
  limit enforced when actually pulling image bytes (that limit lives on the Engine-side transfer in
  step 3, not on any call in this file).
- **List endpoints are paginated** (`page`, `page_size` query params, `page_size` capped at 100) with a
  standard `count`/`next`/`previous`/`results` envelope — always check `next` rather than assuming one
  page is the whole result set.

## Known limitations

- No documented delete-tag or delete-repository endpoint (step 5) — this is a real gap in Docker Hub's
  own published API, not an omission in this procedure.
- Does not perform the actual image byte transfer — see the scope-boundary note above and
  `docker-engine/procedure.md`.
- Organization/team administration, webhooks, and automated-build configuration are out of this
  procedure's scope even though some of those endpoints exist on the same API — this file covers only
  what's needed to authenticate, prepare a repository, and verify a tag as part of a deployment.

## Tools

Every operation maps to Docker Hub's v2 REST API — see `endpoints.md` for literal routes,
request/response fields, and status codes.

| Operation | Description | Category |
|---|---|---|
| Create access token | Authenticate and obtain a short-lived bearer JWT | Authentication |
| Create / List / Get repository | Prepare and inspect the target repository | Repository Management |
| List / Get repository tag | Verify what tag/digest is actually present after a push | Tag Management |
| Create / List / Get / Update / Delete personal access token | Manage longer-lived credentials used as the `secret` in authentication | Access Token Management |

## Verification checklist

- [ ] A fresh access token was obtained (not an expired one) before the call sequence, given the
      10-minute documented lifetime
- [ ] Repository existence was checked before create, rather than assuming create is safe to call blindly
- [ ] `is_private` was set deliberately on repository creation, not left to its public-by-default value
      unintentionally
- [ ] The actual image transfer was routed to Docker Engine's endpoints, not assumed to happen via this
      API
- [ ] Post-push verification used Docker Hub's own tag read, not just the Engine-side push response
- [ ] No delete-tag/-repository call was fabricated — the documented gap (step 5) was reported instead
