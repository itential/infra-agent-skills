---
name: pipeline-job-management
description: >-
  Start and inspect automation pipeline executions and supported job controls. Use for listing and reading GitHub Actions runs or GitLab pipelines, dispatching a run, and retrying/canceling GitLab pipelines or reading their job logs. Covers GitHub Actions and GitLab CI/CD. Assumes an authenticated API client and an already configured workflow or pipeline.
---

# Pipeline and job management

Start and inspect automation pipeline executions and supported job controls.

## When to use this skill

Use for listing and reading GitHub Actions runs or GitLab pipelines, dispatching a run, and retrying/canceling GitLab pipelines or reading their job logs.

## Universal concepts

No common wire protocol is implied by this capability. An accepted execution request is not proof of successful completion. The platform returns run identity and state; pipeline definitions determine what the run changes.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

No authoring pipeline definitions, changing secrets, approving deployments, or diagnosing job content. GitHub scope is dispatch/list/read; retry, cancel, and job-log operations here are GitLab only.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated API client and an already configured workflow or pipeline. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
