# Nexus EVPN/VXLAN observations

Read Nexus 9000 NX-OS NVE, EVPN route and Ethernet-segment evidence without changing the fabric.

Sources: Cisco [NX-OS 10.4 VXLAN BGP EVPN verification](https://www.cisco.com/c/en/us/td/docs/dcn/nx-os/nexus9000/104x/configuration/vxlan/cisco-nexus-9000-series-nx-os-vxlan-configuration-guide-release-104x/m_configuring_vxlan_bgp_evpn.html), [NX-OS 10.6 ESI multihoming verification](https://www.cisco.com/c/en/us/td/docs/dcn/nx-os/nexus9000/106x/configuration/vxlan/cisco-nexus-9000-series-nx-os-vxlan-configuration-guide-release-106x/configuring-esi-tx.html), retrieved 2026-10-09. This procedure isolates the show-command verification portions of those configuration guides.

## Common Sequences

- Overlay evidence: Read NVE peers and VNIs → Read EVPN BGP → Read MAC/IP forwarding observations.
- Ethernet-segment evidence on 10.6: Read Ethernet segments → Read EAD and BGP route-type evidence.

### Read NVE peers and VNIs

`show nve peers` returns peer address, state, learning type and uptime. `show nve vni` returns VNI state, mode and L2 bridge-domain or L3 VRF association. Success is the returned observations for the requested device/VNI. The guide's Up examples demonstrate native state vocabulary, not a guarantee that every configured VNI should be Up in every deployment.

### Read EVPN BGP

`show bgp l2vpn evpn summary` returns the EVPN address-family peer summary, including native state/prefix information. `show bgp l2vpn evpn` returns EVPN route entries, route distinguishers, route-type encoding, next hops and path flags. Success is actual EVPN address-family evidence; a row in another BGP address family is not substituted for it.

### Read MAC/IP forwarding observations

`show l2route evpn mac all` and `show l2route evpn mac-ip all` return topology, MAC, producer, next-hop and available host-IP evidence. `show ip arp suppression-cache detail` adds cached IP/MAC/VLAN evidence with local/remote flags where the feature is in use. Success is the returned evidence with its native scope. The publisher's downstream-VNI feature supports asymmetric VNI assignments, so unequal VNI numbers alone do not prove a broken fabric.

### Read Ethernet segments

For the documented NX-OS 10.6 ESI feature, `show nve interface nve1 detail` returns NVE/ESI state and timers, while `show nve ethernet-segment` reports configured NVE segments. `show l2route evpn ethernet-segment all detail` supplies segment details. Success is the requested segment/NVE observations; a configured identifier is not alone proof of redundant forwarding.

### Read EAD and BGP route-type evidence

On the same 10.6 target, `show l2route evpn ead all` returns Ethernet Auto-Discovery routes. `show bgp l2vpn evpn route-type <value>` selects the requested route type from the deployed command schema. The cited ESI examples use type 1 to distinguish locally originated and remotely received ESI paths. Success retains the producer, ESI and next-hop evidence; example topology counts are not converted into universal required counts.

At each step, these references do not enumerate command-specific errors. A rejected command, insufficient privilege, unsupported feature/release or failed session is an unavailable observation with native error text, not an empty healthy table. These observations are evidence for further platform-specific diagnosis; no unverified cause/remediation rule is attached.

## Patterns

- NVE peer state, EVPN BGP state and learned forwarding entries are distinct observations.
- The source supports downstream asymmetric VNIs; an equality-only VNI audit would produce false failures.
- The guide excludes the VXLAN-interface display command on Nexus 9300-EX, FX/FX2/FX3 and GX. This procedure does not rely on that command.

## Known limitations

- The ESI sequence is specifically grounded in the 10.6 guide, not implied for every 10.4 platform.
- Full underlay reachability, designated-forwarder/LACP diagnosis, anycast-gateway policy and silent-host remediation require further platform-specific procedures.
- No data-plane test traffic or fabric mutation is generated.

## Tools

| Mechanism | Description | Category |
|---|---|---|
| Authenticated NX-OS CLI session | Retrieve the listed verification outputs from the selected device | Read |

## Verification checklist

- Device, release and feature scope match the chosen sequence.
- NVE, BGP and forwarding-table evidence remain separately identified.
- ESI/route-type observations retain identifiers and producer/next-hop data.
- Unsupported commands or incomplete output remain explicit.
- No cross-device VNI equality rule or root-cause conclusion was invented.
