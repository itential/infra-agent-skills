# RIPE Atlas inventory bindings

Base `https://atlas.ripe.net`. These endpoints support anonymous reads.

| Operation | Request | Verified query parameters |
|---|---|---|
| Probes | `GET /api/v2/probes/` | `asn`, `asn_v4`, `asn_v6`, `country_code`, `is_anchor`, `is_public`, `status`, `page`, `page_size` |
| Anchors | `GET /api/v2/anchors/` | `as_v4`, `as_v6`, `country`, `is_active`, `is_disabled`, `is_decommissioned`, `is_public`, `probe_status`, `page`, `page_size` |

HTTP 200 JSON has `count`, `next`, `previous`, `results`. Probe status IDs are `0` Never Connected, `1` Connected, `2` Disconnected, `3` Abandoned, `4` Written Off. The probe record's `id` differs from an anchor's `id`; anchor `probe` identifies the hosted probe. Follow server-provided `next` links within the same API origin.

No complete error-code list is supplied by these operation pages. Preserve native failures and any retry guidance rather than assuming missing data is a valid empty collection.

Sources: [probes](https://atlas.ripe.net/docs/apis/rest-api-reference/probes/probes_list/), [anchors](https://atlas.ripe.net/docs/apis/rest-api-reference/anchors/anchors_list/), retrieved 2026-10-09.
