# Prisma SD-WAN Unified API bindings

Sources: [Unified API prerequisite](https://pan.dev/sdwan/api/), [SASE authentication](https://pan.dev/sase/docs/getstarted/), [current Unified OpenAPI](https://github.com/PaloAltoNetworks/pan.dev/blob/master/openapi-specs/sdwan/unified/open_api_unified.json), retrieved 2026-10-09. Individual operation versions are pinned below; the document labels its overall version Latest.

Base: `https://api.sase.paloaltonetworks.com`; authenticated requests use `Authorization: Bearer <access-token>` and JSON. The preconfigured service account requires roles for the intended TSG.

| Operation | Literal binding | Success body |
|---|---|---|
| Initialize profile | `GET /sdwan/v2.1/api/profile` | Successful profile response; mandatory after token creation before other SD-WAN calls. |
| Sites | `GET /sdwan/v4.13/api/sites` | `items[]` of sites, with `id`, `name`, `element_cluster_role`, related policy identifiers. |
| Elements | `GET /sdwan/v3.2/api/elements` | `items[]`, including `id`, `site_id`, `name`, `connected`, `state`, `software_version`. |
| Machines | `GET /sdwan/v2.5/api/machines` | Machine records; see schema inconsistency and secret-field warning in procedure. |
| Element status | `GET /sdwan/v2.6/api/elements/{element_id}/status` | `ElementStatusV2N6`; missing status gives 404 / `ELEMENT_STATUS_NOT_FOUND`. |
| Software status | `GET /sdwan/v2.1/api/elements/{element_id}/software/status` | Up to five tenant-initiated upgrade status records. |
| Interfaces | `GET /sdwan/v4.21/api/sites/{site_id}/elements/{element_id}/interfaces` | `items[]` of interface configuration. |
| BGP peers | `GET /sdwan/v3.0/api/sites/{site_id}/elements/{element_id}/bgppeers` | `items[]` of peer configuration. |
| Static routes | `GET /sdwan/v2.3/api/sites/{site_id}/elements/{element_id}/staticroutes` | `items[]` of static routes. |
| WAN interfaces | `GET /sdwan/v2.10/api/sites/{site_id}/waninterfaces` | Site-level `items[]`. |
| Security zones | `GET /sdwan/v2.2/api/securityzones` | Zone `items[]`. |
| Path policy sets | `GET /sdwan/v3.0/api/policysets` | Policy-set `items[]`. |
| Application definitions | `GET /sdwan/v2.6/api/appdefs` | `items[]` of `AppDefV2N6`. |
| Topology query | `POST /sdwan/v3.6/api/topology` | `NetworkTopologyV3N6`. |
| Event query | `POST /sdwan/v3.7/api/events/query` | `EventQueryResponseV3_7`. |

Topology body uses documented fields only: `type` (`ANYNET`, `ANYNETPLUS`, `BASENET`, `PHYSICAL`), optional `site_id`, `nodes[]`, `links[]`, `links_only`, `servicelinks`, `stub_links`. The deployment determines the requested topology; no default is inferred. HTTP 400 codes include `INVALID_JSON_INPUT`, `INVALID_JSON_EXTRA_ATTRIBUTE`, `INVALID_TOPO_QUERY`, `INVALID_TOPOLOGY_STUB_LINKS_OPTION`, `TOPOLOGY_REBUILD_IN_PROGRESS`.

Event body: `start_time`/`end_time` ISO 8601, `time_type` (`raised` or `created`), optional `query` filters such as `site[]`, `code[]`, `type[]` (`alarm`/`alert`), `entity_ref[]`; `limit.count`, `limit.sort_on`, `limit.sort_order` (`ascending`/`descending`); `severity[]` (`critical`, `major`, `minor`); `acknowledged`, `suppressed`; optional `temporal_scope` (`include_standing`/`standing_only`). Pagination uses `_offset` from the previous response. Invalid queries return 400 / `INVALID_REQUEST_ERROR_0001`.

Machine errors include 400 / `TENANT_REGION_ASSOCIATION_NOT_FOUND` or `MACHINE_UNKNOWN`, and 404. Machine schema fields `token` and `console_conf_passphrase` are sensitive and are not reporting fields. Application definitions do not define NetClaw's example `risk` attribute; missing risk information remains unknown.
