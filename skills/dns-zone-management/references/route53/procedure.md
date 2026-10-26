# AWS Route 53 — DNS Zone Management Procedure

Create, read, update (comment only), and delete a Route 53 hosted zone, including the automatically
managed SOA/NS record set, and delegate a subdomain into its own hosted zone when the parent domain's
authoritative DNS lives elsewhere. Covers the hosted zone object itself, not the individual records
inside it — see the separate `dns-record-management` skill's Route 53 procedure for that. Assumes an
authenticated Route 53 API client (`route53:CreateHostedZone`, `DeleteHostedZone`, `GetHostedZone`,
`UpdateHostedZoneComment`, `ListHostedZones`/`ListHostedZonesByName`, `GetChange`, and, for private
zones, `ec2:DescribeVpcs`) is already available to the caller.

Source: AWS Route 53 API Reference (API version `2013-04-01`) and Route 53 Developer Guide,
docs.aws.amazon.com, retrieved 2026-09-17.

## Operational procedure

### 1. Create a hosted zone

A hosted zone can be public (routes internet-facing DNS for the domain and its subdomains) or
private (routes DNS only inside one or more associated Amazon VPCs). A zone can't be created for a
bare top-level domain (e.g. `.com` itself), and a zone's public/private nature can't be changed after
creation — creating the wrong kind means creating a fresh zone of the right kind instead.

Supply:
- A caller-generated idempotency token, unique per creation attempt — reusing the same token against
  an already-created zone is how Route 53 recognizes a retried request rather than a duplicate create
  (see step 5's `HostedZoneAlreadyExists`).
- The fully qualified domain name for the zone (a trailing dot is accepted but not required — Route 53
  treats the name identically either way).
- Optionally, a free-text comment describing the zone's purpose.
- For a private zone: exactly one associated VPC (its ID and region) at creation time — additional
  VPCs are associated afterward through a separate capability, not covered here. The caller's
  credentials need permission to describe that VPC, and the VPC must belong to the same AWS
  partition (standard AWS, China, or GovCloud) as the zone being created.
- Optionally, a reusable delegation set ID, if the caller wants this zone to share a fixed set of name
  servers with other zones rather than getting a fresh set assigned. If reused across a parent and
  child zone that share one or more name servers, creation is rejected (step 5).

On success, Route 53 auto-generates the zone's default SOA record and a 4-entry NS record set (see
"SOA and NS defaults" below) and returns the new zone's identifier, its assigned name servers, and a
change reference whose status starts `PENDING`. A public zone's SOA/NS aren't yet live on every
Route 53 name server the moment creation returns — see step 6 for confirming that.

See `endpoints.md` § "Create a Hosted Zone" for the exact request/response shape.

### 2. Read a hosted zone

Fetch a hosted zone's current state (its ID, name, public/private config, comment, associated VPCs if
private, and current record count) plus its assigned name servers, by the zone's identifier. This is
also the mechanism for retrieving a zone's 4 name servers when preparing subdomain delegation (step 4)
or simply reporting a zone's status back to the operator.

See `endpoints.md` § "Read a Hosted Zone" for the exact request/response shape and errors.

### 3. Update a hosted zone's comment

The only zone-level attribute changeable after creation through this API is the free-text comment —
name, public/private designation, and VPC associations at creation are not mutable this way.
Submitting the call with no comment value clears any existing comment rather than leaving it
unchanged, so always pass the full intended comment text, not a partial or empty one unless clearing
it is the actual intent.

See `endpoints.md` § "Update a Hosted Zone's Comment" for the exact request/response shape.

### 4. Delegate a subdomain to its own hosted zone

Use this when a domain's authoritative DNS is hosted elsewhere (not Route 53) and only a subdomain of
it should be delegated into Route 53 — e.g. the domain `example.com` is served by another provider,
but `test.example.com` should resolve via Route 53. (A subdomain of a domain that is *already* a
Route 53 zone is a different, simpler case — just add records for it inside the existing parent
zone — and is not what this procedure addresses.)

1. Create a new hosted zone for the subdomain itself, following step 1.
2. Populate that new zone with whatever records the subdomain needs (via the `dns-record-management`
   skill). Do not add extra SOA or NS records into this zone beyond the ones Route 53 generated at
   creation, and do not remove the generated ones — they are what makes the delegation resolve
   correctly.
3. If confirmation of propagation matters to the caller, poll the change status from step 1's
   creation (see step 6) before proceeding.
4. Read the new zone's assigned name servers (step 2 above).
5. On the other DNS service — the one that hosts the *parent* domain, not Route 53 — add NS records
   for the subdomain name, listing the 4 name servers from step 4, using whatever mechanism that other
   provider exposes (out of scope for this Route 53–specific procedure). Before doing so, back up that
   provider's existing zone data for the parent domain. Do not add an SOA record for the subdomain on
   the parent's side — the subdomain's own SOA already exists in the new Route 53 zone, and the parent
   provider is not meant to claim authority over it. If the parent-side provider auto-generated an SOA
   for the new subdomain name on its own, remove that one specifically — never touch the parent
   domain's own SOA record.

### 5. Handle documented errors (create/delete/update)

- **ConflictingDomainExists** — depends on context: creating a public zone whose name matches (or is
  parent/child of) an existing zone while sharing one or more name servers via the same reusable
  delegation set; or creating a private zone already associated with the same VPC under the same
  name. Report to the operator rather than retrying blindly — this reflects a real naming/delegation
  conflict, not a transient condition.
- **DelegationSetNotAvailable** — the account has hit Route 53's limit on how many zones can share the
  same name (a rare, documented cap); escalate rather than retry.
- **DelegationSetNotReusable** / **NoSuchDelegationSet** — the supplied reusable delegation set ID
  doesn't exist or isn't of the reusable kind; verify the ID with the operator.
- **HostedZoneAlreadyExists** — the idempotency token from step 1 was already used to create a zone;
  this is Route 53 recognizing a retried create, not a new conflict — check whether the original
  create already succeeded before treating this as a failure.
- **InvalidDomainName** / **InvalidInput** — malformed domain name or other malformed input; check
  field values against `endpoints.md`.
- **InvalidVPCId** — the VPC ID either doesn't exist or the caller's credentials can't access it.
- **TooManyHostedZones** — the account (or the reusable delegation set) is at its zone-count limit;
  report to the operator — this needs a support request or delegation-set change, not a retry.
- **HostedZoneNotEmpty** (delete only) — the zone being deleted still contains records other than the
  default SOA/NS, or has DNSSEC signing enabled. Delete those other records (via
  `dns-record-management`) and disable DNSSEC first; do not attempt to force the deletion another way.
- **NoSuchHostedZone** — the zone ID doesn't exist; re-verify it rather than substituting a guess.
- **PriorRequestNotComplete** — Route 53 is still finishing a prior request against this zone; wait,
  using increasing intervals between retries, before resubmitting.

### 6. Confirm propagation of a create or delete

Poll the change-status capability with the change ID returned by create (step 1) or delete (step 7)
using the same mechanism `dns-record-management`'s Route 53 procedure uses for record changes:
- `Status: PENDING` — not yet propagated to every Route 53 name server responsible for the zone; poll
  again. Changes generally propagate within about 60 seconds per the source, though no hard timeout is
  documented.
- `Status: INSYNC` — propagation is complete; this is the success condition.
- If still `PENDING` well past that guideline, keep polling a reasonable number of times, then report
  `TIMED_OUT_PENDING` rather than declaring success or failure — do not invent a hard timeout the
  source doesn't state.

### 7. Delete a hosted zone — confirmation gate required

**Stop and confirm with the operator before deleting any hosted zone.** Deletion cannot be undone —
there is no restore. Recreating the zone afterward means a brand-new zone with newly assigned name
servers, requiring the domain's registrar (or, for a delegated subdomain, the parent zone) to be
updated again, which can take up to 48 hours to fully take effect. Until that re-pointing happens, an
orphaned but still-registered domain name is at risk of being claimed and misused by someone else.
State to the operator: the zone name and ID, that this is irreversible, and that if the intent is only
to stop routing traffic (not to stop paying for or fully abandon the zone), deleting the records
inside the zone is the safer alternative to deleting the zone itself.

Before submitting the delete call, the zone must contain nothing but its default SOA and NS records,
and must have DNSSEC signing disabled (see step 5's `HostedZoneNotEmpty`). If the zone being deleted
was itself delegated to from a parent zone (step 4), remind the operator that the parent's delegating
NS records will now point at nothing and should be updated or removed there too.

See `endpoints.md` § "Delete a Hosted Zone" for the exact request/response shape.

## SOA and NS defaults (what Route 53 auto-generates on zone creation)

- **NS record**: created at the zone's own name, listing 4 name servers assigned from Route 53's
  pool (one from each of several different top-level domains, by design, for resilience against a
  single TLD's DNS infrastructure having a problem). The source recommends not adding, changing, or
  removing entries in this record except in rare, deliberate cases.
  - The exact 4 values are visible via step 2 (read) — never guess or reuse an example value from
    documentation as if it were a real assigned name server.
- **SOA record**: one record, holding these fields in order — the source's own worked example is
  `ns-2048.awsdns-64.net. hostmaster.example.com. 1 7200 900 1209600 86400`:
  1. The Route 53 name server that generated the record.
  2. An administrator contact address, with the usual `@` replaced by a `.` (e.g.
     `hostmaster.example.com` means `hostmaster@example.com`) — defaults to an Amazon-owned address
     that is not monitored, so an operator relying on this contact address for real notifications
     needs to know it's a placeholder.
  3. A serial number, which Route 53 never increments on its own — only a caller changing a record
     bumps it, and only if the caller chooses to. It exists for secondary DNS servers that track zone
     versions.
  4. A refresh interval (seconds) — how long a secondary server waits before re-checking the primary's
     SOA for changes.
  5. A retry interval (seconds), normally shorter than the refresh interval — how long a secondary
     waits before retrying a zone transfer after a failed attempt.
  6. An expire interval (seconds) — how long a secondary keeps answering queries with stale data before
     giving up if it can't complete a transfer in that window.
  7. A negative-caching (minimum) TTL (seconds) — governs how long resolvers cache an NXDOMAIN (name
     doesn't exist at all) or NODATA (name exists, but not for the queried record type) response. The
     effective cache duration is whichever is smaller: this value, or the SOA record's own TTL
     (900 seconds by default). Raising either value reduces query volume/cost but also means an
     accidentally deleted-then-recreated record stays unreachable to already-caching resolvers for
     longer.

## Patterns

- **A hosted zone's public/private nature and name are fixed at creation.** There is no in-place
  conversion between public and private, or renaming — only "create a new zone of the right kind" if
  the wrong one was made.
- **Deletion requires the zone to be reduced to just its defaults first.** Route 53 will not delete a
  zone carrying any other record, or one with DNSSEC still enabled — this is a structural safeguard,
  not a preference, and there's no override.
- **The only vendor-side undo for an accidental deletion is a full recreation**, with all the
  registrar/parent-zone re-pointing and propagation delay that implies — this is why step 7's
  confirmation gate exists.

## Known limitations

- Does not cover associating additional VPCs with an existing private zone after creation, reusable
  delegation set lifecycle management, or DNSSEC key management for a zone — all separate capabilities
  from the source, not fetched here.
- Does not cover the case of adding a subdomain that stays within an *already-Route-53* parent zone —
  that's ordinary record management inside the existing zone (`dns-record-management`), not a
  separate zone or a delegation, and this procedure's subdomain-delegation step (step 4) assumes the
  parent domain is hosted elsewhere.
- **Zone deletion is irreversible** — see step 7. Never skip its confirmation gate.
- The exact hard cap on hosted zones per account/reusable delegation set is not itself documented as a
  fixed number in the sources — when `TooManyHostedZones` occurs, report it to the
  operator rather than assuming a specific number was exceeded.

## Tools

Every operation below maps to the Route 53 REST API (`2013-04-01`) — see `endpoints.md` for the
literal request/response shape.

| Operation | Description | Category |
|---|---|---|
| `CreateHostedZone` | Create a public or private hosted zone | Zone Management |
| `GetHostedZone` | Read a zone's config, comment, VPC associations, and assigned name servers | Zone Management |
| `UpdateHostedZoneComment` | Change (or clear) a zone's free-text comment | Zone Management |
| `DeleteHostedZone` | Delete a hosted zone reduced to just its default SOA/NS records | Zone Management |
| `ListHostedZones` / `ListHostedZonesByName` | Enumerate or look up zones by name | Zone Management |
| `GetChange` | Check propagation status (`PENDING` → `INSYNC`) of a create/delete | Zone Management |

## Verification checklist

- [ ] For create: the idempotency token was unique to this creation attempt, not reused from a prior
      unrelated call
- [ ] For a private zone: exactly one VPC was supplied at creation, in the same AWS partition as the
      zone
- [ ] For delete: the zone was confirmed to contain only its default SOA/NS records and to have
      DNSSEC disabled before submitting, and the operator explicitly confirmed the irreversible delete
      beforehand
- [ ] For subdomain delegation: the new zone's own SOA/NS were left untouched, and no SOA record was
      added on the parent-domain side — only NS delegation records
- [ ] Propagation (`INSYNC`) was confirmed after create/delete, or the caller explicitly didn't need
      that confirmation
- [ ] Outcome reported using this procedure's own status vocabulary (`PENDING`, `INSYNC`,
      `TIMED_OUT_PENDING`, or the specific error name) — not normalized away
