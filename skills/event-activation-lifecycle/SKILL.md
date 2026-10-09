---
name: event-activation-lifecycle
description: >-
  Create and manage an existing rulebook activation through its documented lifecycle. Use for Red Hat AAP 2.6 activation creation, list/detail/output inspection, enable, disable, restart and deletion. Covers Red Hat Ansible Automation Platform Event-Driven Ansible. Assumes an authenticated browser session with appropriate Automation Decisions permissions and an existing project, rulebook and decision environment.
---

# Event Activation Lifecycle

Create and manage an existing rulebook activation through its documented lifecycle.

## When to use this skill

Use for Red Hat AAP 2.6 activation creation, list/detail/output inspection, enable, disable, restart and deletion.

## Universal concepts

No common wire protocol is implied by this capability. An activation processes events using its selected rulebook and runtime environment. Running state is separate from success of an individual triggered action.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

This version uses the documented platform UI. Decision-environment creation, rulebook authoring and event-stream administration are outside scope.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated browser session with appropriate Automation Decisions permissions and an existing project, rulebook and decision environment. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
