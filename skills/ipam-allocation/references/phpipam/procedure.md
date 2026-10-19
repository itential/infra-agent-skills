# phpIPAM — Subnet and IP Address Allocation Procedure

Allocate address space in phpIPAM: create a subnet inside a section, carve the first free child subnet
of a given mask out of an existing subnet, and assign an IP address (either a chosen one or the first
free one in a subnet). Also covers reading subnet usage and finding an existing subnet by CIDR. Covers
the subnets and addresses API controllers only — not VLANs, VRFs, devices, section management, custom
fields, permissions, or ping/scan features. REST API. Assumes an authenticated tool for the phpIPAM API
is already available, bound to an API app whose permissions allow reading and writing subnets and
addresses.

Source: phpIPAM API documentation, https://phpipam.net/api/api_documentation/, retrieved 2026-10-19.
Facts below are restated from it; items it does not state are marked as unknown or assumed.

Each named capability below maps to a concrete operation in `endpoints.md` — bind it there, not here.

## Operational procedure

### Common Sequences

**Allocate a new subnet from an existing parent, with its first usable IP assigned:**
1. Allocate (Carve Out) the First Free Child Subnet — from the parent subnet's ID, at the requested mask.
2. Allocate the First Free Address — in the subnet ID returned by step 1.
3. Report the new subnet and the assigned address together as one outcome.

**Create a top-level subnet with no parent, then assign an address:**
1. Create a Subnet — with its network, mask and section.
2. Allocate the First Free Address (or Create an Address for a caller-chosen IP) in the new subnet.

**Just assign the next IP in an existing subnet:**
1. Allocate the First Free Address directly against the known subnet ID. Do not create or carve
   anything first.

**Check capacity before allocating:**
1. Get Subnet Usage for the subnet; proceed only if free addresses remain.

Confirm success at each step before the next — never chain calls without checking the prior one returned
a usable record.

### Find a Subnet by CIDR

Look up an existing subnet by its CIDR notation, to obtain its ID before carving from it or assigning in
it. If nothing matches, the lookup reports not found (404); treat that as "no such subnet", not a failure
of the API.

### Create a Subnet

Create a subnet from a network address, a mask, and the section it belongs to. All three are required.
Optional fields include description, VLAN, VRF, and the master (parent) subnet ID for nesting.

- Confirm success: the response is a created-object response (code 201) carrying the new record's ID.
  Record the ID.
- Unknown: the documentation does not state how overlap with an existing subnet is handled. Do not
  assume duplicates are rejected — look up the CIDR first (see Find a Subnet by CIDR) and stop if a
  subnet already exists.

### Get Subnet Usage

Read the capacity statistics for a subnet. Use them to confirm space remains before an address
allocation. The documentation describes the result only as capacity metrics; read the response rather
than assuming specific field names.

### Allocate (Carve Out) the First Free Child Subnet

Allocate the first available child subnet of the given mask inside the given parent subnet. The read
form returns the candidate; the write form creates the child subnet at that slot, taking an optional
description.

- Confirm success: the write response is a created-object response with the new subnet's ID; record the
  ID and the network from the response.
- Unknown: the documentation does not state the response when no slot of that mask is free. Treat any
  non-success response as exhaustion-or-error: report it with the response message and do not retry the
  same request.
- Assumption: the child inherits its section from the parent. The documentation does not say so
  explicitly; verify the new record's section in the response.

### Allocate the First Free Address

Allocate the first free IP address in the given subnet. The read form only reports the candidate and
reserves nothing; the write form creates the address record at that position and accepts the same
optional fields as address creation (hostname, description, and similar).

- Prefer the write form directly. Reading the candidate and then creating a specific address is two
  steps with a gap in between, where another client can take the same address.
- Confirm success: the write response is a created-object response carrying the new address record ID;
  record the assigned address and the ID.
- Unknown: the documented response for a subnet with no free address is not stated. Report any
  non-success response with its message and do not retry.

### Create an Address (caller-chosen IP)

Create an address record for a specific IP in a specific subnet. The IP and the subnet ID are required;
hostname, description, MAC, owner, tag and device are optional.

- Confirm success: created-object response with the new ID.
- If the chosen IP is already recorded in that subnet, stop and report; do not overwrite it. The
  documentation does not state the duplicate response, so look the address up first.

### Look Up an Address

Find existing address records by IP value within a subnet, by IP across subnets, or by hostname, before
creating, to avoid duplicating a record.

## Patterns

- **Free-address and free-subnet reads are computed candidates.** Only the write form of each operation
  creates a record.
- **Create responses use code 201; other successful calls use 200.** The response envelope carries the
  numeric code, a success flag, an optional message and the data. Check the envelope's success flag, not
  just the transport status.
- **Every request goes under the API app's own path segment**, and the token travels in a request
  header (see `endpoints.md`).
- **Each write call creates a new record.** Re-running with corrected input leaves the earlier record in place (inferred from the create semantics, not stated by the documentation).

## Error Handling

- **Not found (404)** on a lookup or filter with no matches: report "not found".
- **Missing required field** (network, mask or section on subnet create; IP or subnet ID on address
  create; mask on carve-out): report and stop before calling.
- **Authentication or permission failure** (4xx): report and stop; do not retry with other credentials.
- **Rate limits:** the documentation states none. On an HTTP 429 or 5xx, back off and honor any
  `Retry-After` header; do not loop.
- Any other error: report the envelope's message and stop. Do not retry automatically.

## Known limitations

- Subnets and addresses controllers only; not VLANs, VRFs, devices, section management, custom fields,
  permissions, or scanning.
- Created subnets and addresses are real and persistent, and other tooling may depend on them.
- Deleting a subnet also removes every address and child subnet inside it. Deletion is out of scope for
  this procedure; if a caller asks for it, stop and confirm explicitly with the operator before doing
  anything, since the removal cascades and cannot be undone by re-running this skill.
- Failure behavior when a pool is exhausted is not documented (see the steps above).

## Tools

| Operation | Description | Category |
|---|---|---|
| Find Subnet by CIDR | Look up a subnet record by CIDR | IPAM |
| Create Subnet | Create a subnet in a section | IPAM |
| Get Subnet Usage | Read capacity statistics for a subnet | IPAM |
| Carve Out First Free Child Subnet (read / create) | Show or create the first free child subnet of a mask | IPAM |
| First Free Address (read / create) | Show or create the first free address in a subnet | IPAM |
| Create Address | Create an address record for a chosen IP | IPAM |
| Look Up Address | Find address records by IP in a subnet or by hostname | IPAM |

## Verification checklist

- [ ] Every create response was checked for the created-object code, the success flag and a record ID,
      not just a 2xx status
- [ ] The parent subnet or target subnet was confirmed to exist (lookup by CIDR or ID) before allocating
- [ ] A subnet or address was not created when an identical one already existed
- [ ] Required fields were supplied before calling, not discovered from a rejection
- [ ] The parent/target identifier and the specific subnet or address allocated are in the final report
