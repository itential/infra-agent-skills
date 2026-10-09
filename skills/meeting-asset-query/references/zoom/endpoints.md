# Zoom Meetings MCP bindings

Official sources: [Zoom publisher Meetings skill](https://github.com/zoom/skills/blob/main/skills/zoom-mcp/meetings/SKILL.md), [Zoom publisher tool guide](https://github.com/zoom/skills/blob/main/skills/zoom-mcp/meetings/references/tools.md), [Zoom MCP server overview](https://developers.zoom.us/docs/mcp/servers/), retrieved 2026-10-09.

The publisher's Meetings bundle uses Streamable HTTP at `https://mcp.zoom.us/mcp/meeting/streamable`. The general overview also shows a `zoom.us` example endpoint; this binding follows the product-specific publisher bundle. Existing OAuth 2.1 authentication is required, with PKCE for authorization-code clients. Credentials remain in the authenticated client.

| Operation | MCP binding | Required publisher scope |
|---|---|---|
| Discover tools | `tools/list` | Authenticated server access |
| Search meetings | `tools/call` with `name=search_meetings` | `meeting:read:search` |
| Read meeting assets | `tools/call` with `name=get_meeting_assets` | `meeting:read:assets` |
| List recordings | `tools/call` with `name=recordings_list` | `cloud_recording:read:list_user_recordings` |
| Retrieve recording resource | `tools/call` with `name=get_recording_resource` | `cloud_recording:read:content` |

For each selected `tools/call`, `arguments` is constructed only from the live `tools/list` `inputSchema`, retaining its required fields and type constraints. The publisher guide does not specify those field names or output paths, so they are unknown until discovery. Schema absence is a blocking condition. This is an explicit discovered binding, not an invented static API.

The publisher recommends REST when exact request control, bulk pagination, or retry policy is required; those operations are outside this reference. No independent recording download endpoint or bearer forwarding to an asset URL is inferred.
