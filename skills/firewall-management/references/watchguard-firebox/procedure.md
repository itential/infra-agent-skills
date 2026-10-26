# WatchGuard Firebox (WatchGuard Cloud) — Firewall Policy Management Procedure

Manages firewall policies on Fireboxes managed through **WatchGuard Cloud**, via the Firebox
Management API. Requests go to a regional WatchGuard Cloud API host, not to the appliance. Assumes
an authenticated client holding a valid access token and API key for the target account is already
available. See `endpoints.md` for literal request shapes.

Scope note: the API documents policy CRUD, an enable/disable operation, read-only access to policy
groups and to the aliases that policies reference, and a **deployment** command that pushes saved
configuration to devices. Alias create/update/delete are not in the documented endpoint set (read-only), so this skill does not manage address objects on this platform.

Sources: WatchGuard, Firebox Management API release notes and Cloud help (watchguard.com/help),
retrieved 2026-10-19. Wording is original. Items marked *(assumption)* or *(assets)* are not
confirmed from vendor pages; *(assets)* means taken from the curated spec in itential/assets.

## Operational procedure

### Identify scope before any call

Confirm the WatchGuard Cloud account ID and region, and which Fireboxes (or fleet) the policy
belongs to. A policy object is addressed by account and object id.

### Read policies and the objects they reference

List policies, or fetch one by object id. Policies point at aliases (named address groups); read
the alias list to resolve the names a policy uses rather than inventing them. Policy groups can be
read the same way.

### Create a policy

Submit the policy definition (name, action, from/to, service, and so on) for the account. The API
saves it in WatchGuard Cloud; this does not by itself change any Firebox. Field names for the
definition were not verified — follow the vendor's published schema.

### Update a policy

A full update replaces the policy by id, so send the complete intended definition. A separate
narrow operation only toggles a policy between enabled and disabled; prefer it when that is the
only change, since it cannot alter other fields.

### Delete a policy

**Stop and confirm with the operator before proceeding.** Deleting removes the traffic handling the
rule provided and shifts which later rule matches. No platform reference check was documented.

### Deploy — required before the Firebox enforces anything

Saved changes live in WatchGuard Cloud until a deployment is issued for the target devices. Release
notes describe a deployments command that pushes saved configuration (or exceptions) and, from API
v1.29.0, supports staged deployments; v1.23.0 limits a request to **50 devices**. Check the
deployment's resulting status before reporting a change as live *(status polling path not verified)*.

**Stop and confirm with the operator before deploying.** Deployment pushes to production
appliances and carries every pending saved change for those devices, not only the one just made.

## Patterns

- **Saved is not deployed.** Distinguish "stored in WatchGuard Cloud" from "deployed to the device".
- **Two credentials.** Both a bearer token and an API key header are needed on every call *(assets)*.
- **Batch limit.** Deploy in chunks of at most 50 devices.

## Known limitations

- Policy schema fields, alias writes, NAT policy modeling and deployment status polling are unverified.
- Standalone (non-Cloud-managed) Fireboxes and Fireware CLI are out of scope.
- API version drift: policy endpoints arrived in v1.27.0; confirm the target API version.

## Tools

| Operation | Description | Category |
|---|---|---|
| Policy create/read/update/delete | Manage Firebox firewall policies | Policies |
| Policy enable/disable | Toggle without editing | Policies |
| Alias / policy group read | Resolve referenced objects | Objects |
| Deployment | Push saved configuration to devices | Deploy |

## Verification checklist

- [ ] Account, region and target devices confirmed
- [ ] Referenced aliases resolved by reading, not guessed
- [ ] Delete and deploy each preceded by operator confirmation
- [ ] Deployment batch at most 50 devices; result checked
- [ ] Reported "saved" and "deployed" as separate states
