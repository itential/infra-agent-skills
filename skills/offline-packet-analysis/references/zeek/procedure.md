# Zeek offline session reconstruction

Generate and correlate Zeek logs from an existing capture.

### 1. Generate logs in a clean directory

The publisher’s offline invocation is `zeek -r <capture-file> LogAscii::use_json=T`. It writes JSON logs in the current directory. A new output directory keeps the run separate; before overwriting existing analysis files, stop and confirm with the operator before proceeding. File, script or analyzer errors remain failed/incomplete processing.

Zeek normally rejects packets with checksum errors. For a capture known to contain checksum-offload artifacts, the documented `-C` option disables checksum validation. The invocation and checksum choice are retained with the findings; ignoring checksums is not evidence that the capture is complete or correct.

### 2. Inspect available connection evidence

The generated log set determines available evidence. `conn.log` contains connection identifiers, endpoint addresses/ports, protocol, detected service and connection-state evidence. An absent log is not interchangeable with an empty successfully generated log. Processing diagnostics and checksum handling must accompany any claim about absence.

### 3. Pivot by the connection identifier

For a selected connection, its `uid` correlates records in available protocol logs such as `http.log`, `dns.log` and `ssl.log`. The publisher demonstrates JSON filtering, for example `jq --arg uid '<connection-uid>' 'select(.uid == $uid)' dns.log`. The same key can select HTTP/TLS records when those logs exist; the procedure does not assert that every Zeek log type contains this key.

### 4. Report the observations

The result includes endpoints, timestamps, the connection UID, protocol records found and any `weird.log` entries associated with that connection. Zeek’s unusual-protocol records are evidence of analyzer observations, not automatically IDS alerts. Encrypted DNS or HTTP cannot be presumed visible as cleartext application records.

## Patterns

One connection may correspond to several protocol transactions. Connection-state semantics depend on protocol: UDP does not acquire a TCP handshake merely because a state label is shared.

## Known limitations

No NetClaw-specific posture enum, fixed log count or capture checksum quality is assumed. Optional logs depend on traffic, configured analyzers and visible payload. The procedure does not start ZeekControl or live monitoring.

## Tools

| Mechanism | Description | Category |
|---|---|---|
| Local CLI and JSON reader | Run Zeek and inspect generated JSON logs | Offline analysis |

## Verification checklist

- Capture, output directory and checksum setting are recorded.
- Correlated records share the selected UID where that schema supports it.
- Missing logs and analyzer errors remain visible.
- No universal every-log-has-UID assertion is made.

## Sources

- [Zeek quick start, offline section](https://docs.zeek.org/en/current/quickstart.html). Retrieved 2026-10-09.
- [Zeek connection log](https://docs.zeek.org/en/current/reference/logs/conn.html). Retrieved 2026-10-09.
- [Zeek DNS log](https://docs.zeek.org/en/current/reference/logs/dns.html). Retrieved 2026-10-09.
- [Zeek HTTP log](https://docs.zeek.org/en/current/reference/logs/http.html). Retrieved 2026-10-09.
- [Zeek TLS log](https://docs.zeek.org/en/current/reference/logs/ssl.html). Retrieved 2026-10-09.
