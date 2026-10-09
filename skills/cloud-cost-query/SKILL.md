---
name: cloud-cost-query
description: >-
  Retrieve cloud cost, forecast, or detected cost-anomaly data. Use for AWS Cost Explorer historical cost and usage grouping, cost forecasts, and anomaly retrieval. Covers AWS Cost Explorer. Assumes an authenticated AWS Cost Explorer API/SDK client with access to the selected billing scope.
---

# Cloud cost query

Retrieve cloud cost, forecast, or detected cost-anomaly data.

## When to use this skill

Use for AWS Cost Explorer historical cost and usage grouping, cost forecasts, and anomaly retrieval.

## Universal concepts

No common wire protocol is implied by this capability. Actual charges, estimates and forecasts are different outputs; cost and usage units remain part of the result.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

This skill does not choose cost-optimization changes, purchase commitments, or quote service prices.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated AWS Cost Explorer API/SDK client with access to the selected billing scope. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
