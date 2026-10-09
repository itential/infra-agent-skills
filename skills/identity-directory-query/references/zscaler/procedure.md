# Zscaler ZIdentity: query an identity and its memberships

Retrieve a selected user or group and its directory relationships.

Sources: publisher [user tool reference](https://github.com/zscaler/zscaler-mcp-server/blob/master/src/zscaler_mcp/tools/zid/users.py) and [group tool reference](https://github.com/zscaler/zscaler-mcp-server/blob/master/src/zscaler_mcp/tools/zid/groups.py), master retrieved 2026-10-09. Bindings are in [endpoints.md](endpoints.md).

## Common Sequences

- User membership: Find user → Read selected identity → Read relationships.
- Group membership: Find group → Read selected identity → Read relationships.

## Find user or group

The directory search applies the supplied partial-name filter. User search treats text containing an at-sign as an email search; other text searches login names first, then display names if no login matched. Group search uses its name. List operations provide the documented additional filters and paging controls.

Success: matching records expose identifiers for selection. Multiple matches remain distinct; no match does not justify silently broadening the filter. A missing search value is an input error; upstream query failure remains an error.

## Read selected identity

The record-read operation uses the chosen user or group identifier, supplied as a string. It returns that identity's data.

Success: the returned identity matches the intended identifier. Missing identifiers or a failed upstream lookup are not empty successful membership results.

## Read relationships

The membership operation reads groups for the selected user, or users for the selected group. Optional offset and limit retain the requested page scope.

Success: the returned relationship records belong to the selected identity. The result identifies the page and filters; the current MCP implementation does not preserve a universal pagination-total contract, so complete-directory claims require separate verified collection coverage.

## Patterns

The publisher also provides name-to-membership convenience tools which use the first partial match. This procedure resolves the identifier explicitly to avoid silently choosing a different same-name identity. That is a scope choice, not an assertion that the convenience tool rejects ambiguity.

## Known limitations

The current publisher ZIdentity toolsets cover users and groups. NetClaw's generic department, administrator-role, IdP-configuration, SCIM and SAML mapping names are not established by these toolsets and are excluded. No mutation or access entitlement assessment is implied.

## Tools

| Operation | Description | Category |
|---|---|---|
| Find user/group | Retrieve scoped identity matches | MCP query |
| Read identity | Retrieve one record by ID | MCP query |
| Read relationships | Retrieve memberships for one identity | MCP query |

## Verification checklist

- The identity was selected from explicit returned IDs.
- Partial matches and paging were not hidden.
- Membership direction and owner identity match the request.
- Input and upstream errors remain failures.
