# F5 BIG-IP LTM — Virtual Server (VIP) and Pool/Pool-Member CRUD Procedure

Creates, reads, updates, and deletes an LTM virtual server (VIP) and an LTM pool, and manages pool
membership (add, remove, enable/disable a member), on F5 BIG-IP via the iControl REST management
API. Assumes an authenticated REST client against a BIG-IP management endpoint is already
available. Does not cover TLS profile/certificate provisioning (see `certificate-management`), iRule
authoring, GTM/DNS wide-IP configuration, or AS3/declarative-onboarding-style bulk application
templates — this procedure targets the object-level iControl REST resources directly.

Source: F5 clouddocs iControl REST API Reference, `APIRef_tm_ltm_virtual`, `APIRef_tm_ltm_pool`, and
`APIRef_tm_ltm_pool_members` pages (https://clouddocs.f5.com/api/icontrol-rest/), retrieved
2026-09-17. **Sourcing caveat:** this specific reference sub-site carries its own published notice
that it holds community-contributed content that F5 does not monitor or control — treat the field
lists below as a solid, broadly reliable picture of the BIG-IP TMOS object model, but not as a
guarantee of F5's own current, warranted wording. Where a fact could not be pinned to this source at
all, that is called out explicitly below rather than presented as page-confirmed.

## Operational procedure

### Create a pool (with initial members)

1. **Confirm the target partition** — BIG-IP objects live under an administrative partition
   (default `Common`); resolve which partition the pool and virtual server belong to before
   building any payload, since the resource's natural key is name + partition + subPath, not name
   alone.
2. **Build the pool object** — set `name`, the target partition, and any load-balancing behavior
   fields needed: `loadBalancingMode` (defaults to round-robin if not set), `monitor` (one or more
   health monitor names; BIG-IP accepts a single monitor, an "and"-joined list, or a "min N of {...}"
   quorum expression — if the request doesn't specify one, leave it unset rather than guessing a
   monitor name that may not exist), and `slowRampTime` if new members should ramp up gradually
   (documented default 10 seconds) rather than receiving full traffic immediately.
3. **Create the pool** — submit the pool object. See `endpoints.md` for the literal call. Treat a
   2xx response containing the created pool's own `name`/`partition`/`selfLink` as success; anything
   else, report FAILED with the response body verbatim rather than guessing at a cause (this
   source did not document a specific set of pool-create error strings).
4. **Add each initial pool member** — for each member, submit a member object to the pool's
   `members` sub-collection with the member's address:port as its identifying name (this address:
   port naming convention is well-established BIG-IP practice; it was not found spelled out
   verbatim on the specific members reference page retrieved for this procedure, so treat it as a
   secondary/general-knowledge convention rather than a page-cited fact when precision matters —
   confirm against the target BIG-IP's own existing pool member objects if unsure). Optionally set
   `ratio` (weight for ratio-based load-balancing modes, default 1), `priorityGroup` (default 0),
   and `connectionLimit` (default 0, meaning unlimited) per member.
5. **Confirm membership** — read the pool's `members` sub-collection back and confirm each intended
   member is present before reporting the pool CREATED.

### Read a pool or virtual server

6. **Look up by name and partition** — a single resource is identified by its natural key
   (name, partition, subPath). If the object cannot be found, report NOT_FOUND rather than an
   assumed-empty result.

### Create a virtual server (VIP)

7. **Assemble the virtual server object** — set `name`, partition, `destination` (the VIP's own
   address and port, in `<address>:<port>` form), `ipProtocol` (e.g. `tcp` or `udp`), and `pool`
   (the default pool this VIP directs traffic to — must already exist per steps 1-5, or be created
   first). Set `mask` only for a network/wildcard virtual server; a host virtual server's default
   mask is an all-ones mask equivalent to a single host route, so most single-address VIPs can leave
   it unset. Set `source` only if traffic should be restricted to a specific source network;
   otherwise BIG-IP's own default accepts traffic from any source.
8. **Attach profiles if required** — if the request specifies TLS termination, association of a
   client-SSL or server-SSL profile happens through the virtual server's `profiles` list, and that
   profile must reference an already-provisioned certificate/key pair. Provisioning that certificate
   itself is out of scope here — see `certificate-management`. Do not fabricate a profile name; if
   the caller didn't supply one and TLS termination is required, stop and ask rather than guessing.
9. **Create the virtual server** — submit the assembled object. See `endpoints.md`. Treat a 2xx
   response containing the object's own name/partition/selfLink as CREATED. Confirm the `pool`
   field on the response matches what was requested before declaring success, since a
   misconfigured/nonexistent pool name is a plausible silent-mismatch source this reference doesn't
   document an explicit rejection code for.

### Update a virtual server or pool

10. **Read current state first** — before any update, read the object back so the update only
    changes the fields the caller actually intends (a PUT-style full replace against a set of
    fields you didn't intend to touch can silently reset unrelated fields to their defaults on this
    platform's object model, since PUT and PATCH are both offered as resource-level methods per this
    source — prefer PATCH-shaped, partial-field submissions where the calling tool supports
    distinguishing the two, and if it can't, read-modify-write the full object rather than
    submitting a minimal payload against a PUT-only tool).
11. **Submit only the changed fields** — e.g. flipping a virtual server between `enabled` and
    `disabled` state, or changing a pool's `loadBalancingMode` or `monitor`. Confirm the response
    reflects the new value before declaring the change applied.

### Enable / disable a pool member (drain without removing)

12. **Distinguish disabling new sessions from forcing a member fully offline** — this source
    documents two separate per-member fields with different meanings: `session` (`user-enabled` by
    default; setting it to a disabled value stops the member from receiving *new* sessions) and
    `state` (`user-up` by default; setting it to `user-down` forces the member offline immediately,
    overriding health monitors, until reverted to `user-up`). Do not treat these as interchangeable —
    if the request is "drain gracefully," that maps to disabling `session`; if the request is
    "force this member down right now regardless of monitor status," that maps to `state: user-down`.
    This source's own field description does not state whether disabling `session` alone waits for
    existing connections to finish before stopping traffic entirely — treat that as an explicit
    unknown rather than asserting a drain guarantee, and say so in the outcome report if the caller
    needs that guarantee confirmed.
13. **Stop and confirm with the operator before setting `state: user-down`** on a pool member serving
    live traffic — this immediately overrides health-monitor status and can remove serving capacity
    from a production pool with no ramp-down.

### Remove a pool member / delete a pool / delete a virtual server

14. **Stop and confirm with the operator before any delete** — removing a pool member, deleting a
    pool, or deleting a virtual server are all hard-to-reverse, traffic-affecting changes on this
    platform (a virtual server delete stops all traffic to that VIP's address:port immediately; a
    pool delete fails or orphans any virtual server still referencing it — see Known limitations).
15. **Delete the target object** — submit the delete against the object's resource URI (see
    `endpoints.md`). Treat a 2xx response (typically with an empty body) as success; if the platform
    rejects the delete (e.g. a pool still referenced by a virtual server), report the failure
    verbatim rather than retrying with a guessed workaround — this source doesn't document the
    specific rejection string for a still-referenced pool delete.

## Patterns

- **A pool member's identity is address:port, not a free-form name**, by well-established BIG-IP
  convention — see the sourcing caveat in step 4. Get this confirmed against the live system before
  scripting member adds/removes at scale.
- **`session` and `state` are two independent per-member controls, not one.** See step 12 — conflating
  them misreports what actually happened to a member.
- **PUT and PATCH are both offered at the resource level.** Prefer the narrowest field-scoped update
  the calling tool supports (step 10) to avoid an unintended full-object replace.

## Known limitations

- This procedure covers object-level iControl REST CRUD only — it does not cover F5's AS3
  (Application Services 3) declarative onboarding model, which some BIG-IP deployments use instead
  of direct `ltm virtual`/`ltm pool` object manipulation and may behave differently (e.g. whole-app
  declarations, different idempotency semantics). If the target environment is AS3-managed, this
  procedure's direct-object approach may conflict with it — confirm which model is in use first.
- The specific reference pages this procedure is grounded in carry F5's own notice that they contain
  community-contributed content not monitored by F5 — see the sourcing caveat at the top of this
  file.
- Authentication mechanism for iControl REST (HTTP Basic Auth vs. a token obtained from a login
  endpoint) was not independently confirmed against a primary F5 source in this research pass — an
  authenticated client is assumed already available per this skill's scope, but do not extend that
  assumption into asserting a specific auth flow as F5-documented without your own confirmation.
- Does not cover FQDN-based pool members (a member that tracks a DNS name rather than a static
  address), GTM/wide-IP configuration, or iRule authoring.
- Whether disabling a member's `session` field alone guarantees existing connections drain before
  the member stops receiving any traffic is not stated in the source used here — treat as unknown
  (see step 12).

## Tools

| Operation | Description | Category |
|---|---|---|
| Pool CRUD | Create/read/update/delete an `ltm pool` object | LTM Pool |
| Pool member CRUD | Create/read/update/delete a member within a pool's `members` sub-collection | LTM Pool Member |
| Virtual server CRUD | Create/read/update/delete an `ltm virtual` object | LTM Virtual Server |

## Verification checklist

- [ ] Target partition confirmed before building any payload (natural key is name+partition+subPath)
- [ ] Pool created and its `members` sub-collection read back to confirm intended membership before
      reporting CREATED
- [ ] Virtual server's `pool` field confirmed to match the intended pool name in the response before
      reporting CREATED
- [ ] Updates submitted as narrowly-scoped field changes, not an unintended full-object replace
      (step 10)
- [ ] `session` vs. `state` distinguished correctly when draining/disabling/forcing a pool member
      (step 12) — outcome reported using the correct one of these, not conflated
- [ ] Operator confirmation obtained before forcing a member `state: user-down`, deleting a pool
      member, deleting a pool, or deleting a virtual server
- [ ] Failure responses reported verbatim, not paraphrased into a guessed cause, where this source
      doesn't document a specific error string
