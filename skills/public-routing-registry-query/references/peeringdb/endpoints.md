# PeeringDB bindings

Base `https://www.peeringdb.com`. Public reads omit authentication. Authorized reads use `Authorization: Api-Key <key>` with `Accept: application/json`. Basic authentication is documented as rejected with HTTP 403.

| Operation | Request | Evidence |
|---|---|---|
| Find network | `GET /api/net?asn=<asn>&depth=0` | `data` array; selected record's `id` and ASN |
| Expanded detail | `GET /api/net/<id>?depth=2` | Network and first-level related objects, including returned `netixlan_set` / `netfac_set` where available |
| Exchange presence | `GET /api/netixlan?net_id=<id>&limit=<limit>&skip=<offset>` | Network-at-exchange rows |
| Facility presence | `GET /api/netfac?net_id=<id>&limit=<limit>&skip=<offset>` | Network-at-facility rows |

The API always wraps records in `data: []`; optional `meta` can contain status/message. Collection `depth=0` avoids expansion, `1` expands first-level sets to IDs, `2` to objects. Single-object expansion supports levels one through four. The procedure uses explicit depth because publisher examples disagree about the default.

Sources: [API specification](https://docs.peeringdb.com/api_specs/), [HOWTO](https://docs.peeringdb.com/howto/search/), retrieved 2026-10-09.
