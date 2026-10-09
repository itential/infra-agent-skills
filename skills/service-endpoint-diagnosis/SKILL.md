---
name: service-endpoint-diagnosis
description: >-
  Diagnose Kubernetes Service selection and backend endpoint state from API objects. Use for a Service with missing or unexpected backends, incorrect target-port mapping, or an Ingress backend reference that does not resolve. Covers Kubernetes kubectl. Assumes authenticated kubectl read access to Services, Pods, EndpointSlices and requested Ingress objects.
---

# Service endpoint diagnosis

Diagnose Kubernetes Service selection and backend endpoint state from API objects.

## When to use this skill

Use for a Service with missing or unexpected backends, incorrect target-port mapping, or an Ingress backend reference that does not resolve.

This is diagnostic-shaped: the result is an evidence-backed finding from the documented decision tree, rather than a changed record.

## Universal concepts

No common wire protocol is implied by this capability. A configured relationship is not evidence of packet delivery. Missing objects, unmatched selectors and non-ready endpoints are different findings.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

This procedure stops at object-model diagnosis; DNS probes, proxy/CNI internals, application tests and mutations are outside scope.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes authenticated kubectl read access to Services, Pods, EndpointSlices and requested Ingress objects. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
