# Cloudflare Load Balancing — Load Balancer, Pool, and Origin Procedure

Creates, changes, and removes a Cloudflare load balancer (a hostname that answers with the best
healthy pool), the pools it fails over between, and the origins inside each pool, and manages an
origin's live state. Assumes an authenticated REST client holding an API token with the load
balancing write permissions for the target account and zone is already available. Does not cover
Cloudflare DNS records outside a load balancer (see `dns-record-management`), TLS certificates, custom
rules (`rules`, flagged beta in the reference), or Enterprise-only point-of-presence steering.

Sources (retrieved 2026-10-19): Cloudflare API reference for Load Balancers, Pools, and Monitors and
Cloudflare's load balancing overview, https://developers.cloudflare.com/load-balancing/. Nothing here
was run against a live account.

This platform does not have a listener address. The load balancer is identified by the DNS hostname in
its `name` field, so this procedure's "VIP" is that hostname.

## Common Sequences

- **Stand up a new balanced hostname:** create monitor, create pool, create load balancer, read back
  the balancer, read pool health.
- **Take an origin out of rotation:** read pool, update the pool with that origin's `enabled` set to
  false (complete origins list), re-read the pool.
- **Retire a hostname:** read the pool and monitor references, delete the load balancer, delete unused
  pools, delete unused monitors.

## Operational procedure

### Create the health check, pool, and load balancer (in this order)

1. **Create a monitor** if the pool should be health checked. Choose a `type`; tcp, udp and smtp types
   require a `port`. Record the returned monitor `id`. Skip only if the caller explicitly wants an
   unmonitored pool.
2. **Create a pool** with a unique `name` and at least one origin (`name`, `address`, optional `port`,
   `weight`, `enabled`). Attach `monitor`. Set `minimum_origins` if the pool should count as unhealthy
   below a threshold. Record the pool `id`.
3. **Create the load balancer** with `name` (the hostname), `default_pools` (pool IDs, first is highest
   failover priority), and `fallback_pool`. Decide `proxied` explicitly. **Stop and confirm with the
   operator before creating or enabling a balancer on a hostname that already receives production
   traffic**, because the hostname's answers change. Choose zone or account scope and use that scope's
   path.
4. **Confirm** the response carries `success: true` and a `result.id`, then read the balancer back and
   check `default_pools` order and `enabled`. Read the pool's health to see whether its origins report
   healthy. Report the health state as read, not as assumed.

### Add, remove, or change an origin (pool member)

5. **Read the pool first.** The origin's identity here is its `name` within the pool, with `address`
   (and `port`) as its target. Whether a partial update merges or replaces the `origins` array is not
   documented in the pages used, so send the complete intended origin list and re-read afterwards.
6. **Disable instead of removing** when the goal is to take an origin out of rotation: set that origin's
   `enabled` to false. This is distinct from deleting it from the list. For session-sticky balancers,
   `session_affinity_attributes.drain_duration` exists on the load balancer; its exact drain behavior
   was not detailed in the pages used, so report only that the field was set.
7. **Stop and confirm with the operator before disabling or removing an origin from a pool serving
   live traffic, or setting an origin's `weight` to 0**, particularly if it is the last enabled origin.
8. **Re-read** the pool and confirm the origin list and each `enabled` flag match what was intended.

### Change failover order or steering

9. **Update `default_pools` order, `fallback_pool`, `steering_policy`, or `session_affinity`** on the
   load balancer with a partial update (or full replace). **Confirm with the operator first when
   changing steering or pool order on a live balancer**, because it moves traffic.

### Delete

10. **Before deleting a pool or monitor, call its References endpoint** and stop if any load balancer
    or pool still uses it; the reference documents no behavior for deleting an in-use object.
11. **Stop and confirm with the operator before deleting a load balancer**: the hostname stops being
    answered by Cloudflare's load balancing. Delete the balancer first, then unused pools, then unused
    monitors.

## Patterns

- Build bottom-up (monitor, pool, balancer) and delete top-down (balancer, pool, monitor).
- Pool health is read from the pool's health endpoint, not inferred from the balancer's `enabled` flag.
- `proxied` and `ttl` interact: TTL applies only to DNS-only (not proxied) balancers.
- An origin `weight` is 0 to 1, not a percentage.

## Known limitations

- Delete behavior for in-use pools and monitors is undocumented in the pages used (step 10).
- `origins` update semantics on partial update are undocumented in the pages used (step 5).
- Rate limit is 1200 requests per five minutes; on HTTP 429 wait for the `retry-after` seconds before
  retrying.
- `rules`, `pop_pools`, and other Enterprise or beta options are not covered.
- The zone-or-account path prefix for load balancers carries an assumption noted in `endpoints.md`.

## Tools

| Operation | Description | Category |
|---|---|---|
| Create/read/update/delete monitor | Health check definition | REST |
| Create/read/update/delete pool, read pool health and references | Origins and failover unit | REST |
| Create/read/update/delete load balancer | Hostname, pool order, steering, affinity | REST |

## Verification checklist

- [ ] Monitor, pool, and balancer created in that order, and IDs recorded
- [ ] Balancer read back with the intended `default_pools` order and `enabled` state
- [ ] Pool health read after creation or origin change and reported as read
- [ ] Operator confirmation obtained before touching a live hostname, disabling or removing a live
      origin, or deleting a balancer
- [ ] References checked before deleting a pool or monitor
- [ ] Any `errors` array reported verbatim
