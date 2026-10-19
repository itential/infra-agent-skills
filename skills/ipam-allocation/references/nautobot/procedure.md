# Nautobot — IPAM Prefix and IP Allocation Procedure

Allocate address space in Nautobot IPAM: find and carve out a child prefix from a parent prefix, and
allocate the next free IP address inside a prefix. Covers only the prefix and IP address objects of the
IPAM app (and the namespace they live in). Does not cover VRFs, VLANs, RIRs, route targets, locations,
roles, or any non-IPAM app. Assumes an authenticated tool for the Nautobot REST API with permission to
view and add prefixes and IP addresses is already available to the calling agent. Each named operation
maps to a concrete call in `endpoints.md` — bind it there, not here.

Sources: Nautobot core documentation, "Prefix" and "IP Address" data-model pages
(docs.nautobot.com, retrieved 2026-10-19). Allocation-call behavior is **not described in those pages**;
it was taken from Nautobot's own generated OpenAPI schema (version 2.4.14) as copied into the Itential
`assets` repository, which is a secondary source — every detail from it is marked *(unverified)* below.

## Operational procedure

### Common Sequences

**Allocate a new subnet from an existing pool, with its first IP reserved:**
1. Allocate a Child Prefix — from the given parent, at the requested prefix length.
2. Allocate the Next Available IP — inside the prefix ID returned by step 1.
3. Report the new prefix and the reserved IP together.

**Just reserve the next IP in an existing prefix:**
1. Allocate the Next Available IP — against the known prefix ID. Do not create or carve anything first.

### Data-model facts the steps rely on

- Every prefix belongs to one namespace and must be unique within it. A prefix needs a CIDR, a status
  (Active, Reserved or Deprecated by default) and a namespace.
- Prefix types are network (default), container and pool. For network and container prefixes the first
  and last IPv4 addresses are not usable hosts; in a pool every address is usable.
- Every IP address must have a parent prefix; Nautobot derives the parent from the IP's namespace.
  IP addresses are unique per namespace.
- Editing a prefix's network or namespace re-links descendants but does not renumber them.

### List Available Child Prefixes

List the child prefixes Nautobot offers inside the given parent. These are computed candidates, not
stored records. Use to show options or confirm space before allocating.

### Allocate a Child Prefix

Create the next available child prefix of the requested length inside the given parent. The prefix
length and a status are both required *(unverified: from the generated schema; a maintainer-tracker issue
also reports a 400 when status is omitted)*. Optional attributes (role, location, tenant, VLAN, RIR,
description) may be supplied.

- Confirm success: the response is a full prefix record. Record its ID and CIDR.
- If the parent has no room for the requested length, the exhaustion error response is not documented in
  the sources *(unverified)*; report the failure and the requested length, do not retry the same request.

### List Available IPs in a Prefix

List free addresses Nautobot offers in the given prefix, up to the page limit; not a full enumeration for
a large prefix. Optional range start/end bounds exist *(unverified: schema parameters only)*.

### Allocate the Next Available IP

Create an IP address record for the next free address in the given prefix. A status is required
*(unverified: schema; same tracker issue)*. Optional attributes: DNS name, description, role, tenant,
tags.

- Confirm success: the response is a full IP address record including the assigned address.

## Patterns

- Availability lists are computed. Nothing is reserved until an allocate call succeeds.
- Each allocate call creates a new record, so re-running with corrected input leaves the earlier record in place *(inferred from the create semantics, not stated in the sources)*.
- The tracker issue reports that invalid allocation requests have returned an empty 204 rather than a
  400 *(unverified, may be fixed in current releases)*. Treat an empty response without a record as a
  failure, never as success.

## Known limitations

- Created prefixes and IPs are real and persistent. Deleting a wrong allocation is a manual delete in
  Nautobot, not part of this skill. Before any delete or overwrite of an existing record, stop and
  confirm with the operator.
- Exhaustion response, rate limits and bulk-allocation behavior are not documented in the sources used.
- Covers Nautobot 2.x data-model terms only (namespace-based).

## Tools

| Operation | Description | Category |
|---|---|---|
| List Available Child Prefixes | Computed candidate child prefixes under a parent | IPAM |
| Allocate a Child Prefix | Create a real child prefix of a given length | IPAM |
| List Available IPs in a Prefix | Computed candidate free IPs in a prefix | IPAM |
| Allocate Next Available IP | Create a real IP record in a prefix | IPAM |

## Verification checklist

- [ ] Each allocate response contained a full record (ID plus CIDR or address), not just a 2xx or empty body
- [ ] A required status (and prefix length for prefixes) was supplied before calling
- [ ] The parent prefix and the allocated value are included in the final report
- [ ] Any failure was reported as a failure with the requested length, not retried blindly
