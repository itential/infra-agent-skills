# Endpoints — Rundeck Job Execution

Literal wiring layer for `procedure.md`. `{v}` is the API version (examples use 17+).

Sources: docs.rundeck.com/docs/api/ sections named in `procedure.md`; retrieved 2026-10-19.
Base: `https://{rundeck-host}`.

## Authentication

API token in header `X-Rundeck-Auth-Token` (a URL parameter `authtoken` also works but exposes the
token in URLs — prefer the header). Password login via a session cookie exists but is not used here.

## Run job

```
POST /api/{v}/job/{id}/run      (equivalent: POST /api/12/job/{id}/executions)
```

Body (JSON; ignores query parameters when `Content-Type: application/json`): `argString`, `loglevel`,
`asUser`, `filter`, `runAtTime` (ISO-8601 with zone), `options` (map; API v18+). Query form:
`argString`, `loglevel`, `asUser`, `filter`, `runAtTime`, `option.NAME`, `meta.KEY`.

## Get execution

```
GET /api/{v}/execution/{id}
```

`status`: `succeeded`, `failed`, `aborted`, `timedout`, `retried`, `other`. Also `date-started`,
`date-ended`, `successfulNodes`, `failedNodes`.

## Get execution output

```
GET /api/{v}/execution/{id}/output
GET /api/{v}/execution/{id}/output/node/{node}
GET /api/{v}/execution/{id}/output/step/{stepctx}
GET /api/{v}/execution/{id}/output/node/{node}/step/{stepctx}
```

JSON or plain text; incremental-read parameters exist for tailing a running execution.

## Abort execution

```
GET /api/{v}/execution/{id}/abort?forceIncomplete=
```

Response `abort.status`: `pending`, `failed` (with `reason`), `aborted`.

## Retry execution

```
POST /api/{v}/job/{id}/retry/{execid}      (API v24+)
```
