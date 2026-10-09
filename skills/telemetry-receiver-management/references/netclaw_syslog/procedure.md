# NetClaw syslog receiver lifecycle

Manage only the selected publisher receiver process, without changing exporters.

## Common Sequences

- Start: **Inspect listener** → **Start listener** → **Inspect listener**.
- Stop: **Inspect listener** → **Stop listener** → **Inspect listener**.

### Inspect listener

Status returns running state, bind/port, receive/store/transport counters and available audit statistics. A running process is not proof of received or successfully decoded data. Rate-limit, parse, overflow and audit failures remain visible when returned. A tool response containing an error string is a failure even if the MCP envelope is not marked as an error.

### Start listener

Starting binds a socket and initializes a fresh store: stop and confirm with the operator before proceeding. Bind address, port and supported transport are explicit inputs; wildcard exposure is not selected by default in this procedure. Already-running output means no reconfiguration occurred. Permission, occupied-port, unsupported-protocol or other errors leave startup failed. The subsequent status must identify the requested running listener; an uncertain result is inspected before retry.

### Stop listener

Stopping interrupts collection and can drop incoming observations: stop and confirm with the operator before proceeding. Native stopped output and a non-running status establish listener shutdown. Already-stopped output is reported separately. The operation does not disable exporters, and no automatic restart follows.

## Patterns

A stop/start cycle recreates the store and is not a lossless restart. Start does not configure network devices.

## Known limitations

Store data is in memory; restarting a stopped receiver creates a new store. Retention cleanup occurs on insertion, so idle-store reads can contain older data. The publisher records bounded audit data locally; its pending/error status is distinct from receive success. TCP is newline-framed only; no TLS or octet-counted framing is established by this implementation.

## Tools

Assumes the authenticated client described in [the bindings](endpoints.md).

| Operation | Description | Category |
|---|---|---|
| Inspect | Read receiver and store counters | Read |
| Start/stop | Change selected listener state | Collection change |

## Verification checklist

- Exact bind/port and supported protocol are confirmed.
- Status matches the requested lifecycle outcome.
- Collection gaps, parser failures and audit errors remain visible.
- No device exporter configuration was sent.

## Sources

- [NetClaw publisher receiver implementation](https://github.com/automateyournetwork/netclaw/blob/95bb17e27a6a2538fcb0168d0b1d0ab5bbe34692/mcp-servers/syslog-mcp/syslog_mcp_server.py). Retrieved 2026-10-09.
- [Publisher receiver guide](https://github.com/automateyournetwork/netclaw/blob/95bb17e27a6a2538fcb0168d0b1d0ab5bbe34692/mcp-servers/syslog-mcp/README.md). Retrieved 2026-10-09.
- [Publisher store behavior](https://github.com/automateyournetwork/netclaw/blob/95bb17e27a6a2538fcb0168d0b1d0ab5bbe34692/mcp-servers/syslog-mcp/message_store.py). Retrieved 2026-10-09.
- [Publisher record schema](https://github.com/automateyournetwork/netclaw/blob/95bb17e27a6a2538fcb0168d0b1d0ab5bbe34692/mcp-servers/syslog-mcp/models.py). Retrieved 2026-10-09.
