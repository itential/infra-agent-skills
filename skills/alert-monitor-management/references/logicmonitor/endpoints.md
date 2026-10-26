# Endpoints — LogicMonitor DataSource/AlertRule Creation & Alert Acknowledge

Literal wiring layer. `procedure.md` steps reference these by name; bind them to whatever REST
client/adapter is assumed available. Base URL is portal-specific:
`https://<portal-name>.logicmonitor.com/santaba/rest`.

## Import a DataSource from XML

**Method/path (verbatim from the LogicMonitor REST API v1 reference):**

```
POST /setting/datasources/importxml
```

**Request:** `multipart/form-data`, with the DataSource's exported/authored XML file attached as
the form part (LogicMonitor's own example curl usage names the field inline with the file
attachment rather than a separate named parameter — consult the current reference page for the
exact multipart field name at call time).

**Success:** a response confirming the DataSource was created/updated, including its identifier.

**Failure:** not enumerated in the sources — surface the response body verbatim.

## Get DataSources

```
GET /setting/datasources
```

Used to confirm an import landed, or to look up an existing DataSource's ID/datapoint set before
building an Alert Rule against it.

## Add Alert Rules

**Method/path (verbatim from the LogicMonitor REST API v1 reference):**

```
POST /setting/alert/rules
```

**Request body fields** (per the LogicMonitor REST API v1 reference and v3 resource
cross-check):
- `name` (required)
- `priority` — integer; lower numbers are evaluated first against incoming alerts.
- `levelStr` — the alert severity this rule applies to (documented default is "All" when not set).
- `datasource` — the DataSource name/filter this rule matches against.
- `instance` — instance-name filter, where the DataSource has instances.
- `datapoint` — the specific datapoint name filter.
- `devices` / device-group and resource-property filters — which resources this rule applies to.
- `escalatingChainId` — the ID of the existing escalation chain that actually delivers
  notifications for alerts this rule matches.
- `escalationInterval` — time between escalation steps.
- `suppressAlertClear` — whether to suppress the "alert cleared" notification for alerts this rule
  matches.

**Success:** the created alert rule object, including its identifier.

**Failure:** not enumerated in the sources — surface the response body verbatim.

## Get Alert Rules

```
GET /setting/alert/rules
```

Used to review existing rule priority ordering before adding a new one.

## Acknowledge an Alert

**Method/path (verbatim from the LogicMonitor REST API v1 reference; confirmed present in the v3
resource cross-check at `/alert/alerts/{id}/ack`):**

```
POST /alert/alerts/{id}/ack
```

`{id}` is the alert's `id` or `internalId`.

**Request body:**
```json
{"ackComment": "<reason the alert is being acknowledged>"}
```
`ackComment` is required — LogicMonitor's own documentation states the acknowledge call must
include this comment.

**Success:** the updated alert object reflecting the acknowledgment.

**Failure:** not enumerated in the sources — surface the response body verbatim.

## Add a note to an alert (related, not acknowledgment)

```
POST /alert/alerts/{id}/note
```

Adds an annotation without changing acknowledgment state — documented as a separate action from
acknowledge; do not use this call when the caller actually wants to acknowledge.

**Authentication:** every call requires LogicMonitor's documented HMAC-SHA256 request signature,
built from an Access ID/Access Key pair and sent via the `Authorization` header, or an equivalent
Bearer token where the portal is configured for it. Requests should also specify API version 3 via
either a `?v=3` query parameter or an `X-Version: 3` header, per LogicMonitor's own versioning
guidance, unless the caller specifically needs v1/v2 response shapes.
