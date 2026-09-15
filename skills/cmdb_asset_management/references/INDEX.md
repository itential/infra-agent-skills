# CMDB / Asset Management — Platform Index

One row per supported CMDB/asset-management platform. Each platform directory holds its own
`procedure.md` (capability-language, per the REST convention) and `endpoints.md` (literal wiring).

| Platform | Directory | Scope | Notes |
|---|---|---|---|
| ServiceNow | `servicenow/` | Configuration Item CRUD (preferring the CMDB Instance API for writes, Table API for reads/bulk/relationships) and relationship reads via `cmdb_rel_ci` | The CMDB Instance API routes through ServiceNow's Identification and Reconciliation Engine (IRE) to avoid duplicate CIs — a real, documented reason to prefer it over a raw Table API write, not just an alternate path. One record per call, no bulk. |
| Freshservice | `freshservice_cmdb/` | Asset (CI) CRUD via the Assets API | Asset type determines valid custom fields; unrecognized fields for a type are silently dropped rather than rejected. |

**Distinct from `change_management`'s ServiceNow procedure, despite being the same vendor:** that skill
covers change *requests* (`sn_chg_rest`); this one covers the configuration-item inventory those
changes reference. Same product, genuinely different object model and API surface — this is the
grouping rule from `software_upgrade_lifecycle` applied at the category level: split by what's actually
being managed, not by vendor name alone.

## Adding a new platform

1. Create `references/<platform>/procedure.md` in capability language (no literal HTTP method+path —
   see `endpoints.md` convention), following the shape of `servicenow/procedure.md` (Operational
   procedure → Patterns → Known limitations → Tools → Verification checklist).
2. Add `endpoints.md` with the literal wiring for every capability named in `procedure.md`.
3. Add one row to the table above.
4. Do NOT add platform-specific procedure content to the top-level `SKILL.md` — see that file's own
   contribution note.
