# Paessler PRTG — Sensor Creation & Alarm Acknowledge/Resolve Procedure

Creates a sensor (PRTG's monitor object) on a device already registered in PRTG, and manages the
lifecycle of the alarms it raises. PRTG ships two parallel APIs; this procedure uses the newer PRTG
API v2 for sensor creation (since PRTG's own v1 HTTP API documentation states outright that
creating brand-new objects from scratch isn't supported through it) and documents the
acknowledgment call on both APIs, since either may be what an existing integration expects.
Assumes an authenticated client against the target PRTG core server is already available (a
username/password or username/passhash pair for the older HTTP API; an API key sent as a Bearer
token, or a session login, for API v2 — see `endpoints.md` for the literal call).

Sources consulted (retrieved 2026-09-29): PRTG API v2 Overview
(https://www.paessler.com/support/prtg/api/v2/overview); PRTG Manual, "HTTP API"
(https://www.paessler.com/manuals/prtg/http_api); PRTG Manual, "Object Manipulation"
(https://www.paessler.com/manuals/prtg/object_manipulation); PRTG Manual, "Alarms"
(https://www.paessler.com/manuals/prtg/alarms); Paessler Knowledge Base, "Acknowledge a Warning"
(https://helpdesk.paessler.com/en/support/solutions/articles/76000075361-acknowledge-a-warning).
PRTG's own published API v2 OpenAPI/Swagger description was used only to cross-check the
acknowledge/pause request-body field names (`duration`, `message`) already indicated by the prose
sources above, never as a wording source.

## Operational procedure — create a sensor

1. **Confirm the target device already exists in PRTG.** A sensor is always created underneath an
   existing device object; this procedure does not cover device (or probe/group) creation. If the
   caller's target device doesn't exist yet, that's a prerequisite outside this skill's scope.
2. **Choose the sensor type.** PRTG ships a large library of built-in sensor types (e.g. ping,
   SNMP-based, WMI-based, HTTP-based, and many device/service-specific types), each with its own
   parameter set and its own default channel/threshold configuration. Confirm the exact sensor type
   the caller wants monitored — do not substitute a similarly-named type.
3. **Set the sensor's monitoring parameters** as required by the chosen type (e.g. target
   URL/OID/query, polling interval) — PRTG's manual documents these per sensor type; supply only
   what the caller specified plus whatever that sensor type requires to function, without inventing
   thresholds or intervals the caller didn't ask for.
4. **Submit the create-sensor call** against the target device's ID. See `endpoints.md`.
5. **Confirm creation.** PRTG API v2 documents that a successful creation returns HTTP 204 with a
   `Location` header identifying the new sensor, and may also return a `Wait-For` header
   indicating the object isn't necessarily queryable immediately — if the calling tool needs to
   confirm the sensor exists right away, respect that `Wait-For` value before polling rather than
   immediately retrying. Report `CREATED` with the sensor ID parsed from `Location`. On failure,
   report `FAILED` with the response body verbatim.
6. **A newly-created sensor typically starts in a paused or "unusual" (not-yet-scanned) state**
   until its first successful scan interval completes — do not report an alarm/error state as a
   creation failure if the sensor simply hasn't been polled yet; confirm status after at least one
   full scanning interval has elapsed.

## Operational procedure — acknowledge or resolve an alarm

1. **Confirm which API generation the caller's integration targets**, since PRTG documents
   acknowledgment on both:
   - **PRTG API v2:** acknowledge a specific sensor's alarm, or acknowledge every sensor matching a
     filter, via a dedicated acknowledge call that accepts an optional `duration` and `message`.
   - **Older HTTP API:** acknowledge via a parameter-based call (`acknowledgealarm.htm`) that
     PRTG's own manual documents as supporting several preset acknowledgment durations (5 minutes,
     15 minutes, 1 hour, 3 hours, 1 day, indefinitely, or a specific "until" time) plus a message.
2. **Acknowledging does not clear the alarm condition.** PRTG's own alarm handling documents
   acknowledgment as marking the alarm as seen/being handled and silencing further repeat
   notification for it — the sensor's underlying channel value still has to return within its
   configured limits for the sensor to actually leave its Down/alarm state. Do not represent
   acknowledgment as resolution.
3. **Choose a duration deliberately.** An indefinite acknowledgment silences the alarm's repeat
   notifications until someone manually reverses it or the underlying condition changes the
   sensor's status outright — **stop and confirm with the operator before acknowledging
   indefinitely** on a sensor where the caller hasn't specified how long the issue is expected to
   take to fix; prefer a bounded duration (e.g. one of PRTG's documented presets) when the caller
   hasn't been explicit.
4. **Submit the acknowledge call** with a real message describing why (`ackmsg`/`message` — do not
   submit an empty or placeholder value) and the chosen duration. See `endpoints.md`. Report
   `ACKNOWLEDGED` on success.
5. **There is no separate manual "resolve" call for a PRTG sensor's alarm.** Per PRTG's own alarm
   model, a sensor leaves its Down/alarm state once its monitored channel value is back within the
   configured limits — this happens automatically on a later scan, not via an API call. If the
   caller wants the alarm state cleared immediately regardless of the actual measured value, that
   is not something PRTG's documented API supports; say so rather than fabricating an endpoint.
6. **Pausing is a distinct, stronger action from acknowledging** — pausing (`pause.htm`, or the API
   v2 pause call) stops the sensor from being scanned/evaluated at all for the pause window, rather
   than just silencing notifications for an existing alarm. Do not substitute pause for acknowledge
   or vice versa without the caller specifically asking for that stronger suppression; pausing a
   sensor to "resolve" an alarm hides the underlying problem from monitoring entirely rather than
   addressing it.

## Patterns

- **API v2 responses defer object availability via `Wait-For`.** Treat this as a real instruction,
  not an incidental header — a follow-up read immediately after creation may legitimately 404 or
  return stale data before that window elapses.
- **The older HTTP API's duration presets are UI-driven language, not raw parameter names** — when
  building the literal call, use the numeric/duration parameter PRTG's HTTP API documents (see
  `endpoints.md`), not the preset labels themselves.

## Known limitations

- Creating a brand-new device or probe is out of scope — sensor creation in this procedure assumes
  the target device already exists.
- PRTG's v1 HTTP API documentation states directly that creating new objects from scratch isn't
  supported through that API — its own documented workaround is cloning an existing "template"
  object (`duplicateobject.htm`) rather than defining one from nothing. This procedure uses API v2
  for creation instead, per the sources consulted, precisely because v2 does document direct
  creation; if a target PRTG instance's API v2 surface is unavailable or disabled, the v1
  clone-a-template pattern is the documented fallback, but is out of scope for this procedure's
  step-by-step since it depends on an existing template object the caller would need to identify.
- No documented API call forces a sensor's alarm to clear ahead of its next scan returning a
  within-limits value — see step 5 above.

## Tools

| Operation | Description | Category |
|---|---|---|
| Create sensor on device (API v2) | Add a new sensor of a given type under an existing device | Sensors |
| Get sensor | Confirm sensor state/config after creation, respecting `Wait-For` | Sensors |
| Acknowledge sensor alarm (API v2) | Silence repeat notification for one sensor's active alarm | Sensors |
| Acknowledge alarm (HTTP API, `acknowledgealarm.htm`) | Same action via the older parameter-based API | Sensors |
| Pause sensor | Stop scanning/evaluating a sensor entirely for a window (distinct from acknowledge) | Sensors |

## Verification checklist

- [ ] Target device confirmed to already exist before attempting sensor creation
- [ ] Sensor type matched exactly what the caller asked to monitor
- [ ] Creation confirmed via the `Location` header (API v2), respecting any `Wait-For` delay before
      a follow-up read
- [ ] Acknowledge duration chosen deliberately — indefinite only after confirming with the operator
      when the caller didn't specify a timeframe
- [ ] Acknowledge included a real, non-placeholder message
- [ ] Acknowledge was not represented as resolving the alarm, and pause was not substituted for
      acknowledge
- [ ] Outcome reported using this skill's status vocabulary (`CREATED`, `ACKNOWLEDGED`, `FAILED`),
      with the response body verbatim on failure
