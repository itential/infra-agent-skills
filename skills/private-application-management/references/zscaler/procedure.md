# Zscaler ZPA standard application segments

Manage a standard ZPA application segment using the publisher MCP server and existing group identifiers.

Sources: [application segment implementation](https://github.com/zscaler/zscaler-mcp-server/blob/master/src/zscaler_mcp/tools/zpa/app_segments.py), [MCP confirmation guide](https://github.com/zscaler/zscaler-mcp-server/blob/master/docs/guides/mcp-protocol.md), retrieved 2026-10-09; current publisher master. Literal bindings and exact errors are in [endpoints.md](endpoints.md).

## Common Sequences

- Inspect: List segments → Read segment.
- Create: Validate inputs → Confirmed create → Read segment.
- Change/remove: Read segment → Confirmed update or Confirmed delete → Record outcome.

### List segments

The list operation optionally restricts names by substring and selects a microtenant. Page numbers begin at one; the page size is bounded by the published schema. A returned list is success for that requested page, not proof of a complete tenant inventory. The wrapper does not expose a continuation token; coverage remains bounded by the pages retrieved. An empty name match is an empty match, not permission to broaden the search. An SDK error remains a failed list.

### Read segment

An explicit segment identifier and matching microtenant select one record. Success is the returned segment record, including the relevant domains, port ranges, and group references. Missing identifiers fail validation; a failed get retains the API error rather than implying absence from unrelated scopes.

### Validate inputs

Creation requires a name, an existing segment-group identifier, and TCP or UDP port ranges. Existing server-group identifiers and domain names supply the requested service bindings. The basic port representation consists of start/end string pairs. The publisher rejects a create with no port range. Advanced fields are passed through to the installed SDK; an undocumented field remains unverified and requires the applicable SDK schema before use. Advanced input can override basic fields, so the final merged values are the values requiring approval.

### Confirmed create

Creating a segment changes application publication: stop and confirm with the operator before proceeding. The enabled-by-default behavior is included in that confirmation. The enabled write tool submits the validated segment and returns its record. A subsequent segment read establishes the assigned ID and intended values. A create error is failure; no blind repeated create is justified when the result is ambiguous.

### Confirmed update

Changing domains, ports, enablement, or group membership changes publication: stop and confirm with the operator before proceeding. The wrapper sends the provided fields for the selected identifier and microtenant. Success is an updated segment record whose readback contains the requested values. An SDK error or mismatched readback remains unresolved.

### Confirmed delete

Deletion cannot be undone: stop and confirm with the operator before proceeding. The publisher's delete confirmation remains in place: an unanswered or cancelled native prompt does not delete; clients without elicitation receive a confirmation-token challenge that requires an actual operator decision before continuation. The challenge itself is not a deletion result. Only the final operation result indicating success confirms deletion; failure retains the underlying error.

### Record outcome

Read/create/update returns the native segment record. Delete returns the publisher's success flag and message. The result identifies the microtenant and operation without claiming that application reachability or policy authorization has been tested.

## Patterns

- Segment groups and server groups are existing dependencies; this procedure never manufactures their IDs.
- The update wrapper omits unspecified basic fields. Advanced fields are merged after those basics and can override them.
- Deletion confirmation depends on client protocol support. The token fallback cryptographically binds a call but cannot itself prove a human approved it; the publisher documents this limitation.

## Known limitations

- Group lifecycle, connector placement, access policy rules, Browser Access, PRA and end-user connectivity diagnosis are separate operations.
- The wrapper does not establish complete list coverage through response pagination metadata.
- Delete is irreversible. No undo operation or universal propagation timeout is documented in these sources.
- The server write allowlist is required; create/update tools do not supply the delete tool's built-in human prompt.

## Tools

| Operation | Description | Category |
|---|---|---|
| List segments | Query standard segments by optional name/microtenant/page | Read |
| Read segment | Retrieve one known segment | Read |
| Create segment | Add a standard segment with port/group scope | Write |
| Update segment | Change specified segment fields | Write |
| Delete segment | Remove one segment through confirmation flow | Destructive |

## Verification checklist

- The ID, microtenant and existing group references match the intended segment.
- Creation includes the required name, segment group and port range.
- Confirmations cover the exact merged payload; deletion retains the publisher challenge.
- Returned/readback fields match the request; failures and incomplete pages remain explicit.
- No connectivity or access-policy success is inferred from segment persistence.
