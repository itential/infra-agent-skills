# Cisco CML link capture

Capture and retrieve packets from one explicitly selected CML lab link.

## Common Sequences

- Collect a capture: **Select link** → **Start capture** → **Inspect capture** → **Stop capture** → **Retrieve**.
- Retrieve an existing capture: **Select link** → **Inspect capture** → **Retrieve**.

### Select link

Lab link inventory resolves the link and both interfaces. An unresolved link ends the sequence before capture. The client’s HTTP/transport errors are retained; no generic retry interval is supplied by the cited SDK.

### Start capture

The publisher accepts a packet ceiling, duration ceiling, optional Berkeley filter, and encapsulation. Before starting collection on the selected lab link: stop and confirm with the operator before proceeding. The returned dictionary describes the capture and its configuration. Rejected parameters are corrected against the binding limits, not silently broadened.

### Inspect capture

The status operation returns capture configuration, start time and packet count. This dictionary is the evidence; a universal status-field enum is not defined in the cited SDK and must not be fabricated.

### Stop capture

Before ending an existing collection: stop and confirm with the operator before proceeding. The publisher stop operation returns normally on completion; an HTTP/transport error is a failure, not an empty capture.

### Retrieve

The download operation returns bytes for the link’s last PCAP. The decoded-packet operations can retrieve all packet dictionaries or one 1-based packet number. Before saving those bytes over an existing local artifact: stop and confirm with the operator before proceeding. Byte retrieval is distinct from the earlier capture-start acknowledgement. No traffic is generated or protocol reset performed by this procedure.

## Patterns

The download concerns the link’s last capture. A filter that matches no packets can produce an empty collection; the procedure preserves status and packet count alongside the artifact.

## Known limitations

The SDK does not document all server capture error bodies, overwrite behavior or retention limits. Unknown failures are reported with their native details. Packet payloads can contain secrets.

## Tools

Assumes the authenticated client described in [the bindings](endpoints.md).

| Operation | Description | Category |
|---|---|---|
| Resolve/inspect | Read link and capture metadata | Read |
| Start/stop capture | Control collection on a lab link | Change |
| Retrieve capture | Download PCAP or decoded packets | Read |

## Verification checklist

- The intended link and requested capture limits are retained.
- Capture status and packet count are reported without guessed field meanings.
- Downloaded bytes are saved separately from status JSON.
- Failed download is not reported as a zero-packet success.

## Sources

- [Cisco CML Link documentation and implementation](https://github.com/CiscoDevNet/virl2-client/blob/7ac2c924ccbdc02264578a95327f8a1363172076/virl2_client/models/link.py). Retrieved 2026-10-09.
