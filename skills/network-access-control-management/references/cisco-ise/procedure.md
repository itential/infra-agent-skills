# Cisco Identity Services Engine (ISE) — Read-Only Endpoint and Session Lookup

Reads endpoint records, their identity-group assignment, and live session state from Cisco ISE.
**Read-only.** No operation here changes ISE state, so no confirmation gates apply. Registering,
updating, deleting, quarantining or releasing endpoints, ending sessions, and editing policy are out
of scope; stop and report if the request needs one of them. Assumes an authenticated client already
exists; creating the ISE account is out of scope.

Sources: Cisco DevNet, Cisco Identity Services Engine API v1 documentation — API families, "Read a
Resource", "Pagination", "Introduction to the Monitoring REST API", "Using API calls for Session
Management" (developer.cisco.com/docs/identity-services-engine/latest/), retrieved 2026-10-26. The
per-resource Endpoint and Endpoint Identity Group reference pages did not render; their field and
filter names are marked unverified below.

## Common Sequences

- **Look up an endpoint:** Read endpoint (by MAC) → Read endpoint identity group (if the group name is needed).
- **Is this endpoint connected now:** Read session (by MAC) → Read endpoint, for the static versus
  dynamic record context.
- **Survey activity:** Read session counters → Read session list (bounded).

## Operational procedure

### 1. Confirm access

- ISE has three API families with different access paths: the configuration API for endpoint records,
  the monitoring API for sessions, and a separate Open API family (policy and other areas, not used
  here). Each must be enabled in the ISE API service settings; a family that is disabled is
  unreachable, so stop and report it.
- Configuration reads require an account in the read/write ERS admin group, the read-only ERS
  operator group, or Super Admin. The read-only operator role is sufficient and is the one to use.
- Monitoring reads require an account in Super Admin, System Admin, or MnT Admin, and that account must
  be stored in ISE's internal database. Accounts from external identity stores are not supported there.
- Credentials travel as basic-authentication headers, so use only a TLS connection whose certificate
  has been validated. If the certificate cannot be validated, stop; do not disable verification.
- Not documented: rate limits. On HTTP 429 or a timeout, back off before retrying.

### 2. Read endpoint(s)

- **By MAC address:** the configuration API offers a lookup by endpoint name, and the endpoint name is
  conventionally the MAC address (assumption, from community usage; unverified in the pages read).
  A filtered list on the MAC field is the alternative (field name unverified).
- **List:** results are paged. The first page is page 1, the default page size is 20, and the maximum
  is 100. Filters are written field, operator, value; several filters are ANDed unless the logical
  operator is switched to OR. Documented operators: equals, not equals, greater/less than, starts-with,
  ends-with, contains and their negations. Page until the result set is exhausted rather than
  assuming one page is everything.
- A list returns only each record's name, id, description and a link; a second read of each id returns
  the full record. Unverified: the full-record fields (MAC, endpoint identity group id, profile id,
  static group and profile assignment flags, portal user, identity store).
- Success is the record or a page of results. Not documented in the pages read: the status code and
  body for a missing endpoint; treat any non-success as "not found or error" and report it verbatim.

### 3. Read endpoint identity group

- The group an endpoint belongs to is referenced by id on the endpoint record (unverified field). To
  show a group name, read the endpoint identity group resource by that id. Unverified: the resource
  name used on the wire.
- A static assignment flag on the record distinguishes an operator-assigned group from one the
  profiler chose (unverified flag name); report it rather than assuming either.

### 4. Read session state

- **By identifier:** the monitoring API reads a current session by endpoint MAC, username, NAS IP,
  endpoint IP, or audit session id. MAC must be uppercase colon-separated; the calls are
  case-sensitive. Usernames containing a backslash cannot go in the GET path; the vendor documents a
  POST variant as the workaround for that read.
- **Lists and counts:** a call returns all active sessions, optionally within a start/end time window
  (0 to 432,000 seconds, five days); separate calls return active, posture-assessed and profiler
  session counts. Displayable active sessions are capped (the pages give 100,000 for the list call and
  250,000 in the overview; treat the cap as unresolved and the list as possibly truncated).
- Responses are XML by default. Success is a session record with fields such as authentication
  method, VLAN, downloadable ACL, endpoint policy, posture status and audit session id. An empty
  result means no current session matched, not that the endpoint never authenticated.
- The calls must reach a monitoring node; a node that is not a monitoring node returns an error.
- Delete calls for stale sessions exist in the same API family. They change state and are out of scope.

## Patterns

- The endpoint record shows what ISE has stored; the session shows what is happening now. Neither
  proves what policy decided, and this procedure does not read policy.
- Session identifiers differ: the audit session id and the accounting session id are separate fields.
- Session detail carries usernames and device identifiers; report only what the request needs.

## Known limitations

- Read-only. No writes, quarantine, release, change of authorization, or session deletion.
- Policy sets, authentication rules and authorization rules are not covered (not documented here).
- Cannot read sessions for accounts stored outside ISE's internal database.
- Endpoint and endpoint-group wire details are partly unverified (see steps 2 and 3).

## Tools

| Operation | Description | Category |
|---|---|---|
| Read endpoint | Fetch one endpoint record or a filtered, paged list | Read |
| Read endpoint identity group | Fetch the group an endpoint is assigned to | Read |
| Read session | Fetch current session detail by one identifier | Read |
| Read session list | List active sessions, optionally time-windowed | Read |
| Read session counters | Count active, posture and profiler sessions | Read |

## Verification checklist

- [ ] Account used has only read access; transport validated
- [ ] Lists paged to completion, or reported as partial
- [ ] Empty session result reported as "no current session", not "endpoint unknown"
- [ ] Unverified fields reported as such if the response differs from what is described here
- [ ] No write or delete call issued
