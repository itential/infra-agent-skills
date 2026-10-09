# Itential MCP workflow bindings

Sources: [tool reference](https://github.com/itential/itential-mcp/blob/devel/docs/tools.md) and [Operations Manager implementation](https://github.com/itential/itential-mcp/blob/devel/src/itential_mcp/models/operations_manager.py), retrieved 2026-10-09. The authenticated configured MCP client supplies the instance and transport.

| Operation | Tool | Inputs / result |
|---|---|---|
| Discover workflows | `get_workflows` | No operator arguments; enabled endpoints with `route_name` and input schema |
| Start workflow | `start_workflow` | `route_name`, optional `data`; delegates to generic automation trigger |
| List jobs | `get_jobs` | Optional `name` (workflow name), `project` filters; exact deployed schema governs names |
| Read job | `describe_job` | `object_id`; job tasks, metrics and native status |

The current start response for a workflow contains `object_id`, `name`, `description`, `tasks`, `status`, `metrics`. The generic trigger can instead return `session_id` and status for an agent. That result is outside this workflow-only procedure. The publisher describes statuses `error`, `complete`, `running`, `cancelled`/`canceled`, `incomplete`, `paused`; cancellation spelling differs between its list and detail documentation. A full stable error catalogue is not published here; returned errors are retained.
