---
name: log-source-query
description: >-
  Discover accessible log indexes and platform metadata before selecting a query scope. Use for Splunk index inventory and instance-information reads. Covers Splunk Python SDK. Assumes an authenticated TLS-verifying Splunk SDK service object with the required read permissions.
---

# Log source query

Discover accessible log indexes and platform metadata before selecting a query scope.

## When to use this skill

Use for Splunk index inventory and instance-information reads.

## Universal concepts

No common wire protocol is implied by this capability. Accessible source inventory defines query visibility; index existence does not prove it contains the requested events.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

No configuration-file dump, secret retrieval, index creation or deletion is included.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated TLS-verifying Splunk SDK service object with the required read permissions. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
