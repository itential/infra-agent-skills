# Auvik — Collect Discovered Device and Network Inventory State

Reads the devices, networks, interfaces, and components Auvik has discovered, per tenant, through the Auvik API (v1). Read-only: nothing is created, changed, or deleted, so there are no confirmation gates.

Source: Auvik API v1 OpenAPI specification (retrieved 2026-10-26); wire details are in [endpoints.md](endpoints.md).

Unverified: Auvik's API integration guide could not be retrieved (the support site blocked automated access), so documented request-rate limits and any IP-based blocking behavior are not confirmed. See Patterns for how to react safely.

## Common Sequences

- **Device state for one tenant:** Verify credentials → Resolve tenants → Read device info → Read device detail.
- **All devices of one type:** Resolve tenants → Read extended device detail with a device-type filter.

## Verify credentials and resolve tenants

Verify the credentials first, then list the tenants the account can reach. Success is an accepted verification and a tenant list containing the requested tenant. An invalid-credentials answer is final: correct the credentials rather than retrying. Query each tenant separately by passing its identifier so a failure stays attributed to one tenant.

## Read device info

Read device records, optionally filtered by network, device type, make and model, vendor, online status, modified-after, not-seen-since, and known-state. The device detail relationship can be included in the same call.
Success is a list of device records. A successful empty list is still a success response and means no device matched in that tenant; it is not evidence of a healthy network. Online status values are Auvik's own observations (online, offline, unreachable, testing, unknown, dormant, not present, lower-layer down) and are reported as returned, not re-tested.
A device name or IP does not identify a device: resolve it to the Auvik device identifier before reading one record.

## Read device detail

Device detail and extended detail add discovery and platform information beyond the info view. The extended collection refuses requests that omit a device-type filter, so supply one. Info, detail, and extended detail are different views of a device; report which view was used.

## Read networks, interfaces, and components

Each has its own list read with filters (for interfaces: type, parent device, administrative and operational status; for components: owning device and current status ok, degraded, or failed). Keep each record's own identifier and its relationship to the parent device.

## Handle paging and errors

Lists page with a first/after or last/before cursor pair. Follow the continuation until it is exhausted, or report the result as partial if stopped early.
The specification names these failures: 400 bad request (correct the parameters), 403 forbidden, 404 not found (check the resource identifier), 500 internal error (retry later, not in a tight loop). Do not retry 400 or 404 unchanged.

## Patterns

- **A 403 can have more than one cause.** The specification lists 403 as forbidden, which fits a user whose role lacks permission. Unverified: Auvik's integration guide is reported to describe an IP-level block on excessive requests that also surfaces as 403. When a 403 follows a burst of calls from one address, or hits calls that worked before, stop sending requests and report it as a possible block, rather than assuming a role fault or retrying in a loop.
- Not documented in the specification: rate limits and a 429 response. Pause on any throttling or repeated 403 and resume later.
- Dates in filters use the ISO 8601 form with milliseconds and a trailing Z.

## Known limitations

- API v1 only; this procedure reads current discovered state and keeps no snapshots. A before/after comparison needs the caller to save the earlier result.
- Observed data only: no tickets, no source-of-truth reconciliation, no replacement decisions. Notes, audit, warranty, lifecycle, and backup reads are not covered.
- Discovery gaps: a device Auvik has not discovered is absent from results, not healthy.

## Tools

| Operation | Description | Category |
|---|---|---|
| Verify credentials | Check the credentials are accepted | REST API |
| Resolve tenants | List accessible tenant identities | REST API |
| Read devices | Read device info, detail, extended detail | REST API |
| Read networks, interfaces, components | Read related inventory lists | REST API |

## Verification checklist

- [ ] The tenant was resolved and each tenant was queried separately.
- [ ] The device view used (info, detail, extended) and the filters are stated.
- [ ] Paging finished or the result is labeled partial.
- [ ] Empty results and 4xx/5xx errors are reported as such, not as healthy state.
