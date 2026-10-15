# PowerDNS Authoritative Server — DNS Zone Management Procedure

Create, read, update (zone-level attributes), and delete a zone in PowerDNS Authoritative Server via
its HTTP API's Zones resource, including the zone's kind (native/primary vs. secondary), its
nameserver set, and where subdomain delegation fits for this platform. Covers the zone object itself —
not the individual RRsets inside it, which the `dns-record-management` skill's PowerDNS procedure
already covers (RRset create/replace/delete/extend/prune, plus DNSSEC rectification). Assumes an
authenticated HTTP API client against the target PowerDNS Authoritative Server (an `X-API-Key` header
value) is already available to the caller.

Source: PowerDNS Authoritative Server HTTP API documentation ("Zones" resource), doc.powerdns.com,
retrieved 2026-09-17 via an LLM-mediated documentation fetch rather than a direct line-by-line read of
the raw reference page — where this affects confidence in a specific claim (the full `kind` enum,
exact error strings, and the default SOA record's literal placeholder content), it's flagged explicitly
below as an open item rather than stated as certain.

## Operational procedure

### 1. Create a zone

Supply the zone's fully qualified name (with a trailing dot), its kind, and the nameservers it should
be seeded with:

- **`kind`** determines the zone's role: a primary/authoritative zone that PowerDNS itself serves and
  can be edited via this API (documented as `Native` in the material behind this procedure — PowerDNS
  also documents `Master`/`Slave` roles for primary/secondary replication relationships, but this
  research did not confirm the complete, current enum; verify the exact accepted values against the
  target PowerDNS instance's own API schema before assuming one beyond `Native`/`Slave`).
- For a secondary (`Slave`) zone, supply the primary server address(es) it should transfer from; for a
  primary zone created and managed directly through this API, that list is empty.
- **`nameservers`** — the list of authoritative name server hostnames this zone should be seeded with.
  PowerDNS uses this list to generate the zone's initial NS RRset at creation time.

On creation, PowerDNS automatically generates the zone's initial SOA and NS records from the supplied
nameservers — the caller does not construct these RRsets by hand as part of zone creation. The
generated SOA's contact address and timing fields are placeholder values, not meant to be left as-is
for a production zone — the exact literal defaults were not confirmed by this research, so don't assume
a specific value; instead, after creation, read the zone back (step 2) to see what was actually
generated, and if it needs real values (a genuine administrative contact address, deliberately chosen
refresh/retry/expire/minimum timers), update it via a normal RRset replace on the SOA record — see
`dns-record-management`'s PowerDNS procedure for that mechanism, since this zone-management procedure
does not re-document RRset-level operations.

See `endpoints.md` § "Create a Zone" for the exact request/response shape.

### 2. Read a zone

Fetch a zone's current configuration and, optionally, its RRsets, by its name. Useful both for general
status reporting and specifically for confirming what SOA/NS content PowerDNS actually generated at
creation (step 1), since this research did not confirm the exact default values in advance.

### 3. Update a zone's configuration

A defined, specific set of zone-level attributes can be changed after creation — this research
confirmed `kind`, `masters`, `catalog`, `account`, `soa_edit`, `soa_edit_api`, `api_rectify`, `dnssec`,
and `nsec3param` as the changeable fields. Any other field included in the request body is silently
ignored rather than applied — in particular, the zone's own current serial-tracking fields
(`serial`/`notified_serial`) and its name cannot be changed this way. If a caller's request implies
changing something outside that confirmed list, treat it as unsupported by this call rather than
assuming it will silently work.

A request with a change PowerDNS itself considers invalid is rejected distinctly from a request that's
simply malformed — the exact triggering conditions for each weren't confirmed by this research, so
report whichever the server actually returns rather than assuming which category a given bad input
falls into.

### 4. Delete a zone — confirmation gate required

**Stop and confirm with the operator before deleting any zone.** Deleting a zone through this API
removes the zone's configuration and metadata together with every RRset it contains — this is a
complete removal, not a soft-disable, and no explicit precondition (such as requiring the zone be
reduced to only its default records first, the way some other platforms require) was confirmed by this
research. Treat that absence of a documented safeguard as a reason for more caution, not less — verify
with the operator what the zone currently contains before proceeding, since PowerDNS itself may not
stop the deletion the way another platform would.

### 5. Subdomain delegation (PowerDNS)

This research did not surface a delegation-specific primitive distinct from ordinary zone creation for
PowerDNS. Where a subdomain needs to be served as its own independently-managed zone, the documented
mechanism is simply: create a new zone for the subdomain's own name (step 1), let PowerDNS generate its
SOA/NS as usual, and then — on whichever system is authoritative for the parent domain — add NS
records for the subdomain pointing at the new zone's name servers. If the parent domain is also served
by this same PowerDNS instance, that means adding an NS RRset for the subdomain name inside the
parent's own zone, via the RRset-management operations documented in `dns-record-management`'s PowerDNS
procedure — not a capability specific to this zone-management procedure.

### 6. Related zone-lifecycle operations (secondary/replication zones)

These apply specifically to zones configured for replication between PowerDNS instances (`kind` other
than a self-managed primary):

- **Notify** — send a DNS NOTIFY message to a zone's configured secondaries, prompting them to check
  for updates. Documented as meaningful for a primary (`Master`-role) zone, or for a secondary zone that
  has re-notify behavior enabled; calling it against a zone that's neither is not expected to accomplish
  anything.
- **Export** — retrieve the zone's full current contents in zone-file/AXFR text form. Read-only,
  non-destructive.
- **Trigger a transfer** (`axfr-retrieve`) — for a secondary zone, ask PowerDNS to immediately pull a
  fresh copy from its configured primary, optionally naming a specific primary address to pull from
  rather than the zone's already-configured one. This research did not confirm what happens if this is
  called against a zone that isn't configured as a secondary — treat that as an unknown, and confirm the
  zone's `kind` before calling it.

## Patterns

- **Zone creation and SOA/NS content are linked, not independent steps.** Unlike a platform where the
  caller writes the SOA/NS RRsets directly, here they're a byproduct of the `nameservers` list supplied
  at creation — get that list right at creation time rather than expecting to freely redefine the NS set
  afterward through this same call.
- **The zone-update call's field list is a fixed, narrow set.** Anything not in the confirmed list
  (`kind`, `masters`, `catalog`, `account`, `soa_edit`, `soa_edit_api`, `api_rectify`, `dnssec`,
  `nsec3param`) is ignored, not rejected — a caller expecting a silently-ignored field to have taken
  effect needs to read the zone back afterward (step 2) to confirm, rather than trusting a success
  status alone.

## Known limitations

- Does not cover RRset-level operations inside an existing zone (create/replace/delete/extend/prune of
  individual records) or DNSSEC rectification — see `dns-record-management`'s PowerDNS procedure for
  both.
- The complete, current enum of accepted `kind` values, the literal default SOA content PowerDNS
  generates at creation, and the exact error codes/strings for zone create/update/delete failures were
  not confirmed by this research — treat each as an item to verify against the target instance's own
  API schema/behavior before depending on a specific value.
- No documented requirement was found that a zone be emptied of non-default records before deletion —
  do not assume PowerDNS either requires or doesn't require this; confirm zone contents with the
  operator regardless before deleting (step 4).
- Whether calling the transfer-trigger or notify operations against a zone of the wrong `kind` fails
  outright or is simply a no-op was not confirmed — check the zone's `kind` first rather than relying on
  the call itself to reject a mismatched zone.
- Some material in this procedure came from an LLM-mediated documentation summary rather than a direct
  read of PowerDNS's raw reference page — re-verify field completeness and error behavior against the
  live docs or the target instance before treating this procedure as complete for production use.

## Tools

Every operation below maps to the PowerDNS Authoritative Server HTTP API — see `endpoints.md` for the
literal request/response shape.

| Operation | Description | Category |
|---|---|---|
| Create Zone | Create a zone with a given kind, nameservers, and (for secondaries) masters | Zone Management |
| Retrieve Zone | Read a zone's current configuration and, optionally, its RRsets | Zone Management |
| Update Zone | Change a defined set of zone-level attributes | Zone Management |
| Delete Zone | Remove a zone, its metadata, and every RRset it contains | Zone Management |
| Notify Zone | Send a DNS NOTIFY to a zone's secondaries | Zone Management (replication) |
| Export Zone | Retrieve the zone's contents in zone-file/AXFR form | Zone Management |
| Retrieve Slave Zone (axfr-retrieve) | Trigger an immediate transfer from a secondary zone's primary | Zone Management (replication) |

## Verification checklist

- [ ] `kind` and `nameservers` were deliberately chosen at creation — not defaulted without
      confirming what the operator actually wants seeded into the new zone's NS set
- [ ] The generated SOA record was read back (step 2) rather than assumed, and updated via
      `dns-record-management`'s RRset-replace mechanism if its placeholder values need to become
      real production values
- [ ] An update request only relied on the confirmed-changeable field list (`kind`, `masters`,
      `catalog`, `account`, `soa_edit`, `soa_edit_api`, `api_rectify`, `dnssec`, `nsec3param`) —
      anything else was verified by re-reading the zone, not assumed applied
- [ ] Deletion was confirmed with the operator beforehand, with zone contents checked first, given
      the absence of a documented emptiness precondition
- [ ] Notify/transfer-trigger calls were only made against a zone whose `kind` was confirmed to make
      that call meaningful
