---
name: load-balancer-state-query
description: >-
  Retrieve load-balancer configuration and operational observations. Use for F5 BIG-IP virtual-server, pool and iRule reads plus software, hardware, failover and configuration-sync state. Covers F5 BIG-IP TMSH v17. Assumes an authenticated TMSH session with access to the requested partition and objects.
---

# Load balancer state query

Retrieve load-balancer configuration and operational observations.

## When to use this skill

Use for F5 BIG-IP virtual-server, pool and iRule reads plus software, hardware, failover and configuration-sync state.

## Universal concepts

No common wire protocol is implied by this capability. Configuration properties and runtime observations are separate evidence. Native state and measurement values remain visible without universal severity thresholds.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

No generic root-cause decision tree, arbitrary health thresholds, log-code mapping, TLS remediation, GTM catalogue or object changes are included.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated TMSH session with access to the requested partition and objects. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
