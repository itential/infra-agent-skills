# Cloudflare One Access — Reusable Access Policy Procedure

List, create, update, delete, and convert reusable Access policies: the account-level policies that
decide who may reach a self-hosted, SaaS, or non-HTTP application protected by Cloudflare Access.
Source: Cloudflare Docs "Access policies", "Manage Access policies", "Rule groups", "Enforce MFA",
"Temporary authentication", "Require purpose justification", "Isolate self-hosted application",
"External Evaluation rules", "Common policies", and the Access reusable policies API reference
(retrieved 2026-10-26).

A reusable policy is a standalone object holding an action, match rules, and optional session
settings, and it is shared by every application that uses it. Applications, rule groups, identity
providers, lists, service tokens, device posture checks, and the step of attaching a policy to an
application (including the policy's position in that application's list) are separate objects and
are not covered. Bind each operation through `endpoints.md`.

## Common Sequences

1. **Add a policy:** list policies → choose action, rules, and settings → confirm with the operator
   → create → read back. The policy has no effect until an application uses it.
2. **Change a policy:** get the policy → confirm with the operator → update with the full desired
   policy → read back.
3. **Retire a policy:** get the policy and check how many applications use it → confirm with the
   operator → remove it from those applications → delete → confirm it no longer appears in the list.
4. **Convert a legacy policy:** confirm with the operator → convert the application-scoped policy →
   get the result as a reusable policy.

## Step 0: Choose the action, rules, and settings

A policy has exactly one action.

| Action | Effect on a matching user or request | Notes |
|---|---|---|
| Allow | Grants access | Infrastructure applications accept only Allow policies. |
| Block | Denies access | Used to carve exceptions out of Allow policies. |
| Bypass | Turns off Access enforcement for the traffic | No Access security controls apply and requests are not logged. Identity-based selectors are not available. |
| Service Auth | Authenticates without an identity provider login | For service tokens and client certificates. |

- Every policy needs at least one Include rule. Include rules combine as OR: one match is enough.
  Require rules combine as AND: every one must match. Exclude rules combine as NOT: matching any one
  removes the user.
- Several values inside one Require rule are ANDed, so two countries in one Require rule match
  nobody. To express OR inside a Require rule, put the alternatives in a rule group (an Include
  rule inside the group) and require the group.
- The Service Token, Any Access Service Token, and Linked App Token selectors need the Service Auth
  action; Linked App Token works only with Service Auth and Bypass.
- Selectors that name an identity provider (Okta, Azure, GitHub, Google Workspace, SAML, OIDC, or
  Cloudflare account membership) work only when that provider is configured. User Risk Score
  appears only on Enterprise plans. Device posture, Warp, and Gateway selectors appear only after
  the matching posture check exists.
- Referenced groups, lists, identity providers, service tokens, email lists, and posture
  integrations must already exist; their IDs come from their own services.
- An External Evaluation rule sends the authenticated user's identity to the evaluate URL named in
  the rule and trusts the signed answer from the keys URL. Use only endpoints the operator supplied.
- Optional settings on a policy: session duration; purpose justification, with a custom prompt;
  temporary authentication (the user requests approval at the start of every session, using
  approver email addresses or an approver email list, with a stated number of approvals); serving
  the application through an isolated browser (requires Browser Isolation and the account's client web
  isolation setting); independent MFA (see Patterns); and connection context for infrastructure and
  browser RDP applications.

Success: the action, every rule, and every setting are fixed, and the combination is valid for the
action.

## Step 1: List and read policies

List policies, or get one by ID. Note each policy's name, action, rules, session duration, and the
count of applications using it. Legacy policies are scoped to one application and are listed under
that application, not here.

Success: the policy set is in hand, with no policy of the same name that would make a new policy a
duplicate.

## Step 2: Create a policy

1. **Stop and confirm with the operator before proceeding.** Say plainly who the policy will let in,
   keep out, or exempt once an application uses it. State separately whether it is a Bypass policy
   (Access enforcement and logging are off for matching traffic) or an Allow policy whose Include
   rules could match everyone (see Patterns).
2. Create the policy with its name, action, Include rules, optional Require and Exclude rules, and
   any optional settings.
3. Read the policy back.

Success: the response returns a policy ID, the stored rules match what was sent, and the
application count is zero. A policy with no application attached enforces nothing.

## Step 3: Update a policy

1. Get the policy first so nothing is dropped.
2. **Stop and confirm with the operator before proceeding.** An update takes effect on every
   application that uses the policy. Adding Include rules, removing Require or Exclude rules, or
   changing the action to Allow or Bypass grants more access; the reverse locks users out.
3. Send the update with the full desired policy (assumption: the update replaces the stored policy,
   because the call requires the action, Include rules, and name; merge behavior is not stated).
4. Read the policy back.

Success: the read-back shows the intended rules, action, and settings, and the application count is
unchanged.

## Step 4: Delete a policy

1. Get the policy and show the operator its name, action, rules, and application count.
2. **Stop and confirm with the operator before proceeding.** Access denies by default, so removing
   the only Allow policy from an application locks its users out, and removing a Block policy
   reopens whatever it blocked. No undo is documented; recreating the policy gives it a new ID.
3. The dashboard procedure removes the policy from every application that uses it before deleting
   it; the API's behavior for a policy still in use is not documented. Detaching
   is an application operation with no binding here: if none is available, stop and report the
   applications that still use the policy.
4. Delete by ID, then confirm the policy is gone from the list.

Success: the policy no longer appears in the list.

## Step 5: Convert a legacy policy to reusable

A legacy policy belongs to one application and cannot be added to new applications.

1. **Stop and confirm with the operator before proceeding.** The policy leaves the application's own
   policy list and is thereafter managed as a reusable policy.
2. Convert it by sending the conversion call for that application and policy with an empty body.
3. Get the policy as a reusable policy.

Success: the policy no longer appears under the application's policies and is returned as reusable.
Removing a legacy policy from its application deletes it permanently, so create the reusable
replacement first. Duplicate legacy policies can be replaced by one reusable policy this way.

## Patterns

- **Order belongs to the application.** Within one application there are two tiers: Bypass and
  Service Auth policies, then Block and Allow policies, each tier in listed order. A match on Allow
  or Block ends evaluation.
  The policy model lists an optional precedence value (documented as unique per policy) that the
  create and update calls do not accept; treat position as set on the application.
- **Deny by default.** A user who matches no Allow policy is denied, so a Block policy only matters
  alongside an Allow it carves exceptions from.
- **One edit, many applications.** A shared policy change reaches every application that uses it.
  Check the application count before updating or deleting.
- **Open-to-anyone mistakes.** An Allow policy that includes Everyone, or the one-time PIN login
  method, admits anyone who can complete the login.
- **Bypass limits.** Bypass skips logging and falls back to the zone's own settings, including
  Always Use HTTPS. A Bypass policy with device posture rules stops working when Zaraz is enabled on
  the zone or a Worker intercepts the request; use Service Auth there instead. Test Bypass policies
  before production.
- **Check timing differs by selector.** Identity-based selectors are checked at login only;
  non-identity attributes (IP, country, certificate, device posture, service token, risk score) are
  re-checked on each request. For SaaS applications, policies apply at sign-on and when the SaaS
  session is reissued.
- **IP rules live better in a rule group.** With several addresses, place them in a group's Include
  rule so one edit updates every policy. Without an Include rule the policy would require traffic
  from all the ranges.
- **MFA.** Independent MFA must be switched on for the organization before a policy can use it. The
  policy setting overrides the application setting, which overrides the organization setting. An
  identity-provider MFA requirement uses a Require rule on the authentication method and works only
  with Okta, Entra ID, generic OIDC, and generic SAML. PIV and FIDO2 keys work only for
  infrastructure applications: if they are the only globally allowed methods, other applications
  cannot be signed in to.
- **Temporary authentication.** Approvers must themselves be authenticated by Access. Approval lasts
  at most 24 hours. Users who should keep persistent access need a separate Allow policy placed
  earlier in the application's order.
- **Isolation.** The remote browser needs third-party cookies allowed on the application domain,
  and Gateway HTTP policies then apply to the isolated traffic.

## Known limitations

- Covers reusable account-level policies only. Applications, attaching a policy, per-application
  ordering, rule groups, identity providers, lists, service tokens, posture checks, and the
  dashboard policy tester are out of scope; no API for the tester is documented.
- Not documented: rate limits and quotas, maximum rules per policy, exact API error codes, whether
  update merges or replaces, and what delete does to a policy still in use. On HTTP 429, back off
  and honor any `Retry-After` header.
- A policy change reaches live applications with no draft or staged state, and no propagation time
  is stated.

## Tools

| Operation | Description | Category |
|---|---|---|
| List policies | Enumerate reusable policies with application counts | Read |
| Get policy | Fetch one policy | Read |
| Create policy | Add a reusable policy | Write |
| Update policy | Replace a policy's rules, action, or settings | Write |
| Delete policy | Remove a reusable policy | Write (destructive) |
| Convert legacy policy | Turn an application-scoped policy into a reusable one | Write |

## Verification checklist

- [ ] Action, rules, and settings confirmed valid together before creating
- [ ] Operator confirmed every create, every update, every delete, and every conversion
- [ ] Read-back shows the intended name, action, rules, and settings
- [ ] Application count checked before an update or delete
- [ ] Any Bypass policy, and any Allow policy matching Everyone, called out explicitly to the operator
- [ ] Policy removed from every application before deletion
- [ ] Order within each affected application checked by the operator, since position is set on the application
