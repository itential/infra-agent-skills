# PagerDuty service bindings

Base: `https://api.pagerduty.com` (the configured regional API host must match the account). Headers: `Authorization: Token token=<api-key>`, `Accept: application/vnd.pagerduty+json;version=2`, `Content-Type: application/json`. OAuth scopes are named per operation below. Write operations that require `From` use the email of an existing account user, not a fabricated address. Offset-paginated lists use `limit`, `offset`, and response `more`; optional `total=true` requests an actual count.

| Operation | Binding | Fields / response | Errors |
|---|---|---|---|
| List | `GET /services` | `query`,`name`,`team_ids[]`,paging; `services` | 400401403 |
| Detail | `GET /services/{id}` | optional `include[]=integrations`; `service` | 400401403404 |
| Policy | `GET /escalation_policies/{id}` | `escalation_policy` | 401403404 |
| Create | `POST /services` | `service:{type:"service",name:<name>,escalation_policy:{id:<id>,type:"escalation_policy_reference"}}`;201 | 400401402403 |
| Update | `PUT /services/{id}` | `service` with intended writable fields;200 | 401402403404 |

Scope: `services.read`/`services.write`, and `escalation_policies.read` for policy inspection. Core writable properties: `name`,`description`,`status`,`auto_resolve_timeout`,`acknowledgement_timeout`,`escalation_policy`; timeout units are seconds, nonnegative, with 0/null disabling the respective behavior. `status` on creation may only be `active`. Readonly `teams` and `integrations` are not copied back as assignments. Advanced urgency/support-hour settings require their cited schemas; no inferred values are used here.

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
