# Cloudflare One Gateway — DNS, Network, and HTTP Rule Procedure

List, create, update, reorder, disable, and delete a Gateway policy rule that filters DNS queries,
network (layer 4) connections, or HTTP(S) requests for users and devices behind Cloudflare One.
Source: Cloudflare Docs "DNS policies", "Network policies", "HTTP policies", "Order of enforcement",
"Common DNS policies", and the Gateway rules API reference (retrieved 2026-10-23).

DNS, network, and HTTP rules are one rule object distinguished by a single filter value. Egress and
DNS-resolver rules share that object but are Enterprise features with their own behavior and are not
covered. Lists, TLS decryption settings, locations, certificates, and block pages are separate
objects: this procedure references them but does not create them. Bind each operation through
`endpoints.md`.

## Common Sequences

1. **Add a rule:** list existing rules → choose rule type, action, match expression, and precedence
   → confirm with the operator → create → read back.
2. **Reorder or pause a rule:** get the rule → confirm with the operator → update it with a new
   precedence value or the enabled flag turned off → read back the ordered list.
3. **Remove a rule:** get the rule → confirm with the operator → delete → confirm it no longer
   appears in the list.

## Step 0: Choose the rule type and action

A rule has exactly one filter value, and the filter fixes which actions are valid.

| Rule type | Applies to | Actions |
|---|---|---|
| DNS | DNS queries | Allow, Block, Override, Safe Search, YouTube Restricted Mode |
| Network | Layer 4 connections | Allow, Block, Network Override |
| HTTP | HTTP and inspected HTTPS requests | Allow, Block, Redirect, Isolate, Do Not Inspect, Do Not Isolate, Do Not Scan, Quarantine |

- HTTP also documents a Forward action (beta). It is absent from the accepted action values on the
  API page, so do not use it without confirming it with the operator.
- HTTPS requests reach HTTP rules only when TLS decryption is turned on; without it, only plain HTTP
  on the default port is inspected. A Do Not Inspect rule must match the server name in the TLS
  header, because the full URL is not visible to it.
- A DNS Override cannot use selectors that are evaluated during or after resolution (for example
  the resolved IP).
- A match expression that mixes a query-side attribute and a response-side attribute is evaluated
  once the response arrives.
- Lists referenced by a match expression must already exist; their IDs come from the lists service,
  not from this procedure.

Success: rule type, action, and match criteria are fixed, and the action is valid for the type.

## Step 1: List existing rules

List all rules and note, for each, its name, rule type, action, precedence, and enabled state.
Group by rule type: precedence is only meaningful among rules of the same type. A rule marked
read-only is shared from a parent organization and cannot be changed here.

Success: the ordered list for the target rule type is in hand, with no rule of the same name that
would make the new rule a duplicate.

## Step 2: Choose precedence

Gateway evaluates rules in ascending precedence value, so the lowest number is checked first, and
within a filtering phase the first matching Allow or Block decides the outcome. Give narrow
exceptions a lower value than the broad rules they carve out of. The dashboard numbers rules from 1
upward in list order; the API accepts any value not already in use. If precedence is omitted on create, Gateway
assigns one starting at 1000 and counting upward, which puts the rule at the bottom.

Two rules cannot share a precedence value: pick one not already used.

## Step 3: Create a rule

1. **Stop and confirm with the operator before proceeding.** The rule takes effect on live traffic
   for every user in scope. Say plainly what it will block, bypass, or rewrite. State separately
   whether it is a Do Not Inspect rule (it takes matching traffic out of HTTP inspection, so
   HTTP Allow and Block rules never see it), a DNS Override (it changes answers), or disables DNSSEC validation (documented as
   insecure).
2. Create the rule with its name, optional description, rule type, action, match expression, optional
   identity and device-posture expressions, precedence, enabled flag, and any action-specific
   settings (block page and reason, redirect target, override addresses, quarantine file types,
   and similar). For a DNS rule only, an expiry time or duration may be set; it overrides any
   schedule.
3. Read the rule back.

Success: the response returns a rule ID and the stored rule. The platform reformats expressions on
save, so keep the stored form rather than the submitted one. A non-empty warning status means the
rule is misconfigured: report it.

## Step 4: Update, reorder, or disable a rule

1. Get the rule first so nothing is dropped.
2. **Stop and confirm with the operator before proceeding.** Any change to a live rule alters what
   traffic is blocked, bypassed, or rewritten: disabling or deprioritizing a Block rule opens
   traffic just as deleting it does, and enabling, widening, or raising a Block, Do Not Inspect, or
   Override rule restricts or bypasses more.
3. Send the update with the full desired rule (assumption: the update replaces the stored rule, as
   the create body is documented in full; the API page does not state merge behavior). To reorder,
   change the precedence value. To pause, set the enabled flag off.
4. Read the ordered list back.

Success: the read-back shows the intended precedence and enabled state, and the other rules of the
same type kept their relative order.

## Step 5: Delete a rule

1. Get the rule and show the operator its name, type, action, and match.
2. **Stop and confirm with the operator before proceeding.** Removing a Block rule opens what it
   blocked; removing an Allow rule lets its traffic fall through to later, broader rules. The documentation
   describes no undo, so recreating the rule is the only recovery. Disabling a rule, by contrast,
   stops it applying without removing it.
3. Delete by ID, then confirm the rule is gone from the list.

## Patterns

- **Phases, not one global list.** DNS, network, and HTTP are separate evaluation phases. Network
  rules are evaluated before application-level (HTTP) rules since 2025-07-14. In the HTTP phase,
  Do Not Inspect rules run before Allow and Block regardless of their position, and a request that
  passes request rules is still subject to later body inspection (DLP, antivirus, sandboxing).
- **HTTP tiers**, in order: Do Not Inspect, Isolate (needs the Browser Isolation add-on), Allow/Block/
  Do Not Scan, Forward, body inspection. A Do Not Inspect match skips every later tier, except that
  clientless web isolation isolates those sites anyway.
- **DNS timing.** Rules whose selectors are evaluated before resolution run first; the query is then
  resolved, and rules with post-resolution selectors run. An Allow listed first can still lose to a
  later Block that uses a pre-resolution selector such as Domain. A rule mixing both kinds of
  selector is evaluated after resolution.
- **Default is allow.** Traffic matching no rule is allowed in each phase, unless the account sets a
  default Block for HTTP. For default-deny, give a catch-all Block the highest precedence number (so it is
  evaluated last) and the specific Allow rules lower numbers.
- **Allow is not a bypass.** A Gateway Allow does not override an Access application's own policies
  for the same private destination; a Gateway Block ends evaluation.
- **Logged decision can differ from the final one.** An Allow followed by a DLP Block is logged as
  Allow even though the request is blocked.
- **Precedence from Terraform.** Terraform provider version 4 stores a hashed precedence (for
  example 1000 becoming 1000901) that breaks later reordering. Set precedence through the API for
  rules Terraform created, or move to provider version 5.
- **Expression drift.** The platform rewrites traffic, identity, and device-posture expressions on
  save; compare against the stored form, not what was sent.
- Regular expressions in match values use the Rust engine, whose syntax differs slightly from
  other regex libraries.

## Known limitations

- Covers DNS, network, and HTTP rules only. Egress rules, DNS-resolver rules, lists, TLS decryption
  settings, locations, certificates, block pages, and the separate packet-level network firewall
  product are out of scope.
- Not documented: rate limits and quotas, maximum rules per account, the token permission needed
  for each call, exact API error codes, and whether a delete can be reversed. On HTTP 429, back off and honor any `Retry-After` header.
- A rule change reaches live traffic; no draft or staged state is documented, and the time to
  propagate is not stated.

## Tools

| Operation | Description | Category |
|---|---|---|
| List rules | Enumerate rules with precedence and enabled state | Read |
| Get rule | Fetch one rule | Read |
| Create rule | Add a DNS, network, or HTTP rule | Write |
| Update rule | Change a rule, including precedence and enabled state | Write |
| Delete rule | Remove a rule | Write (destructive) |

## Verification checklist

- [ ] Rule type, action, and match criteria confirmed valid together before creating
- [ ] Operator confirmed every create or risky update, and every delete
- [ ] Read-back shows the intended name, type, action, precedence, and enabled state
- [ ] Stored (reformatted) expressions are what the report cites; no warning status is set
- [ ] Other rules of the same type kept their relative order after a reorder
- [ ] For HTTP rules over HTTPS, TLS decryption was confirmed on
- [ ] Rules created through Terraform had precedence set through the API
