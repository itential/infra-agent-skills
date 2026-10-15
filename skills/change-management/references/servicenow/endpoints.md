# Endpoint Mapping — ServiceNow Change Management Lifecycle

Literal `sn_chg_rest` operations behind each capability named in `SKILL.md`. Use this to bind the skill
to a concrete tool (e.g. a FlowAI-discovered adapter tool, a direct REST call). Sourced from the
source API reference.

| Capability (SKILL.md) | Operation | Body / notes |
|---|---|---|
| Create | `POST /api/sn_chg_rest/change` | Body: fields + `chg_model` and/or `type` (source strongly advises setting at least one). |
| Update | `PATCH /api/sn_chg_rest/change/{sys_id}` | Body: `data` — name-value pairs to change. |
| Check Gates | `GET /api/sn_chg_rest/change/{change_sys_id}/nextstates` | No body. Returns `available_states`, `state_transitions[]`. |
| Get current record (pre-close verification) | `GET /api/sn_chg_rest/change/{sys_id}` | No body. |
| Close | `PATCH /api/sn_chg_rest/change/{sys_id}` | Body: `{"state": "<target_state>", "close_code": "<code>", "close_notes": "<notes>"}`. Same operation as Update — only the fields differ. |
| Approve / Reject | `PATCH /api/sn_chg_rest/change/{sys_id}/approvals` | Body: `{"state": "approved"}` or `{"state": "rejected", "comments": "<reason>"}`. `comments` required if rejecting. |

## Documented error strings / codes worth pattern-matching

- Approvals `400`: "the user not having the authority to approve or reject the change request" —
  distinct from a generic malformed-request 400.
- `nextstates` `404`: "Not found. The requested item wasn't found."
- Standard codes across all listed endpoints: `200` success, `400` bad/malformed, `401` unauthorized,
  `404` not found, `500` internal server error.
