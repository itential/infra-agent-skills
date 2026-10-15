# CMDB / Asset Management — Platform Index

One row per supported CMDB/asset-management platform. Each platform directory holds its own
`procedure.md` (capability-language, per the REST convention) and `endpoints.md` (literal wiring).

| Platform | Directory | Scope | Notes |
|---|---|---|---|
| ServiceNow | `servicenow/` | Configuration Item CRUD (preferring the CMDB Instance API for writes, Table API for reads/bulk/relationships) and relationship reads via `cmdb_rel_ci` | The CMDB Instance API routes through ServiceNow's Identification and Reconciliation Engine (IRE) to avoid duplicate CIs — a real, documented reason to prefer it over a raw Table API write, not just an alternate path. One record per call, no bulk. |

**Distinct from `change-management`'s ServiceNow procedure, despite being the same vendor:** that skill
covers change *requests* (`sn_chg_rest`); this one covers the configuration-item inventory those
changes reference. Same product, genuinely different object model and API surface — split by what's
actually being managed, not by vendor name alone.
