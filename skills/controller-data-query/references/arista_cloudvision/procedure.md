# CloudVision inventory, event and probe observations

Read CloudVision Resource API device inventory, active/historical events and existing Connectivity Monitor statistics.

Sources: Arista [REST inventory](https://aristanetworks.github.io/cloudvision-apis/examples/REST/inventory/), [events](https://aristanetworks.github.io/cloudvision-apis/examples/REST/events/), [GetAll semantics](https://aristanetworks.github.io/cloudvision-apis/rpcs/getall), [error handling](https://aristanetworks.github.io/cloudvision-apis/rpcs/errors), [connection guidance](https://aristanetworks.github.io/cloudvision-apis/connecting), [probe schema](https://github.com/aristanetworks/cloudvision-apis/blob/trunk/arista/connectivitymonitor.v1/connectivitymonitor.proto), current trunk retrieved 2026-10-09. Bindings are in [endpoints.md](endpoints.md).

## Common Sequences

- Inventory snapshot: Read inventory → Complete the response stream.
- Event evidence: Read inventory → Complete the response stream → Read events → Complete the response stream → Read selected event.
- Probe evidence: Read inventory → Complete the response stream → Read probe statistics → Complete the response stream.

### Read inventory

The device collection returns device identifiers, reported identity/software/model fields and telemetry streaming state. An optional equality filter narrows the read to actively streaming devices, optionally with a software version. Success is the scoped device records with native state/timestamps. Streaming active means telemetry streaming, not that every service or interface is healthy.

### Read events

The event collection returns current active events by default. Optional time bounds retrieve state that existed within that interval, including events that began earlier and remained active. Filtering uses documented equality fields such as native severity and event type. Success is event evidence retaining identifiers, descriptions, severity and component references; custom policy thresholds are not universal defaults.

### Read selected event

An event's identity contains both its key and its key timestamp; the single-event read uses both. Success is that identified event and its state timestamp. The event identity timestamp and resource state timestamp are different values.

### Read probe statistics

Existing probe statistics are keyed by device, destination host, VRF and source interface. Success is the returned latency/jitter/HTTP-response measurements in milliseconds, loss percentage and reported probe error. An error or missing measurement remains explicit; zero loss is not fabricated for an unavailable probe. This read does not create or run a new probe.

### Complete the response stream

Collection responses are streams of result envelopes, not one JSON array. Completion requires a normal end of the stream. The publisher distinguishes stream initialization failure, mid-stream failure and normal completion: a broken stream leaves partial evidence. Time-bounded state/history can include subsequent partial changes; these are applied to the identified resource rather than counted as independent devices or events. A current snapshot avoids inventing a history model.

The publisher maps API failures to standard gRPC status conventions, with HTTP mappings for REST. Native code/detail is retained for failed reads; authentication/access, invalid input, missing resource or transport problems do not become empty successful inventory.

## Patterns

- A time interval includes records already active at its beginning, not only newly created records.
- Single-record and streamed-collection envelopes differ.
- Publisher REST examples disable TLS validation. That example setting is unsafe for token-bearing production requests; the documented connection guidance also supports a trusted custom CA, which this procedure assumes.

## Known limitations

- REST Resource bindings require CloudVision 2021.1 or later and the selected resource in the deployed release.
- Tag creation/assignment, workspaces, builds, change controls and device onboarding are excluded.
- Inventory state does not prove tag assignment. No fixed ten-second build wait from the source wrapper is retained.

## Tools

| Operation | Description | Category |
|---|---|---|
| Read inventory | Retrieve reported device records | Read |
| Read events | Retrieve current or time-bounded events | Read |
| Read selected event | Retrieve the record identified by key and timestamp | Read |
| Read probe statistics | Retrieve existing per-interface probe measurements | Read |

## Verification checklist

- Target tenant/region and trusted TLS connection are correct.
- Native identifiers, scope, timestamps and streaming state remain visible.
- Every stream completed normally or partial coverage is explicit.
- Probe errors/missing measurements remain distinct from measured zero values.
