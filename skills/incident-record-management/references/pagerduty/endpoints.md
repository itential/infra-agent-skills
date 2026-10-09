# PagerDuty incident bindings

Base: `https://api.pagerduty.com` (the configured regional API host must match the account). Headers: `Authorization: Token token=<api-key>`, `Accept: application/vnd.pagerduty+json;version=2`, `Content-Type: application/json`. OAuth scopes are named per operation below. Write operations that require `From` use the email of an existing account user, not a fabricated address. Offset-paginated lists use `limit`, `offset`, and response `more`; optional `total=true` requests an actual count.

| Operation | Binding | Inputs / output | Documented errors |
|---|---|---|---|
| List | `GET /incidents` | `statuses[]`, `urgencies[]`, `service_ids[]`, `team_ids[]`, `user_ids[]`, `since`, `until`, `time_zone`; or `date_range=all`; response `incidents` | 400401402403429 |
| Detail | `GET /incidents/{id}` | response `incident` | 400401403404429 |
| Alerts | `GET /incidents/{id}/alerts` | optional `statuses[]`, `alert_key`; response `alerts`, pagination | 400401403429 |
| Single alert | `GET /incidents/{id}/alerts/{alert_id}` | response `alert` | 400401403404429 |
| Notes | `GET /incidents/{id}/notes` | response `notes` | 400401403404429 |
| Outlier | `GET /incidents/{id}/outlier_incident` | optional `since`, `additional_details[]`; native outlier result | 400403404429500 |
| Past | `GET /incidents/{id}/past_incidents` | optional `limit`,`total`; native past incidents | 400403404500 |
| Related | `GET /incidents/{id}/related_incidents` | optional `additional_details[]`; native related incidents | 400403404429500 |
| Create | `POST /incidents` | `From`; body `incident:{type:"incident",title:<text>,service:{id:<id>,type:"service_reference"}}`;201 | 400401403429 |
| Update | `PUT /incidents/{id}` | `From`; body `incident:{type:"incident_reference",status:<state>}`;200. Supported states `triggered`,`acknowledged`,`resolved` | 401403404429 |
| Add note | `POST /incidents/{id}/notes` | `From`; `note:{content:<text>}`;200 | 400401403404429 |
| Request responders | `POST /incidents/{id}/responder_requests` | `requester_id`,`message`,`responder_request_targets` (user or escalation-policy references);200 | 400401403404429; description also documents402 for missing ability |
| Merge | `PUT /incidents/{id}/merge` | `From`; `source_incidents:[{id:<id>,type:"incident_reference"}]`;200 | 400401403404429 |

Read scope: `incidents.read`; mutation scope: `incidents.write`. Optional creation fields include `incident_key`, `urgency`, `assignments:[{assignee:{id:<user-id>,type:"user_reference"}}]` or `escalation_policy:{id:<policy-id>,type:"escalation_policy_reference"}`. Update supports `assignments`, `escalation_policy`, `escalation_level`, `title`, `urgency`, and `resolution` for resolution notes. Numeric time shortcuts from an MCP wrapper are not REST timestamp values.

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
