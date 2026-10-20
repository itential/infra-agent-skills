# Endpoints — Azure DevOps Pipeline Run

Literal wiring layer for `procedure.md`. All calls carry `api-version=7.1`.

Sources: Microsoft Learn Azure DevOps REST API 7.1 pages named in `procedure.md`; retrieved 2026-10-19.
Base: `https://dev.azure.com/{organization}/{project}`.

## Authentication

PAT via HTTP Basic: the username may be empty; Base64-encode `:{PAT}` and send
`Authorization: Basic <value>`. Scopes seen in the docs: `vso.build_execute` (run), `vso.build`
(read/cancel).

## Run pipeline

```
POST /_apis/pipelines/{pipelineId}/runs?api-version=7.1
```

Optional query `pipelineVersion`. Body keys: `previewRun` (bool; no run is created, final YAML is
returned), `resources`, `stagesToSkip` (string[]), `templateParameters` (object), `variables`
(`{name: {value, isSecret}}`), `yamlOverride` (only with preview). **Success:** `200` run object.

## Get run

```
GET /_apis/pipelines/{pipelineId}/runs/{runId}?api-version=7.1
```

`state`: `unknown`, `inProgress`, `canceling`, `completed`. `result`: `unknown`, `succeeded`,
`failed`, `canceled`.

## List logs (pipeline run)

```
GET /_apis/pipelines/{pipelineId}/runs/{runId}/logs?api-version=7.1
```

Optional `$expand`.

## Get log (pipeline run)

```
GET /_apis/pipelines/{pipelineId}/runs/{runId}/logs/{logId}?api-version=7.1
```

Optional `$expand` (`none`, `signedContent`).

## Get build log (build resource)

```
GET /_apis/build/builds/{buildId}/logs/{logId}?api-version=7.1
```

Optional `startLine`, `endLine`. Media types: `text/plain`, `application/json`, `application/zip`.

## Update build (cancel)

```
PATCH /_apis/build/builds/{buildId}?api-version=7.1
```

Body: build object with `status` set to `cancelling`. Build `status` values: `none`, `inProgress`,
`completed`, `cancelling`, `postponed`, `notStarted`, `all`.
