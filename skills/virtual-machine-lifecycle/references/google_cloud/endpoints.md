# Compute Engine lifecycle MCP bindings

Sources: [create](https://docs.cloud.google.com/compute/docs/reference/mcp/tools_list/create_instance), [delete](https://docs.cloud.google.com/compute/docs/reference/mcp/tools_list/delete_instance), [start](https://docs.cloud.google.com/compute/docs/reference/mcp/tools_list/start_instance), [stop](https://docs.cloud.google.com/compute/docs/reference/mcp/tools_list/stop_instance), [reset](https://docs.cloud.google.com/compute/docs/reference/mcp/tools_list/reset_instance), [resize](https://docs.cloud.google.com/compute/docs/reference/mcp/tools_list/set_instance_machine_type), [operation](https://docs.cloud.google.com/compute/docs/reference/mcp/tools_list/get_zone_operation), retrieved 2026-10-09.

Configured OAuth MCP endpoint: `https://compute.googleapis.com/mcp`. Calls use `tools/call` with `name` and `arguments` following the published JSON schema.

| Operation | Tool | Arguments |
|---|---|---|
| Read instance | `get_instance_basic_info` | `project`, `zone`, `name` |
| Create | `create_instance` | Required `project`, `zone`, `name`; optional `machineType`, `imageFamily`, `imageProject`, `guestAccelerators`, `maintenancePolicy` |
| Delete | `delete_instance` | `project`, `zone`, `name` |
| Start | `start_instance` | `project`, `zone`, `name` |
| Stop | `stop_instance` | `project`, `zone`, `name` |
| Reset | `reset_instance` | `project`, `zone`, `name` |
| Resize | `set_instance_machine_type` | `project`, `zone`, `name`, `machineType` |
| Track operation | `get_zone_operation` | `project`, `zone`, `name` set to returned operation name |

Mutation results contain `operationName`. Operation detail contains `status`, `error.errors` and `warnings`, plus available HTTP error information. Success is `status=DONE` without errors. Accelerator entries use `acceleratorType`, `acceleratorCount`. Creation defaults documented in prose are `machineType=e2-medium`, `imageFamily=debian-12`, `imageProject=debian-cloud`; no other omitted default is inferred. Exact enum/options are checked against the deployed tool schema.
