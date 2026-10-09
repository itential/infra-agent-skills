---
name: workload-state-query
description: >-
  Read workload objects, container state and related events. Use for Kubernetes pod/controller inventory and events, or VMware ESXi registered-VM and snapshot-tree inspection. Covers Kubernetes kubectl and VMware ESXi CLI. Assumes an authenticated Kubernetes context or authorized ESXi shell session for the selected read-only operation.
---

# Workload state query

Read workload objects, container state and related events.

## When to use this skill

Use for Kubernetes pod/controller inventory and events, or VMware ESXi registered-VM and snapshot-tree inspection. Supported platforms: Kubernetes kubectl and VMware ESXi CLI.

## Universal concepts

No common wire protocol is implied by this capability. Object existence, process state and readiness are separate observations. An inaccessible scope is not an empty inventory.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

No mutations, container execution, secret retrieval or proof of application reachability is included.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated Kubernetes context or authorized ESXi shell session for the selected read-only operation. The selected procedure lists required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
