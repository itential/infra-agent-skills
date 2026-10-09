# Junos configuration bindings

Source: [published Junos MCP tool schemas and handlers](https://github.com/Juniper/junos-mcp-server/blob/main/jmcp.py), main retrieved 2026-10-09.

| Operation | Tool and inputs | Output |
|---|---|---|
| Resolve target | `get_router_list()` | Mapped device information with authentication secrets filtered. |
| Read facts/configuration | `gather_device_facts(router_name)` / `get_junos_config(router_name)` | Facts or configuration text. |
| Render only | `render_and_apply_j2_template(template_content, vars_content, apply_config=false)` | Rendered configuration; no device connection. |
| Check candidate | Same tool, `apply_config=true, dry_run=true`, with `router_name` or `router_names[]` | Commit-check result, difference and candidate rollback/cleanup messages. |
| Commit template | Same tool, `apply_config=true, dry_run=false` | Per-router commit/no-change/failure messages. |
| Commit literal payload | `load_and_commit_config(router_name, config_text, config_format, commit_comment)` | Commit or no-change text; errors for blocklist, lock, format or load/commit failures. |
| Compare history | `junos_config_diff(router_name, version)` | Running-versus-rollback difference; version 1–49 in the documented schema. |

Template arguments also support `config_format` (`set`, `text`, `xml`), `commit_comment`, and `timeout` in seconds. `vars_content` contains YAML text, not an already-decoded object. Neither apply nor dry-run defaults to true: render-only is the default.

Recognizable literal-load outcomes include `No configuration changes detected`, `Failed to lock configuration`, and `Failed to load/commit configuration`. A successful literal load starts with `Configuration successfully loaded and committed`. Template outcomes and all associated cleanup messages must be read together; a successful check does not override a later rollback failure.
