# Endpoints — Cloudflare Load Balancing API

Literal wiring layer. `procedure.md` steps reference these by name; bind them to whatever
authenticated REST client is assumed available.

Sources (retrieved 2026-10-19): Cloudflare API reference pages for Load Balancers
(https://developers.cloudflare.com/api/resources/load_balancers/), Pools
(.../load_balancers/subresources/pools/), Monitors (.../subresources/monitors/); "Make API calls"
(https://developers.cloudflare.com/fundamentals/api/how-to/make-api-calls/); API rate limits
(https://developers.cloudflare.com/fundamentals/api/reference/limits/).

Base URL: `https://api.cloudflare.com/client/v4`. Auth: `Authorization: Bearer <API_TOKEN>`.

## Load balancer

A load balancer lives either under a zone or under an account; the two path prefixes are mutually
exclusive per object. `{scope}` below is `zones/{zone_id}` or `accounts/{account_id}`.

| Operation | Method and path | Required fields |
|---|---|---|
| List | `GET /{scope}/load_balancers` | none |
| Read | `GET /{scope}/load_balancers/{lb_id}` | id |
| Create | `POST /{scope}/load_balancers` | `name`, `default_pools` |
| Replace | `PUT /{scope}/load_balancers/{lb_id}` | `name`, `default_pools` |
| Partial update | `PATCH /{scope}/load_balancers/{lb_id}` | whichever fields change |
| Delete | `DELETE /{scope}/load_balancers/{lb_id}` | id |

The reference writes the prefix as `/{accounts_or_zones}/{id}/load_balancers`. Reading that as the literal
segments `zones` or `accounts` followed by the matching ID is an assumption; confirm against the live reference.

Fields: `name` (the DNS hostname the balancer answers for), `default_pools` (pool IDs, ordered by
failover priority), `fallback_pool` (pool ID used when every other pool is unhealthy), `enabled`
(default true), `proxied` (true routes through Cloudflare, false is DNS-only), `ttl` (only meaningful
when not proxied), `description`, `steering_policy` (`off`, `geo`, `random`, `dynamic_latency`,
`proximity`, `least_outstanding_requests`, `least_connections`, or empty), `region_pools` and
`country_pools` (code to pool-ID list), `session_affinity` (`none`, `cookie`, `ip_cookie`, `header`),
`session_affinity_ttl` (1800-604800 for cookie types, 30-3600 for header), and
`session_affinity_attributes` (includes `drain_duration`).

## Pool

| Operation | Method and path | Required fields |
|---|---|---|
| List | `GET /accounts/{account_id}/load_balancers/pools` | none |
| Read | `GET /accounts/{account_id}/load_balancers/pools/{pool_id}` | id |
| Create | `POST /accounts/{account_id}/load_balancers/pools` | `name`, `origins` |
| Replace | `PUT /accounts/{account_id}/load_balancers/pools/{pool_id}` | full pool body |
| Partial update | `PATCH /accounts/{account_id}/load_balancers/pools/{pool_id}` | changed fields |
| Delete | `DELETE /accounts/{account_id}/load_balancers/pools/{pool_id}` | id |
| Health | `GET /accounts/{account_id}/load_balancers/pools/{pool_id}/health` | id |
| References | `GET /accounts/{account_id}/load_balancers/pools/{pool_id}/references` | id |

Pool fields: `name` (letters, digits, hyphens, underscores), `origins`, `enabled` (default true),
`monitor` (monitor ID) or `monitor_group`, `minimum_origins`, `check_regions`, `description`.

Origin fields (each entry in `origins`): `name`, `address` (IP or hostname), `port` (0 means the
default port), `enabled` (default true), `weight` (0 to 1 in steps of 0.01), `header.Host`,
`virtual_network_id`.

Health response includes `pool_id` and per-location health under `pop_health`.
References response lists `resource_id` and `resource_type` of objects that use the pool.

## Monitor

| Operation | Method and path |
|---|---|
| List | `GET /accounts/{account_id}/load_balancers/monitors` |
| Read | `GET /accounts/{account_id}/load_balancers/monitors/{monitor_id}` |
| Create | `POST /accounts/{account_id}/load_balancers/monitors` |
| Replace / partial update | `PUT` / `PATCH` on the monitor path |
| Delete | `DELETE` on the monitor path |
| References | `GET .../monitors/{monitor_id}/references` |

Monitor fields: `type` (`http`, `https`, `tcp`, `udp_icmp`, `icmp_ping`, `smtp`), `port` (required for
tcp, udp and smtp types, defaults to 80 or 443 for http and https), `path`, `method`
(default GET), `expected_codes`, `expected_body`, `interval`, `timeout`, `retries`, `consecutive_up`,
`consecutive_down`, `follow_redirects`, `allow_insecure`, `header`, `description`.

## Envelope, permissions, limits

- Success: HTTP 2xx and a JSON body with `success: true` and a `result` object (delete returns
  `result.id`). Failure: `success: false` and an `errors` array of `{code, message}` objects. Report the
  `errors` array verbatim.
- Permissions named in the reference: pool and monitor writes need "Load Balancing: Monitors and
  Pools Write"; load balancer writes need the load balancer write permission for the zone or account.
- Rate limit: 1200 requests per five minutes per user across all access methods. Exceeding it blocks
  calls for the next five minutes with HTTP 429. A `retry-after` header (seconds) is present only when
  limited.
- Lists use `page` and `per_page` query parameters.

## Not documented in the pages retrieved

- What happens when a pool still referenced by a load balancer is deleted. Use the References call
  first and treat the outcome of a direct delete as unknown.
- Whether a `PATCH` that carries an `origins` array replaces the whole array or merges entries.
  Assume replacement and send the complete list.
