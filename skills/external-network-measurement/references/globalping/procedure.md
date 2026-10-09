# Globalping public-target measurement

Run and retrieve a bounded, explicitly selected external measurement.

## Common Sequences

- New measurement: **Select scope** → **Inspect availability** → **Create measurement** → **Retrieve final results**.
- Existing measurement: **Retrieve final results** with its supplied identifier.

### Select scope

The request supplies a publicly reachable target, test type, protocol options and desired probe locations/count. Targets sent to the public service must be authorized for external measurement; internal addresses/names are outside this procedure. The selected method determines the measurement options, rather than treating ping, DNS and HTTP as interchangeable.

### Inspect availability

Probe discovery returns current locations and metadata; it does not expose a stable probe identifier for direct selection. Limits inspection supplies the caller's current allowance. Location conditions can use structured fields or fuzzy matching; combined conditions narrow the selection. Current discovery, not a hard-coded ASN list or probe count, establishes availability.

### Create measurement

The measurement sends traffic and can consume paid credits: stop and confirm with the operator before proceeding. The request specifies the global limit or per-location limits, not both. Acceptance returns 202 with a measurement ID and result location. Invalid input requires correcting the request. No suitable probes means the test did not run, not that the target failed. Quota or credit errors leave the test uncreated and retain the response's allowance information.

### Retrieve final results

The result is read at the returned measurement location. While its native state is in-progress, the documented client waits 500 milliseconds after receiving each response before another read. Conditional reads use the ETag where available. A not-modified response reuses the cached representation. A missing measurement is not an empty successful test. Rate limiting follows the returned retry delay.

Any non-running state is final, but each probe result still has its own outcome. Offline/internal/resolver failures are distinguished from target responses. The experimental failure-source classification is best-effort, not a proven cause. Raw output, location, protocol, resolved target and timings accompany the finding. DNS disagreement is preserved per probe. One location's result is not generalized to an entire region or the Internet.

## Patterns

A prior measurement ID can select the same probes for a comparison. The API typically retains measurements for up to six months; the NetClaw claim that no history exists is not retained.

## Known limitations

IPv6 target support is marked experimental by the retrieved schema. No complete region coverage is promised. A final measurement does not guarantee that every probe succeeded. No fixed credit balance or global probe count is assumed.

## Tools

Assumes the authenticated client described in [the bindings](endpoints.md).

| Operation | Description | Category |
|---|---|---|
| Inspect probes/limits | Discover current vantage points and allowance | Public monitoring read |
| Create measurement | Launch the selected external tests | Active measurement |
| Retrieve result | Read progress and per-probe output | Monitoring read |

## Verification checklist

- Public target, test options and probe budget are explicit.
- Accepted, running and final states are distinguished.
- Polling follows the documented cadence.
- Every probe outcome retains its location and failure class.
- No-probe/authorization/quota failures are not called target outages.

## Sources

- [Globalping OpenAPI 1.0.0](https://api.globalping.io/v1/spec.yaml). Retrieved 2026-10-09.
