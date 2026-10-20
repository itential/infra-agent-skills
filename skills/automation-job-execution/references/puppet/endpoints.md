# Endpoints — Puppet Enterprise Orchestrator Job Execution

Literal wiring layer for `procedure.md`.

Sources: help.puppet.com PE "current" (2026.0) orchestrator API pages named in `procedure.md`;
retrieved 2026-10-19. Base: `https://{puppet-server}:8143/orchestrator/v1`.

## Authentication

RBAC token in the `X-Authentication` request header (the docs obtain it with `puppet-access show`).
Content type for commands is `application/json`.

## Run task

```
POST /command/task
```

Body: `environment`, `task` (required), `params` (required, may be `{}`), `scope` (required; exactly
one of `nodes` array / `query` / `node_group` id), `targets` (required array; per-entry `hostnames`
plus connection keys), optional `description`, `noop`, `timeout`, `userdata`. **Success:** `202`
`{"job": {"id": "<url>", "name": "<job-id>"}}`. **Errors (`kind`):**
`puppetlabs.orchestrator/unknown-environment` (404), `puppetlabs.orchestrator/empty-target` (400),
`puppetlabs.orchestrator/puppetdb-error`.

## Run plan

```
POST /command/plan_run
```

Body: `plan_name` (required), `params`, `environment`, `description`, `timeout`, `userdata`. A variant
for a specified environment exists (`/command/environment_plan_run`).

## Get job

```
GET /jobs/{job-id}
```

Keys: `state` (`new`, `ready`, `running`, `stopping`, `stopped`, `finished`, `failed`), `type`,
`timestamp`, `started_timestamp`, `finished_timestamp`, `duration`, `node_count`, links to `nodes`,
`report`, `events`.

## Get job nodes

```
GET /jobs/{job-id}/nodes?limit=&offset=&order_by=&order=&state=
```

## Get job report

```
GET /jobs/{job-id}/report
```

`items[]` with `node` and per-node `state`.

## Stop job

```
POST /command/stop
```

Body: `{"job": "<id>"}`; add `"force": true` to end in-progress runs immediately. **Success:** `202`
with the job and node-status counts. **Errors:** `puppetlabs.orchestrator/validation-error` (400),
`puppetlabs.orchestrator/unknown-job` (404).
