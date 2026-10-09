---
name: saved-search-execution
description: >-
  Inspect and dispatch an existing saved search, then retrieve its final results. Use for Splunk saved-search discovery and explicitly approved execution in a selected owner/application namespace. Covers Splunk Enterprise and enabled Splunk Cloud REST API. Assumes an authenticated TLS-verifying Splunk API client with access to the saved search.
---

# Saved search execution

Inspect and dispatch an existing saved search, then retrieve its final results.

## When to use this skill

Use for Splunk saved-search discovery and explicitly approved execution in a selected owner/application namespace.

## Universal concepts

No common wire protocol is implied by this capability. Saved query definitions and individual execution jobs are different resources. Acceptance does not establish successful completion.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

No saved-search creation, scheduling changes or automatic alert delivery is included.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated TLS-verifying Splunk API client with access to the saved search. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
