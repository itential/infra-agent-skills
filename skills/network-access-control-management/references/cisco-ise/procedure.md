# Cisco Identity Services Engine (ISE) — Read-Only Session Lookup

Reads live session state and session counts from Cisco ISE through its monitoring API.
**Read-only.** No operation here changes ISE state, so no confirmation gates apply. Registering,
updating, deleting, quarantining or releasing endpoints, ending sessions, and editing policy are out
of scope; stop and report if the request needs one of them. Assumes an authenticated client already
exists; creating the ISE account is out of scope. Literal routes are in `endpoints.md`.

Source: Cisco DevNet, Cisco Identity Services Engine API v1 documentation — "Introduction to the
Monitoring REST API" and "Using API calls for Session Management"
(developer.cisco.com/docs/identity-services-engine/latest/), retrieved 2026-10-26.

## Common Sequences

- **Is this endpoint connected now:** Read session (by MAC).
- **Survey activity:** Read session counters → Read session list (bounded).

## Operational procedure

### 1. Confirm access

- ISE has three API families with different access paths: the configuration API for endpoint
  records (not covered, see Known limitations), the monitoring API for sessions, and a separate Open
  API family (policy and other areas, not used here). The monitoring API must be enabled in the ISE
  API service settings; a family that is disabled is unreachable, so stop and report it.
- Monitoring reads require an account in Super Admin, System Admin, or MnT Admin, and that account must
  be stored in ISE's internal database. Accounts from external identity stores are not supported there.
- Credentials travel as basic-authentication headers, so the connection must be TLS with a validated
  certificate.
- Not documented: rate limits. On HTTP 429 or a timeout, back off before retrying.

### 2. Read session state

- **By identifier:** the monitoring API reads a current session by endpoint MAC, username, NAS IP,
  endpoint IP, or audit session id. MAC must be uppercase colon-separated; the calls are
  case-sensitive. Usernames containing a backslash cannot go in the GET path; the vendor documents a
  POST variant as the workaround for that read.
- **Lists and counts:** a call returns all active sessions, optionally within a start/end time window
  (0 to 432,000 seconds, five days); separate calls return active, posture-assessed and profiler
  session counts. Displayable active sessions are capped (the documentation gives 100,000 for the
  list call and 250,000 in the overview; the cap is unresolved, so treat the list as possibly
  truncated).
- Responses are XML by default. Success is a session record with fields such as authentication
  method, VLAN, downloadable ACL, endpoint policy, posture status and audit session id. An empty
  result means no current session matched, not that the endpoint never authenticated.
- The calls must reach a monitoring node; a node that is not a monitoring node returns an error.
- Not documented: the status code and body for a missing session or a failed call. Report any
  non-success verbatim.
- Delete calls for stale sessions exist in the same API family. They change state and are out of scope.

## Patterns

- A session shows what is happening now. It does not show what policy decided, and this procedure
  does not read policy or stored endpoint records.
- Session identifiers differ: the audit session id and the accounting session id are separate fields.
- Session detail carries usernames and device identifiers; report only what the request needs.

## Known limitations

- Read-only. No writes, quarantine, release, change of authorization, or session deletion.
- Endpoint records and endpoint identity groups (configuration API) are not covered: Unverified
  resource names and fields.
- Policy sets, authentication rules and authorization rules are not covered.
- Cannot read sessions for accounts stored outside ISE's internal database.

## Tools

| Operation | Description | Category |
|---|---|---|
| Read session | Fetch current session detail by one identifier | Read |
| Read session list | List active sessions, optionally time-windowed | Read |
| Read session counters | Count active, posture and profiler sessions | Read |

## Verification checklist

- [ ] Account used has only read access; transport validated
- [ ] Empty session result reported as "no current session", not "endpoint unknown"
- [ ] A capped list reported as possibly truncated
- [ ] No write or delete call issued
