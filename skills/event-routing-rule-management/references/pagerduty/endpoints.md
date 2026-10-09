# PagerDuty routing bindings

Base: `https://api.pagerduty.com` (the configured regional API host must match the account). Headers: `Authorization: Token token=<api-key>`, `Accept: application/vnd.pagerduty+json;version=2`, `Content-Type: application/json`. OAuth scopes are named per operation below. Write operations that require `From` use the email of an existing account user, not a fabricated address. Offset-paginated lists use `limit`, `offset`, and response `more`; optional `total=true` requests an actual count.

| Operation | Binding | Response | Errors |
|---|---|---|---|
| List | `GET /event_orchestrations` | paginated `orchestrations` | 401403404 |
| Detail | `GET /event_orchestrations/{id}` | `orchestration` | 400401403404 |
| Global path | `GET /event_orchestrations/{id}/global` | `orchestration_path` | 400401403404 |
| Router | `GET /event_orchestrations/{id}/router` | `orchestration_path` | 400401403404 |
| Service path | `GET /event_orchestrations/services/{service_id}` | `orchestration_path` | 400401403404 |
| Replace router | `PUT /event_orchestrations/{id}/router` |200 with `orchestration_path` and possible `warnings` | 400401403404405409 |

Read scope: `event_orchestrations.read`, except the service path uses `services.read`. Replacement scope: `event_orchestrations.write`.

Replacement body: `orchestration_path` containing `sets:[{id:"start",rules:[...]}]` and the intended `catch_all`. Ordinary rules contain existing `id` where applicable, optional `label`, `conditions:[{expression:<PagerDuty-condition-expression>}]`, and `actions:{route_to:<service-id>}`. Fallback uses `catch_all:{actions:{route_to:<service-id-or-unrouted>}}`. The router has one start set. Omitted rules and properties are deleted. Full condition syntax is supplied from the installed vendor schema; this procedure invents no expressions. Warnings with `warning_type:"forbidden_feature"` indicate unavailable plan features despite storage success.

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
