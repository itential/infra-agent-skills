# ZPA application segment bindings

Source: [publisher implementation](https://github.com/zscaler/zscaler-mcp-server/blob/master/src/zscaler_mcp/tools/zpa/app_segments.py) and [confirmation protocol](https://github.com/zscaler/zscaler-mcp-server/blob/master/docs/guides/mcp-protocol.md), current master, retrieved 2026-10-09. These are MCP bindings, not interchangeable REST request bodies.

| Operation | Tool | Inputs |
|---|---|---|
| List segments | `zpa_list_application_segments` | Optional `search`, `microtenant_id`, integer `page >= 1`, integer `page_size` from 1–500 |
| Read segment | `zpa_get_application_segment` | String `segment_id`; optional `microtenant_id` |
| Create segment | `zpa_create_application_segment` | Required `name`, `segment_group_id`; at least one `tcp_port_ranges` or `udp_port_ranges` list; optional fields below |
| Update segment | `zpa_update_application_segment` | Required `segment_id`; optional fields below |
| Delete segment | `zpa_delete_application_segment` | String `segment_id`; optional `microtenant_id` |

Common create/update inputs: `domain_names`, `server_group_ids`, `tcp_port_ranges`, `udp_port_ranges` are string arrays; port lists contain consecutive start/end values, for example `["443", "443"]`. `name`, `description`, `segment_group_id`, `microtenant_id` are strings; `enabled` is boolean and defaults to true for create; `advanced` is a dictionary of installed SDK keyword fields. It merges last and can override other payload entries.

Read and write responses retain the segment record. A completed delete returns `success: true` and a message. Exact local validation errors include `name and segment_group_id are required`, `At least one port range is required (tcp_port_ranges/udp_port_ranges).`, and `segment_id is required for update` / `segment_id is required for delete`. API failures appear as operation-specific RuntimeError messages containing the SDK error; no complete HTTP error catalogue is established here.

Native elicitation uses protocol confirmation rather than an input field. A client without elicitation gets `DESTRUCTIVE OPERATION - CONFIRMATION REQUIRED`; after human approval its retry preserves the identical resource inputs and carries `kwargs={"confirmation_token": "<returned-token>"}`. Invalid, expired or reused fallback tokens are rejected. The publisher documents process-bound confirmation state; a restarted server or a different replica may require a new confirmation.
