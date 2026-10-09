# RIPEstat bindings

Base `https://stat.ripe.net`. Every response envelope has `status` (`ok`, `error`, `maintenance`), `status_code`, `data_call_status`, `version`, `cached`, and endpoint-specific `data`. The guide mentions both `message` and `messages`; error payloads are retained without assuming one shape.

| Operation | Request | Inputs / data |
|---|---|---|
| ASN overview | `GET /data/as-overview/data.json` | `resource=<ASN>`; `announced`, `holder`, `query_starttime`, `query_endtime` |
| Prefixes | `GET /data/announced-prefixes/data.json` | `resource`, optional `starttime`, `endtime`, `min_peers_seeing` (default 10); `prefixes` with `timelines` |
| Registry | `GET /data/whois/data.json` | `resource=<ASN-or-IP>`; `authorities`, `records`, `irr_records`, `query_time` |
| Abuse contact | `GET /data/abuse-contact-finder/data.json` | `resource=<ASN-IP-or-prefix>`; `abuse_contacts`, `authoritative_rir` |
| Origin validation | `GET /data/rpki-validation/data.json` | `resource=<ASN>`, `prefix=<CIDR>`; `data.status`: `valid`, `invalid_asn`, `invalid_length`, `unknown`; `description` |

API endpoint lifecycle states include `supported`, `deprecated`, `development`. No callback or cache-refresh parameter is needed for these reads. The publisher documents at most eight concurrent calls per source IP; this is not a universal daily quota.

Sources: [API basics](https://stat.ripe.net/docs/data-api/ripestat-data-api/) and each operation's [API reference catalog](https://stat.ripe.net/docs/data-api/api-endpoints/rpki-validation), retrieved 2026-10-09; the procedure links all individual operation references.
