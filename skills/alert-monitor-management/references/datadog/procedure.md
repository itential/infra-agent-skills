# Datadog — Monitor Creation & Alert Acknowledge/Resolve Procedure

Creates a monitor on Datadog and manages the lifecycle of alerts it raises by scheduling or
canceling a downtime against it. Covers the Monitors API (v1) for creation and the Downtimes API
(v2) for suppression/acknowledgment. Assumes an authenticated REST client against the Datadog API
(an API key plus an application key, both scoped to the target Datadog org/site) is already
available.

Sources (retrieved 2026-09-29): Datadog API reference, "Monitors" section
(https://docs.datadoghq.com/api/latest/monitors/); Datadog API reference, "Downtimes" section
(https://docs.datadoghq.com/api/latest/downtimes/); Datadog "Monitor API Options" guide
(https://docs.datadoghq.com/monitors/guide/monitor_api_options/); Datadog's published OpenAPI
description of the v1 Monitors resource and v2 Downtimes resource, for field names.

## Operational procedure — create a monitor

1. **Choose the monitor type.** Datadog's Monitors API distinguishes several evaluation types
   (metric threshold, log-based, APM trace-analytics, service check, composite of other monitors,
   and several more specialized types). Confirm which one matches the caller's request — the
   `type` field is required and there is no generic fallback type.
2. **Build the query and alert message.** A monitor's `query` field holds the actual
   condition-detection expression appropriate to its type (e.g. a metric aggregation with a
   comparison operator and threshold for a metric-alert type). The `message` field is the text
   shown/sent when the monitor changes state — this is also where Datadog's `@`-mention
   notification-target syntax goes, if the caller specifies where to notify; do not invent a
   notification target that wasn't given.
3. **Set monitor options relevant to the request** — most commonly: `notify_no_data` (whether the
   monitor should alert when its query stops returning data) paired with `no_data_timeframe`
   (minutes of missing data before that no-data alert fires), and `renotify_interval` (minutes
   between repeat notifications while a monitor stays in a non-OK state) paired with
   `renotify_statuses` (which states re-trigger notification — Datadog defaults this to alert and
   no-data states). Only set what the caller actually asked for; do not default thresholds or
   renotification behavior the caller didn't specify.
4. **Do not set the `silenced` option.** It is documented as deprecated (kept only for backward
   compatibility with an older, v1-only downtime mechanism) — see "Suppress or acknowledge an
   alert" below for the current mechanism.
5. **Submit the create call** with `type` and `query` at minimum (both required), plus `name`,
   `message`, `tags`, `priority`, and `options` as applicable. See `endpoints.md` for the literal
   call.
6. **Confirm creation** — a successful response returns the created monitor object including a
   numeric `id`. Report `CREATED` with that id. If the call fails, report `FAILED` with the
   response body verbatim rather than guessing at the cause — the sources do not
   enumerate every possible validation-error string.

## Operational procedure — suppress, acknowledge, or resolve an alert

1. **Confirm which action the caller actually wants**, because Datadog does not offer a single
   "acknowledge" call the way some other platforms do:
   - To silence notifications for a monitor (with or without narrowing to a specific scope, e.g.
     one host or tag combination) while someone works the underlying issue, use a **downtime** —
     this is the current, documented mechanism and is the closest equivalent to "acknowledge" on
     this platform.
   - To force a monitor back to a non-alerting state outright, Datadog's own monitor-options
     guidance describes a UI/monitor-level "resolve" behavior intended specifically for monitors
     whose data reporting has stopped (so the monitor can no longer naturally re-evaluate back to
     OK) — this is not the same as acknowledging a still-actively-breaching monitor, and the
     sources do not document a corresponding API call distinct from the
     downtime/data-driven mechanisms above. If the caller needs this specific behavior, say so
     explicitly rather than fabricating an endpoint.
   - Outright resolution of a monitor that is still actively breaching its threshold is not
     something either mechanism does — the monitor returns to OK on its own once the underlying
     query result is no longer in violation (see `SKILL.md`'s universal concepts).
2. **Schedule a downtime** — build the request with the two required attributes: `scope` (a
   Datadog tag-query string identifying what the downtime applies to, e.g. a host, tag, or `*` for
   everything) and `monitor_identifier` (either a specific `monitor_id` to scope the downtime to
   one monitor, or a `monitor_tags` list to scope it to every monitor matching those tags). Add
   `message` (shown alongside the downtime) and a `schedule` object if the caller wants a
   recurring or specifically-timed window rather than "starting now, open-ended."
3. **This is a live suppression of alert notifications — stop and confirm with the operator
   before scheduling a downtime**, especially one with a broad `scope` (e.g. `*` or a tag that
   matches many resources) or no end time. A downtime silences every notification within its
   scope for its full duration, not just for the specific alert the caller may have had in mind.
4. **Submit the create-downtime call.** See `endpoints.md` for the literal call and body shape.
5. **Confirm scheduling** — a successful response returns the created downtime object including
   its `id`. Report `ACKNOWLEDGED` (as the closest available status in this skill's vocabulary) with
   that id.
6. **To end suppression early ("un-acknowledge")**, cancel the downtime by its `id`. Report
   `RESOLVED` once the cancel call succeeds — this only ends the suppression window; it does not
   and cannot force the monitor's own state, which is separately driven by the query result (see
   step 1).

## Patterns

- **Monitor and downtime are two different objects, on two different API versions.** A common
  mistake is looking for a mute/unmute field on the monitor itself — that mechanism still exists
  in the API surface but is documented as deprecated; new work should always go through the
  Downtimes API.
- **A downtime's `monitor_identifier` decides the blast radius, not just `scope`.** Omitting
  `monitor_id` in favor of only `monitor_tags` (or an unrestricted scope) will suppress every
  currently- and future-matching monitor, not just the one the caller had in mind — always confirm
  which the caller intended before submitting.

## Known limitations

- No documented API call exists (per the sources) to force a specific,
  still-actively-breaching monitor back to OK on demand — only downtime-based notification
  suppression and the data-driven no-data "resolve" behavior described above. Do not represent a
  downtime as having resolved the underlying condition; it only stops notifications.
- Monitor `type` values documented include several categories not covered in operational depth
  here (log-based, APM, RUM, synthetics, composite, and several more) — this procedure covers the
  fields common to monitor creation generally; type-specific query syntax is out of scope and
  should be validated against the caller's actual monitor type before submission.
- Creating the notification-target list beyond what's embedded in `message` (e.g. configuring a
  new Slack/PagerDuty integration) is out of scope — see `SKILL.md`'s "Known limitations."

## Tools

| Operation | Description | Category |
|---|---|---|
| Create a Monitor | Create a new monitor definition | Monitors |
| Get a monitor's details | Confirm current monitor state/config after creation | Monitors |
| Schedule a Downtime | Suppress notifications for a monitor/scope for a window | Downtimes |
| Cancel a Downtime | End an active downtime early | Downtimes |

## Verification checklist

- [ ] Monitor `type` and `query` matched what the caller actually asked to monitor, not a guessed
      default
- [ ] `silenced` was not used — downtimes are the mechanism for suppression
- [ ] Before scheduling a downtime: confirmed with the operator, especially for broad `scope` or an
      open-ended window
- [ ] `monitor_identifier` was set deliberately (specific monitor vs. tag-matched set), not left to
      default to the widest possible match
- [ ] Outcome reported using this skill's status vocabulary (`CREATED`, `ACKNOWLEDGED`, `RESOLVED`,
      `FAILED`), with the actual response body on failure
