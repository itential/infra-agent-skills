# Kubernetes (apps/v1 Deployment) — Container Workload Deployment Procedure

Create, scale, update, or delete a workload managed as an `apps/v1` Deployment against a Kubernetes
API server. Covers plain Deployments only — StatefulSet, DaemonSet, Job, and bare Pod management are
out of scope, since each has different lifecycle semantics this procedure doesn't address. Assumes an
authenticated Kubernetes API client (bearer token, client certificate, or equivalent already
established) with RBAC permission on the `deployments` resource (and its `scale`/`status`
subresources) in the target namespace.

Grounding: Kubernetes documents a resource-independent set of API conventions that apply to every
object type, not just Deployments — optimistic concurrency via `metadata.resourceVersion`, a shared
`Status` object returned on every error, and three interchangeable PATCH content types (source:
kubernetes.io "API Concepts" reference, retrieved 2026-09-29). This procedure treats that convention
layer as load-bearing background, the way the DNS skill treats RFC 1035 — cited once here rather than
repeated at every step. The Deployment resource's own fields and the scale subresource are documented
separately (source: kubernetes.io Deployment v1 API reference, retrieved 2026-09-29).

## Operational procedure

### 1. Confirm the target namespace and workload name

A Deployment is namespaced — every path below requires `{namespace}`. If the namespace isn't already
known from the caller's request, do not guess or default to `default` silently; confirm it with the
operator. The workload name (`{name}`) must be unique within that namespace for the `deployments`
resource.

### 2. Decide the operation: create, roll forward, scale, or delete

These are handled differently against the API — pick the right one rather than always doing a full
replace:

- **Create** — the Deployment does not yet exist in the namespace.
- **Roll forward to a new image / change other pod-template fields** — the Deployment exists; only
  `spec.template` (or another non-selector field) needs to change.
- **Scale** — only the desired replica count needs to change; use the scale subresource (step 6), not
  a full-object update, so the write surface stays narrow and matches how autoscalers themselves are
  documented to interact with a Deployment.
- **Delete** — the workload is being torn down entirely.

### 3. Build the Deployment manifest (create)

Assemble the object with at minimum:
- `apiVersion: apps/v1`, `kind: Deployment`, `metadata.name`, `metadata.namespace`.
- `spec.replicas` — desired pod count (defaults to 1 if omitted; always set it explicitly for an
  automation-driven create so the outcome doesn't depend on a hidden default).
- `spec.selector.matchLabels` — the label selector the Deployment uses to own its Pods. This field is
  immutable once the object is created (see step 5's error handling) — get it right at create time.
- `spec.template` — the Pod template (`metadata.labels` must satisfy `spec.selector`, plus the usual
  Pod `spec.containers[].image`/`ports`/`env`/`resources`).
- `spec.strategy.type` — `RollingUpdate` (default) or `Recreate`. Under `RollingUpdate`,
  `spec.strategy.rollingUpdate.maxSurge` and `.maxUnavailable` bound how many extra/unavailable pods
  are allowed mid-rollout (each defaults to 25% of desired replicas if unset).
- Optional: `spec.minReadySeconds` (how long a new pod must be healthy before counting as available),
  `spec.progressDeadlineSeconds` (defaults to 600 — how long a rollout may run before the controller
  marks it as not progressing), `spec.revisionHistoryLimit` (how many old ReplicaSets to retain for
  rollback), `spec.paused` (create the rollout in a paused state).

Submit via the create call in `endpoints.md`. A `201` response returns the full object including
`metadata.uid` and the starting `metadata.resourceVersion` — capture the latter if a follow-up update
is expected soon, since it's needed for optimistic-concurrency checks.

### 4. Confirm the create/rollout by watching status, not just the create response

A `201`/`200` response only means the API server accepted and persisted the object — it does not mean
pods are running yet. Poll the Deployment (or its status subresource; literal path in `endpoints.md`) and evaluate:
- `status.observedGeneration` vs `metadata.generation` — until these match, the controller hasn't
  finished reconciling the latest spec change; anything read before that point may be stale.
- `status.conditions[]` — look for an entry with `type: Progressing` and `reason:
  NewReplicaSetAvailable` (rollout's new ReplicaSet is up), and an entry with `type: Available` and
  `reason: MinimumReplicasAvailable` (enough pods are ready). A `Progressing` condition with `reason:
  ProgressDeadlineExceeded` means the rollout stalled past `spec.progressDeadlineSeconds` — report this
  rather than continuing to poll indefinitely.
- `status.replicas`/`status.updatedReplicas`/`status.readyReplicas`/`status.availableReplicas` — all
  reaching `spec.replicas` is the concrete success condition for "the workload is fully up."

### 5. Roll forward to a new image or other template change

Use PATCH against the Deployment (not PUT) so an unrelated concurrent field isn't clobbered — pick one
of the three documented content types (see `endpoints.md` for the literal header value and body shape
of each): JSON Patch for precise single-field operations, JSON Merge Patch for a simple recursive
merge, or Kubernetes' own Strategic Merge Patch (the default `kubectl` uses) for intelligent
list-merging on nested fields like `containers`. Then repeat step 4's status confirmation — a
successful PATCH response only reflects the stored spec, not that the rollout has completed.

**`spec.selector` is immutable after creation** and must continue to match `spec.template.metadata.labels`.
A PATCH/PUT attempting to change it is rejected (documented as a `422 Invalid` validation failure,
surfaced via the `Status` object's `reason: Invalid`) — if the workload genuinely needs a different
selector, that requires deleting and recreating the Deployment (step 8), with that step's own
confirmation gate.

### 6. Scale via the dedicated scale subresource

For a replica-count-only change, update the dedicated scale subresource with an `autoscaling/v1` `Scale`
object body (`spec.replicas` set to the desired count) rather than editing the full Deployment's
`spec.replicas` directly — this is the narrower, purpose-built write path and the one autoscaler
controllers are documented to use themselves. Read the same subresource first if the current replica
count and `status.selector` aren't already known (see `endpoints.md` for the literal calls).

**Scaling down (including to 0) terminates running pods and is hard to reverse** in the sense that any
in-flight work on those pods is lost — stop and confirm with the operator before submitting a
scale-down, the same as any other destructive step in this skill.

Confirm the scale took effect the same way as step 4: poll until `status.replicas` (and
`status.readyReplicas`/`status.availableReplicas` for a scale-up) match the new `spec.replicas`.

### 7. Roll back to a prior revision

Kubernetes tracks rollout history via the `deployment.kubernetes.io/revision` annotation on each
ReplicaSet the Deployment has owned (not on the Deployment object itself). To roll back through the
API directly: find the target ReplicaSet owned by this Deployment carrying the desired revision
annotation value, read its `spec.template`, and PATCH the Deployment's own `spec.template` to match it
— this creates a new rollout (a new ReplicaSet, or reuse of a still-retained old one) using the prior
pod template, which is the same mechanism a rollback command is documented to trigger under the hood.
`spec.revisionHistoryLimit` bounds how many old ReplicaSets remain available to roll back to; if the
target revision's ReplicaSet has already been garbage-collected, there's nothing to read back and this
approach doesn't apply — report that rather than fabricating a template.

### 8. Delete the Deployment

**Stop and confirm with the operator before deleting** — state the namespace, name, current replica
count, and which propagation policy will be used. Cascading deletion of the Deployment's ReplicaSets
and Pods is controlled by `propagationPolicy` on the delete call:
- `Foreground` — the Deployment stays visible (in a deleting state) until its ReplicaSets/Pods are
  actually gone.
- `Background` — the Deployment is deleted immediately; ReplicaSets/Pods are garbage-collected
  asynchronously.
- `Orphan` — the Deployment is deleted but its ReplicaSets/Pods are left running, now unowned.

If the caller doesn't specify one, don't silently assume — confirm which behavior is wanted, since the
practical difference (pods kept running or not, and how soon) is exactly what makes this destructive.

### 9. Handle documented errors

Every non-2xx response carries a `Status` object (`kind: Status`, `status: Failure`, `reason`, `code`,
`message`) — use `reason` to branch, not string-matching `message`:
- `NotFound` (404) — no Deployment with that name/namespace. Don't retry blindly; confirm the name.
- `AlreadyExists` (409, on create) — a Deployment with that name already exists in the namespace; this
  is a create-vs-update routing mistake, not a transient error.
- `Conflict` (409, on update) — `metadata.resourceVersion` in the request no longer matches the
  server's current value (someone else updated it since it was last read). Re-fetch the object, rebase
  the intended change onto the new version, and retry — never blindly resubmit the stale version.
- `Invalid` (422) — validation failure, including the immutable-selector case in step 5. The `Status`
  object's `details.causes[]` names the specific field(s) that failed.
- `Unauthorized` (401) / `Forbidden` (403) — the client's credentials or RBAC grant don't cover this
  operation; not something to retry without fixing the underlying access.

## Patterns

- **Prefer PATCH over PUT for anything short of a full-object create.** PUT requires resubmitting the
  entire object including server-populated fields (`status`, `metadata.resourceVersion`, etc.) and is
  easy to get wrong by dropping a field the caller didn't intend to touch.
- **`?dryRun=All` validates a request (including admission checks) without persisting it** — useful to
  check whether a create/update/patch would succeed before submitting it for real.
- **`?fieldValidation=Strict`** rejects unknown/duplicate fields in the request body outright, instead
  of silently ignoring them (the default, permissive behavior) — worth setting on anything
  automation-generated, to catch a typo'd field name instead of having it silently dropped.

## Known limitations

- Deployments only — no StatefulSet, DaemonSet, Job, or bare Pod handling.
- Does not cover HorizontalPodAutoscaler configuration — an HPA drives the same scale subresource
  documented in step 6, but configuring the autoscaler itself is a different object/procedure.
- Rollback (step 7) requires the target ReplicaSet to still exist within `spec.revisionHistoryLimit`'s
  retention — past that, there's nothing to read the prior template back from.

## Tools

Every operation maps to the Kubernetes API server's Deployments REST interface — see `endpoints.md`
for literal paths, request/response shapes, and the PATCH content-type table.

| Operation | Description | Category |
|---|---|---|
| Create Deployment | Create a new Deployment in a namespace | Workload Management |
| Get/List Deployment(s) | Read one or all Deployments in a namespace (or cluster-wide) | Workload Management |
| Patch/Replace Deployment | Update an existing Deployment's spec (image, template, strategy, etc.) | Workload Management |
| Delete Deployment | Remove a Deployment with a chosen cascade policy | Workload Management |
| Get/Patch/Replace Scale | Read or set the desired replica count via the scale subresource | Scaling |
| Get/Patch/Replace Status | Read or (rarely, from automation) set status fields directly | Status |

## Verification checklist

- [ ] Namespace and workload name were confirmed, not assumed/defaulted
- [ ] The right operation was used for the intent (full create/PATCH vs. the scale subresource for a
      pure replica-count change)
- [ ] `status.observedGeneration` matched `metadata.generation` before trusting any other status field
- [ ] Rollout success was confirmed via `status.conditions`/`status.*Replicas` reaching the desired
      state, not just a successful HTTP response on the initial call
- [ ] Any delete or scale-down was confirmed with the operator first, including which
      `propagationPolicy` applies to a delete
- [ ] Errors were branched on the `Status` object's `reason`, not the free-text `message`
