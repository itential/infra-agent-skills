# Endpoints — Opsgenie incidents (REST API v1)

Literal wiring layer for `procedure.md`. Operation names in its Tools table map to the calls below.

Written against Atlassian's Opsgenie incident API reference and API rate-limiting page, retrieved 2026-10-19. Details not on those pages are marked as assumptions or as taken from the curated OpenAPI copy in the `itential/assets` repository (a secondary source). Values are placeholders.

## Base URL, headers, and authentication

Base URL: `https://api.opsgenie.com`. Accounts on the EU instance use `https://api.eu.opsgenie.com`; the reference states requests fail otherwise.

Headers:

- `Authorization: GenieKey <API_KEY>` (assumption: header name and scheme from the OpenAPI copy; the reference says only that a GenieKey is required).
- `Content-Type: application/json` on calls with a body.

Identifiers: every path takes `{identifier}`, which is the incident identifier by default or the tiny identifier when `identifierType=tiny` is added as a query parameter (`id` or `tiny`).

## Asynchronous writes and errors

Every write returns HTTP 202 with a request identifier. The incident is not changed until the request completes. Use get_request_status. Specific error codes and error strings for 400, 401, 403, 404, 422, and 429 were not on the pages read; report FAILED with the actual status and body.

## Rate limits

Incident calls use their own token-bucket domain. Limits depend on the plan and user count and are not published as fixed numbers. Response headers: `X-RateLimit-State` (`OK`, `BURST`, `THROTTLED`), `X-RateLimit-Reason` (`ACCOUNT` or `INTEGRATION`), `X-RateLimit-Period-In-Sec` (`60` or `1`). A throttled request gets HTTP 429; a burst request is delayed about five seconds. The documented backoff is waiting 2 to the power of the attempt count times 200 milliseconds between retries.

## find_incidents

```
GET /v1/incidents
```
Query parameters (documented): `query`, `offset` (default 0), `limit` (1 to 100, default 20), `sort` (`createdAt`, `insertedAt`, `updatedAt`, `status`, `priority`, `postmortemStatus`, `postmortemPublishDueDate`), `order` (`desc` or `asc`). Success: 200 with results and paging links.

## read_incident

```
GET /v1/incidents/{identifier}
```
Response fields of interest: `id`, `tinyId`, `message`, `status`, `priority`, `tags`, `responders`, `impactedServices`, `extraProperties`, `createdAt`, `updatedAt`, `impactStartDate`, `impactEndDate`. Success: 200.

## get_request_status

```
GET /v1/incidents/requests/{requestId}
```
Response fields: a success flag (`isSuccess`), `action` (for example create, resolve, delete), a descriptive `status` message, `incidentId` (empty on failure), `processedAt`, `integrationId`. Success: 200. The exact set of status messages was not read beyond examples.

## create_incident

```
POST /v1/incidents/create
```
Body: `message` (required, at most 130 characters). Optional: `description` (15000), `responders` (team or user objects), `tags` (20 by 50), `details` (8000 total), `priority` (`P1` to `P5`, default `P3`), `note` (25000), `impactedServices` (up to 20), `statusPageEntry`, `notifyStakeholders`. Success: 202 with a request identifier.

## add_note and list_notes

```
POST /v1/incidents/{identifier}/notes
GET  /v1/incidents/{identifier}/notes
```
Create body: `note` (required, 25000). Success: 202. List query: `offset`, `limit` (1 to 100, default 20), `direction`, `order`.

## add_responder

```
POST /v1/incidents/{identifier}/responders
```
Body: `responder` object with `type` (`team` or `user`) and an identifier (assumption: `id`, by analogy with the incident response shape); optional `note`. POST, PUT, and PATCH are all documented. Success: 202.

## Field updates

```
POST /v1/incidents/{identifier}/priority      body: priority
POST /v1/incidents/{identifier}/message       body: message
POST /v1/incidents/{identifier}/description   body: description (may be empty)
POST /v1/incidents/{identifier}/tags          body: tags, optional note
DELETE /v1/incidents/{identifier}/tags        query: tags (comma separated), optional note
POST /v1/incidents/{identifier}/details       body: details, optional note
DELETE /v1/incidents/{identifier}/details     query: keys (comma separated, at most 10), optional note
```
All return 202. Priority, description, and the other body calls also accept PUT and PATCH where the reference lists them.

## resolve_incident, close_incident, reopen_incident

```
POST /v1/incidents/{identifier}/resolve
POST /v1/incidents/{identifier}/close
POST /v1/incidents/{identifier}/reopen
```
Optional body `note` (25000). POST, PUT, and PATCH are all documented. Success: 202. No required starting state is documented.

## delete_incident

```
DELETE /v1/incidents/{identifier}
```
Success: 202.

## Not covered

- Associated alert and responder-alert lookups, and incident logs.
- Alerts, schedules, escalation policies, services, teams, integrations, post-incident reviews, and status pages.
