# Zabbix item history and trends

Retrieve typed item history or numeric trend aggregates for a selected host and interval.

Primary sources: [item retrieval](https://www.zabbix.com/documentation/current/en/manual/api/reference/item/get),
[item fields](https://www.zabbix.com/documentation/current/en/manual/api/reference/item/object),
[history retrieval](https://www.zabbix.com/documentation/current/en/manual/api/reference/history/get),
[trend retrieval](https://www.zabbix.com/documentation/current/en/manual/api/reference/trend/get), and
[API authentication/errors](https://www.zabbix.com/documentation/current/en/manual/api), current
reference, retrieved 2026-10-09. Bindings: [endpoints.md](endpoints.md).

## Common Sequences

- Raw samples: Discover items → Select history type → Retrieve history → Interpret observations.
- Hourly aggregates: Discover items → Retrieve trends → Interpret observations.

## Discover items

Item retrieval selects the requested host and key and returns item identifiers, value types, units,
and configured history/trend retention. No match means no matching visible item, not proof that a
host is unmonitored. Permissions depend on the user, role, and groups.

Retention strings can contain macros. Their effective values are unknown until the deployment
resolves them; the procedure does not infer an expiry timestamp from unresolved text.

## Select history type

Each history request selects one value type. The selection matches the discovered item type;
items of different types are queried in separate groups. The default unsigned type is not suitable
for every item. The binding table provides the published type values.

## Retrieve history

The history operation supplies item identifiers, matching type, and the requested time bounds.
Returned samples include item identity, collection time, and value; sorting and a result limit can
be requested. A bounded result is identified as such. JSON-RPC errors remain errors even when the
HTTP exchange succeeds; invalid parameters require correction rather than reinterpretation as zero.

## Retrieve trends

The trend operation selects numeric items and the requested interval. Returned rows contain a time,
sample count, minimum, mean, and maximum. They are aggregate observations, not raw measurements.
The documented method has no sorting parameter; this procedure does not invent one.

## Interpret observations

The response identifier matches the request and contains a result or a documented JSON-RPC error.
Authentication/permission errors leave the requested observations unavailable. Empty results may
reflect selection or retention, and do not prove zero utilization.

## Patterns

An item's last-value timestamp is subject to Zabbix's history display window, normally 24 hours.
A missing last timestamp therefore does **not** establish that the item has never collected data.
This corrects the NetClaw source's stronger inference. Historic data can remain after an entity
has been deleted until housekeeping removes it.

## Known limitations

The configured retention is not a guarantee that every expected sample exists. This read-only
procedure neither adjusts housekeeping nor reclassifies absent samples as a collection failure.

## Tools

| Operation | Description | Category |
|---|---|---|
| Discover items | Resolve item IDs, value types, units, and retention | Read |
| Retrieve history | Read samples for one value type | Read |
| Retrieve trends | Read numeric aggregate rows | Read |

## Verification checklist

- Returned item identifiers match the selected host/items and request identifier.
- History type matches each item's type; trends are labeled as aggregates.
- Time bounds, units, limits, unresolved retention, and API errors remain explicit.
