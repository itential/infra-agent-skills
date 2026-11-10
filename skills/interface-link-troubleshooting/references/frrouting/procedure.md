# FRRouting — Interface / Link Troubleshooting Decision Tree

Read-only diagnosis of interface and link problems as FRRouting's zebra daemon sees them on a Linux host, organized by symptom. Follow the entry point matching the observed symptom. Source: FRR "latest" user manual, chapters "Zebra", "VRRP", and "Basic commands" (retrieved 2026-11-10). Behavior varies by release; confirm with `show version`.

FRR does not manage the physical layer. The interfaces are kernel interfaces; zebra reads their state, and routing daemons act on what zebra reports. The manual documents no physical-layer diagnostics, error counters, or negotiation display, so the entry points below cover what FRR itself states and mark the rest as not documented. Commands are entered in the FRR shell (`vtysh`).

## Platform facts the entry points rest on

- Interface state shown by FRR comes from the kernel. `shutdown` in the interface's FRR configuration brings the interface down; its absence leaves it up.
- `link-detect` makes FRR follow link state. It is on by default, works only on Linux, and only where the network driver reports link state through the `IFF_RUNNING` flag.
- Display: `show interface [NAME] [vrf VRF|brief] [json]`. With no name it lists every interface; with a name it shows that interface in detail.
- `protodown` is an interface mode that behaves like `NO-CARRIER` without removing addresses. The manual documents FRR setting it on the virtual interfaces of a VRRP router that moves to the Backup state (Linux kernel 5.1 or later; the zebra chapter states "> 5.1", so confirm the exact minimum on the host). The reason bit needs a descriptor under `/etc/iproute2/protodown_reasons.d/`, and the host's `ip -d link show` displays protodown information. The global command `zebra protodown reason-bit (0-31)` changes the kernel reason bit FRR uses, default 7, in case another program on the host uses it.
- Logging and debug: `log syslog`, `log file`, `log stdout`; `show logging` lists active destinations; `debug zebra events` (zebra events), `debug zebra kernel` (kernel and OS events), `debug zebra dplane` (dataplane and FIB events).

## Entry point: interface_down

1. Run `show interface brief` to find the interface, then `show interface NAME` for its detail (add `json` when the output is parsed by a program).
2. Read whether the interface is administratively down. Compare with `show running-config`: a `shutdown` line under the interface means an operator disabled it in FRR configuration. Confirm with the operator whether that is intended before treating it as a fault.
3. If the interface is not administratively shut down but the detail shows no carrier, go to the no_link entry point.
4. If the interface is a virtual one used by VRRP and the router is Backup, `protodown` is expected: it is the documented behavior of a Backup router. Confirm with `show vrrp interface INTERFACE`, which reports Master or Backup state, priority, and advertisement counts. A VRRP interface that stays down on the Master is a different condition; report it with the `show vrrp` evidence.
5. If the interface is `protodown` and no VRRP router explains it, report the protodown state and the evidence. Read the reason with the host's `ip -d link show`. Not documented: which other FRR features set `protodown`, whether `show interface` shows the reason, and how it is cleared. Do not invent them.

Success: the diagnosis names one of administratively shut down, no carrier, or protodown with a documented VRRP cause, each with the command output that shows it.

## Entry point: flapping

1. Not documented: an FRR-specific flap diagnosis, damping feature, or list of flap causes for interfaces. Report that gap.
2. To observe transitions, enable `debug zebra kernel` and `debug zebra events` and read the log destination listed by `show logging`. Enabling debug changes runtime logging on the device: stop and confirm with the operator before enabling it, unless standing instructions already allow it, and disable the debug groups after the observation. Assumption: interface up and down notifications from the kernel appear under these debug groups; the manual describes them only as kernel/OS events and zebra events.
3. Assumption: a VRRP router that alternates between Master and Backup toggles `protodown` on its virtual interfaces, since the manual ties `protodown` to the Backup transition. Check `show vrrp` for state and advertisement counts before looking at the link.
4. A physical cause is not visible to FRR; report that the host's own tooling is needed for it.

## Entry point: high_errors

Not documented: error, discard, or drop counters for interfaces in FRR's manual. `show interface NAME` prints interface detail, but its field list is not specified there, so do not assert counter names. Report the values actually printed, say that no FRR-documented diagnosis maps them to causes, and that counters at the host level are outside FRR's documentation.

## Entry point: duplex_mismatch

Not documented: duplex or speed negotiation in FRR's manual. The interface's speed and duplex come from the kernel and driver. Report that FRR cannot diagnose a duplex mismatch and that the host's own link tooling is needed; do not carry over another platform's documented signs.

## Entry point: no_link

1. Run `show interface NAME` and read whether it reports carrier or link up.
2. Check that `link-detect` is in effect for the interface (it is the default; `show running-config` shows a changed setting). If it is disabled, or the driver does not report `IFF_RUNNING`, FRR does not follow link state. Assumption: the interface state shown may then not reflect the link; report that caveat.
3. For a VRRP virtual interface, also check the parent interface: IPv4 VRRP needs an IPv4 address on the base interface, and the virtual interface must be a macvlan in bridge mode, as VRRP does not work otherwise.
4. Not documented: further FRR-specific causes of no link. Anything beyond the above is a physical or driver question for the host's own tooling.

## Patterns

- Report both FRR's view and what it cannot see: FRR reflects kernel flags, not the cable or optics.
- When a routing symptom is the real complaint and the link is up, hand off to routing troubleshooting. For a VRRP Master that does not forward traffic, the VRRP chapter names the kernel setting `net.ipv4.conf.<interface>.ignore_routes_with_linkdown=1`.

## Known limitations

- No documented FRR diagnosis for flapping beyond observing events, for high errors, or for duplex mismatch.
- The field list of `show interface` is not specified in the manual.
- Which features other than VRRP set `protodown`, and how a stuck `protodown` is cleared, are not documented.
- Behavior depends on the installed FRR release and the host kernel.

## Tools

| Operation | Description | Category |
|---|---|---|
| FRR shell session (`vtysh`) | Run `show` commands against zebra | read |
| FRR shell session (`vtysh`), debug | Enable and disable zebra debug groups | diagnostic (runtime logging change) |
| Host shell | `ip -d link show` for protodown information | read |
| Log destination read | Read the file or syslog destination reported by `show logging` | read |

## Verification checklist

- [ ] Interface identified with `show interface brief` or `show interface NAME`
- [ ] Diagnosis names one documented state: administratively shut down, no carrier, protodown with VRRP evidence, or the `link-detect` caveat
- [ ] Literal command output reported with the diagnosis
- [ ] Not-documented symptoms reported as gaps, with no other vendor's behavior carried over
- [ ] Any debug group enabled was confirmed first and disabled afterward
