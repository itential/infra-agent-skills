# Container Workload Deployment — Vendor Index

One row per supported vendor/platform. Each directory holds its own `procedure.md` (the full
step-by-step) plus wire-level `endpoints.md` for API implementations. CLI implementations keep commands inline.

| Vendor / Platform | Directory | Scope | Notes |
|---|---|---|---|
| Kubernetes | `kubernetes/` | Create/read/update/delete an `apps/v1` Deployment; scale it via the dedicated scale subresource; roll forward to a new image; roll back to a prior ReplicaSet's pod template | The only platform here with a formally documented, resource-independent API convention layer (optimistic concurrency, a shared `Status` error object, three PATCH content-types) — see its own procedure for the grounding citation |
| Docker Engine | `docker_engine/` | Create/start/stop/restart/update/remove a container; pull/push/tag an image locally | No native replica-count/scale primitive — "scaling" is documented here only as an inferred pattern (multiple distinctly-named containers), not a vendor-documented call |
| Docker Hub | `docker_hub/` | Authenticate; create/list/read a repository; list/read an image tag; manage personal access tokens | Registry *metadata* API only — actual image byte transfer (push/pull) happens through Docker Engine's image endpoints (see `docker_engine/procedure.md`), authenticated with credentials obtained here. No documented delete-tag or delete-repository endpoint as of research — flagged as an explicit gap, not fabricated |
| Cisco pyATS on Docker | [cisco_pyats/](cisco_pyats/procedure.md) | Pull the published pyATS image, start a container, run an existing test job, and inspect results | CLI execution; no new scale API or image build behavior. Image references and destructive-removal constraints are unchanged. |

## Adding a new vendor

1. Create `references/<vendor>/procedure.md` following the shape of an existing vendor file
   (Operational procedure → Patterns → Known limitations → Tools → Verification checklist).
2. Add `endpoints.md` (wire-level calls) alongside it. If the vendor ever grows a second
   platform-family or install mode, name both files after that family (e.g.
   `<platform-family-and-mode>-procedure.md` / `-endpoints.md`) instead of the bare names used today —
   see `AGENTS.md` rule 8.
3. Add one row to the table above.
4. Check every claim in `SKILL.md`'s "Universal concepts" against the new vendor's actual documented
   behavior before assuming it still holds — correct `SKILL.md` if the new vendor contradicts it, and
   note the correction here (see `AGENTS.md` rule 4).
5. Do NOT add vendor-specific procedure content to the top-level `SKILL.md` — see that file's own
   contribution note.
