# PagerDuty schedule bindings

Base: `https://api.pagerduty.com` (the configured regional API host must match the account). Headers: `Authorization: Token token=<api-key>`, `Accept: application/vnd.pagerduty+json;version=2`, `Content-Type: application/json`. OAuth scopes are named per operation below. Write operations that require `From` use the email of an existing account user, not a fabricated address. Offset-paginated lists use `limit`, `offset`, and response `more`; optional `total=true` requests an actual count.

| Operation | Binding | Input and response | Errors |
|---|---|---|---|
| List schedules | `GET /schedules` | `query`, paging, optional interval; `schedules` | 400401403429 |
| Schedule detail | `GET /schedules/{id}` | `since`,`until`,`time_zone`,`overflow`; `schedule` | 400401403404429 |
| List policies | `GET /escalation_policies` | `query`,paging; `escalation_policies` | 400401403429 |
| Policy detail | `GET /escalation_policies/{id}` | policy resource | 401403404 |
| On-call entries | `GET /oncalls` | `since`,`until`,`time_zone`,`schedule_ids[]`,`escalation_policy_ids[]`,`user_ids[]`; `oncalls`,paging | 400401403429 |
| Schedule users | `GET /schedules/{id}/users` | `since`,`until`; `users` | 400401403404429 |
| Create schedule | `POST /schedules` | `schedule` body;201 | 400401403429 |
| Update schedule | `PUT /schedules/{id}` | `schedule` body;200 | 400401403404429 |
| Create overrides | `POST /schedules/{id}/overrides` | `overrides:[{start:<timestamp>,end:<timestamp>,user:{id:<id>,type:"user_reference"}}]`;201 with per-item status | 400401403404429 |

Schedule body: `type:"schedule"`, `time_zone`, optional `name`,`description`, and `schedule_layers`. Each layer needs `start`, `rotation_virtual_start`, `rotation_turn_length_seconds` and ordered `users:[{user:{id:<id>,type:"user_reference"}}]`; optional `end`,`name`,`restrictions`. Restriction syntax must follow the cited `Restriction` schema; no default business hours are imposed. Scope names: `schedules.read`, `schedules.write`, `oncalls.read`, `escalation_policies.read`; the schedule-user operation specifically requires `users.read`.

## Error conditions

- 400: invalid request; correct the returned validation detail before retry.
- 401: missing or invalid authentication; establish the authorized session.
- 402: required account capability is absent; report that restriction.
- 403: permission denied; do not interpret it as an empty collection.
- 404: selected resource was not found; stop operations on that identifier.
- 405: method unsupported; recheck the documented binding.
- 409: conflict with current state; reread and resolve before another write.
- 429: rate limit reached; defer calls according to returned rate-limit guidance.
- 500: server failure; retain the incomplete outcome. An uncertain mutation needs reconciliation before repetition.

Only the codes listed for each binding below are documented for that operation; unexpected responses remain unclassified failures.


Source: [PagerDuty REST OpenAPI reference](https://github.com/PagerDuty/api-schema/blob/main/reference/REST/openapiv3.json), REST v2, retrieved 2026-10-09.
