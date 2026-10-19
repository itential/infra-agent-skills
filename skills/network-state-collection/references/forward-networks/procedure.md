# Forward Networks — Collect and Compare Network State from Snapshots

Reads modeled network state with the Network Query Engine (NQE) against a Forward Networks snapshot and diffs query results between two snapshots.

Sources (Forward Networks API documentation, release 25.12; retrieved 2026-10-19):

- [API reference](https://docs.fwd.app/25.12/api-doc/).
- Network Snapshots and NQE OpenAPI specifications linked from that page (see [endpoints.md](endpoints.md)).
- Secondary source: the Studio Project for Forward Networks in the itential/assets repository, used only to choose which operations to cover.

## Common Sequences

- **Read current state:** Select snapshot → Run NQE query.
- **Before/after evidence:** Select snapshot (before) → Select snapshot (after) → Diff NQE results.
- **Device detail:** Select snapshot → List devices → Read one device.

## Select snapshot

State is organized per network and per snapshot. List a network's snapshots, optionally filtered by processing state and by collection or parsing failure limits, and take the latest processed snapshot or a specific identifier.
Snapshot states include processed, processing, failed, canceled and timed out, among others. Success is a snapshot in the processed state. Asking for the latest processed snapshot returns not-found when none exists and a conflict while processing has begun on the latest; treat both as no usable data yet.
A snapshot with collection or parsing failures on some devices is partial data: use the failure filters when listing, and report which devices failed rather than treating their absence as healthy.

## Run NQE query

NQE runs a saved query (by identifier, optionally pinned to a commit) or an inline query against a snapshot, with optional parameters, sort, column filters, offset and limit. The default limit is 1000 results and the documented maximum is 10000; page with the offset when the total exceeds the limit.
Success is a result set naming the snapshot it was run against, with a total item count. A parse error, invalid filter, timeout or permission problem returns a client error; fix the query or narrow it, do not treat it as empty state.

## Diff NQE results

A diff takes the "before" and "after" snapshot identifiers and a saved query identifier, with the same options and parameters, and returns rows marked added, deleted or modified, each carrying the before and after records.
Success is a row list and a total row count. An empty diff establishes equality only for what that query selects. Both snapshots must be processed and should cover the same devices; otherwise report the comparison as not like-for-like.

## List devices and read a device

List devices in a snapshot, read one device's details, or read its raw collected configuration or state data. The list of "missing devices" names neighbors apparently present but not collected.
Raw data may contain secrets from device configurations; handle the output as sensitive and do not paste it into tickets or logs.

## Patterns

- Credentials: the documentation prefers an API token (access key and secret) sent as HTTP Basic authentication; a username and password also work except for SSO accounts.
- Pin explicit snapshot identifiers for before/after work; the latest-processed snapshot changes as collections finish.

## Known limitations

- Observed data only. This procedure does not diagnose root causes or approve a change.
- Starting a collection, importing, exporting or deleting snapshots, and policy checks are not covered.
- Coverage depends on which devices the platform collected.

## Tools

| Operation | Description | Category |
|---|---|---|
| List snapshots | Find processed snapshots | REST API |
| Run NQE query | Read modeled state | REST API |
| Diff NQE results | Compare two snapshots | REST API |
| List and read devices | Device inventory and raw data | REST API |

## Verification checklist

- [ ] Snapshots used are processed and identified explicitly.
- [ ] Partial collection (failed devices) is reported, not hidden.
- [ ] The same query and options were used on both sides of a diff.
- [ ] Empty results, empty diffs and query errors are not reported as healthy state.
