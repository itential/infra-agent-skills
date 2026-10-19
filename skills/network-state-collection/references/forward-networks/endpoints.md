# Forward Networks — State Collection Wiring

Sources (Forward Networks API documentation, release 25.12; retrieved 2026-10-19):
[API reference](https://docs.fwd.app/25.12/api-doc/); its Network Snapshots, Network Devices and NQE OpenAPI specifications (`api/spec/network-snapshots.json`, `network-devices.json`, `nqe.json` beneath that page).

Placeholders: `{host}`, `{networkId}`, `{snapshotId}`, `{deviceName}`, `{before}`, `{after}`. The API root is the instance host; on-premises instances also serve the documentation at their own `/api-doc`.

## Authentication

`Authorization: Basic <base64 of access-key:secret-key>` using an API token pair. Username and password work for non-SSO accounts.

## Calls

| Operation | Method and path | Notes |
|---|---|---|
| List snapshots | `GET /api/networks/{networkId}/snapshots` | Query: `state`, `minSuccessfulDevices`, `minSuccessfulDevicePct`, `maxCollectionFailureDevices`, `maxCollectionFailureDevicePct`, `maxParsingFailureDevices`, `maxParsingFailureDevicePct`, `limit`, `includeArchived` |
| Latest processed | `GET /api/networks/{networkId}/snapshots/latestProcessed` | 404 none exist; 409 processing begun |
| Snapshot metrics | `GET /api/snapshots/{snapshotId}/metrics` | 404 not found |
| Run NQE | `POST /api/nqe?networkId={networkId}&snapshotId={snapshotId}` | `networkId` required unless `snapshotId` given |
| Diff NQE | `POST /api/nqe-diffs/{before}/{after}` | Body: `queryId` (required), `commitId`, `options`, `parameters` |
| List NQE queries | `GET /api/nqe/queries` | Optional `dir` such as `/L3/Advanced/` |
| List devices | `GET /api/networks/{networkId}/snapshots/{snapshotId}/devices` | |
| Read device | `GET /api/networks/{networkId}/snapshots/{snapshotId}/devices/{deviceName}` | |
| Raw device data | `GET /api/networks/{networkId}/snapshots/{snapshotId}/devices/{deviceName}/raw-data` | Sensitive |
| Missing devices | `GET /api/networks/{networkId}/snapshots/{snapshotId}/missing-devices` | |

## NQE run body

Exactly one of `query` or `queryId`; optional `commitId`, `parameters`, and `queryOptions` (`offset` default 0, `limit` default 1000 maximum 10000, `sortBy` column and ASC/DESC, `columnFilters`, `itemFormat`). Response: `snapshotId`, `items`, `totalNumItems`. Errors: 400 for parse error, invalid filter, timeout or permissions.

## Diff response

`rows` (each with before and after records and a type of ADDED, DELETED or MODIFIED) and `totalNumRows`; options may filter by change type.

## Snapshot fields

`id`, `state` (UNPACKING, UNPROCESSED, PROCESSING, PROCESSED, FAILED, CANCELED, TIMED_OUT, ARCHIVED, RESTORING, RESTORE_FAILED), `processingTrigger` (UNKNOWN, COLLECTION, IMPORT, REPROCESS, FORK), `creationDateMillis`, `processedAtMillis`, `isDraft`, `note`, `parentSnapshotId`.

## Unverified

- Rate limits and exact error bodies beyond the status codes above.
- The diff body's `options` shape is described only as the query options plus a change-type filter; confirm field names in the OpenAPI file.
- Whether the run-NQE path is under `/api/nqe` only (as the NQE spec shows) or also nested under the snapshot (as the summary table on the reference page lists) — confirm against the instance's own `/api-doc`.
