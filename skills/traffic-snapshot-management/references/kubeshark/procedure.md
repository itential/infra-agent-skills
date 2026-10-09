# Kubeshark snapshot lifecycle

Preserve available packet observations and retrieve a scoped PCAP.

## Common Sequences

- Export retained observations: **Check availability** → **Create** → **Inspect** → **Export**.
- Use an existing snapshot: **Inspect** → **Export**.
- Remove a snapshot: **Inspect** → **Delete**.

### Check availability

The raw-capture status must indicate enabled. Data-boundary retrieval identifies the available cluster/node time ranges. A requested interval outside retained data cannot be reconstructed by this procedure. Disabled capture or unavailable access ends snapshot creation; the procedure does not change capture settings.

### Create

Creating a snapshot consumes storage and persists captured payloads: stop and confirm with the operator before proceeding. The request supplies a unique name and duration. A success response with in-progress state is acceptance only; inspection establishes completion. The cited API page does not define a universal polling interval or full error catalogue.

### Inspect

Snapshot listing or named inspection returns native status and, when available, size, timestamps, node count and packet count. Only a completed snapshot is reported as ready for export. An error, missing snapshot or still-running result remains distinct; no automatic duplicate creation is a recovery step.

### Export

The export operation uses the resolved snapshot name, with optional node selection, time boundaries and BPF filter. Time boundaries use Unix milliseconds. The response is PCAP bytes; a service error body is not a capture. Full export is the default when filters are omitted. Before overwriting a local output: stop and confirm with the operator before proceeding. A downloaded relative path can be retrieved through the publisher download operation within its configured destination directory.

### Delete

Snapshot deletion removes retained evidence: stop and confirm with the operator before proceeding. The operation's success response identifies the removed snapshot. A failure remains failed; it is not hidden by removing a local filename. This procedure does not delete delayed-indexing databases or cloud copies.

## Patterns

Raw capture is a prerequisite for PCAP snapshots, while L4 flow observations are independent. Download containment is a publisher safeguard: traversal, absolute paths outside the base directory and outward symlinks are rejected.

## Known limitations

PCAP may contain sensitive payloads; publishing or forwarding it is a separate action. A snapshot name and creation status do not prove that every node retained the requested time range. TLS decryption is not guaranteed by this procedure.

## Tools

Assumes the authenticated client described in [the bindings](endpoints.md).

| Operation | Description | Category |
|---|---|---|
| Check availability | Read capture state/time bounds | Traffic read |
| Create/inspect | Persist and track a snapshot | Traffic storage |
| Export/download | Retrieve PCAP bytes | Artifact read/write |
| Delete | Remove a named snapshot | Destructive storage |

## Verification checklist

- Capture and retained interval support the request.
- Creation acceptance is distinguished from completion.
- Export filters and time units are explicit.
- PCAP bytes, size and destination are verified.
- Writes/deletion have inline gates.

## Sources

- [Kubeshark snapshot and raw-capture tools](https://docs.kubeshark.com/en/mcp/raw_capture_tools). Retrieved 2026-10-09.
- [Kubeshark MCP installation](https://docs.kubeshark.com/en/mcp/cli). Retrieved 2026-10-09.
