# Endpoints — F5 BIG-IP LTM iControl REST

Literal wiring layer. `procedure.md` steps reference these by name; bind them to whatever
authenticated REST client/adapter is assumed available for the target BIG-IP.

Source: F5 clouddocs iControl REST API Reference (`APIRef_tm_ltm_virtual`, `APIRef_tm_ltm_pool`,
`APIRef_tm_ltm_pool_members`), https://clouddocs.f5.com/api/icontrol-rest/, retrieved 2026-09-17.
These pages carry F5's own notice that they contain community-contributed content F5 does not
monitor — treat paths/methods/field names below as reliable (they match the documented TMOS object
model) but not as F5-guaranteed current wording.

## Virtual server (`ltm/virtual`)

**Collection:** `/mgmt/tm/ltm/virtual` — methods: `OPTIONS`, `GET`.
**Resource:** `/mgmt/tm/ltm/virtual/~<partition>~<name>` — methods: `OPTIONS`, `GET`, `PUT`, `PATCH`,
`DELETE`, `POST`.

Natural key: `name` + `partition` + `subPath`.

Fields relevant to basic VIP CRUD (see `procedure.md` for how to use them):
- `name` — object identifier.
- `tmPartition` — administrative partition (default `Common`).
- `destination` — the VIP's own address and port, formatted `<address>:<port>`.
- `pool` — name of the default pool this virtual server sends traffic to.
- `mask` — netmask for a network/wildcard virtual server (documented default is an all-ones mask
  equivalent to a single host).
- `ipProtocol` — e.g. `tcp`, `udp`.
- `source` — accepted traffic source address/network.
- `enabled` / `disabled` — admin state. (Source lists both as boolean fields on the same object;
  confirm against a live read which one the target system actually toggles before assuming they're
  simple opposites — the reference table's own default-value column is internally inconsistent on this pair.)
- `profiles` — array of associated profiles (e.g. TCP/HTTP/client-SSL/server-SSL); no field-level
  sub-schema for an individual profile entry was retrieved.
- `rules` — associated iRule names.
- `vlansEnabled` / `vlansDisabled` + `vlans` — VLAN scoping.
- `source-address-translation` structure (`pool`, `type` — default `none`) — SNAT configuration.

**Success:** 2xx response containing the object's own fields plus a `selfLink`.
**Failure:** no specific error-string catalog was found for virtual-server-specific failures in the
reference — surface the response body verbatim.

## Pool (`ltm/pool`)

**Collection:** `/mgmt/tm/ltm/pool` — methods: `OPTIONS`, `GET`.
**Resource:** `/mgmt/tm/ltm/pool/~<partition>~<name>` — methods: `OPTIONS`, `GET`, `PUT`, `PATCH`,
`DELETE`, `POST`.

Natural key: `name` + `partition` + `subPath`.

Fields relevant to basic pool CRUD:
- `name`, `tmPartition` (default `Common`).
- `loadBalancingMode` — default `round-robin`.
- `monitor` — health monitor name, "and"-joined list, or "min N of {...}" quorum expression.
- `slowRampTime` — integer seconds, default 10.
- `minActiveMembers`, `minUpMembers`, `minUpMembersAction` (default `failover`),
  `minUpMembersChecking` (default `disabled`) — availability thresholds, optional.
- `allowNat`, `allowSnat` — both default `yes`.
- `reselectTries` — default 0.
- `serviceDownAction` — default `none`.
- `members` — sub-collection, see below.

**Success:** 2xx response containing the object's own fields plus `selfLink`.
**Failure:** no specific error-string catalog found for pool-specific failures — surface the
response body verbatim. A pool delete while still referenced by a virtual server is expected to be
rejected by the platform, but the exact rejection string is not documented in the reference for
this contribution — do not fabricate one; report whatever the platform actually returns.

## Pool members (`ltm/pool/<pool>/members`)

**Collection and resource share the same base path:**
`/mgmt/tm/ltm/pool/~<partition>~<pool-name>/members` — collection methods: `OPTIONS`, `GET`;
per-member resource methods: `OPTIONS`, `GET`, `PUT`, `PATCH`, `DELETE`, `POST`.

Natural key: `name` + `partition` + `subPath`. **The member's `name` is conventionally its
`<address>:<port>`** — this is well-established BIG-IP practice, not something spelled out verbatim
on this specific reference page; confirm against the live system's existing member objects if exact
formatting matters for a given call.

Per-member fields:
- `address` — only needed to implicitly create a new node when the member name doesn't already
  correspond to an existing node object.
- `connectionLimit` — default 0 (0 conventionally means unlimited on this platform; not itself
  restated as such on this reference page).
- `ratio` — default 1, weight for ratio-based load-balancing modes.
- `priorityGroup` — default 0.
- `dynamicRatio` — default 1.
- `session` — default `user-enabled`; enables/disables the member for **new** sessions.
- `state` — `user-up` (default) reverts a forced-down member and then reflects live monitor status;
  `user-down` forces the member offline immediately, overriding monitors, until reverted.
- `monitor` — per-member health monitor override.
- `logging` — default `disabled`; per-member monitor-action logging.
- `inheritProfile` — default `enabled`.
- `rateLimit` — default `0`.
- `fqdn` structure (`autopopulate` default `disabled`, `name`) — for FQDN-tracking members; out of
  scope for static address:port CRUD, see `procedure.md` Known limitations.

**Success:** 2xx response containing the member object plus `selfLink`.
**Failure:** no specific error-string catalog found for member-specific failures — surface the
response body verbatim.

## Authentication

Unverified against F5's documentation — this skill assumes
an authenticated REST client is already available (per `SKILL.md`'s stated assumption) rather than
asserting a specific login/token flow here. If a calling tool needs to establish that session
itself, confirm the exact mechanism against the target BIG-IP's own current documentation before
scripting it, rather than reusing a remembered convention from a different F5 product line.
