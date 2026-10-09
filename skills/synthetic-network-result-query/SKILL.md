---
name: synthetic-network-result-query
description: >-
  Retrieve existing synthetic network measurements and path traces. Use for Cisco ThousandEyes network test results, path summaries and agent/round hop details for a known test. Covers Cisco ThousandEyes API v7. Assumes an authenticated HTTPS API client, an existing test ID and access to the requested account group.
---

# Synthetic network result query

Retrieve existing synthetic network measurements and path traces.

## When to use this skill

Use for Cisco ThousandEyes network test results, path summaries and agent/round hop details for a known test.

## Universal concepts

No common wire protocol is implied by this capability. Test, account group, time interval, agent and direction define the evidence scope. Missing measurements are not zero and a path observation alone does not establish a root cause.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

No instant-test execution, test creation, BGP analysis, endpoint-agent diagnostics, alert lifecycle or dashboard operations are included.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated HTTPS API client, an existing test ID and access to the requested account group. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
