---
name: container_workload_deployment
description: Create, scale, update, or remove a containerized workload — and manage the images that back it — on Kubernetes (apps/v1 Deployments, including the scale subresource), Docker Engine (the Container API for creating/starting/stopping/removing containers and for pulling/pushing/tagging images locally), or Docker Hub (the registry-side v2 REST API for authenticating, creating/browsing repositories, and reading/listing image tags). Use when a Deployment or container needs to be created, scaled, rolled forward, or torn down on one of these platforms, or when a repository/tag on Docker Hub needs to be inspected or created as part of getting an image ready to deploy. Assumes an authenticated client is already available for the target platform (a Kubernetes API server bearer token or client certificate, a Docker Engine API socket or TLS client, or a Docker Hub bearer token) — this skill does not provision or authenticate that client. Does not cover building a container image (Dockerfile/BuildKit), Kubernetes objects other than Deployments (StatefulSet, DaemonSet, Job, bare Pod), Docker Swarm services, or Docker Compose orchestration — see references/INDEX.md.
argument-hint: "[platform] [action] [workload_name] [image] [replicas]"
---

# Container Workload Deployment

Creates, scales, updates, or removes a containerized workload on one of the supported platforms,
and covers the registry-side operations (repository/tag management on Docker Hub) needed to get an
image ready for that workload. Each platform's own documented procedure, field rules, and error
handling live in `references/<platform>/procedure.md`.

## When to use this skill

- A workload needs to be deployed, scaled up/down, rolled forward to a new image, or removed on
  Kubernetes (as an `apps/v1` Deployment), Docker Engine (as a container), or when Docker Hub's own
  repository/tag API needs to be used to prepare or verify an image before/after that deployment.
- Not for building the image itself (Dockerfile builds, BuildKit) — this skill assumes the image
  already exists somewhere pullable. Not for Kubernetes workload types other than Deployment
  (StatefulSet, DaemonSet, Job, or a bare Pod each have different semantics this skill doesn't
  cover), Docker Swarm services, or Docker Compose's own multi-container orchestration model — see
  `references/INDEX.md`.

## Universal concepts (apply regardless of platform)

- **A container image reference (`repository[:tag][@digest]`) is the one thing every platform below
  agrees identifies "what to run."** Kubernetes and Docker Engine both actually run it; Docker Hub is
  the registry that stores and serves that reference rather than a runtime — its role in this skill
  is preparing/verifying the reference the other two consume, not deploying anything itself.
- **There is no single wire-level standard spanning all three platforms**, unlike DNS's RFC 1035 —
  treat every endpoint, field name, and status code as platform-specific unless stated otherwise here.
  Kubernetes is the one outlier with unusually rigorous, centrally documented API behavior: a set of
  API conventions apply uniformly across every Kubernetes resource type, not just Deployments — see
  `references/kubernetes/procedure.md` for the specifics. Docker Engine and Docker Hub each define
  their own request/response shapes independently, with no equivalent shared convention layer
  between them.
- **Removing a running workload is destructive and hard to reverse** — a Kubernetes Deployment delete
  tears down its ReplicaSets and Pods, and a Docker Engine container removal discards the container's
  writable layer unless volumes were used. Every platform procedure below has its own confirmation
  gate built into the relevant step; never skip it because "the API call would succeed."
- **"Scaling" is a native, separately-documented primitive only on Kubernetes** (the Deployment scale
  subresource). Docker Engine has no built-in replica-count concept for a plain container — its
  procedure documents the practical workaround (running multiple distinctly-named containers) as an
  inferred pattern, not a vendor-documented "scale" call. Docker Hub has no runtime concept at all.

## Procedure

1. **Identify the target platform** — from the caller's request or the `platform` argument. If it
   isn't one of the platforms in `references/INDEX.md`, stop: this skill doesn't cover it, and does
   not improvise a generic procedure for an unsupported platform.
2. **Open `references/<platform>/procedure.md`** and follow it exactly — it contains that platform's
   full operational procedure, error handling, patterns, known limitations, tools, and verification
   checklist. This file is intentionally the router; the real steps live per platform because the
   platforms genuinely do not share one procedure (a Kubernetes Deployment, a Docker Engine container,
   and a Docker Hub repository/tag are three different kinds of object with three different lifecycles).
3. **Report the outcome** using that platform procedure's own status vocabulary (e.g. Kubernetes'
   `Status` object `reason` values, Docker Engine's HTTP status per operation, Docker Hub's `message`
   field on error) — don't normalize it away.

## Known limitations

- Does not cover building a container image — every platform procedure assumes the image to deploy
  already exists and is pullable from wherever it's referenced.
- Does not cover Kubernetes workload types other than Deployment, Kubernetes' HorizontalPodAutoscaler
  (autoscaler-driven scaling is a separate controller acting on the same scale subresource this skill
  documents, not a caller-driven call itself), Docker Swarm services, or Docker Compose.
- Docker Engine has no documented native scale/replica-count primitive for a plain container — see
  Universal concepts and `references/docker_engine/procedure.md` for the workaround pattern and its
  limits (e.g. host port collisions).
- Docker Hub's currently documented v2 REST API does not include a delete-tag or delete-repository
  endpoint — confirmed absent during research, not omitted by oversight. See
  `references/docker_hub/procedure.md` for how this is handled.
- Platform coverage is exactly the three platforms in `references/INDEX.md` — a platform not listed
  there needs a new `references/<platform>/procedure.md` before this skill can be used for it (see
  that file's "Adding a new vendor" section).

## Contributing to this skill

**`SKILL.md` itself should only ever change for two reasons: a bug in the universal concepts/router
logic above, or adding a pointer to a newly-supported platform.** Platform-specific procedure
changes — a new error code, a corrected field name, a changed API path — belong in that platform's
own `references/<platform>/procedure.md` and `endpoints.md`, never here. If you're about to add
vendor-specific detail to this file, put it in the platform's reference file instead.

## Tools

Each platform assumes its own authenticated client (Kubernetes API server client, Docker Engine API
client, Docker Hub REST client) — see `references/INDEX.md` for which, and that platform's
`procedure.md` for the specific operations/mechanisms.

## Verification checklist

- [ ] Target platform confirmed against `references/INDEX.md` before proceeding
- [ ] That platform's own `procedure.md` was followed, including its own confirmation gates and error
      handling — not a generic/improvised sequence
- [ ] Outcome reported using the platform procedure's own status vocabulary
