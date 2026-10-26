# Endpoints — Paessler PRTG Sensor Creation & Alarm Acknowledge

Literal wiring layer. `procedure.md` steps reference these by name; bind them to whatever REST/HTTP
client/adapter is assumed available. Base URL is instance-specific:
`https://<prtg-core-server>`.

## PRTG API v2 — create a sensor

**Method/path (per the PRTG API v2 documentation; the v2 Swagger/OpenAPI description confirms
this call under its `experimental` namespace, reflecting v2's own maturity labeling for some
resources):**

```
POST /api/v2/experimental/devices/{id}/sensor
```

`{id}` is the target device's object ID.

**Request body:** JSON object describing the sensor to create — the sensor type plus that type's
own required monitoring parameters (target address/OID/URL, polling interval, etc., per PRTG's
sensor-type documentation). Field names are sensor-type-specific; confirm against the current PRTG
API v2 Swagger UI reference for the exact schema of the chosen sensor type before submitting.

**Success:** HTTP 204 with a `Location` header pointing to the created sensor resource. May also
include a `Wait-For` header indicating how long to wait before the object is reliably readable.

**Failure:** not enumerated field-by-field in the sources — surface the response body
and status code verbatim.

## PRTG API v2 — acknowledge a sensor's alarm

```
POST /api/v2/sensors/{id}/acknowledge
```

**Request body:**
```json
{"duration": <minutes, optional>, "message": "<reason>"}
```
Omitting `duration` acknowledges indefinitely, per the field's optional status in the v2 schema —
confirm this is what the caller wants before omitting it (see `procedure.md` step 3).

**Success:** 2xx.

## PRTG API v2 — acknowledge multiple sensors by filter

```
POST /api/v2/sensors/acknowledge
```

**Request body:**
```json
{"filter": "<required filter expression>", "duration": <minutes, optional>, "message": "<reason>"}
```
`filter` is required for the bulk form — this acknowledges every currently-matching sensor's
alarm, not one specific sensor; confirm the filter's scope with the operator before submitting,
consistent with `procedure.md`'s confirmation guidance for broad suppression actions.

## PRTG API v2 — pause / resume a sensor

```
POST /api/v2/sensors/{id}/pause
POST /api/v2/sensors/{id}/resume
```

`pause` accepts the same `{"duration": ..., "message": ...}` body shape as acknowledge. Pausing
stops scanning entirely for the window — see `procedure.md` for why this is not a substitute for
acknowledge.

## Older HTTP API — acknowledge an alarm

**Method/path (per the PRTG Manual's HTTP API page and Paessler's own knowledge-base example):**

```
GET /api/acknowledgealarm.htm?id={objectid}&ackmsg={message}&duration={minutes}
```

Authentication parameters (`username`/`passhash`, `username`/`password`, or `apitoken`) are
appended as additional query parameters, per the HTTP API's documented authentication options
below. PRTG's manual documents several UI-level acknowledgment duration presets (5 minutes, 15
minutes, 1 hour, 3 hours, 1 day, indefinitely, or a specific "until" time); when calling the HTTP
API directly, express the chosen duration as the numeric `duration` parameter (minutes) rather than
one of the UI preset labels.

**Success:** HTTP 200; the older HTTP API does not return a structured success/failure body by
default for this call in the sources — treat a non-200 response, or an explicit PRTG
error page in the response body, as failure.

## Older HTTP API — pause / resume an object

```
GET /api/pause.htm?id={objectid}&pausemsg={message}&action=0
GET /api/pause.htm?id={objectid}&action=1
```

`action=0` pauses (with an optional `pausemsg`); `action=1` resumes. For a bounded pause instead of
indefinite:

```
GET /api/pauseobjectfor.htm?id={objectid}&pausemsg={message}&duration={minutes}
```

Supported object types for `pause.htm` are documented as: probe, group, device, sensor,
notification, user account.

## Older HTTP API — clone an object (documented workaround for "creating" a new object)

```
GET /api/duplicateobject.htm?id={source_object_id}&name={new_name}&targetid={target_id}
```

PRTG's own manual states plainly that creating brand-new objects from scratch isn't supported
through the v1 HTTP API because of the complexity of object parameters — the documented pattern
instead is cloning an existing object to serve as a template. A cloned object starts paused, which
allows adjusting its configuration before resuming it via `pause.htm?action=1`. This procedure's
main creation path uses API v2 instead (see above); this call is documented here only as the v1
fallback noted in `procedure.md`'s "Known limitations."

## Authentication (older HTTP API)

- `username={user}&password={pass}`, or
- `username={user}&passhash={hash}` — obtain the passhash via
  `GET /api/getpasshash.htm?username={user}&password={pass}`, or
- `apitoken={key}` (account-level API key, from Account Settings → API Keys).

## Authentication (API v2)

- `Authorization: Bearer {apikey}` (API key created in Account Settings), or
- `POST /api/v2/session` with username/password to establish a session, or
- SSO, if configured on the target PRTG instance.
