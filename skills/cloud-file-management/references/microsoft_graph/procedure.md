# Microsoft Graph drive file inspection and transfer

Microsoft Graph v1.0 exposes file metadata, retained versions, effective sharing, thumbnails, and file-content transfers for OneDrive and SharePoint.

## Common Sequences

- Inspect: **Locate the item → Inspect the requested facets**.
- Download: **Locate the item → Download file content**.
- Publish: **Locate the destination → Upload file content → Locate the item**.

### Locate the item

1. The folder-list operation returns the children visible to the caller. A continuation link leads to the next page until none remains; an empty page does not establish tenant-wide absence.
2. The metadata operation resolves the selected item by drive and item identifier or path. Success returns the selected item's identifier, name and metadata. A conditional unchanged response means cached metadata remains current, not that the file is absent.
3. For each call, malformed input requires correction; missing authentication requires a valid session; denied access or insufficient claims requires the appropriate permission or conditional-access flow. A missing or gone item ends that lookup. Rate limiting defers further calls; temporary unavailability honors the returned retry delay. Other failures retain the documented error code and stop this sequence, as classified in [endpoints](endpoints.md#error-conditions).

### Inspect the requested facets

1. The permission-list operation returns effective direct and inherited sharing entries. Owners can see all sharing permissions; other callers see only entries applicable to them. Secret sharing identifiers or URLs can appear for callers able to create those permissions; such values are excluded from broadly distributed reports.
2. The version-list operation returns retained versions newest first. Available metadata is narrower than current-item metadata; retention depends on service configuration. An empty history does not prove no past edits occurred.
3. The thumbnail-list operation returns zero or more thumbnail sets. No thumbnail is a valid outcome, not a file-transfer failure.
4. Each result is associated with the item and caller context. Failures use the same error handling as **Locate the item**; unavailable facets are reported individually.

### Download file content

1. The selected item's file facet establishes that content can be downloaded. The download operation redirects to a short-lived preauthenticated URL. The client follows that returned URL promptly without forwarding the Graph bearer token.
2. Success yields the file bytes. Conditional unchanged responses preserve the existing local copy. A ranged download may return either the selected bytes or the entire file; the response determines which was received. Expired links require a new content request, not reconstruction of a URL. Other errors follow **Locate the item**.

### Locate the destination

1. The metadata and folder-list operations identify the target folder and whether the requested filename already exists. The selected drive, parent, filename, and overwrite consequence are included in the proposed transfer.
2. Failure to resolve the destination stops publication; it does not authorize a fallback drive or folder.

### Upload file content

1. The documented small-file operation transfers a binary stream of at most 250 MB to a selected new path or existing item. **Repository safeguard: stop and confirm with the operator before proceeding**, including the exact destination and whether existing content will be replaced.
2. The returned drive item identifies the created or updated file. A metadata read confirms its identity and reported size; this confirms transfer, not Visio validity or diagram accuracy.
3. Oversized content requires the separately documented upload-session procedure, outside this scope. App-only replacement of a file protected by a sensitivity label is unsupported; delegated permissions are required. Conflicts, locks, stale preconditions, quota exhaustion, unsupported content, and range errors require correction, not blind retries. An uncertain write outcome requires an item read before another upload.

## Patterns

- Permission results are a view through the caller's access, not a complete sharing audit for non-owners.
- Preauthenticated download URLs grant access without a bearer token and must be handled as sensitive data.
- Version retrieval does not support custom ordering and does not reconstruct full historical metadata.

## Known limitations

No document creation, Visio rendering, rename, delete, permission changes, version restoration, or large-file upload sessions are included. SharePoint Embedded has additional container-specific permissions. This procedure assumes the correct authenticated cloud and drive are already selected.

## Tools

| Operation | Description | Category |
|---|---|---|
| List folder children | Discover visible items and continuation links | Read |
| Get item metadata | Resolve identity and current attributes | Read |
| List permissions, versions or thumbnails | Inspect the requested facet | Read |
| Download content | Retrieve the file stream | Read |
| Upload content | Create or replace a file stream | Write |

## Verification checklist

- Folder pagination was exhausted or clearly reported incomplete.
- Results retain item identity, caller visibility and retention limitations.
- Transfers yielded bytes or a returned drive item; uploads were confirmed and read back.
- Secret download/sharing URLs were not exposed in ordinary reports.

Sources: Microsoft Learn, Graph v1.0 [children](https://learn.microsoft.com/en-us/graph/api/driveitem-list-children), [metadata](https://learn.microsoft.com/en-us/graph/api/driveitem-get), [versions](https://learn.microsoft.com/en-us/graph/api/driveitem-list-versions), [permissions](https://learn.microsoft.com/en-us/graph/api/driveitem-list-permissions), [thumbnails](https://learn.microsoft.com/en-us/graph/api/driveitem-list-thumbnails), [download](https://learn.microsoft.com/en-us/graph/api/driveitem-get-content), [upload](https://learn.microsoft.com/en-us/graph/api/driveitem-put-content), and [errors](https://learn.microsoft.com/en-us/graph/errors), retrieved 2026-10-09.
