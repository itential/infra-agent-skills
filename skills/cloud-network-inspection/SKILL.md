---
name: cloud-network-inspection
description: Read a public cloud's network configuration, effective rules and routes, hybrid-link routing, and existing flow-log or event evidence for a named scope, without changing anything. Use when diagnosing cloud connectivity or inventorying VPC/VNet, transit, VPN, firewall, or load-balancer configuration. Covers AWS (via the AWS Network MCP server) and Azure (via the Azure CLI). Assumes an authenticated MCP client or CLI session with read permissions for the target account or subscription is already available.
argument-hint: "[aws|azure] [scope: account/profile or subscription, region, resource] [what to read]"
---

# Cloud Network Inspection

Reads provider-native network configuration, effective policy, routing, and existing traffic evidence from a public cloud for a named scope, and reports what was observed.

## When to use this skill

- Inventory virtual networks, subnets, security rules, route tables, transit and hybrid links, firewalls, or load balancers in an AWS account or Azure subscription.
- Collect evidence for a connectivity question: which rules and routes apply to a network interface, what a transit or hybrid routing table holds, what flow logs or backend-health data show.
- Not for creating or changing cloud network resources, and not for instance lifecycle (see `compute-instance-provisioning`). Not for device or controller snapshots and before/after comparison (see `network-state-collection`).

## Universal concepts

- Configuration, effective (resolved) state, and observed traffic are different evidence types; a configuration read does not prove packets flow.
- Every result belongs to the scope that was queried (account or subscription, region, resource); an empty result covers only that scope.
- A failed read, a denied permission, or a missing prerequisite is an incomplete observation, never proof that a resource or rule is absent.
- Where a platform documents no rate limits, they are unknown; back off on throttling responses and honor any retry hint returned.

## Procedure

1. Identify the target cloud from the request and find it in [references/INDEX.md](references/INDEX.md). If it is not listed, stop and report that it is not covered.
2. Open that platform's `procedure.md` and follow it exactly, including its scope rules and prerequisites.
3. Report the outcome in that procedure's own terms, keeping partial results and stated limitations visible.

## Known limitations

This skill is read-only: it creates, modifies, and deletes nothing, so its procedures carry no confirmation gates. Any write added to a procedure would need one. It issues no compliance verdict and no health verdict.

## Contributing to this skill

This router changes only to correct shared concepts or to point at a newly supported cloud. Platform-specific operations, errors, and bindings live under `references/<platform>/`.

## Tools

An authenticated client for the selected platform with read permissions. Each platform's `procedure.md` names its mechanism; see `references/INDEX.md`.

## Verification checklist

- The platform, scope, and evidence type match the request.
- The platform procedure's success criteria and error handling were applied.
- The report keeps scope attribution, incomplete results, and stated limitations.
