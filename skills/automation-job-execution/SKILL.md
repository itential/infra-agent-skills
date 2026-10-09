---
name: automation-job-execution
description: >-
  Launch an existing automation definition and inspect its execution result or supported build metadata. Use for launching an approved existing Jenkins job, Itential workflow or unsliced AAP job template, inspecting its native execution evidence, or updating Jenkins build display metadata. Covers Jenkins MCP Server Plugin, Itential Platform and Red Hat Ansible Automation Platform. Assumes an authenticated API/MCP client with the permissions required for the selected inspection, approved launch, or build-metadata update.
---

# Automation Job Execution

Launch an existing automation definition and inspect its execution result or supported build metadata.

## When to use this skill

Use for launching an approved existing Jenkins job, Itential workflow or unsliced AAP job template, inspecting its native execution evidence, or updating Jenkins build display metadata. Supported platforms: Jenkins MCP Server Plugin, Itential Platform and Red Hat Ansible Automation Platform.

## Universal concepts

No common wire protocol is implied by this capability. Launch acceptance and execution completion are separate outcomes. The definition and its inputs determine the affected systems.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

Creating automation definitions, arbitrary script replay and interpreting a platform completion state as external application health are outside scope.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated API/MCP client with the permissions required for the selected inspection, approved launch, or build-metadata update. The selected procedure lists required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
