# Endpoint Wiring — Kubernetes (apps/v1 Deployment) Workload Deployment

Literal API calls behind each capability named in `kubernetes/procedure.md`. All calls are against a
Kubernetes API server, group `apps`, version `v1`, JSON bodies unless noted. Source: kubernetes.io
Deployment v1 API reference and "API Concepts" reference, both retrieved 2026-09-29.

## Create a Deployment

`POST /apis/apps/v1/namespaces/{namespace}/deployments`

Body: a full Deployment object (`apiVersion: apps/v1`, `kind: Deployment`, `metadata`, `spec` — see
`procedure.md` step 3 for the field list). Response `201` returns the stored object, including
server-assigned `metadata.uid` and the initial `metadata.resourceVersion`.

## Read a Deployment

- `GET /apis/apps/v1/namespaces/{namespace}/deployments/{name}` — one Deployment.
- `GET /apis/apps/v1/namespaces/{namespace}/deployments` — list within a namespace.
- `GET /apis/apps/v1/deployments` — list across all namespaces.
- Append `?watch=true` to either list form for a streaming watch instead of a point-in-time list.

## Update a Deployment

- `PUT /apis/apps/v1/namespaces/{namespace}/deployments/{name}` — full replace; body must be the
  complete object including the current `metadata.resourceVersion` (omitting or mismatching it
  produces the `Conflict` error in procedure.md step 9).
- `PATCH /apis/apps/v1/namespaces/{namespace}/deployments/{name}` — partial update. `Content-Type`
  selects the patch semantics:
  - `application/json-patch+json` — RFC 6902 JSON Patch; body is an array of `{op, path, value}`
    operations (`add`/`remove`/`replace`/`move`/`copy`/`test`).
  - `application/merge-patch+json` — RFC 7386 JSON Merge Patch; body is a partial object merged
    recursively into the existing one, `null` deletes a field.
  - `application/strategic-merge-patch+json` — Kubernetes-specific; behaves like merge patch but
    understands per-field merge/replace semantics for known list fields (e.g. `containers` merged by
    `name` rather than replaced wholesale). This is what `kubectl` uses by default.
  - `application/apply-patch+yaml` (or `+json`) — Server-Side Apply; requires a `?fieldManager=<name>`
    query parameter identifying the caller, and accepts an optional `&force=true` to take ownership of
    fields another manager currently owns (otherwise a field-ownership conflict returns `409` with
    `reason: Conflict` and a message naming the competing field manager).

## Delete a Deployment

`DELETE /apis/apps/v1/namespaces/{namespace}/deployments/{name}`

Optional body (`DeleteOptions`) or query param `propagationPolicy`: `Foreground` | `Background` |
`Orphan` (see procedure.md step 8 for the behavioral difference). Optional `gracePeriodSeconds` query
param/body field to control how long owned Pods are given to terminate.

## Scale subresource

- `GET /apis/apps/v1/namespaces/{namespace}/deployments/{name}/scale`
- `PUT /apis/apps/v1/namespaces/{namespace}/deployments/{name}/scale`
- `PATCH /apis/apps/v1/namespaces/{namespace}/deployments/{name}/scale` (same content-type choices as
  the main object's PATCH, above)

Body/response is an `autoscaling/v1` `Scale` object:

```
apiVersion: autoscaling/v1
kind: Scale
metadata:
  name: <deployment-name>
  namespace: <namespace>
  resourceVersion: <current version, for optimistic concurrency on write>
spec:
  replicas: <desired count>        # required on write
status:
  replicas: <current count>
  selector: <string-form label selector>
```

## Status subresource

- `GET /apis/apps/v1/namespaces/{namespace}/deployments/{name}/status`
- `PUT` / `PATCH` on the same path — present for completeness; automation should read status via GET
  and drive changes through the spec (create/update/scale) rather than writing status fields directly.

## Useful query parameters (apply to create/update/patch/delete calls generally)

| Param | Values | Effect |
|---|---|---|
| `dryRun` | `All` | Validates/simulates the request without persisting it |
| `fieldValidation` | `Strict` \| `Warn` \| `Ignore` | Controls whether unknown/duplicate body fields are rejected, warned on, or silently dropped |
| `fieldManager` | any string | Identifies the caller for Server-Side Apply field ownership tracking |
| `force` | `true` | On a Server-Side Apply PATCH, takes ownership of conflicting fields instead of erroring |

## Error/Status object shape

Every non-2xx response body:

```json
{
  "kind": "Status",
  "apiVersion": "v1",
  "status": "Failure",
  "message": "human-readable description",
  "reason": "NotFound | AlreadyExists | Conflict | Invalid | Unauthorized | Forbidden | ...",
  "code": 404
}
```

`reason` is the machine-readable field to branch logic on; `code` mirrors the HTTP status.

## Deployment spec field reference (fields covered by this skill)

| Field | Required | Notes |
|---|---|---|
| `spec.replicas` | no (defaults to 1) | Desired pod count — set explicitly for automation |
| `spec.selector.matchLabels` | yes | Immutable after create; must match `spec.template.metadata.labels` |
| `spec.template` | yes | Pod template (`metadata.labels`, `spec.containers[]`, etc.) |
| `spec.strategy.type` | no (`RollingUpdate` default) | `RollingUpdate` or `Recreate` |
| `spec.strategy.rollingUpdate.maxSurge` | no (25% default) | Extra pods allowed above `replicas` mid-rollout |
| `spec.strategy.rollingUpdate.maxUnavailable` | no (25% default) | Pods allowed unavailable mid-rollout |
| `spec.minReadySeconds` | no (0 default) | Seconds a new pod must stay healthy before counting as available |
| `spec.progressDeadlineSeconds` | no (600 default) | Time budget before a stalled rollout is marked `ProgressDeadlineExceeded` |
| `spec.revisionHistoryLimit` | no (10 default) | Old ReplicaSets retained for rollback |
| `spec.paused` | no (false default) | Creates/leaves the rollout paused |

## Deployment status field reference

| Field | Meaning |
|---|---|
| `status.observedGeneration` | Last `metadata.generation` the controller has reconciled — compare before trusting other status fields |
| `status.replicas` | Total non-terminating pods currently targeted |
| `status.updatedReplicas` | Pods running the current template |
| `status.readyReplicas` | Pods passing their readiness check |
| `status.availableReplicas` | Pods ready for at least `minReadySeconds` |
| `status.unavailableReplicas` | Pods still needed to reach full capacity |
| `status.conditions[].type` | `Progressing` or `Available` |
| `status.conditions[].reason` | e.g. `NewReplicaSetAvailable`, `ProgressDeadlineExceeded`, `MinimumReplicasAvailable` |

## Revision tracking (for rollback, procedure.md step 7)

Each ReplicaSet the Deployment has owned carries an annotation `deployment.kubernetes.io/revision`
with an incrementing integer. There is no dedicated "rollback" API call on the Deployment object
itself — a rollback is performed by reading the target ReplicaSet's `spec.template` and PATCHing it
back into the Deployment's own `spec.template` (see procedure.md step 7).
