# Incident Management — Vendor Index

One row per supported vendor. Each vendor directory holds its own `procedure.md` (the full step-by-step),
plus wire-level `endpoints.md`.

| Vendor / Platform | Directory | Scope | Notes |
|---|---|---|---|
| ServiceNow | `servicenow/` | Create/read/update/assign/hold/resolve/reopen/close an incident (incident table, standard state model) | Also appears under `change-management`; the incident and change state models and close semantics differ, so the files are separate. Cancel, problem and major-incident handling, and the stored values for In Progress/On Hold/Canceled are not covered or not stated in the sources |
| PagerDuty | `pagerduty/` | Create/find/read, note, acknowledge, reassign, escalate, snooze, merge, resolve, reopen an incident (REST API v2) | REST; every write needs an acting user's email. Three statuses only (triggered, acknowledged, resolved): no hold and no separate close. Reopening through the API is unverified. Standalone on-call paging, services, escalation policies, schedules, event ingestion, status updates and responder requests are not covered. Creating an incident notifies responders through the service's escalation policy |

Correction recorded when PagerDuty was added: the universal concept of an open-to-resolved-to-closed state path was rewritten, because PagerDuty has no closed state and adds an acknowledged state.
