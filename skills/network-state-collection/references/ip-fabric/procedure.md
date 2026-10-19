# IP Fabric — Collect and Compare Network State from Snapshots

Reads discovered network state from IP Fabric snapshots and compares two snapshots; optionally starts a new discovery snapshot.

Sources (IP Fabric documentation portal; retrieved 2026-10-19):

- [IP Fabric API overview](https://docs.ipfabric.io/main/IP_Fabric_API/).
- [Authentication](https://docs.ipfabric.io/main/IP_Fabric_API/authentication/).
- [Snapshot Table](https://docs.ipfabric.io/main/IP_Fabric_API/snapshots/snapshot_table/).
- [Create New Snapshots via API](https://docs.ipfabric.io/main/IP_Fabric_API/snapshots/create_new_snapshots_via_api/).
- Secondary source: the Studio Project for IP Fabric in the itential/assets repository, used only to choose which operations to cover.

## Common Sequences

- **Read current state:** Select snapshot → Query a technology table.
- **Before/after evidence:** Select snapshot (before) → Select snapshot (after) → Query the same table on both → Compare results.
- **Fresh evidence:** Start a discovery snapshot → Wait for it to finish → Query a technology table.

## Select snapshot

The platform keeps discovered state as numbered snapshots. A snapshot is named by its identifier or by one of three selectors: the most recent, the previous one, or the last locked one. The snapshot list is itself a queryable table; each row reports whether collection finished, whether it errored, whether it is loaded, whether it is locked, and device and interface counts.
Success is one snapshot identifier whose finish status reports done and whose load status reports done. A snapshot that errored, was canceled, or is still running is incomplete data, not a healthy network. Pin before/after comparisons to explicit identifiers, because the "most recent" selector moves when a new snapshot completes.

## Query a technology table

Reads of discovered state go through table queries. The request names the columns wanted, optional filters, a sort, a page size and offset, and the snapshot. The documentation recommends at most 1000 rows per page; page until the table is exhausted.
Success is a result set for the named snapshot. An empty result means nothing matched in that snapshot, not that the device or feature is healthy. The documentation does not state a rate limit; if the platform throttles or errors, back off and retry later rather than looping.
The table path, column names and filter operators for a given feature are in the platform's own API browser on the instance (see [endpoints.md](endpoints.md)); this procedure does not assume column names.

## Compare results

IP Fabric's documentation read for this procedure shows no snapshot-diff operation. Compare by running the same table query, same columns and same filters, against both pinned snapshots and diffing the two result sets outside the platform.
Success is two result sets that cover the same devices and scope. If the snapshots cover different sites or device sets, report the comparison as not like-for-like. An empty difference establishes equality only for the columns collected.
Whether a native comparison operation exists is unverified here; check the instance's API browser first.

## Start a discovery snapshot

**Stop and confirm with the operator before proceeding.** A new snapshot makes the platform log in to and query live network devices, using the platform's configured credentials, and it consumes platform resources.
The request may be empty, which uses the global settings, or may override the name, note, included and excluded networks, seed list and vendor API usage. Omitted fields default to the global settings, and a custom snapshot does not change later scheduled discoveries.
Success is a new snapshot appearing in the snapshot list; discovery runs asynchronously, so re-query the snapshot list until its finish status reports done. Check the list for error or canceled outcomes before using the data.

## Patterns

- Credentials: an API token header is the documented long-lived option and can be scoped below the owning user's permissions. Basic authentication grants the user's full rights and is documented for dedicated service accounts. The cookie-based login issues a 30-minute access token and a 24-hour refresh token that rotates on each use.
- The API version appears in the path of some calls; use the version the instance supports (see [endpoints.md](endpoints.md)).

## Known limitations

- Observed data only. This procedure does not diagnose root causes or approve a change.
- No native diff, snapshot lock/unlock/delete, or load/unload procedure is covered.
- Coverage depends on which devices the platform discovered; undiscovered devices are absent, not healthy.

## Tools

| Operation | Description | Category |
|---|---|---|
| List snapshots | Read the snapshot table | REST API |
| Query technology table | Read discovered state for a snapshot | REST API |
| Create snapshot | Start a new discovery | REST API |

## Verification checklist

- [ ] The snapshot used finished successfully and is identified by an explicit identifier.
- [ ] Both comparison inputs came from queries with the same columns and filters.
- [ ] Empty results and query failures are reported as such, not as healthy state.
- [ ] A new snapshot, if started, was confirmed by the operator first and reached a finished state.
