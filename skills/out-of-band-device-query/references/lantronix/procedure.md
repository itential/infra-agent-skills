# Lantronix Percepxion device evidence

Read console-server records, full port telemetry, stored configuration, firmware comparison, logs and existing-job evidence through Lantronix's publisher MCP implementation.

## Common Sequences

- Device context: **Authenticate and scope** → **Read inventory** → **Read ports and telemetry**.
- Configuration/firmware evidence: **Authenticate and scope** → **Read inventory** → **Read configuration and firmware**.
- Historical operation evidence: **Authenticate and scope** → **Read logs and audits** or **Read existing job evidence**.

### Authenticate and scope

Authentication uses the server's configured credential provider and establishes its process session. Success is the native successful wrapper, with tokens retained by the server. A credential-provider failure or missing required session tokens is failure, even if the login HTTP request completed. The publisher's missing-token error can include raw login-response details, potentially including the other token: those details are sensitive and are not reproduced in reports.

Organization discovery returns authorized IDs and best-effort names. An organization with no visible devices may have no discoverable name; its UUID is used instead. Project-admin sessions require explicit organization scope for the publisher's protected job, telemetry, catalog and audit operations. Missing/ambiguous/out-of-scope organization resolution remains an error, not a reason to broaden the query.

### Read inventory

The device search returns console-server records, with limit and offset. A selected device detail read requires an identifier or serial number and returns that device's properties. Success is a record matching the requested console server and organization. The organization-specific convenience list has no offset parameter; larger collections use the paginated device search. Missing-device and invalid-identity conditions remain failures.

### Read ports and telemetry

The port index returns port identity and connection-state evidence, while the full telemetry operation returns the console server's collected records including attached-device information where present. Success preserves the console-server identity and the raw per-port evidence; an empty port index does not establish that no device is attached.

The pinned single-port helper incorrectly searches the wrapper instead of its nested data and does not propagate API errors. It can therefore return an empty managed-device object despite available telemetry or a failed read. That helper is excluded; this procedure uses the full telemetry response and its explicit success wrapper. Missing telemetry remains unknown, rather than a cable/power diagnosis.

### Read configuration and firmware

The configuration read returns the full editable configuration tree and its collection metadata; its legacy selection argument is ignored. This is a read despite the implementation's route naming. The publisher tool-reference route is stale; the inspected implementation identifies the user-authenticated route and its device-token mismatch error, captured in the wiring file. Configuration values may be sensitive and are reported only at the requested scope without secret material.

Firmware status returns the selected device's version/state. A comparison uses the operator-supplied expected version and optional exact model filter. Its native compliant/non-compliant/unknown categories are equality comparisons against that supplied value, not a security assessment or a latest-version claim. The tool inspects only its first bounded inventory page; totals describe that evaluated subset. Stored firmware packages, configuration templates and smart groups can be listed with explicit bounds to provide context; their presence does not approve an update.

### Read logs and audits

Existing syslog reads query already-uploaded files; they do not request a fresh upload. Access-log query/download returns existing log evidence. The source's free-text access-log query argument is unsupported by the pinned publisher tool; the supported log-level and paging arguments are used.

Detailed audit search uses explicit dates, search text and optional usernames. User-audit search instead returns user records with latest-action summaries and has no date-range argument. Success is the returned records and their original timestamps/scope. Native wrapper errors remain failures, not empty audit evidence.

### Read existing job evidence

Job search/detail resolves the exact existing job-group identifier. Native Completed/Failed status is retained; nonterminal or unknown statuses remain unresolved. For a completed CLI job, a separate output read supplies the same group and device IDs. Zero output results can mean the job is unfinished, the output is not yet available, or the job is not a CLI job; they are not successful empty command output. The per-device result collection preserves individual results for an existing multi-device group.

The publisher states that CLI-output retrieval uses a route absent from its public API specification and verified through its own UI implementation. This reference binds to the official MCP tool at the pinned revision; it does not claim that underlying route is a stable public API.

Across these reads, unauthorized/expired-token responses clear the session and require authentication again. Other API failures retain native status and sanitized error details. Transport failure leaves the observation unavailable. No fixed retry count or freshness threshold is established here.

## Patterns

The outer successful MCP wrapper confirms the read, while an inner job or device status describes the stored object. Job metadata and actual command output are separate evidence. Exact version equality is deterministic only relative to the operator's supplied expected version and the evaluated page.

## Known limitations

No CLI dispatch, direct SLC API/SSH session, configuration update/clone, firmware upload/update, smart-group/template creation/deletion, device assignment/removal/reboot, syslog upload request, user-access edit or credential-provider switch is included. No serial SSH port formula or universal OOB readiness threshold is inferred from the source skill.

Sources: Lantronix [tool reference](https://github.com/Lantronix/percepxion-mcp-server/blob/533fdc981f0457043e948204db216e2b8a4076f5/docs/tools.md), [server implementation](https://github.com/Lantronix/percepxion-mcp-server/blob/533fdc981f0457043e948204db216e2b8a4076f5/src/percepxion_mcp/server.py), [client/error handling](https://github.com/Lantronix/percepxion-mcp-server/blob/533fdc981f0457043e948204db216e2b8a4076f5/src/percepxion_mcp/client.py), retrieved 2026-10-09. Bindings: [endpoints](endpoints.md).

## Tools

| Operation | Purpose | Category |
|---|---|---|
| Authenticate and scope | Establish session and identify authorized organizations | Authenticate/Read |
| Read inventory | Search/read console-server records | Read |
| Read ports and telemetry | Read port state and full attached-device telemetry | Read |
| Read configuration and firmware | Read config, version comparison and stored catalogs | Read |
| Read logs and audits | Read existing stored logs/audit records | Read |
| Read existing job evidence | Read group status, per-device results and CLI output | Read |

## Verification checklist

- Session success and exact organization/device scope are established.
- Native wrapper errors are checked before inspecting returned records.
- Port-state records and attached-device telemetry remain distinct.
- Bounded firmware comparison and paged inventories are not claimed fleet-complete.
- Job completion and retrieved output are separately verified.
- Publisher API gaps and excluded helper defects remain visible.
