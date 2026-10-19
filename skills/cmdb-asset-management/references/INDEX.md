# CMDB / Asset Management — Platform Index

One row per supported CMDB/asset-management platform. Each platform directory holds its own
`procedure.md` (capability-language, per the REST convention) and `endpoints.md` (literal wiring).

| Platform | Directory | Scope | Notes |
|---|---|---|---|
| ServiceNow | `servicenow/` | Configuration Item CRUD (preferring the CMDB Instance API for writes, Table API for reads/bulk/relationships) and relationship reads via `cmdb_rel_ci` | The CMDB Instance API routes through ServiceNow's Identification and Reconciliation Engine (IRE) to avoid duplicate CIs — a real, documented reason to prefer it over a raw Table API write, not just an alternate path. One record per call, no bulk. |
| iTop | `itop/` | Configuration Item create/read(OQL or id)/update/delete, with a simulated delete, and dependency reads (impacts / depends on) | REST/JSON services via a single endpoint with the operation inside the JSON document; the account needs the REST Services User profile plus write and bulk-write rights per class. Create does not check for an existing match, so search first. Update is one object per call. A delete cascades to linked objects and has a simulate option. State transitions (stimulus), attachments and data synchronization are not covered |

**Distinct from `change-management`'s ServiceNow procedure, despite being the same vendor:** that skill
covers change *requests* (`sn_chg_rest`); this one covers the configuration-item inventory those
changes reference. Same product, genuinely different object model and API surface — split by what's
actually being managed, not by vendor name alone.

Correction recorded when iTop was added: the shared concepts assumed identification on writes and relationship-gated deletes were the common shapes. iTop creates a new object on every create and cascades deletes to linked objects, so those concepts were reworded as "some platforms".
