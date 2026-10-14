# Incident Management — Vendor Index

One row per supported vendor. Each vendor directory holds its own `procedure.md` (the full step-by-step),
plus wire-level `endpoints.md`.

| Vendor / Platform | Directory | Scope | Notes |
|---|---|---|---|
| ServiceNow | `servicenow/` | Create/read/update/assign/hold/resolve/reopen/close an incident (incident table, standard state model) | Only one platform is documented, so `SKILL.md`'s universal concepts are hedged. Also appears under `change_management`; the incident and change state models and close semantics differ, so the files are separate. Cancel, problem and major-incident handling, and the stored values for In Progress/On Hold/Canceled are not covered or not stated in the sources |

## Adding a new vendor

1. Create `references/<vendor>/procedure.md` following the shape of an existing single-vendor
   capability (e.g. `skills/cmdb_asset_management/references/servicenow/procedure.md`) as a
   template: Common Sequences → Status vocabulary → Operations → Patterns → Known limitations → Tools →
   Verification checklist (`AGENTS.md` rule 12), plus any vendor-specific reference sections the platform needs (for example a state model).
2. Add `endpoints.md` (wire-level calls) alongside it, if the platform is REST/API-driven — CLI-driven
   platforms keep commands inline in `procedure.md` instead (see `AGENTS.md` rule 6).
3. If this vendor also appears in `change_management`'s `INDEX.md` (a common case for ITSM suites),
   note that in this row's Notes column. Keep the two skills' reference files separate even for the
   same vendor: the incident and change state models, required fields, and close semantics differ.
4. Add one row to the table above.
5. Check every existing claim in `SKILL.md`'s "Universal concepts" section against this vendor's
   actual behavior before assuming it holds — correct that section explicitly if it doesn't (see
   `AGENTS.md` rule 4). Each added vendor re-tests those claims; a second vendor is the first real test of them.
6. Do NOT add vendor-specific procedure content to the top-level `SKILL.md` — see that file's own
   contribution note.
