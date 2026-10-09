# Kubeshark snapshot lifecycle: bindings

Bindings follow the publisher Hub API. The configured reverse proxy can add a prefix; no arbitrary default external destination is supplied.

| Operation | Binding | Payload/result |
|---|---|---|
| Capture state | `GET /mcp/raw-capture` | `enabled`, `session_id` |
| Time boundaries | `GET /mcp/data-boundaries` | `cluster` and per-node `oldest_ts`, `newest_ts` |
| Create | `POST /mcp/snapshots` | JSON `name`, `duration`; `success`, `name`, `status` |
| List/read | `GET /mcp/snapshots`; `GET /mcp/snapshots/{name}` | Snapshot metadata/status |
| Export | `GET /mcp/snapshots/{name}/pcap` | Optional `nodes`, `bpf_filter`, `start_time`, `end_time`; binary `application/vnd.tcpdump.pcap` |
| Delete | `DELETE /mcp/snapshots/{name}` | `success`, `name` |
| Download relative artifact | MCP `download_file(path, dest?)` | Local `path`, `size`, source `url` |

`start_time`/`end_time` are Unix milliseconds. Native sample states include `in_progress` and `completed`; other returned states are preserved, not guessed. Download destination is relative to `KUBESHARK_MCP_DOWNLOAD_DIR`, or the client's launch directory when unset. The client rejects paths escaping this base. The cited page does not publish a complete snapshot error/status enumeration.

## Sources

- [Kubeshark snapshot and raw-capture tools](https://docs.kubeshark.com/en/mcp/raw_capture_tools). Retrieved 2026-10-09.
- [Kubeshark MCP installation](https://docs.kubeshark.com/en/mcp/cli). Retrieved 2026-10-09.
