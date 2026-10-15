# AWS Route 53 — DNS Record Management Procedure

Create, update (upsert), or delete a basic DNS record (A, AAAA, CNAME, MX, TXT, NS, SOA, PTR, SRV, CAA,
etc.) in an AWS Route 53 hosted zone. Covers plain resource record sets only — alias records, weighted/
failover/geolocation/geoproximity/latency/multivalue-answer/IP-based routing policies, and Traffic Flow
are out of scope. Assumes an authenticated Route 53 API client (`route53:ChangeResourceRecordSets`,
`GetChange`, `ListHostedZonesByName`, `ListHostedZones`) is already available to the caller.

## Operational procedure

### 1. Resolve the hosted zone ID (skip if already known)

**Never guess a hosted zone ID.** A hosted zone ID is an opaque identifier Route 53 assigns; it cannot be
derived from the domain name, and no well-known/placeholder/example ID (from documentation or elsewhere)
is a valid substitute. If it's not given, resolve it first:

- Call the zone-lookup-by-name capability with the record's domain (or its parent domain) as the name to
  match.
- **Verify the returned zone's `Name` actually equals the domain you're looking for** (Route 53 appends a
  trailing dot, e.g. `example.com.`) — this lookup returns the alphabetically-nearest zone, not
  necessarily an exact match. If the top result doesn't match, check whether a shorter parent domain is
  the hosted zone instead (e.g. the record is `agent1.se.example.com` but the hosted zone is
  `example.com` or `se.example.com`), or page further before concluding no zone exists.
- If that lookup is unavailable or ambiguous, fall back to listing all hosted zones and matching `Name`
  client-side (see `endpoints.md`).
- If no matching hosted zone is found after checking, **stop and report this to the operator** — do not
  fabricate an ID or proceed with a guess.

See `endpoints.md` § "Resolve a Domain Name to a Hosted Zone ID" for exact request/response shape and
errors (`InvalidDomainName`, `InvalidInput`).

### 2. Confirm before a destructive or overwriting change

If the action is a DELETE, or a CREATE/UPSERT against a name+type combination known to already exist and
resolve, **stop and confirm with the operator before proceeding** — this affects live DNS resolution.
State the hosted zone, record name, type, action, and (for DELETE) that the exact same values used at
creation must be supplied for the delete to succeed — see step 3.

### 3. Build the change batch

Assemble one `Change` with:
- `Action` — `CREATE`, `DELETE`, or `UPSERT`.
- `ResourceRecordSet.Name`, `Type`, `TTL`, one or more `ResourceRecords.ResourceRecord.Value` entries, and
  optional `HealthCheckId`.
- For `DELETE`: the `ResourceRecordSet` must exactly match the values specified when the record was
  created (Name, Type, TTL, and all Values) — the source is explicit that Route 53 requires this.
- Multiple `Change` entries may be batched into one `ChangeBatch` (with an optional `Comment`) — Route 53
  applies the whole batch transactionally, all-or-nothing.
- Do not submit a `DELETE` for the same `ResourceRecordSet` twice within one batch — this is a documented
  error case (see step 5).

See `endpoints.md` for the exact request syntax and field table.

### 4. Submit the change

Call the change-record-sets capability against the resolved hosted zone ID with the batch from step 3. On
success, capture `ChangeInfo.Id` (the change ID), `Status` (will be `PENDING` — this is the initial status
of every new change), and `SubmittedAt`.

### 5. Handle documented errors

- **InvalidChangeBatch** — one or more validation errors in the batch (includes duplicate-delete case
  above). Report the batch's message list to the operator; do not retry blindly.
- **InvalidInput** — malformed input; check field values against `endpoints.md`.
- **NoSuchHealthCheck** — the health check ID does not exist; drop it or correct it.
- **NoSuchHostedZone** — the hosted zone ID doesn't exist. If it came from step 1's lookup, re-check the
  `Name` match there before retrying; if it was supplied directly, verify it with the operator — do not
  substitute a guessed ID.
- **PriorRequestNotComplete** — Route 53 is still processing a prior request against this hosted zone.
  Wait, using increasing intervals between retries, before resubmitting (source's own guidance — do not
  busy-loop).
- **Throttling** (`Rate exceeded`) — per-account request-rate or change-throughput limit hit. Apply
  exponential backoff before retrying (source's own guidance).

### 6. Confirm propagation

Poll the change-status capability with the change ID from step 4:
- `Status: PENDING` — not yet propagated to all Route 53 name servers managing the hosted zone; poll
  again. The source states changes generally propagate within 60 seconds.
- `Status: INSYNC` — propagation complete to all Route 53 DNS servers managing the hosted zone. This is
  the success condition — stop polling and report `SUCCESS`.
- If still `PENDING` well past the ~60-second guideline, keep polling a reasonable number of times, then
  report `TIMED_OUT_PENDING` with the change ID rather than declaring success or failure — the source
  does not define a hard timeout, so don't invent one. (If the caller doesn't need propagation confirmed
  at all, skip this step and report `SUCCESS` right after step 4's `PENDING` response.)

Errors on this call:
- **InvalidInput** — malformed change ID.
- **NoSuchChange** — the change ID doesn't exist (shouldn't happen with a change ID from step 4; report as
  an anomaly if it does).

### 7. Respect documented limits

Before submitting, if the batch is large, check against the documented caps: 10,000 records per hosted
zone, 400 records per record set, 1,000 `ResourceRecord` elements per request (UPSERT counts each
element twice), and 32,000 characters total across all `Value` elements per request (UPSERT counts
each character twice). If a requested change
would exceed one of these, report it to the operator rather than submitting a request that AWS will
reject.

## Patterns

- **A change batch is all-or-nothing.** A validation failure on any one `Change` in the request cancels
  the entire batch — there's no partial-apply to reason about.
- **DELETE requires an exact match, not just a name+type.** Route 53 rejects a delete unless `Name`,
  `Type`, `TTL`, and every `Value` match what's currently on the record set — capture the exact current
  values before attempting a delete if they aren't already known.

## Known limitations

- Covers plain resource record sets only — alias records, weighted/failover/geolocation/geoproximity/
  latency/multivalue-answer/IP-based routing policies, and Traffic Flow are out of scope.
- **DELETE and any UPSERT/CREATE against a name+type that already resolves in production are hard to
  reverse** — Route 53 keeps no undo/rollback for a completed change. Reversal is only possible by
  submitting an inverse change (recreate a deleted record with its original values, or UPSERT back to
  the prior values), and only if those prior exact values were captured beforehand. This is why step 2's
  confirmation gate exists — do not skip it.

## Tools

Every operation below maps to the Route 53 REST API (2013-04-01) — see `endpoints.md` for the literal
request/response shape.

| Operation | Description | Category |
|---|---|---|
| `ListHostedZonesByName` | Resolve a domain name to its hosted zone (nearest match, not exact) | Zone Lookup |
| `ListHostedZones` | Fallback: list all hosted zones for client-side name matching | Zone Lookup |
| `ChangeResourceRecordSets` | Create, update (upsert), or delete a record set via a change batch | Record Management |
| `GetChange` | Check propagation status (`PENDING` → `INSYNC`) of a submitted change | Record Management |

## Verification checklist

- [ ] The hosted zone used was verified to actually match the target domain (not just the nearest
      alphabetical result from a name-based lookup)
- [ ] For DELETE: the submitted values (Name, Type, TTL, all Values) exactly matched the record as
      currently configured — not assumed or guessed
- [ ] The change's `ChangeInfo.Id` was captured for later status checks
- [ ] Propagation was confirmed via `GetChange` returning `INSYNC` (or the caller explicitly didn't need
      that confirmation)
