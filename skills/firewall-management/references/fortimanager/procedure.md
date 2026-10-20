# Fortinet FortiManager — Firewall Policy Management Procedure

Manages firewall address objects and policies for FortiGate devices **through FortiManager**, the
central management platform, rather than on a FortiGate directly (for direct device CLI see the
`fortios` reference). Assumes an authenticated client for FortiManager's JSON-RPC API with an
administrator account (API user token) holding rights on the target ADOM is already available.
See `endpoints.md` for literal request shapes.

Scope note: FortiManager keeps its own database of objects and **policy packages**, grouped in
**ADOMs** (administrative domains). A change written there changes FortiManager's database only;
managed FortiGates enforce it after the policy package is **installed** to them.

Sources: Fortinet, FortiManager API Best Practices 7.6/8.0 ("Getting started", "Best Practices"),
the 7.6 new-features note on install preview, the 7.4 note on JSON-API partial install, and the
Administration Guide ("Install a policy package"), docs.fortinet.com, retrieved 2026-10-19. Wording
is original. Items marked *(assumption)* are not confirmed from vendor pages.

## Operational procedure

### Session and lock handling

Authenticate with a session login or an API-user token (see `endpoints.md`). Session logins must be
closed when done: vendor says leaked sessions exhaust admin session limits. If the ADOM runs in
**workspace mode**, lock the ADOM once, make all changes, commit once, then unlock; vendor says each
commit copies the database, so repeated lock-edit-commit cycles are costly. Do not log out while an
install or other async task is running, or it may be reported failed.

### Identify scope before any call

Confirm the ADOM and, for rules, the policy package name. The same object or package name can
exist in different ADOMs. Confirm which managed devices a package is assigned to before any install.

### Create / read / update / delete an address object

Address objects live per ADOM. Create supplies name and the address type/value; read fetches one or
lists the ADOM's addresses; update resubmits changed fields at the same name; delete removes by name.
Whether update merges or replaces unspecified fields was not confirmed — *(assumption)* send the
full intended object.

**Delete: stop and confirm with the operator.** No platform reference check on delete was confirmed
for FortiManager; read the policies in the ADOM's packages first and check nothing uses the object.

### Create / read / update / delete a firewall policy rule

Rules live inside a named policy package in an ADOM. Create supplies the rule's source/destination
interfaces, addresses, services, action and any profile settings; read lists a package's rules;
update targets an existing rule by its policy ID; delete removes by policy ID. Rule position matters in general; *(assumption: FortiManager treats
moving a rule as a separate operation from editing it — confirm in the FNDN JSON API reference)*.

**Delete: stop and confirm with the operator**; removing a rule changes which later rule matches.

### Install the policy package — required before anything is enforced

Every write above changes only FortiManager's database. To apply it, run an install of the policy
package to the target devices. The vendor documents an install-preview step that shows what would
change, and says installing also pushes the objects the package references, creating or updating
them on the device. Install returns a task id; poll the task monitor to completion without tight
loops, and check each target device's result before reporting the change applied.

Newer releases (7.4.1+, per vendor) also offer a **partial install** that pushes only the specific
instructed items rather than all pending changes for the device. Prefer it when other unrelated
pending changes exist; otherwise a full install sends everything pending.

**Stop and confirm with the operator before installing.** An install is a live push to production
FortiGates, and a full install carries every
pending change in the package, not only the one just made. Preview first.

## Patterns

- **Database write is not enforcement.** Report "saved in FortiManager" and "installed and live" as
  separate states.
- **ADOM and package are part of identity.** Carry both from read through update/delete/install.
- **Everything runs through one RPC channel.** The verb (get/add/set/update/delete/exec) and a
  resource path select the operation; every vendor example response carries a per-call status block
  with a code and message, so check it on every call rather than trusting the HTTP status.
- **Batch, then commit once** in workspace mode; keep session count low and log out.

## Known limitations

- Rule/address field names, policy-package assignment, task response fields, the exact lock verb and
  per-object locking were not verified; check the target version's JSON API reference.
- Per-device settings (interface mappings, dynamic mappings) are out of scope.
- NAT: policy-level NAT and virtual-IP objects exist on FortiGate-managed devices, but their
  FortiManager paths were not verified. Treat NAT as unconfirmed.
- Vendor documents both session login and bearer API-user tokens; the 7.2.2+ floor for tokens comes
  from the assets README (secondary source); older releases use session login.

## Tools

| Operation | Description | Category |
|---|---|---|
| Address object CRUD | Manage addresses in an ADOM | Objects |
| Policy rule CRUD | Manage rules inside a policy package | Policies |
| Install policy package / partial install | Push to managed devices; returns a pollable task | Install |

## Verification checklist

- [ ] ADOM and policy package confirmed before any call
- [ ] Delete of any object or rule preceded by a reference check and operator confirmation
- [ ] Install preview reviewed and operator confirmed before installing
- [ ] Install task polled to completion and each target device's result checked
- [ ] "Saved" and "installed" reported as distinct states
