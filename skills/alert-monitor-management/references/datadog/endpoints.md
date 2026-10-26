# Endpoints — Datadog Monitor Creation & Downtime Management

Literal wiring layer. `procedure.md` steps reference these by name; bind them to whatever REST
client/adapter is assumed available.

## Create a Monitor

**Method/path (verbatim from the Datadog API reference):**

```
POST /api/v1/monitor
```

**Request body fields:**
- `type` (required) — one of the documented monitor types, e.g. `metric alert`, `query alert`,
  `service check`, `log alert`, `composite`, `event alert`, `process alert`, `rum alert`,
  `synthetics alert`, `trace-analytics alert`, `slo alert`, and several other more specialized
  values.
- `query` (required) — the type-appropriate detection expression, e.g. for a metric/query alert:
  an aggregation window, metric, optional scope/tags filter, comparison operator, and threshold
  (Datadog's own example: `avg(last_5m):sum:system.net.bytes_rcvd{host:host0} > 100`).
- `name` — display name.
- `message` — notification body text; this is also where `@`-mention notification targets go.
- `tags` — array of tag strings.
- `priority` — integer priority.
- `options` — object; commonly used fields: `notify_no_data` (bool), `no_data_timeframe`
  (integer minutes), `renotify_interval` (integer minutes), `renotify_statuses` (array of state
  strings), `evaluation_delay`, `require_full_window`, `thresholds` (per-severity threshold
  overrides: `critical`, `warning`, `ok`, `unknown`, plus `*_recovery`/`*_query` variants for
  some monitor types). The deprecated `silenced` field also lives here — do not set it (see
  `procedure.md`).

**Success:** HTTP 2xx with the created monitor object in the response body, including a numeric
`id`.

**Failure:** the sources do not document a fixed catalog of validation
error strings for this endpoint — surface the response body verbatim rather than fabricating a
specific error condition.

## Get a Monitor's Details

```
GET /api/v1/monitor/{monitor_id}
```

Returns the monitor object, including its current `overall_state`.

## Schedule a Downtime

**Method/path (verbatim from the Datadog API reference, v2 Downtimes resource):**

```
POST /api/v2/downtime
```

**Request body** — JSON:API-shaped, with the real content under `data.attributes`:
- `scope` (required) — a tag-query string, e.g. `env:(staging OR prod) AND datacenter:us-east-1`,
  or `*` for everything.
- `monitor_identifier` (required) — one of:
  - `{"monitor_id": <integer>}` — scope the downtime to one specific monitor, or
  - `{"monitor_tags": [<string>, ...]}` — scope the downtime to every monitor matching those tags.
- `message` — optional text shown with the downtime.
- `display_timezone` — optional, e.g. `America/New_York`.
- `schedule` — optional object; when omitted, the downtime is treated as starting immediately with
  no defined end. When present, carries the recurrence/start/end timing configuration.
- `mute_first_recovery_notification` — optional boolean.
- `notify_end_states` / `notify_end_types` — optional arrays controlling whether a
  downtime-ending notification is sent and for which states/reasons (e.g. `canceled`, `expired`).

**Success:** HTTP 2xx with the created downtime object (JSON:API shape) including its `id`.

**Failure:** not enumerated in the sources — surface the response body verbatim.

## Cancel a Downtime

```
DELETE /api/v2/downtime/{downtime_id}
```

Ends the downtime early. No request body. Treat a 2xx (including 204) as success.

## Deprecated — do not use for new work

- `POST /api/v1/monitor/{monitor_id}/mute` / `POST /api/v1/monitor/{monitor_id}/unmute` — legacy
  per-monitor mute mechanism tied to the deprecated `silenced` monitor field. Datadog's own
  documentation directs callers to the Downtimes API instead.
- `POST /api/v1/monitor/mute_all` / `POST /api/v1/monitor/unmute_all` — legacy, documented as
  deprecated; do not use.

**Authentication:** every call requires both a Datadog API key (`DD-API-KEY` header) and an
application key (`DD-APPLICATION-KEY` header) scoped to the target org/site.
