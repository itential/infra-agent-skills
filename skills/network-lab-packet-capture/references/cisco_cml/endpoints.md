# Cisco CML link capture: bindings

An authenticated, TLS-verifying `virl2_client.ClientLibrary` is available as `client`; `lab`, `node`, and `link` are objects resolved by identifier. Bindings are publisher SDK methods at the cited commit, not NetClaw MCP tool names. Server/SDK compatibility must match the installed release.

| Operation | SDK binding | Inputs/result |
|---|---|---|
| Resolve | `lab.links()`; `lab.get_link_by_id(link_id)` | Link |
| Start | `link.start_capture(maxpackets=None, maxtime=None, bpfilter=None, encap="ethernet")` | `maxpackets`: 1–1,000,000; `maxtime`: seconds, 1–86,400; filter: 1–128 characters; dictionary |
| Inspect | `link.capture_status()` | Capture dictionary |
| Stop | `link.stop_capture()` | Completion or exception |
| Download | `link.download_capture()` | PCAP bytes |
| Decode | `link.get_capture_packets()`; `link.get_capture_packet(packet_id)` | Packet dictionaries; ID starts at 1 |


## Sources

- [Cisco CML Link documentation and implementation](https://github.com/CiscoDevNet/virl2-client/blob/7ac2c924ccbdc02264578a95327f8a1363172076/virl2_client/models/link.py). Retrieved 2026-10-09.
