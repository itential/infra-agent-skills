# CloudVision Resource REST bindings

Sources: Arista [inventory examples](https://aristanetworks.github.io/cloudvision-apis/examples/REST/inventory/), [event examples](https://aristanetworks.github.io/cloudvision-apis/examples/REST/events/), [probe REST schema](https://github.com/aristanetworks/cloudvision-apis/blob/trunk/arista/connectivitymonitor.v1/services.gen.swagger.json), retrieved 2026-10-09.

Base: `https://<cloudvision-host>` on 443. CVaaS uses the tenant's regional hostname; the publisher requires the `www` prefix for its supported CVaaS URLs. Published REST examples support service-account token via cookie `access_token=<token>` and via `Authorization: Bearer <token>`. TLS verification uses the appropriate trusted CA, not the examples' `-k`/`verify=False` shortcuts.

| Operation | Binding | Inputs |
|---|---|---|
| Device collection | `GET /api/resources/inventory/v1/Device/all` | Current state; optional historical time bounds require history handling |
| Filtered devices | `POST /api/resources/inventory/v1/Device/all` | Body `{"partialEqFilter":[{"streamingStatus":"STREAMING_STATUS_ACTIVE"}]}`; optional `softwareVersion` in same filter |
| Single device | `GET /api/resources/inventory/v1/Device?key.deviceId=<id>` | Returned device identifier |
| Current events | `GET /api/resources/event/v1/Event/all` | Optional `time.start`, `time.end` RFC3339 timestamps |
| Filtered events | `POST /api/resources/event/v1/Event/all` | `partialEqFilter` array; fields `severity`, `eventType` |
| Single event | `GET /api/resources/event/v1/Event?key.key=<key>&key.timestamp=<timestamp>` | Both key components |
| Probe statistics | `GET /api/resources/connectivitymonitor/v1/ProbeStats/all` | Current collection |

Single reads return `value` and `time`; streamed reads return newline-separated JSON `result` envelopes with `value`, `time`, `type`. Device fields include `key.deviceId`, `softwareVersion`, `modelName`, `hardwareRevision`, `fqdn`, `hostname`, `domainName`, `systemMacAddress`, `bootTime`, `streamingStatus`. No management-IP field is promised by the Device model.

Probe keys: `deviceId`, `host`, `vrf`, `sourceIntf`. Measurements: `latencyMillis`, `jitterMillis`, `httpResponseTimeMillis`, `packetLossPercent`, `error`. Event fields include `key.key`, `key.timestamp`, `severity`, `title`, `description`, `eventType`, `data`, `components`; resource `time` is separate from key timestamp.

The source error guide uses standard gRPC code/details and corresponding HTTP mappings, without a per-resource universal retry count. A transport failure after some envelopes is incomplete collection coverage.
