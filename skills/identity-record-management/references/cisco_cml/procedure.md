# Cisco CML users and groups

Manage explicitly selected CML user/group records with Cisco’s client.

## Common Sequences

- Create: **Resolve record** → **Create** → **Read result**.
- Update/membership: **Resolve record** → **Update** → **Read result**.
- Remove: **Resolve record** → **Delete**.

### Resolve record

The user/group catalogue supplies the selected record's identifier. Exact record retrieval returns its current object. Names do not substitute for IDs without successful resolution. Authentication, permission, missing-record or other HTTP failures remain native failures; the publisher client does not define a universal retry or error envelope for these calls.

### Create

Account/group creation can grant access: stop and confirm with the operator before proceeding. A user requires a supplied username and securely supplied password; group creation requires a name. Only the requested fields and member/group identifiers are included. The returned object is the creation result. A timeout leaves creation uncertain; record lookup establishes state before any repeat.

### Update

Before changing account properties, privileges, group membership or group properties: stop and confirm with the operator before proceeding. The selected record receives the requested supported fields and returns its updated object. An explicit membership list represents the requested list; no append semantics are assumed. Password-change internals and lab associations are outside this reference.

### Read result

The returned identifier resolves to the updated/created record, whose requested non-secret properties are inspected. Success does not require displaying or distributing a password. Missing/mismatched data leaves the operation unverified.

### Delete

Removing a user/group affects access: stop and confirm with the operator before proceeding. Cisco’s client returns no value on successful deletion; a later catalogue read distinguishes the absent record. A failed/uncertain request is not automatically replayed. Any impact on owned labs or external identity providers is unverified here and requires platform-specific guidance before deletion.

## Patterns

Optional fields are omitted when unspecified; empty membership lists are explicit values. Privilege selection is supplied by the operator, never inferred from a job title.

## Known limitations

Password rotation, lab associations, identity-provider provisioning and resource-pool changes are excluded. Deletion side effects beyond the identity record are not specified by the cited SDK and must be resolved before use.

## Tools

Assumes the authenticated client described in [the bindings](endpoints.md).

| Operation | Description | Category |
|---|---|---|
| Read users/groups | Resolve identity records and membership | Identity read |
| Create/update | Apply approved identity attributes or membership | Access change |
| Delete | Remove the selected identity record | Destructive |

## Verification checklist

- Exact record identity and requested fields are confirmed.
- Every access-affecting operation includes its gate.
- Resulting non-secret properties match.
- Uncertain writes are inspected before retry.
- Passwords are not disclosed.

## Sources

- [Cisco user SDK](https://github.com/CiscoDevNet/virl2-client/blob/7ac2c924ccbdc02264578a95327f8a1363172076/virl2_client/models/user.py). Retrieved 2026-10-09.
- [Cisco group SDK](https://github.com/CiscoDevNet/virl2-client/blob/7ac2c924ccbdc02264578a95327f8a1363172076/virl2_client/models/group.py). Retrieved 2026-10-09.
- [Cisco client initialization](https://github.com/CiscoDevNet/virl2-client/blob/7ac2c924ccbdc02264578a95327f8a1363172076/virl2_client/virl2_client.py). Retrieved 2026-10-09.
