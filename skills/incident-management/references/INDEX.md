# Incident Management — Vendor Index

One row per supported vendor. Each vendor directory holds its own `procedure.md` (the full step-by-step),
plus wire-level `endpoints.md`.

| Vendor / Platform | Directory | Scope | Notes |
|---|---|---|---|
| ServiceNow | `servicenow/` | Create/read/update/assign/hold/resolve/reopen/close an incident (incident table, standard state model) | Only one platform is documented, so `SKILL.md`'s universal concepts are hedged. Also appears under `change-management`; the incident and change state models and close semantics differ, so the files are separate. Cancel, problem and major-incident handling, and the stored values for In Progress/On Hold/Canceled are not covered or not stated in the sources |
