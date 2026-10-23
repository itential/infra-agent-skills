# Cloudflare One CASB — Finding-Triggered Remediation Policy Management

Create, read, update, disable, and delete the policies that make Cloudflare CASB act automatically
on newly detected posture finding instances: fix the asset, notify a webhook destination, or both.
Source: Cloudflare Docs "Remediation Policies", "Manage findings", "Webhooks", and the CASB API
reference for policies, finding types, remediation types, and integrations (retrieved 2026-10-22).

Scope: API-driven, finding-triggered policies only. These react to findings; they are not per-app
allow/block/require-MFA rules or standalone DLP rules. Dashboard steps are not covered; bind each
operation through `endpoints.md`.

## Common Sequences

1. **Create an auto-remediation policy:** list integrations (only if scoping to specific ones) →
   list finding types → list remediation types for that finding type → (optional) look up the
   webhook ID → create the policy → read it back.
2. **Pause or change a policy:** read the policy → update it with the full desired state.
3. **Retire a policy:** read the policy → delete it after operator confirmation.

## Prerequisites

- Paid Cloudflare CASB plan. Policies are not available on free CASB integrations.
- An existing integration for the target cloud or SaaS vendor.
- For a remediation action: the integration is in read-write mode. A read-only integration cannot
  remediate until it is upgraded.
- For a webhook action: a webhook destination already exists and its ID is known.
- An API token with the Zero Trust Write permission for create, update, and delete. The permission
  needed for the read calls is not documented — treat it as unknown.

## Resolve the IDs a policy references

Finding type, remediation type, webhook, and integration are all referenced by ID.

- List finding types, optionally filtered by vendor. A finding type is valid only if the platform
  offers it for the chosen vendor and integrations. The response is paginated.
- List remediation types for the chosen finding type. Few finding types have any (see Known
  limitations). An empty result means the policy can only send webhooks.
- Webhook IDs come from the existing webhook configuration. Creating or editing the webhook
  destination is outside this procedure.
- Integration IDs are needed only when the policy is not applied to all integrations. List
  integrations, optionally filtered by vendor.

Success: each ID needed is in hand. If a finding type is absent for the vendor, stop — the platform
cannot build a policy for it.

## Create a policy

1. Decide the trigger (one finding type, applied to every integration of the vendor or to a named
   set) and the actions. A policy must carry one or more actions: a single remediation type at
   most, with any number of webhooks.
2. **If the policy includes a remediation action, stop and confirm with the operator before
   proceeding.** Matching findings will be changed on the live SaaS tenant automatically (for
   example, public sharing removed from files), with no per-instance review.
3. Create the policy with the name, optional description, enabled flag, scope flag, finding type
   ID, and actions. When the scope flag is false, supply the integration ID list. Supply at least one ID: an empty list is rejected by the Terraform resource and the API's behavior
   is not documented.
4. Read the policy back.

Failure messages for inherited permissions or an unsupported finding type are listed under "Error
strings worth recognizing" in `endpoints.md`.

Success: the create call returns the stored policy with an ID, the expected finding type, and the
actions as submitted; the read-back shows the policy enabled when requested.

Errors: failures for a free-plan integration or an unknown ID are not documented — report the
response body rather than guessing a cause.

## Read policies

List all policies in the account (paginated), or fetch one by ID. A fetched policy shows its actions
by display name and ID, its scope, and a timestamp of the last successful invocation, which is
absent if it has never fired. That timestamp appears only on reads, not on create or update
responses.

## Update or disable a policy

1. Read the current policy so nothing is dropped.
2. An update overwrites the stored policy instead of merging into it. Send the name, enabled flag,
   scope flag, and every action that should remain; any action left out is dropped. Whether an omitted description is
   kept or cleared is undocumented, so resend the one read in step 1 (assumption). Include the integration ID list when the
   scope flag is false (assumption: replacement semantics apply to the list as well; the other
   fields are documented as required).
3. **If the change adds a remediation action, turns a remediation policy on, widens the scope of an
   enabled remediation policy, or drops an existing action, stop and confirm with the operator
   before proceeding.** Do the same when it adds a webhook, since finding data will go to that
   destination.
4. To pause the policy, set enabled to false. A disabled policy takes no action on new findings until it is
   re-enabled.
5. Read the policy back.

The finding type cannot be changed. For a different one, create a replacement policy and delete the old.

Success: the read-back reflects the new state.

## Delete a policy

1. Read the policy and show the operator its name, finding type, and actions.
2. **Stop and confirm with the operator before proceeding.** Deletion stops all automated handling
   for that trigger; no undo is documented.
3. Delete by ID, then confirm a subsequent read no longer returns it.

Prefer disabling (above) when the intent is temporary.

## Patterns

- **Not retroactive.** A new or edited policy acts only on finding instances detected afterward.
  Existing open instances stay untouched; they must be remediated manually or by a webhook send.
- **Replace semantics on update** are the main way an action is lost silently. Always read first.
- **Disable before delete** is the lower-risk way to stop a policy from firing.
- **Inherited permissions are not fixed by a policy.** Remediation only strips access granted on the
  file or folder itself. If the access comes down from a containing folder or shared drive, the
  remediation of the child fails and the container's own permission has to be changed separately.
  Cloudflare never edits the container on its own, and editing it alters access for everything
  beneath it. For Microsoft 365 the
  platform may surface a separate instance for the parent; for Google Workspace it does not identify
  the originating parent.
- Failure messages for inherited permissions and for finding types with no remediation are listed
  under "Error strings worth recognizing" in `endpoints.md`.
- **A webhook action sends the same payload as a manual send**, and delivery is queued in the
  background; acceptance is not proof the destination processed it.

## Known limitations

- Remediation actions exist only for Microsoft 365 and Google Workspace file and folder finding
  types. Every other finding type supports webhook actions only.
- Applies to posture finding instances only; webhooks do not cover content (DLP) findings.
- Policies are not retroactive.
- The finding type is immutable after creation.
- Not documented: rate limits and quotas, maximum policies per account,
  maximum webhooks per policy, the read-permission name, and the exact error codes for invalid
  requests. On HTTP 429, back off and honor any `Retry-After` header.
- The policy object carries no per-instance results: outcomes are tracked in the dashboard and
  logs (see Verification checklist).

## Tools

| Operation | Description | Category |
|---|---|---|
| List integrations | Find integration IDs, filterable by vendor | Read |
| List finding types | Find the trigger ID, filterable by vendor | Read |
| List remediation types | Find remediation IDs for one finding type | Read |
| List policies | Enumerate policies in the account | Read |
| Get policy | Fetch one policy with its actions | Read |
| Create policy | Define trigger, scope, and actions | Write |
| Update policy | Replace a policy's definition, including enable/disable | Write |
| Delete policy | Remove a policy permanently | Write (destructive) |

## Verification checklist

- [ ] Plan, integration mode, and webhook prerequisites confirmed before creating
- [ ] Operator confirmed any remediation action before create/enable, and any delete
- [ ] Read-back shows the intended name, finding type, scope, enabled state, and actions
- [ ] After an update, no previously held action went missing
- [ ] Runtime outcomes checked in Cloudflare One Insights logs: Admin Activity logs record who
      changed a policy; the Cloud & SaaS Security policies log holds one record per policy invocation
      with the affected asset and outcome
- [ ] Per-instance remediation status reviewed where relevant: Pending, Processing, Validating,
      Completed, Failed, Rejected. Final validation may take as long as 48 hours; Failed or Rejected means the
      fix did not happen (Rejected indicates insufficient integration permissions)
