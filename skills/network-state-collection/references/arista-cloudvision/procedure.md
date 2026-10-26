# Arista CloudVision — Read Device Inventory and Events

Reads device inventory and events from the CloudVision Resource API. Read-only: it collects observed state and does not onboard, decommission, tag, or change anything.

Sources (Arista CloudVision APIs documentation, retrieved 2026-10-26): REST examples overview, REST inventory examples, REST events examples, GetAll RPC semantics, GetOne RPC semantics, error handling, connecting guide. Wire bindings are in [endpoints.md](endpoints.md).

## Common Sequences

- **Device inventory:** Read devices → Finish the stream.
- **Event evidence:** Read devices → Finish the stream → Read events → Finish the stream → Read one event (when a specific event needs detail).

## Read devices

Retrieve the device collection, or one device by its device identifier. The collection can be narrowed with an equality filter on fields such as streaming status or software version; every field given must match.
Success is a set of device records carrying identifier, software version, model, hostname, system MAC, boot time and streaming status. A device whose streaming status is active is sending telemetry; that says nothing about the health of its interfaces or protocols. A device absent from the result is not being reported to CloudVision, not a healthy device.

## Read events

Retrieve the event collection. Without time bounds the result reflects current state. With a start and end time (timestamps; exact accepted format is unverified, see endpoints.md), the result covers every event that was active at any point in that window, including events that began before the window and stayed active. Do not read the result as only events created inside the window.
An equality filter on severity and event type narrows the read; several filter objects are alternatives (OR), while several properties inside one object must all match (AND). Severity may be given as a number or as its enum name.
Success is event records with identifier, severity, title, description, event type and component references.

## Read one event

A single event is addressed by two values together: its key and its timestamp. Success is that one event with its state time. The event's key timestamp and the state time returned beside it are different values; do not substitute one for the other.

## Finish the stream

A collection read returns a stream of result messages, not one array, and delivers the first message as soon as it exists. The read is complete only when the stream ends normally. A failure to open the stream and a failure partway through are different errors; after a mid-stream failure the records already received are partial coverage and are reported as such, not as the full inventory or event list.
With a start time but no end, the stream carries the state as of the start followed by later changes (partial updates). Apply those changes to the record they identify; do not count them as additional devices or events.
Errors follow gRPC status conventions, with an HTTP mapping on the REST surface. The exact per-code mapping is not documented; report the native status and detail rather than treating any failure as an empty result.

## Patterns

- Credential: a service-account token; the accepted presentation forms are in endpoints.md. Unverified: token lifetime and whether a lost token can be re-displayed; assume it must be reissued.
- TLS: when the deployment uses a private certificate authority, trust that CA for the connection rather than disabling certificate verification.
- Hostnames: cloud-hosted and on-premises deployments are addressed differently; the form for each is in endpoints.md.
- The REST bindings exist from CloudVision 2021.1 onward. Unverified: which resources are present in a given release; confirm on the deployment.

## Known limitations

- Read-only. Device onboarding, decommissioning, tag assignment, change control and workspaces are outside this procedure.
- Not documented: rate limits and per-request result caps. On a throttling or server error, back off and retry later rather than looping.
- No comparison operation is covered; to compare, repeat the same read with the same time bounds and filters and diff the results outside the platform.

## Tools

| Operation | Description | Category |
|---|---|---|
| Read devices | Retrieve device inventory records | REST API |
| Read events | Retrieve current or time-bounded events | REST API |
| Read one event | Retrieve an event by key and timestamp | REST API |

## Verification checklist

- [ ] Target deployment (on-prem or regional cloud host) and trusted TLS connection are correct.
- [ ] Every stream ended normally, or the partial coverage is stated.
- [ ] Time-bounded reads are described as "active during the window", not "created during the window".
- [ ] Failures and empty results are reported as such, not as a healthy network.
