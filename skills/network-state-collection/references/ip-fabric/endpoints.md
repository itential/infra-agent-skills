# IP Fabric — State Collection Wiring

Sources (IP Fabric documentation portal; retrieved 2026-10-19): the pages listed in [procedure.md](procedure.md).

The instance hosts its own API browser at `/api/rapidoc/` on the IP Fabric host (per the API overview), which lists the table paths and columns for its version. Placeholders: `{host}`, `{api_version}`, `{api_token}`.

## Authentication

| Method | Header or call | Notes |
|---|---|---|
| API token | `X-API-Token: {api_token}` | Created in the UI; long-lived; can be scoped |
| Basic | `Authorization: Basic <base64 user:password>` | Same rights as the user |
| Login | `POST /api/v6.1/auth/login` | Returns accessToken (30 min) and refreshToken (24 h, rotates) as cookies |
| Refresh | `POST /api/auth/token` | Exchanges the refresh token for a new pair |

## Calls

| Operation | Method and path | Notes |
|---|---|---|
| Snapshot table | `POST /tables/management/snapshots` | Payload: `columns`, `filters`, `sort`; filter operators `eq`, `neq`, `empty` |
| Technology table | `POST /tables/{table-path}` (for example `/tables/inventory/devices`) | Payload: `columns`, `filters`, `attributeFilters`, `pagination` (`limit`, `start`), `snapshot`, `reports`; POST only |
| Create snapshot | `POST /api/{api_version}/snapshots` | Optional body: `snapshotName`, `snapshotNote`, `networks.include/exclude`, `seedList`, `vendorApi` |
| Read settings | `GET /api/{api_version}/settings` | Shows the full snapshot settings schema |

**Path-prefix assumption:** the cited pages show table paths without a stated `/api/{version}` prefix in some places and with one in others. Confirm the full path in the instance's API browser before binding.

## Snapshot table columns used

`id`, `status`, `finishStatus` (`done`, `error`, `canceled`, or empty), `loading`, `isLastSnapshot`, `locked`, `name`, `sites`, `totalDevCount`, `interfaceCount`, `tsStart`, `tsEnd` (millisecond timestamps).

## Snapshot selectors

A snapshot field takes a snapshot identifier, `$last`, `$prev`, or `$lastLocked`.

## Unverified

- Rate limits and error response bodies are not stated on the pages read.
- Whether `pagination.limit` has a hard maximum above the recommended 1000 is not stated.
- Whether a native snapshot-comparison call exists is not covered by the pages read.
