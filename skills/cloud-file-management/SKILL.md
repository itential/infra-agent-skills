---
name: cloud-file-management
description: >-
  Inspect or transfer a file in a cloud drive. Use for listing folders, reading file metadata, sharing permissions, versions and thumbnails, downloading files, and uploading or replacing files up to 250 MB in OneDrive or SharePoint. Covers microsoft_graph. Assumes an authenticated API client with access to the requested tenant and resources.
---

# Cloud file management

Inspect or transfer a file in a cloud drive.

## When to use this skill

Use for listing folders, reading file metadata, sharing permissions, versions and thumbnails, downloading files, and uploading or replacing files up to 250 MB in OneDrive or SharePoint.

## Universal concepts

No common wire protocol is implied by this capability. A resource identifier and the caller’s permissions determine the target and visible result. File transfer success does not validate the meaning or rendering of a document.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

Only the operations and versions listed in the reference index are supported; no organizational escalation, naming, or approval policy is inferred.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated API client with access to the requested tenant and resources. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
