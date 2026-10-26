# Zabbix — Collect Monitored Host, Interface, and Item State

Reads the current monitoring state Zabbix holds for hosts, their monitoring interfaces, and their items, through the Zabbix API. Read-only: nothing is created, changed, or deleted, so there are no confirmation gates.

Sources (Zabbix manual, current reference, version 7.4; retrieved 2026-10-26):

- [API overview](https://www.zabbix.com/documentation/current/en/manual/api).
- [host.get](https://www.zabbix.com/documentation/current/en/manual/api/reference/host/get).
- [Host interface object](https://www.zabbix.com/documentation/current/en/manual/api/reference/hostinterface/object).
- [Item object](https://www.zabbix.com/documentation/current/en/manual/api/reference/item/object).

Unverified: the item.get page was not read; item selection parameters in [endpoints.md](endpoints.md) are marked there.

## Common Sequences

- **Host monitoring state:** Retrieve hosts with interface availability → Report availability with its error and onset.
- **Item freshness:** Retrieve hosts → Retrieve items for the selected host identifiers → Report last-update times with the display-window caveat.

## Retrieve hosts with interface availability

Read the visible hosts matching the requested name or group, asking for identity fields plus their monitoring interfaces, linked templates, and host groups. Select interface fields explicitly; never request the full interface object (see Patterns).
Success is an array of host records visible to the API user. No match means no visible host: the host may be absent, or outside what the API user may read (Assumption: permission-scoped visibility); do not conclude it is unmonitored. Do not apply a monitored-only filter unless the request asks for it, because it silently drops hosts that are not monitored.
Each interface reports availability as unknown, available, or unavailable. When unavailable it also carries an error text and the time the interface became unavailable. These describe Zabbix's ability to poll that interface, not device power or forwarding state.

## Retrieve items

Read the items of the selected hosts, asking for key, status, value type, units, history and trend retention, last-update time, and error text.
Success is an item list keyed to the requested host identifiers. An item with an error text is failing its collection; its last value is stale.
The last-update time (and last value) is shown only for values within the display window: 24 hours by default, adjustable by an administrator in general settings. An absent last-update time may mean no value inside the window (Assumption: how an empty time is encoded is not stated in the page read), not that the item never collected one.

## Check the response

A response carries either a result or an error object, never both, and echoes the request identifier. An error (invalid parameters, authentication failure, missing permission) is a failed read, not empty state. A result limit or subselect limit that truncated the output is reported as partial coverage.

## Patterns

- **Credential exposure:** the SNMP interface details object holds the community string and the SNMPv3 authentication and privacy passphrases. Requesting every interface field can return them. Select only availability, error, onset, address, port, and type fields, and keep any returned secret out of reports.
- **Interface onset is not device onset:** the unavailable-since time belongs to one interface. It does not date an outage of the whole device, and it is not an outage duration.
- Host status, item status, and interface availability are separate fields; report each as returned.
- A configured host or item is not proof of a recent successful observation.

## Known limitations

- Current state only. No snapshot or diff operation is covered; a before/after comparison needs the caller to save the earlier result and compare the same fields.
- Problems, triggers, and event history are not covered, so outage durations and flap counts are out of scope.
- Not documented in the pages read: rate limits. Back off and retry later on a throttling error instead of looping.

## Tools

| Operation | Description | Category |
|---|---|---|
| Retrieve hosts | Read host records with interfaces, templates, groups | JSON-RPC API |
| Retrieve items | Read item configuration and last-update state | JSON-RPC API |

## Verification checklist

- [ ] Response identifiers match the request, and no error object was returned.
- [ ] Interface fields were selected explicitly; no credential values appear in the output.
- [ ] Interface availability, host status, and item status are reported separately.
- [ ] Last-update times are reported with the display-window caveat; truncation by limits is stated.
