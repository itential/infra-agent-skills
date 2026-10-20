# GoDaddy — DNS Record Procedure (Domains API v1)

Add, replace, read, or delete DNS records for a domain whose DNS is hosted at GoDaddy, using the Domains
API v1 record operations. Assumes an authenticated client holding a bearer token with write access to DNS
(the vendor's troubleshooting page names the `domains.dns:update` scope for writes and
`domains.domain:read` for reads) is already available. Does not cover nameserver changes, domain
registration, forwarding, or the replace-everything call.

Sources (retrieved 2026-10-19), GoDaddy Developer documentation: Domains v1 REST reference pages "Manage
DNS", "Replace DNS records by type", "Replace DNS records by type and name", "Delete DNS records by type and
name", "Add DNS records", and the "Troubleshoot DNS" guide. Items marked (unverified) are not stated on the
v1 reference pages themselves. The "Get records" page could not be fetched; that operation is described
without a confirmed vendor page and is marked (unverified).

## Model

Records are addressed by **type and name**, never by an individual record ID in v1. Every write other than
add acts on the whole group of records sharing type and name (or on a whole type), so changing one value in
a multi-value group means sending the complete desired group.

| Goal | Operation | Effect |
|---|---|---|
| Append records | Add | Adds the submitted records; existing ones stay |
| Set a type+name group | Replace by type and name | Replaces only that group; all other records stay |
| Set a type across names | Replace by type | Replaces every record of that type at all names; other types stay |
| Remove a group | Delete by type and name | Removes every record of that type and name; others stay |

## Common Sequences

- **Add a record:** confirm the domain (step 1) → read existing records (step 2) → validate and check
  CNAME exclusivity (steps 3-4) → add (step 5) → verify (step 7).
- **Change a record group:** read the group (step 2) → build the full desired group (step 3) → operator
  confirmation and replace by type and name (step 5) → verify (step 7).
- **Remove a record group:** read the group (step 2) → operator confirmation and delete by type and name
  (step 5) → verify (step 7).

## Operational procedure

1. **Confirm the domain** — it must be owned by the account (or by a managed shopper for resellers, see
   `endpoints.md`). A 404 means the domain was not found or is not owned; stop and report FAILED. A 409 on
   delete means the domain is ineligible for record changes.
2. **Read existing records** for the type and name where possible, to detect duplicates and conflicts and to
   assemble the full replacement group. The read response format is (unverified).
3. **Validate** — the vendor's troubleshooting guide reports these rules (v1 applicability not stated, so
   treat as assumptions): TTL below 600 seconds is rejected with 400; a CNAME at the zone apex is rejected
   with 422; SRV records need underscore-prefixed service and protocol fields; invalid data for the type
   (a hostname in an A record) is rejected with 400. NS and SOA records cannot be changed or deleted through
   the record operations; nameserver changes go through a separate nameserver call, which is out of scope.
4. **Check CNAME exclusivity** — a CNAME cannot coexist with other types at the same name (RFC 1035
   §3.6.2); on a conflict stop and report REJECTED_STRUCTURAL_CONFLICT.
5. **Apply the change**
   - Add: success is 204 No Content. Repeating an add is not idempotent: the vendor guidance says identical
     type, name and data are rejected as duplicates, while differing data is appended. (The duplicate
     rejection comes from the troubleshooting guide and is unverified for v1.)
   - Replace by type and name: **stop and confirm with the operator** that the submitted array is the full
     desired group, since existing members not in it are deleted. Success is 200 or 204 (the reference
     page's introduction says 204 while its responses list 200; accept either as success).
   - Replace by type: **stop and confirm with the operator before proceeding** — it rewrites that type at
     every name in the domain.
   - Delete by type and name: **stop and confirm with the operator before proceeding** — it removes all
     matching records and the vendor states deletes are irreversible. Success is 204.
6. **Handle errors** — 400 malformed request or invalid values; 401 invalid or missing authentication;
   403 token lacks the needed scope or access; 404 domain (or record group) not found; 422 invalid domain
   name or schema violation; 429 rate limit exceeded, so back off and honor a `Retry-After` header (limits
   themselves are not stated, unverified); 500 and 504 server or gateway failure, so re-read the group
   before retrying a write.
7. **Verify** — read the records back and compare with the intended state. GoDaddy's authoritative servers
   apply changes within minutes per the troubleshooting guide; resolvers elsewhere may serve the old value
   until the prior TTL expires.

## Patterns

- **Replace-by-type is far wider than it looks.** It touches every name in the domain for that type.
- **Add is not an upsert.** To change an existing value, use replace by type and name or delete then add.
- **After a failed or ambiguous write, re-read** rather than blindly retrying, because the vendor gives no
  undo.

## Known limitations

- Replace-everything and nameserver changes are out of scope.
- Delete is irreversible; there is no documented restore.
- Reseller use needs the shopper header; see `endpoints.md`.
- Field-level constraints for records (priority, port, weight limits) are not stated on the pages read.

## Tools

| Operation | Description | Category |
|---|---|---|
| Get records | Read records by type and name | DNS Records |
| Add records | Append records to the domain | DNS Records |
| Replace records by type and name | Replace one type+name group | DNS Records |
| Replace records by type | Replace a whole type across names | DNS Records |
| Delete records by type and name | Remove one type+name group | DNS Records |

## Verification checklist

- [ ] Domain ownership confirmed before any write
- [ ] NS/SOA changes not attempted through record calls
- [ ] Replace body carried the complete desired group; replace and delete confirmed with the operator
- [ ] Apex CNAME and TTL rules checked (assumptions flagged above)
- [ ] Records read back and matched the intended state
