---
name: issue-record-management
description: >-
  Read, create, update, transition, and comment on issue records. Use for repository issue records on GitHub and GitLab, and issue records on Jira Cloud. Covers GitHub REST, GitLab REST, and Atlassian Jira Cloud REST. Assumes an authenticated API client with access to the selected project or repository.
---

# Issue record management

Read, create, update, transition, and comment on issue records.

## When to use this skill

Use for repository issue records on GitHub and GitLab, and issue records on Jira Cloud.

## Universal concepts

No common wire protocol is implied by this capability. Issue identity, supported fields, visibility, and available state changes are platform-specific. A successful write response does not establish that every optional field was accepted.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

No issue deletion, bulk creation, issue linking, repository metadata administration, or organization-specific incident workflow. Jira transitions use the configured workflow; no universal status names are assumed.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated API client with access to the selected project or repository. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
