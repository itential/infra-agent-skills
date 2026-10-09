# Linux iproute2 network state

Read link, address and route state in the selected Linux network namespace.

## Common Sequences

- Host network snapshot: **Read links** → **Read addresses** → **Read routes**.

### Read links

`ip link show` lists interface objects and their returned attributes in the current namespace. An optional `dev` selector narrows the read to the supplied interface. Missing interface or insufficient access is a failed selection, not a down-interface diagnosis.

### Read addresses

`ip address show` returns IPv4/IPv6 address assignments and attributes. `ip address show dev INTERFACE` narrows the result. The placeholder is replaced with an existing interface from the preceding read. No address add/delete/flush operation is part of this procedure.

### Read routes

`ip -4 route show table all` and, when requested, `ip -6 route show table all` enumerate all tables for the selected address family. The table, route type, destination, next hop and device remain part of the result. An empty successful family/table selection is distinct from a command error. Blackhole/unreachable route types are configuration observations, not automatically unintended faults. These commands do not evaluate all policy rules or prove packet delivery.

## Patterns

All-table selection is explicit because the ordinary route listing defaults to the main table. Address family and namespace constrain every observation.

## Known limitations

Legacy ifconfig/route/netstat bindings are replaced with publisher-documented iproute2 reads. No universal MTU, default-gateway requirement, cross-host symmetry rule or error-counter diagnosis is inferred.

## Tools

| Mechanism | Description | Category |
|---|---|---|
| Authorized Linux shell/SSH | Run iproute2 inspection payloads | Network read |

## Verification checklist

- Selected namespace, interface and address families are retained.
- All-table selection is explicit.
- Link/address/route errors remain separate.
- No state-changing command is sent.

## Sources

- [iproute2 address manual](https://github.com/iproute2/iproute2/blob/main/man/man8/ip-address.8.in). Retrieved 2026-10-09.
- [iproute2 link manual](https://github.com/iproute2/iproute2/blob/main/man/man8/ip-link.8.in). Retrieved 2026-10-09.
- [iproute2 route manual](https://github.com/iproute2/iproute2/blob/main/man/man8/ip-route.8.in). Retrieved 2026-10-09.
