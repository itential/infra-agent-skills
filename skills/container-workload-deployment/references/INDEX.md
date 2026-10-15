# Container Workload Deployment — Vendor Index

One row per supported vendor/platform. Each directory holds its own `procedure.md` (the full
step-by-step) plus wire-level `endpoints.md`.

| Vendor / Platform | Directory | Scope | Notes |
|---|---|---|---|
| Kubernetes | `kubernetes/` | Create/read/update/delete an `apps/v1` Deployment; scale it via the dedicated scale subresource; roll forward to a new image; roll back to a prior ReplicaSet's pod template | The only platform here with a formally documented, resource-independent API convention layer (optimistic concurrency, a shared `Status` error object, three PATCH content-types) — see its own procedure for the grounding citation |
| Docker Engine | `docker-engine/` | Create/start/stop/restart/update/remove a container; pull/push/tag an image locally | No native replica-count/scale primitive — "scaling" is documented here only as an inferred pattern (multiple distinctly-named containers), not a vendor-documented call |
| Docker Hub | `docker-hub/` | Authenticate; create/list/read a repository; list/read an image tag; manage personal access tokens | Registry *metadata* API only — actual image byte transfer (push/pull) happens through Docker Engine's image endpoints (see `docker-engine/procedure.md`), authenticated with credentials obtained here. No documented delete-tag or delete-repository endpoint as of research — flagged as an explicit gap, not fabricated |
