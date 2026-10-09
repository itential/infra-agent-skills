# Wireshark offline packet inspection

Read an existing capture with Capinfos and TShark.

### 1. Inspect the capture

`capinfos -c -u -s -l -t <capture-file>` reports packet count, duration, file size, snapshot length and format. Open/read errors appear on stderr and produce an error exit status. Partial metadata from a damaged file is not a complete capture assessment. The parser detects supported capture formats rather than trusting a filename extension.

### 2. Produce the requested overview

`tshark -n -r <capture-file> -q -z io,phs -z conv,tcp -z endpoints,ip -z expert` produces protocol hierarchy, TCP conversations, IPv4 endpoints and expert findings. Other advertised conversation types include UDP, Ethernet and IPv6. A requested type is selected explicitly; IPv4-only endpoints do not include all IPv6 traffic. Native errors and exit status accompany output.

### 3. Narrow and decode

`tshark -n -r <capture-file> -Y '<display-filter>' -V` returns detailed decoding for matching frames. A particular frame uses the display filter `frame.number == <number>`. JSON output uses `-T json`; selected fields use `-T fields -e <field>`, with repeated field options and optional `-E header=y`.

`tshark -G fields` identifies installed field names before a protocol-specific export. Invalid filters or unsupported fields remain errors, not zero-match results. The request’s filter is passed as one argument rather than evaluated as shell syntax.

### 4. Preserve analysis scope

Two-pass file analysis uses `-2` when future-dependent fields or reassembly relationships are needed; it requires seekable input and cannot be used with pipes/FIFOs. A packet-count cap `-c` counts packets read, including frames that fail the display filter. Thus a capped result is explicitly partial. Native expert classifications, frame numbers and statistics are reported without turning a heuristic finding into a proved cause.

## Patterns

`-n` suppresses name resolution. Packet detail, JSON and field output are alternative representations. Display filters differ from capture filters; this sequence reads a file and never opens a live interface.

## Known limitations

Encrypted payloads may not decode without separately authorized keys. Snapshot truncation and packet loss constrain findings. No Packet Buddy MCP directory allowlist, automatic upload handler or result-size guarantee is inherited.

## Tools

| Mechanism | Description | Category |
|---|---|---|
| Local CLI runner | Execute installed Capinfos/TShark against an existing file | Offline analysis |

## Verification checklist

- The same capture path and requested filters are retained.
- File-read or filter errors are not reported as no traffic.
- Packet caps and address-family scope are explicit.
- Findings include frame/session evidence rather than guessed root cause.

## Sources

- [TShark manual (4.6 documentation at retrieval)](https://www.wireshark.org/docs/man-pages/tshark.html). Retrieved 2026-10-09.
- [Capinfos manual](https://www.wireshark.org/docs/man-pages/capinfos.html). Retrieved 2026-10-09.
