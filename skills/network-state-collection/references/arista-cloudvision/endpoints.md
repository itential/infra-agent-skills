# Arista CloudVision — State Collection Wiring

Sources (Arista CloudVision APIs documentation, retrieved 2026-10-26): REST inventory examples, REST events examples, connecting guide. Placeholders: `{host}`, `{access_token}`, `{device_id}`, `{event_key}`, `{event_timestamp}`.

Base: `https://{host}` on port 443. Cloud-hosted deployments use the regional hostname with the `www` prefix.

## Authentication

| Method | Form | Notes |
|---|---|---|
| Service-account token as cookie | `access_token={access_token}` | Shown in the inventory examples |
| Service-account token as bearer | `Authorization: Bearer {access_token}` | Shown in the events examples |

## Calls

| Operation | Method and path | Notes |
|---|---|---|
| Read devices (all) | `GET /api/resources/inventory/v1/Device/all` | Streamed JSON |
| Read devices (filtered) | `POST /api/resources/inventory/v1/Device/all` | Body `{"partialEqFilter":[{"streamingStatus":"STREAMING_STATUS_ACTIVE"}]}`; `softwareVersion` can join the same object |
| Read one device | `GET /api/resources/inventory/v1/Device?key.deviceId={device_id}` | |
| Read events (all) | `GET /api/resources/event/v1/Event/all` | Optional query `time.start`, `time.end` |
| Read events (filtered) | `POST /api/resources/event/v1/Event/all` | Body `partialEqFilter` array; fields `severity`, `eventType` |
| Read one event | `GET /api/resources/event/v1/Event?key.key={event_key}&key.timestamp={event_timestamp}` | Both key parts required |

## Response shape

Streamed reads return one JSON object per line, each with `result` wrapping `value`, `time` and `type`. Single reads return `value` and `time`. Device fields include `key.deviceId`, `softwareVersion`, `modelName`, `hostname`, `systemMacAddress`, `bootTime`, `streamingStatus`. Event fields include `key.key`, `key.timestamp`, `severity`, `title`, `description`, `eventType`, `components`.

## Unverified

- Exact timestamp format accepted by `time.start`/`time.end` beyond "ISO 8601 style".
- Whether the unfiltered `GET .../all` calls also accept `time.start`/`time.end` for devices; only events show it in the pages read.
- HTTP status values returned for each gRPC error code.
