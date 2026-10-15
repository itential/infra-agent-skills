# NetBox — IPAM Prefix and IP Allocation Procedure

Allocate IP address space in NetBox IPAM — create an aggregate or parent prefix if needed, find and
carve out an available child prefix from a parent, and allocate an available IP address within a
prefix. Covers aggregate/prefix creation and available-prefixes/available-ips list/allocate under the
IPAM app only — does not cover VRFs, VLANs, roles, tenancy, RIR management, IP ranges, services, FHRP
groups, or non-IPAM NetBox apps. Assumes an authenticated tool for the NetBox REST API (add/view
permission on `ipam.prefix` and `ipam.ipaddress`, and `ipam.aggregate` if creating aggregates) is
already available to the calling agent. Confirmed current against NetBox 4.5/4.6 documentation — the
Aggregate model and its RIR relationship remain unchanged terminology as of that version.

Each named capability below maps to a concrete NetBox operation in `endpoints.md` — bind it there, not
here.

## Operational procedure

### Common Sequences

These are the realistic end-to-end asks — follow the named steps in order, don't stop partway and call
it done.

**Allocate a new subnet from an existing pool, with its first usable IP reserved:**
1. Allocate (Carve Out) a Child Prefix — from the given parent, at the requested prefix length.
2. Allocate the Next Available IP — within the prefix ID just returned by step 1.
3. Report both the new prefix and the reserved IP together as one outcome.

**Stand up a brand-new address block from scratch (no existing parent yet) and carve the first subnet
from it:**
1. Create an Aggregate — the top-level block under the appropriate RIR.
2. Create a Prefix — for a `container`-status prefix inside that aggregate (or skip if the aggregate
   itself is the intended allocation parent — check whether the caller wants an intermediate container).
3. Allocate (Carve Out) a Child Prefix — from that container, at the requested prefix length.
4. Optionally continue with Allocate the Next Available IP as in the sequence above.

**Just reserve the next IP in an already-existing prefix (no new subnet needed):**
1. Allocate the Next Available IP — directly against the known prefix ID. Skip straight here; do not
   create or carve anything first.

If a caller's ask doesn't match one of these shapes, use the individual capability sections directly and
still confirm success at each step before proceeding to the next — never chain calls without checking
the prior one actually returned a usable record.

### Create an Aggregate (top-level address block)

Create an aggregate for the given CIDR under the given RIR. Both the network and the RIR are required —
NetBox will reject the request without an RIR reference.

Confirm success: the response record includes the aggregate's NetBox ID and the `prefix` echoed back.

### Create a Prefix (directly, not carved from a parent)

Create a prefix for the given CIDR. Only the network itself is required; set the status explicitly
(`container`, `active`, `reserved`, or `deprecated`) when the caller's intent implies one — don't rely on
an unstated instance default when the action matters (e.g. marking a block as `container` before
allocating children from it).

### List Available Child Prefixes

List the prefixes NetBox considers available to carve out of the given parent — these are computed,
not-yet-existing candidates, not real records. Use this to show options or confirm space exists before
allocating.

### Allocate (Carve Out) a Child Prefix

Allocate the next available child prefix of the given length from the given parent — this field is
required with no default; do not omit it or guess a value. Supports allocating more than one prefix of
the same length from the same parent in a single call.

- If the parent doesn't have room for the requested length, the pool-exhaustion signal applies (see
  Error Handling) — do not retry the same request; report the actual available capacity from the error
  message.
- Confirm success: the response contains full prefix record(s), not just the candidate shape from List
  — record the new prefix's NetBox ID and CIDR.

### List Available IPs in a Prefix

List IPs NetBox considers available within the given prefix — up to the pagination limit; for a large
prefix this is not a complete enumeration of every free address, only a preview page.

### Allocate the Next Available IP

Allocate the next available IP address within the given prefix. A specific mask length is optional —
omit it to use the prefix's own mask, or set it to assign a different mask (e.g. a /32 host route inside
a /24). Supports allocating more than one IP from the same prefix in a single call.

- Confirm success: the response contains the full IP address record(s), including the assigned address.

## Patterns

- **Availability lists are computed, not real records.** Both list-available operations return
  candidates NetBox calculates on the fly — they don't reserve anything until an allocate call actually
  runs.
- **A wrong allocation doesn't self-correct.** Allocating the wrong prefix length creates an additional
  record rather than replacing one — re-running the same action with corrected input adds a second
  record instead of fixing the first.

## Error Handling

- **Pool exhaustion** (allocate_prefix or allocate_ip): the tool call errors instead of silently
  returning nothing — recognize this by the documented message pattern in `endpoints.md`, not just a
  generic failure. Report as EXHAUSTED with the requested vs. available counts from the message if
  present.
- **Missing required field** (RIR on create_aggregate, prefix length on allocate_prefix): report and
  stop before calling — don't let NetBox reject an incomplete request when the gap is knowable upfront.
- Any other tool/capability error: report and stop. Do not retry automatically.

## Known limitations

- Covers aggregate/prefix creation and available-prefixes/available-ips list/allocate under the IPAM
  app only — does not cover VRFs, VLANs, roles, tenancy, RIR management, IP ranges, services, FHRP
  groups, or non-IPAM NetBox apps.
- Created records (aggregates, prefixes, IPs) are real and persistent — other tooling/automation may
  depend on them. Reversible only via NetBox's standard delete operations, which are not part of this
  skill's scope — not by re-invoking this skill.
- No documented auto-abort/rollback exists for a wrong allocation — see Patterns above; correcting a
  mistake means a manual delete of the wrong record via NetBox's own tooling, not something this skill
  does.

## Tools

| Operation | Description | Category |
|---|---|---|
| Create Aggregate | Create a top-level address block under an RIR | IPAM |
| Create Prefix | Create a prefix directly (not carved from a parent) | IPAM |
| List Available Prefixes | List computed candidate child prefixes under a parent | IPAM |
| Allocate (Carve Out) Prefix | Allocate a real child prefix of a given length from a parent | IPAM |
| List Available IPs | List computed candidate free IPs within a prefix | IPAM |
| Allocate Next Available IP | Allocate a real IP address within a prefix | IPAM |

## Verification checklist

- [ ] Every allocate call's response was checked for a full record (ID + CIDR/address), not just
      accepted on a 2xx status
- [ ] Pool exhaustion, if it occurred, was reported as EXHAUSTED with requested-vs-available counts, not
      treated as a generic failure
- [ ] Required fields (RIR for aggregates, prefix length for allocate_prefix) were supplied before
      calling, not discovered from a rejection
- [ ] The parent/target identifier (CIDR or NetBox ID) and, for allocate actions, the specific value
      allocated, are included in the final report
