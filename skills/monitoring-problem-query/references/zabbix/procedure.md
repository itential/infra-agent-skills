# Zabbix current and historical problems

Read trigger problems or events while preserving acknowledgement, timing, and scope.

Sources: [problem retrieval](https://www.zabbix.com/documentation/current/en/manual/api/reference/problem/get),
[event retrieval](https://www.zabbix.com/documentation/current/en/manual/api/reference/event/get), and
[API/errors](https://www.zabbix.com/documentation/current/en/manual/api), current documentation,
retrieved 2026-10-09. Bindings: [endpoints.md](endpoints.md).

## Common Sequences

- Current problems: Select scope → Read unresolved problems → Report native evidence.
- Historical investigation: Select scope → Read historical events → Report native evidence.

## Select scope

The query identifies hosts/groups or trigger objects and requested severity/time filters. These
filters define the population; a filtered count is not a system-wide count.

## Read unresolved problems

The problem operation without recent resolved records returns unresolved problems. A recent mode
also includes resolutions within the deployment's configured recent period. Acknowledgements,
tags, and suppression information are requested as needed. Success returns the matching problem
records; acknowledgement is reported independently of whether the problem remains unresolved.

## Read historical events

Older resolved problems use event history because the problem table does not retain them indefinitely.
A creation-time window selects event onsets; a problem-overlap window selects trigger problems that
were active during the window regardless of current status. Both overlap bounds are supplied together.
Host and related-object subselects provide the documented event context. Event updates have their own
timestamps and actions and are not assumed to be resolution events.

## Report native evidence

The successful JSON-RPC result retains event IDs, selected time boundaries, acknowledgement state,
and any result limit. A request error, unreachable API, or denied permission is unavailable evidence,
not a successful empty list. Native invalid-parameter errors require corrected input.

## Patterns

The recent-resolved period is deployment-specific. Housekeeping can leave events/problems for a
deleted entity temporarily present, so event presence does not prove current inventory membership.

## Known limitations

No universal severity-to-escalation rule or outage-duration calculation is imposed. Recovery pairing
requires the returned recovery relationships; a bare acknowledgement is insufficient. No writes occur.

## Tools

| Operation | Description | Category |
|---|---|---|
| Read unresolved problems | Retrieve current/recent problem records | Read |
| Read historical events | Retrieve events in a selected window | Read |

## Verification checklist

- Current/recent versus historical selection matches the requested question.
- Filters, bounds, response IDs, and limits are retained.
- Acknowledgement, suppression, and recovery are not conflated.
