# Zabbix host and monitoring inventory

Inspect visible hosts, monitoring interfaces, and configured items.

Sources: [host retrieval](https://www.zabbix.com/documentation/current/en/manual/api/reference/host/get),
[host interface fields](https://www.zabbix.com/documentation/current/en/manual/api/reference/hostinterface/object),
[item retrieval](https://www.zabbix.com/documentation/current/en/manual/api/reference/item/get),
[item fields](https://www.zabbix.com/documentation/current/en/manual/api/reference/item/object), and
[API access/errors](https://www.zabbix.com/documentation/current/en/manual/api), current reference,
retrieved 2026-10-09. Bindings: [endpoints.md](endpoints.md).

## 1. Retrieve matching hosts

The host query filters the requested identity/group and returns selected identity fields plus
interfaces, linked templates, and host groups. Success is an array of visible host records.
A missing host is reported as no visible match; it is not automatically classified as unmonitored.
A monitored-only filter excludes other hosts, so inventory review leaves that filter unset unless
such restriction is part of the requested scope.

## 2. Inspect monitoring interfaces

Each selected interface exposes its availability classification: unknown, available, or unavailable.
An unavailable interface may include an error and the time it became unavailable. Those fields refer
to the monitoring interface, not a universal observation of forwarding or device power. The query
collects selected fields rather than exposing the interface's authentication details.

## 3. Retrieve configured items

The item query selects the returned host identifiers and includes key, status, value type, units,
retention, last-value timestamp, and update error. A last-value timestamp is limited by the configured
history display window; absence does not prove that an item has never collected a value.

## 4. Qualify the inventory

The JSON-RPC response correlates to the request and contains a result or error. Invalid-parameter,
authentication, or authorization errors are reported as failed reads. A result limit or subselect
limit is retained as a coverage boundary. No hidden records are inferred from an empty response.

## Patterns

Host monitoring status, item status, and monitoring-interface availability are separate fields.
A configured inventory record is not proof of a recent successful observation.

## Known limitations

No host/item changes are made. This inventory procedure does not compute outage durations or flap
counts; those require the relevant trigger's event history and its documented definition.

## Tools

| Operation | Description | Category |
|---|---|---|
| Retrieve hosts | Read visible host records and selected relations | Read |
| Retrieve items | Read configured monitoring item metadata | Read |

## Verification checklist

- The selected host IDs, query scope, and response IDs match.
- Interface availability and host/item status remain distinct.
- Timestamp display limits, permission scope, and query bounds are reported.
