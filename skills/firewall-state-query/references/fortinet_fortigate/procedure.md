# FortiGate observed device state

Read FortiOS 7.6 system, interface, routing, HA and IPsec observations from an existing CLI session.

Sources: Fortinet [7.6.0 CLI troubleshooting cheat sheet](https://docs.fortinet.com/document/fortigate/7.6.0/cli-troubleshooting-cheat-sheet/420966/cli-troubleshooting-cheat-sheet) and [7.6.5 IPsec diagnose commands](https://docs.fortinet.com/document/fortigate/7.6.5/administration-guide/44240/ipsec-related-diagnose-commands), retrieved 2026-10-09. Literal CLI payloads remain inline.

## Common Sequences

- Device state snapshot: Identify responding context → Read interface state → Read routes → Read HA state.
- IPsec state snapshot: Identify responding context → Read phase 1 → Read phase 2 → Read tunnel summary and counters.

### Identify responding context

`get system status` returns system identity/version information; `execute time` returns the device time. `diagnose sys vd list` reports available virtual-domain context and statistics. Success is actual output from the intended device and established session context. The cited cheat sheet does not define a VDOM-switching sequence; an already scoped session is a prerequisite. Missing scope remains an incomplete observation.

### Read interface state

`get system interface` returns interface/address details. A selected interface's detailed observation uses `diagnose hardware deviceinfo nic <interface>`. Success is the returned interface evidence, without assuming every hardware family exposes identical counters.

### Read routes

`get router info routing-table all` returns the observed IPv4 routing table. Success is the table in the session's routing context; a manager's intended routes are not a replacement when the device read fails.

### Read HA state

`get system ha status` returns HA information. The result remains associated with the device that answered; the procedure does not change HA role or log into another member automatically.

### Read phase 1

`diagnose vpn ike gateway list` returns IKE gateway records with virtual-domain, gateway and IKE security-association evidence. The publisher examples distinguish created associations from established associations. Success is the selected gateway's returned evidence; an established IKE association alone does not demonstrate an established IPsec association.

### Read phase 2

`diagnose vpn tunnel list` returns phase-2 tunnel and selector/security-association evidence. The result includes selector-specific state and counters where available. The publisher's actual output can expose encryption/authentication key material. This is a secret-bearing response: report only required nonsecret state, with keys omitted from logs and artifacts. The example's tunnel-level up field is not substituted for selector association evidence.

### Read tunnel summary and counters

`get vpn ipsec tunnel summary` and `get vpn ipsec tunnel details` provide the documented tunnel views. `diagnose vpn ipsec status` provides cryptographic counters. Success is the returned state for the observed scope; counter values do not establish application reachability or identify a unique fault cause.

For every read, the cited pages do not enumerate command error messages. A rejected command, missing permission, incompatible release or failed session is a failed observation with the native error preserved; none is reported as an empty healthy table.

## Patterns

- IKE and IPsec observations remain separate and retain their gateway/selector context.
- Manager intent and device observations answer different questions.

## Known limitations

- CLI transport replaces the unverified NetClaw-authored REST wrapper.
- No universal licensing/authentication rule, capacity threshold, drift verdict or selector-mismatch diagnosis is claimed.
- Tunnel clearing, live debugging, session clearing, reboot and configuration changes are excluded.
- VPN diagnostics can expose keys even though these commands do not change configuration.

## Tools

| Mechanism | Description | Category |
|---|---|---|
| Authenticated FortiOS CLI session | Execute the listed observation commands in the established device/VDOM context | Read |

## Verification checklist

- Responding device, release, timestamp and VDOM context are recorded.
- Successful output and rejected/unavailable observations are distinguished.
- IKE and phase-2 association evidence remain separate.
- No key material appears in the report or saved artifact.
