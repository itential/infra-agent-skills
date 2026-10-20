# Endpoints — PagerDuty incidents (REST API v2)

Literal wiring layer for `procedure.md`. Operation names in its Tools table map to the calls below.

Written against PagerDuty's developer API reference for the incidents resources and its REST rate-limit page, retrieved 2026-10-19. Where a detail was not on a retrieved page it is marked as an assumption or as taken from a copy of PagerDuty's OpenAPI description. Values are placeholders.

## Base URL, headers, and authentication

Base URL: `https://api.pagerduty.com` (assumption: the global service host, as published in PagerDuty's OpenAPI description; accounts in other regions may use a different host, which was not checked).

Headers:

- `Authorization: Token token=<API_KEY>` (API key). Scoped OAuth is an alternative; incident writes need the `incidents.write` scope.
- `Accept: application/vnd.pagerduty+json;version=2` (the documented default versioning header).
- `Content-Type: application/json` on calls with a body.
- `From: <email of a valid account user>`. Documented as required on the write calls below (create, update, notes, snooze, merge).

## Rate limits and errors

Default limit: 960 requests per minute (per account key, per user, and per app token). An exceeded limit gives HTTP 429 with the message `Rate Limit Exceeded` and code `2020`. The response headers `ratelimit-limit`, `ratelimit-remaining`, and `ratelimit-reset` (seconds until reset) report the state; wait for the reset value before retrying. Other documented statuses: 400 (bad request), 401 (authentication failure), 403 (insufficient permission), 404 (not found), and 402 on the incident list. Error body strings other than the rate-limit one were not read; report FAILED with the actual status and body.

## find_incidents

```
GET /incidents
```
Query parameters (documented): `statuses[]` (`triggered`, `acknowledged`, `resolved`), `incident_key`, `service_ids[]`, `team_ids[]`, `user_ids[]`, `urgencies[]` (`high`, `low`; requires the account's urgency feature), `since` and `until` (window of at most six months, default one month), `date_range=all` (ignore the window defaults), `sort_by` (up to two of `incident_number`, `created_at`, `resolved_at`, `urgency`, each with a direction), `limit` (at most 100), `offset`, `total=true` (fill the total, off by default). With `user_ids[]`, only triggered and acknowledged incidents are returned. Success: 200.

## read_incident

```
GET /incidents/{id}
```
`{id}` is the incident identifier; the documentation says the incident number is also accepted. Response fields of interest: `status`, `incident_number`, `html_url`, `urgency`, `assignments`, `acknowledgements`, `resolve_reason` (null when unresolved), `last_status_change_at`. Success: 200.

## create_incident

```
POST /incidents
```
Body, wrapped in an `incident` object (assumption: the wrapper, as in PagerDuty's examples and OpenAPI description):

```json
{
  "incident": {
    "type": "incident",
    "title": "<summary>",
    "service": { "id": "<service id>", "type": "service_reference" },
    "urgency": "high",
    "incident_key": "<dedup key>",
    "body": { "type": "incident_body", "details": "<details>" }
  }
}
```
Required: `type`, `title`, `service`. Optional: `priority` (`{ "id", "type": "priority_reference" }`), `urgency`, `incident_key`, `body`, `incident_type` (object with a `name`), `escalation_policy` (reference), `assignments`. Success: 201 with the incident. The documented rate limits for this operation may be stricter than the default; read the rate-limit headers.

## update_incident

```
PUT /incidents/{id}
```
Body, wrapped in an `incident` object (assumption, as above), only the fields to change. Documented fields: `status`, `resolution`, `priority`, `assignments`, `escalation_level`, `escalation_policy`, `urgency`, `title`, `conflict_resolution`. Success: 200 with the full incident. Used for acknowledge, reassign, escalate, field updates, resolve, and reopen.

- `status`: the reference page summary lists `acknowledged` and `resolved`. A copy of PagerDuty's OpenAPI description also lists `triggered` and states that setting `triggered` or `acknowledged` on a resolved incident reopens it; this is the only source for that and is unverified on the live page.
- `resolution`: used only when setting status to resolved. Stored as a note in the resolve log entry.
- `assignments`: list of assignee objects. Assumption of shape: `{ "assignee": { "id": "<user id>", "type": "user_reference" } }`, from PagerDuty's OpenAPI description and not read on the retrieved reference page.
- `escalation_level`: integer level in the escalation policy (assumption: positive integer counted from 1).

## create_note and list_notes

```
POST /incidents/{id}/notes
GET  /incidents/{id}/notes
```
Create body: `{ "note": { "content": "<text>" } }`. Needs `Content-Type`, `Accept`, and `From`. Documented success: 200 with the note (id, creator, timestamps, content). At most 2000 notes per incident. List response shape was not read.

## snooze_incident

```
POST /incidents/{id}/snooze
```
Body: `{ "duration": <seconds> }`, an integer from 1 to 604800. Success: 201 with the incident.

## merge_incidents

```
PUT /incidents/{id}/merge
```
`{id}` is the target incident. Body: `{ "source_incidents": [ { "id": "<incident id>", "type": "incident_reference" } ] }`. Target must be open; sources must carry alerts or have been created manually in the web interface; the merged total may not exceed 1000 alerts. Success: 200 with the target incident; source alerts move and the sources are resolved.

## Not covered

- Deleting or editing notes, incident alerts, status updates, and responder requests.
- Services, escalation policies, schedules, users, teams, maintenance windows, and event ingestion.
