# Cisco Catalyst SD-WAN — Centralized Policy Lifecycle (Manager template policy)

Manage the lifecycle of a centralized policy on Cisco Catalyst SD-WAN Manager using its original
template-policy model: look up, create, edit, activate, deactivate, and delete a policy that
assembles existing rule definitions and applies them to site lists. Covers centralized (controller-side)
policy only.

Written against Cisco Catalyst SD-WAN Manager API release 26.2 (original configuration area) and the
17.x Catalyst SD-WAN policy configuration guidance, checked 2026-10-14. Where the vendor's
documentation does not say how the API behaves, this file says so instead of filling the gap.

Assumes an authenticated API client for the target Manager is available. The login methods are
described in `endpoints.md` for reference only.

## Scope

In scope: the centralized policy object and its states (saved, active, inactive).

Out of scope, each a separate procedure if added later:
- Creating or editing the lists (site, VPN, prefix, TLOC) and rule definitions (control, data,
  application-aware routing, topology) a policy is built from. This procedure assumes they exist and
  reads them only to check the assembly.
- Localized policy, which is attached to devices through device templates rather than activated.
- The newer configuration-group and policy-group model, which uses different objects and calls.
- Policies stored as text (policy type `cli`): see *Look up the target*.

## Common Sequences

Steps marked (gated) contain an operator confirmation.

- **Put a new policy into effect:** *Look up the target* → *Validate the assembly before saving it* →
  *Check the name and description* → *Create the policy* (stops if no reference entries shape exists) → *Check controller reachability before
  activation* → *Activate* (gated) → *Confirm the outcome of activate and deactivate*.
- **Change a policy that is already active:** *Look up the target* → *Validate the assembly before saving
  it* → *Edit an existing policy* (gated). Report SAVED_EDIT_UNCONFIRMED and let the operator decide
  whether to re-activate; the documentation does not say whether an edit alone reaches the controllers or
  what the activation flag for an edited policy means when set.
- **Take a policy out of effect and remove it:** *Look up the target* → *Deactivate* (gated) → *Confirm
  the outcome of activate and deactivate* → *Delete* (gated).

## Status vocabulary

| Status | Meaning |
|---|---|
| FOUND / NOT_FOUND | A lookup matched or did not match |
| REJECTED_INVALID_ASSEMBLY | A pre-save check failed; nothing was created or changed |
| REJECTED_OUT_OF_SCOPE | The policy or request is a text-type (`cli`) policy, which this procedure does not create, edit, or validate |
| SAVED | A create or edit returned success and the read-back matches |
| SAVED_EDIT_UNCONFIRMED | An edit to an active policy succeeded, but whether it reached the controllers is unknown (see *Edit an existing policy*) |
| ACTIVATED / DEACTIVATED | The task reached a final non-failure state and the activation flag reads true / false |
| ACTIVATION_UNCONFIRMED / DEACTIVATION_UNCONFIRMED | The call returned a task identifier, but the task's final state could not be read or the flag does not match. Say what the flag shows |
| DELETED | The delete returned success and a re-read no longer lists the policy |
| DECLINED | The operator did not confirm |
| FAILED | The platform returned an error, or the task ended in a failure state. Include status and body |

## Operations

### Look up the target

Binds to: list_policies, read_policy, read_active_policies.

- List centralized policies and find the one by name. Read the active set too.
- Success: FOUND, with the policy's identifier, its policy type, its activation flag, and its saved
  definition. NOT_FOUND blocks edit, activate, deactivate, and delete.
- The policy type is `feature` (assembled from definitions) or `cli` (stored as policy text). For `cli`
  there is no assembly to validate; report REJECTED_OUT_OF_SCOPE for create, edit, and validation. How
  activate, deactivate, and delete behave for a `cli` policy is not shown in the sources; do not run them
  on one, and tell the operator.
- In the examples, a `feature` policy's definition is an object with an assembly, and a `cli` policy's is
  plain text. Parse accordingly.

### Validate the assembly before saving it

Binds to: read_definition_or_list. A feature policy is built from one or more lists, a policy
definition, and at least one application of that definition to site lists.

Check each item from the referenced definitions and lists; on any failure report
REJECTED_INVALID_ASSEMBLY naming the offending list or site.

- Every referenced definition and site list exists (read each by identifier). Resolve names to
  identifiers first; do not guess one.
- Within one site list, one policy of each type applies. Control policies are the clear case: a second outbound one is not permitted. A control policy works in one direction only, so inbound and outbound needs
  two definitions. Data policies follow the per-direction rule below instead.
- No site belongs to two site lists that receive the same policy type. Cisco warns that the outcome is not deterministic and can be serious. For data and application-aware routing policies it adds that its CLI validate command does not detect an overlap. Expand any site
  ranges from the list read to compare them.
- Data policy, per site and per direction: one from-service plus one from-tunnel, or one for all
  directions. A policy for all directions combined with one of the others at the same site is
  unsupported, and so are two in the same direction. Cisco's guide also states the broader "one data
  policy per site" elsewhere; the per-direction statement is the more specific one and is followed here
  (the source is inconsistent here).
- At most one application-aware routing policy per site.

### Check the name and description

- The name uses letters, digits, hyphens, and underscores only, no spaces. The description is required and
  may be up to 2048 characters. These limits are stated for the management interface; whether the API
  enforces the same ones is not stated (assumption).
- A name-length limit for a top-level centralized policy is not stated. Keep it short (assumption: 32
  characters, the limit Cisco gives for most policy objects, is a safe ceiling).

### Create the policy

Binds to: create_policy, read_policy.

- Submit the name, description, and the assembly with the activation flag false.
- Documentation gap: Cisco's create example carries only each definition's identifier and type. The
  site-list and direction entries shown in list responses are not shown in any create example. Copy the
  entries shape from an existing policy read with *Look up the target* (assumption), and if none exists,
  stop and tell the operator that applying a definition to site lists through create is not documented.
  Whether a policy created without entries can later be activated is also not documented.
- Saving does not change forwarding or control behavior; only activation does.
- Success: the platform returns the new policy's identifier; read it back; report SAVED.
- Errors (bad request, forbidden, server error): report FAILED with the status and body.

### Check controller reachability before activation

Binds to: read_controller_connectivity.

- Read the connectivity status. Activation goes to the connected controllers; the guide's activation
  prompt lists the reachable ones.
- If a controller is unreachable, tell the operator before the activation confirmation. The response
  format is not documented; report it as read.

### Edit an existing policy

Binds to: read_policy, edit_policy. Only for `feature` policies.

- Read the current policy, change only what was asked, and submit the whole updated policy (assumption:
  the edit replaces the saved object).
- **If the policy is active, stop and confirm with the operator before submitting the edit.** The sources
  do not say whether an edit to an active policy is held until re-activation or applied at once, so treat it
  as a live change.
- A second documented edit variant skips lock checks to allow several component edits. Do not use it
  unless the caller explicitly needs that behavior; the lock rules are not documented.
- If the operator declines, report DECLINED and make no call.
- Success: SAVED for an inactive policy once the read-back matches; SAVED_EDIT_UNCONFIRMED for an active one.
- Errors (bad request, forbidden, server error): FAILED with the status and body.

### Activate

Binds to: activate_policy.

**Stop and confirm with the operator before activating.** Show the policy, its site lists and direction,
and the controllers that will receive it. Activation sends the policy to every connected controller and
changes live routing or traffic behavior for the matched sites and VPNs.

- The sources do not say what happens to a policy that is already active. If the active set from *Look up
  the target* is not empty, include it in the confirmation and let the operator decide.
- Submit with the edited flag set to false, as Cisco's example does. Its meaning when true is not
  documented.
- If the operator declines, report DECLINED and make no call.
- Success: the call returns a task identifier; continue with *Confirm the outcome of activate and
  deactivate*.
- Errors (bad request, forbidden, server error): FAILED with the status and body.

### Deactivate

Binds to: deactivate_policy.

**Stop and confirm with the operator before deactivating:** removing the policy from the controllers
removes whatever behavior it enforced for the matched sites.

- If the operator declines, report DECLINED and make no call.
- Success: the call returns a task identifier; continue with *Confirm the outcome of activate and
  deactivate*.
- Errors (bad request, forbidden, server error): FAILED with the status and body.

### Delete

Binds to: read_active_policies, delete_policy, list_policies.

**Stop and confirm with the operator before deleting.** The sources do not describe a way to restore a
deleted policy (assumption: none), so treat it as permanent.

- The policy must not be active. The sources do not say what delete does to an active policy; deactivate
  it first.
- If the operator declines, report DECLINED and make no call.
- Success: DELETED when the delete returns success with no body and the policy no longer appears in the list.
- Errors (bad request, forbidden, server error): FAILED with the status and body.

### Confirm the outcome of activate and deactivate

Binds to: poll_task, list_policies.

The returned task identifier only means the request was accepted.

- Poll the task until it reports a final state (poll_task is an unverified binding; see `endpoints.md`).
  Polling is only meaningful for the first 30 minutes after submission: Cisco documents no tracking beyond that, even for a large policy. Stop polling at 30 minutes and report the matching UNCONFIRMED status if no final state was seen.
- The literal success value of the task state is not documented. Read the final state as returned and rely
  on the re-read below as the authoritative check.
- Re-read the policy list and check the policy's activation flag: true after activation, false after
  deactivation. The active-set read can be used as a second check; its response format is not
  documented.
- When the flag flips is not documented (at acceptance or when deployment finishes), so the flag alone
  does not prove completion.
- Report ACTIVATED or DEACTIVATED only when the task has reached a final state that is not a failure and
  the flag matches. If poll_task cannot be bound or the task never reports a final state, report
  ACTIVATION_UNCONFIRMED or DEACTIVATION_UNCONFIRMED with the task identifier and the flag value, and let
  the operator decide. Report FAILED if the task ended in a failure state.

## Patterns

- **Saved is not active.** A policy can be created and edited without effect on the network, so always
  report which state it is in.
- **Control policy direction is relative to the controller.** An outbound control policy applies to what
  the controller sends to the sites, not to what a site sends.
- **Shared definitions (assumption, not stated by the sources).** Policies are assembled from definition
  identifiers, so one definition may be referenced by more than one policy; where a platform allows that,
  check where a definition is used before changing it.
- **Multiple tenants.** The active-policy read spans all tenants, and API access in a multitenant
  deployment is limited to provider-level and tenant-level views. Do not treat the full set as one
  tenant's.
- **Authentication expiry.** Sessions and access tokens expire (limits are in `endpoints.md`), so a long
  procedure can outlive its login. A rejected call after a long gap may be an expired login.

## Known limitations

- Covers centralized `feature` policy only; text policies, localized policy, list and definition authoring, and the configuration-group model are not covered.
- Not documented in the sources used: whether an edit of a `feature` policy is sent as an assembly or as policy text (read the policy first and send the form it uses; stop and report if unclear), the task-status call and its success value, how a create applies a definition to site lists, the effect of editing or deleting an active policy, and the lock rules for plain edits.
- **Activation changes live behavior until deactivated,** and a deleted policy is treated as permanent.

## Tools

| Operation | Description | Category |
|---|---|---|
| list_policies | List centralized policies with type, flag, and saved definition | Read |
| read_policy | Read one policy's definition by identifier | Read |
| read_active_policies | List identifiers of active policies | Read |
| read_controller_connectivity | Read controller connectivity status | Read |
| read_definition_or_list | Read a referenced rule definition or list | Read |
| create_policy | Save a new, not-activated policy | Write |
| edit_policy | Replace a saved policy | Write (gated if active) |
| activate_policy | Push a policy to the controllers | Write (gated) |
| deactivate_policy | Remove a policy from the controllers | Write (gated) |
| delete_policy | Remove a saved policy | Write (gated) |
| poll_task | Read the final state of an activation task (unverified binding) | Read |

## Verification checklist

- [ ] Every referenced definition and site list was read and exists
- [ ] No same-type policy overlap on any site list or site, and the per-direction data policy rule holds
- [ ] Name uses only allowed characters and the description is present
- [ ] The create step did not invent a site-list entries shape
- [ ] Controller connectivity was read before activation
- [ ] The operator confirmed before every activate, deactivate, delete, and edit of an active policy
- [ ] The activation flag was re-read after activate or deactivate, and the result reported with the
      matching status
