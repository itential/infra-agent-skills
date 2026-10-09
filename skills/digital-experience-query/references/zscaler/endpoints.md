# ZDX experience bindings

Sources: [applications](https://github.com/zscaler/zscaler-mcp-server/blob/master/src/zscaler_mcp/tools/zdx/list_applications.py), [scores](https://github.com/zscaler/zscaler-mcp-server/blob/master/src/zscaler_mcp/tools/zdx/get_application_score.py), [alerts](https://github.com/zscaler/zscaler-mcp-server/blob/master/src/zscaler_mcp/tools/zdx/list_alerts.py), master retrieved 2026-10-09.

| Operation | MCP tool | Inputs |
|---|---|---|
| Find application | `zdx_list_applications` | Optional scope fields below. |
| Read score | `zdx_get_application` | `app_id` string plus scope. |
| Read trend | `zdx_get_application_score_trend` | `app_id` string plus scope. |
| Find ongoing alerts | `zdx_list_alerts` | Scope plus optional `offset`, `limit`. |
| Read alert | `zdx_get_alert` | `alert_id` string. |
| Read affected devices | `zdx_list_alert_affected_devices` | `alert_id`, scope, optional `location_groups` integer list, `offset`, `limit`. |

Scope fields: `location_id`, `department_id`, `geo_id` are lists of strings; `since` is an integer number of hours, at least 1. The documented service default is 2 hours; alert lists cap `since` at 336 hours. `offset` is a string continuation value, not an integer row count; the publisher input describes it as a prior `next_offset`. `limit` is a positive integer.

List outputs are arrays; score/trend and alert details are dictionaries. Missing IDs cause input errors and SDK failures become tool errors. In the inspected implementation, list outputs unwrap the records and can lose upstream cursor metadata: completeness is unknown when no continuation information is returned.
