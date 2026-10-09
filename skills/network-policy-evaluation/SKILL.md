---
name: network-policy-evaluation
description: >-
  Evaluate the documented effect of Kubernetes NetworkPolicy objects on a specified connection. Use for read-only assessment of pod ingress and egress isolation for an explicit source, destination, protocol and port. Covers Kubernetes NetworkPolicy. Assumes authenticated kubectl access to policies and relevant Pod/Namespace labels, plus known network-plugin support.
---

# Network policy evaluation

Evaluate the documented effect of Kubernetes NetworkPolicy objects on a specified connection.

## When to use this skill

Use for read-only assessment of pod ingress and egress isolation for an explicit source, destination, protocol and port.

This is diagnostic-shaped: the result is an evidence-backed finding from the documented decision tree, rather than a changed record.

## Universal concepts

No common wire protocol is implied by this capability. Policy intent and effective dataplane enforcement are distinct. Scope, selectors and traffic direction affect the result.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

CNI-specific policies, host firewalls, service meshes and live connectivity tests are outside this core NetworkPolicy evaluation.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes authenticated kubectl access to policies and relevant Pod/Namespace labels, plus known network-plugin support. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
