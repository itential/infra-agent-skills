# APIC observation REST bindings

Source: [Cisco APIC REST guide](https://www.cisco.com/c/en/us/td/docs/dcn/aci/apic/all/apic-rest-api-configuration-guide/cisco-apic-rest-api-configuration-guide/m_using_the_rest_api.html), retrieved 2026-10-09.

Base `https://<apic>`; authenticated session cookie `APIC-cookie=<token>` and any session challenge requirements already handled by the client. The deployed model is available at `https://<apic>/doc/html/`.

| Operation | Binding | Query |
|---|---|---|
| Systems | `GET /api/class/topSystem.json` | Optional scoped paging |
| Attached endpoints | `GET /api/class/fvCEp.json` | Optional scoped paging |
| Current faults | `GET /api/class/faultInst.json` | Optional `query-target-filter=eq(faultInst.cause,"config-failure")` |
| Known object | `GET /api/mo/{dn}.json` | `query-target=self`; optional `rsp-subtree-include=health` or `faults` where model-supported |

The guide explicitly allows `.json` and `.xml`, and `/api/node/class` or `/api/node/mo` aliases. Object identity uses the complete DN, for example placeholder `uni/tn-<tenant>`.

Collection options: `page=0` initially, positive caller-selected `page-size`, then successive pages. `imdata` contains class-keyed objects with `attributes` and optional `children`; `totalCount` describes the generated query result. The source's introductory singular `attribute` spelling conflicts with its worked JSON structures; the working schema uses `attributes`.

Known large-query errors: `Unable to deliver the message, destination is not available` (documented 503/timeout case); `Unable to process the query, result dataset is too big` (narrow the query). The guide's invalid `e(stultification,...)` filter example is not reproduced as executable syntax.
