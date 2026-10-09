# Juniper Junos MCP: validate and commit configuration

Render an approved template, inspect a device-side candidate check, and commit the reviewed change.

Sources: [Juniper README](https://github.com/Juniper/junos-mcp-server) and [tool implementation and schemas](https://github.com/Juniper/junos-mcp-server/blob/main/jmcp.py), main retrieved 2026-10-09. Bindings appear in [endpoints.md](endpoints.md).

## Common Sequences

- Template change: Resolve target → Render template → Check candidate → Commit template → Read result.
- Already reviewed literal configuration: Resolve target → Commit literal configuration → Read result.

## Resolve target

The configured router list establishes exact names. Template application validates every supplied name before touching a device. Device facts and configuration reads can identify the intended target and current state.

Success: all target names resolve. Missing names stop the operation rather than being substituted by a guessed match.

## Render template

Local rendering combines the supplied Jinja2 template and YAML variables without connecting to a device. Missing template variables fail instead of becoming empty strings. The rendered payload and declared configuration format are the review artifact.

Success: rendered text matches the requested change. YAML/template failures are corrected before any device application.

## Check candidate

**This loads a candidate on a live device: stop and confirm with the operator before proceeding.** Template application in dry-run mode uses an exclusive configuration session, loads the rendered candidate, displays its difference and runs a commit check. The documented implementation then rolls back the candidate and verifies that no pending difference remains.

Success: the check passes and candidate cleanup succeeds; a clean no-change result is also explicit. Configuration load, lock, or commit-check errors end this candidate attempt. A rollback/cleanup error remains a failure even if validation passed; the session is not treated as ready for a commit.

## Commit template

**This commits live configuration: stop and confirm with the operator before proceeding.** The same reviewed template and variables are applied with dry-run disabled. The implementation takes an exclusive session, loads the candidate, checks its difference, runs a commit check, and commits with the supplied comment.

Success: the per-router result confirms the commit or reports no configuration difference. Lock, load, commit-check, and commit errors remain distinct failure evidence. A timeout during commit may leave the resulting device state unknown and requires inspection before retrying.

## Commit literal configuration

**This loads and commits live configuration in one call: stop and confirm with the operator before proceeding.** The literal operation checks the publisher's configuration blocklist, locks configuration, loads the approved payload, evaluates its difference and commits. It does not offer a separate candidate-review pause inside the call. A blocked pattern is rejected before load/commit.

Success: explicit committed or no-change text is returned. Unsupported format, lock failure and load/commit failure are reported rather than ignored. The implementation attempts rollback and unlock after failure and closes the connection if cleanup fails; this is not an automatic rollback of a successful earlier commit.

## Read result

The outcome preserves each target's messages. Current configuration can be retrieved for the caller's requested verification. The rollback comparison operation compares running configuration against a historical version, not a pending candidate.

Success: reported commit/no-change/failure agrees with the per-device result and available configuration evidence. Batch application runs devices in parallel and can have mixed outcomes.

## Patterns

Local render-only and device dry-run are different operations. The literal and template paths also have different validation behavior; a template commit check must not be claimed for a literal commit call.

## Known limitations

The MCP implementation includes submitted configuration text in returned annotations for literal loads. Such output can expose configuration secrets; reports must avoid redistributing raw sensitive configuration. Publisher SSH-key and secured-server requirements apply. The server's blocklist is a safeguard, not a substitute for reviewing a valid but disruptive configuration.

## Tools

| Operation | Description | Category |
|---|---|---|
| Resolve/read device | Retrieve mapped names, facts or current configuration | MCP query |
| Render template | Produce candidate text without a device session | Local template operation |
| Check candidate | Validate and roll back a temporary candidate | Device configuration session |
| Commit configuration | Load and commit an approved payload | Device configuration mutation |

## Verification checklist

- Exact targets and rendered/literal payload were reviewed.
- Candidate validation and cleanup outcomes were preserved.
- Live candidate loads and commits used their confirmation gates.
- Every device's native commit, no-change, or error result is reported.
