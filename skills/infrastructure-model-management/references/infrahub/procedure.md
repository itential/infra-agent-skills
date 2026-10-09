# Infrahub object change proposal

OpsMill Infrahub MCP queries the schema and objects, then records requested object edits on a session branch for review.

Source: [MCP methods](https://docs.infrahub.app/mcp/references/methods) and [branch isolation](https://docs.infrahub.app/mcp/use-cases/safe-changes-branch-isolation), current documentation, retrieved 2026-10-09. Literal tool bindings are in [endpoints.md](endpoints.md).

## Common Sequences

- Inventory: Discover schema → Read objects or Search names → Report query result.
- Proposed object change: Inspect session → Discover schema → Read objects → Change objects → Inspect session → Read objects on the session branch → Propose change.
- Independent next change: Reset session → Inspect session → follow the proposed-object-change sequence.

## Discover schema

The schema catalog identifies available kinds; kind detail identifies scalar attributes, relationships and supported filters. A successful result is a catalog or the requested kind's detail, not an assumed device/IPAM model. Structured detail can use TOON rather than JSON. An absent kind or schema error prevents constructing a valid object request; the native error remains part of the result.

## Inspect session

Session inspection returns the active branch and instance address. Before a first write the branch is null. The first write creates a session branch; a later write recovers to a fresh branch if its prior branch was merged or deleted. The returned branch determines the explicit target for subsequent verification reads.

## Read objects

A typed query uses schema-supported filters and pagination. Success returns nodes, count, total count, offset, limit and a continuation indication. A null continuation indication means the count query failed and completeness is unknown. GraphQL reads are available for expressions beyond typed queries; mutations are rejected by the read tool. Ordinary reads default to the instance default branch, so verification specifies the session branch explicitly. Query errors remain errors, not zero matching objects.

## Search names

The name search matches a substring in the name attribute. Success returns matching nodes within the requested limit. Other attributes require a typed query and the relevant schema filter. The current method contract does not support the older wrapper's any-attribute search claim.

## Change objects

Before creating, updating or deleting an object, or executing a relationship mutation, **stop and confirm with the operator before proceeding**, including the intended session branch and proposed changes. Scalar changes use the typed object operation: creation omits both identifiers, while update supplies an existing identifier. Relationships use a schema-valid GraphQL mutation. Deletion requires an existing object identifier.

Success is the native write result followed by matching object state on the actual session branch; deletion is verified by absence of the identified object there. These write methods are non-idempotent: an ambiguous response is investigated by reading state before any replay. Write tools are unavailable in read-only mode. Branch-management and schema mutations are rejected by the mutation tool; they are not alternate paths around the review boundary. Validation or permission errors leave the operation failed, with the native details retained.

## Propose change

Before recording the proposal, **stop and confirm with the operator before proceeding** with its title, description and destination branch. The operation creates a proposed-change object from the active branch. Success is that returned object for review, not a merge. The active session branch remains usable. A proposal failure does not imply that preceding object edits disappeared; their branch state remains independently verifiable.

## Reset session

Before switching the session's write target, **stop and confirm with the operator before proceeding**. An empty reset clears the cached branch for fresh creation on the next write. A named reset selects a branch and can create it when its name meets the configured pattern. The default branch and merged or read-only branches are rejected. Session inspection confirms the new state; this does not merge or delete existing changes.

## Report query result

The result retains the selected branch, kind, filters and completeness. An empty complete query is a valid empty result. A truncated or failed query is not a complete inventory.

## Patterns

- A method named upsert does not imply retry-safe deduplication: its current contract distinguishes create and update by supplied identifiers and labels it non-idempotent.
- Read defaults do not automatically follow the session write branch.
- Session isolation is preserved through the published write tools; branch/schema operations are deliberately outside this procedure.

## Known limitations

No automatic merge or device change occurs here. The source does not publish a complete stable error-code catalog for these MCP methods; unclassified errors remain visible and require platform-specific guidance. Graph traversal methods added after the source skill are outside this extraction.

## Tools

| Operation | Purpose | Category |
|---|---|---|
| Discover schema | Read kinds, fields and filters | Read |
| Inspect session | Identify active branch | Read |
| Read objects / Search names | Retrieve selected model data | Read |
| Change objects | Create, update or delete branch objects | Write |
| Propose change | Create a review object | Write |
| Reset session | Change the session branch selection | Write |

## Verification checklist

- Schema and filters match the selected kind.
- Read completeness and native errors are retained.
- Verification reads specify the actual session branch.
- The returned proposed-change object is reported as awaiting review, without claiming a merge.
