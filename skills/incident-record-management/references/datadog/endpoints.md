# Datadog incident bindings

Base URL: the selected Datadog site's API endpoint; US1 uses `https://api.datadoghq.com`. Auth: `DD-API-KEY` and `DD-APPLICATION-KEY`; permissions/OAuth scopes `incident_read` or `incident_write` per operation. These methods are public beta.

| Operation | Binding | Input/result |
|---|---|---|
| List | `GET /api/v2/incidents` | `page[size]` at most100, `page[offset]`, optional `include`;200 `data[]`, `meta.pagination.next_offset` |
| Read | `GET /api/v2/incidents/{incident_id}` | UUID, optional `include`;200 `data` |
| Create | `POST /api/v2/incidents` | `data:{type:"incidents",attributes:{title:<text>,customer_impacted:<boolean>}}`;201 `data` |
| Update | `PATCH /api/v2/incidents/{incident_id}` | `data:{id:<uuid>,type:"incidents",attributes:{<requested-fields>}}`;200 `data` |

Creation with `customer_impacted:true` also needs `attributes.customer_impact_scope`. Optional commander uses `relationships.commander_user.data:{id:<user-uuid>,type:"users"}`. When the relationships object is supplied on creation, the schema marks its commander relationship required. State selection uses `attributes.fields.state:{type:"dropdown",value:<documented-state>}`; the vendor example demonstrates `resolved`. Custom single-value fields use `type` of `dropdown`/`textbox` and string `value`; multi-value fields use a supported type such as `multiselect` and an array `value`. No exhaustive custom-field vocabulary is assumed.

Optional notification entries use `attributes.notification_handles:[{handle:<approved-handle>,display_name:<label>}]`. Update supports impact timestamps, detected time, title, field selections and supplied relationships. The response exposes `id` (UUID), `attributes.public_id` (number), state, impact fields and timestamps.

All four methods document400,401,403,404,429 with `errors` array. Correct input for400; restore authentication for401; stop on403; report missing resource on404; defer calls on429. An unknown write outcome requires reconciliation rather than automatic duplication.

Sources: the four method references linked in [procedure](procedure.md), v2, retrieved 2026-10-09.
