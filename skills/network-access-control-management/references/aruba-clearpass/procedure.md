# Aruba ClearPass Policy Manager — Endpoint Repository Procedure

Reads, registers, updates, blocks/allows, and deletes records in ClearPass Policy Manager's endpoint
repository through its REST API. Assumes an authenticated client already holding a valid OAuth2
bearer token; obtaining the token is out of scope (see Known limitations).

Sources: HPE Aruba Networking Developer Hub, ClearPass Policy Manager API reference — the token
endpoint and the endpoint list/create/get/update/replace/delete operation pages
(developer.arubanetworks.com/cppm/reference/...), retrieved 2026-10-19. The meaning of the three
endpoint statuses comes from a search-result summary of the ClearPass Policy Manager administration
guide (the guide page itself returned HTTP 403); it is marked below where used.

## Common Sequences

- **Look up an endpoint:** Read endpoint by MAC address (with profile details if needed).
- **Register an endpoint:** Read endpoint by MAC address (confirm absent) → Create endpoint.
- **Block or release an endpoint:** Read endpoint by MAC address → (operator confirmation) → Update
  endpoint status → Read endpoint by MAC address to confirm.
- **Remove an endpoint:** Read endpoint by MAC address → (operator confirmation) → Delete endpoint.

## Operational procedure

### 1. Confirm access

Every call needs an OAuth2 bearer token issued to an API client defined on the ClearPass server.
A token request names a grant type; the documented ones are client credentials, password, and
refresh token. A missing, expired, or under-privileged token is returned as unauthorized or
forbidden; stop and let the caller obtain a valid token. This skill does not manage that lifecycle.

### 2. Read endpoint(s)

- **By MAC address:** read the single record. Two flags, both documented as required and defaulting
  to false, add the profiling block (addresses, hostname, device category, OS family, device name,
  profiling timestamps) and the network-access-device block (NAD address and port). Request them only
  when needed.
- **List:** supports a JSON filter expression, a sort order (default by ascending id), a zero-based
  offset, a limit (default 25, maximum 1000), and an optional total count. Page with offset and limit
  rather than assuming one response holds everything.
- Success is a 200 with the endpoint record(s): numeric id, MAC address, description, status,
  randomized-MAC flag, tags, free-form attributes, and added/updated timestamps. A 404 on a
  by-MAC read means no such endpoint exists, which is not the same as an endpoint with empty fields.

### 3. Register (create) an endpoint

- Required: the MAC address and a status. Optional: description, randomized-MAC flag, device
  insight tags, and a free-form key/value attributes object.
- Success is a 201 with the created record. A 422 means a submitted value was rejected (for example an
  invalid status or malformed MAC); correct it and resubmit rather than retrying unchanged.
- Whether creating a MAC that already exists is rejected or merged is not stated in the pages read —
  consult platform-specific guidance, and read first (see Common Sequences) to avoid depending on it.

### 4. Update an endpoint, including block and release

- Use a partial update by MAC address (or by numeric id). Updatable fields: description, status, tags,
  attributes, the randomized-MAC flag, and, by MAC address, three profile fields only — device
  category, OS family, and device name. Success is 200 (updated record) or 204; 304 means nothing
  changed; 404 means no such endpoint; 422 means an invalid value.
- A full replace by MAC address exists but requires the MAC, a status, and a profile object with all
  three profile fields. Prefer the partial update; a full replace is a bigger overwrite.
- **Status values are Known, Unknown, and Disabled.** Per the administration guide summary
  (secondary; unverified against the guide page itself), Disabled is the status used to block an
  endpoint's network access and Known is the status used to allow it, and role-mapping policy decides
  what each status means in practice. On that unverified basis, blocking would be done by setting
  Disabled and releasing by setting Known (or Unknown, to return it to unclassified); confirm what
  each status does under the site's own policies before relying on it.
- **Before changing status on a live endpoint, stop and confirm with the operator** — a status change
  can cut off a connected device and the effect depends on how the site's policies use the status.
  Whether an already-connected session is terminated immediately is not stated in the pages read;
  consult platform-specific guidance.
- The same summary says Disabled endpoints are not removed by the repository's automatic cleanup and
  must be moved back to Unknown or deleted by hand (secondary; unverified).

### 5. Delete an endpoint

- **Stop and confirm with the operator before deleting.** The source flags deletion as permanent.
- Delete by MAC address (or numeric id). Success is 204 with no body; 404 means no such endpoint.
- Deleting removes the record and its profiling data; the endpoint can be re-learned later only
  through normal profiling or re-registration. Blocking (status Disabled) is the reversible
  alternative when the goal is only to deny access.

## Patterns

- Identify endpoints by MAC address for human-facing work; the numeric id is assigned by the server
  and differs per server.
- Read before every write, and read again after a status change to confirm the stored value.
- Profile fields written by a client are limited to three; everything else in the profile block is
  produced by profiling and is read-only here.

## Known limitations

- Covers the endpoint repository only. Not covered: endpoint group or profile assignment, live session
  state, enforcement or role-mapping policy authoring, guest or onboarding workflows, token issuance.
- The pages read do not document rate limits; back off on a 429 and honor any `Retry-After` header
  (general safe handling, not a documented ClearPass figure).
- Quarantine and release are expressed here as status changes; ClearPass pages read describe no
  separate quarantine operation.
- Unverified against a live server; see the assumptions marked above.

## Tools

| Operation | Description | Category |
|---|---|---|
| Read endpoint | Fetch one endpoint by MAC address or id | Read |
| List endpoints | Filtered, paged listing | Read |
| Create endpoint | Register a new endpoint | Write |
| Update endpoint | Partial update including status | Write |
| Replace endpoint | Full replace by MAC address | Write |
| Delete endpoint | Permanent removal | Destructive |

## Verification checklist

- [ ] A bearer token was in hand and the server accepted it (no 401/403)
- [ ] Endpoint read first; existence matched expectation (404 only when creating)
- [ ] Operator confirmed any status change on a live endpoint and any delete
- [ ] Create returned 201; update returned 200/204; delete returned 204
- [ ] A follow-up read shows the intended status or the endpoint absent
