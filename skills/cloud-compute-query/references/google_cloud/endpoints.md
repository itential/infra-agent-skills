# Google Cloud compute read bindings

Sources: [Compute MCP reference](https://docs.cloud.google.com/compute/docs/reference/mcp) and [Resource Manager project search](https://docs.cloud.google.com/resource-manager/reference/mcp/search_projects), retrieved 2026-10-09. OAuth-authenticated MCP endpoints are `https://compute.googleapis.com/mcp` and `https://cloudresourcemanager.googleapis.com/mcp`. The configured client handles protocol headers. `tools/list` supplies current detailed schemas; tool names below are the publisher catalogue, not inferred REST paths.

| Family | Tool(s) | Required scope from publisher overview |
|---|---|---|
| Projects | `search_projects` | Optional `query`, `pageSize`, `pageToken`; returns `projects`, `nextPageToken` |
| Instances | `list_instances`, `get_instance_basic_info` | `project`, `zone`; detail adds `name` |
| Attached disks | `list_instance_attached_disks` | Project, zone, instance name |
| Managed groups | `list_instance_group_managers`, `get_instance_group_manager_basic_info`, `list_managed_instances` | Project and zone; detail/member query adds group name |
| Templates | `list_instance_templates`, `get_instance_template_basic_info`, `get_instance_template_properties` | Project; detail adds template name |
| Disks | `list_disks`, `get_disk_basic_info`, `get_disk_performance_config` | Project and zone; detail adds disk name |
| Snapshots | `list_snapshots` | Project |
| Machine / accelerator types | `list_machine_types`, `list_accelerator_types` | Project and zone |
| Images | `list_images` | Project |
| Reservations | `list_reservations`, `get_reservation_basic_info`, `get_reservation_details` | Project and zone; detail adds reservation name |
| Commitments | `list_commitments`, `get_commitment_basic_info`, `list_commitment_reservations` | Project and region; detail/relationship adds commitment name |

Instance listing accepts `pageSize` and `pageToken`, returning `instances` and `nextPageToken`. Current basic-info members are `name`, `id`, `status`, `machineType`, `createTime`, `guestAccelerators`. Companion names/fields in other family rows are resolved from that tool's published/live schema rather than assuming the instance argument name applies universally. Project search token descriptions mention snake_case in prose; its JSON contract is `pageToken` and `nextPageToken`.
