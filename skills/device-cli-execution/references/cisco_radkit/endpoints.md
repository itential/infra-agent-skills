# Cisco RADKit command bindings

Source: [publisher connector README](https://github.com/CiscoDevNet/radkit-mcp-server-community), main retrieved 2026-10-09.

| Operation | Literal tool | Parameters/result |
|---|---|---|
| List enrolled names | `get_device_inventory_names()` | String containing the inventory names. |
| Inspect attributes | `get_device_attributes(target_device)` | JSON string describing that enrolled device. |
| Run raw CLI | `exec_cli_commands_in_device(target_device, cli_commands, timeout?, max_lines?, service_serial?)` | Raw command response string. |
| Run structured CLI | `exec_command(device_name, command, service_serial?, timeout?, max_lines?)` | Dictionary or list of dictionaries with status and truncation metadata. |

The installed tool schema defines the optional argument types and defaults; the README does not publish a complete stable error enumeration. Raw command output is not itself a parsed success verdict. Authentication is configured at the server, using RADKit certificates or the documented direct-RPC credentials; these values are not repeated in invocation payloads or reports.
