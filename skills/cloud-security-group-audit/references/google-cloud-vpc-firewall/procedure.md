# Google Cloud VPC Firewall Rules — Audit

Read the VPC firewall rules in the projects in scope, evaluate exposure and breadth, and, where Firewall Insights is enabled, read its findings on shadowed, overly permissive, and unused rules. Source: Google Cloud VPC "Firewall rules" documentation, Network Intelligence Center "Firewall Insights" documentation, and the `gcloud compute firewall-rules` and `gcloud recommender insights` references bound in `endpoints.md` (retrieved 2026-11-10).

Read-only and diagnostic: a decision list keyed by check, no confirmation gates. No rule is changed, disabled, or deleted.

## Platform facts the checks rest on

- A rule belongs to one VPC network, applies to ingress or egress (never both), and either allows or denies. Priority runs 0–65535 and the lowest number that matches is the only rule applied; at equal priority a deny beats an allow.
- Targets: all instances in the network, instances with given network tags, or instances running as given service accounts. A rule cannot mix tags and service accounts.
- Two rules are implied: deny all ingress, allow all egress. They are lowest priority and not listed.
- A rule can be disabled; a disabled rule is not enforced.
- The automatically created default network starts with rules allowing internal traffic, SSH (22) from anywhere, RDP (3389) from anywhere, and ICMP from anywhere.
- There is no attachment object: a rule applies to whatever instances match its network and target selector.
- Rule changes affect new connections only.
- Firewall rule logging is optional and metrics-based insights depend on it.

## Common Sequences

1. **Full audit:** Scope → Read rules → run every check → Read Firewall Insights (if enabled) → Report.
2. **Internet exposure only:** Read rules → run "Open to the internet" → Report.
3. **Rule cleanup candidates:** Check Firewall Insights state → Read insights → cross-check each against the rule → Report.

## Step 1: Scope

List the projects in scope (one project, or all the credentials can read). Run steps 2 and 4 per project. Record a project whose read fails or is denied as not read with the error.

## Step 2: Read rules

List all VPC firewall rules in the project, following pages to the end. Keep per rule: name, network, direction, priority, action (allowed or denied entries with protocols and ports), source ranges, destination ranges, target tags, target service accounts, disabled flag, and logging setting.

Success: every page read.

## Check A: Open to the internet

Report an enabled ingress allow rule whose source ranges include `0.0.0.0/0`. Assumption: `::/0` is the IPv6 equivalent, as the platform supports IPv6 ranges; report it the same way.
1. Look at every enabled ingress deny rule in the same network with a lower priority number, or equal priority, that matches the same protocol, ports, and targets. If one exists, the allow does not apply there; report under Check D.
2. Classify the allowed entries: administrative port (22 or 3389 in range), all protocols or a wide port range, other port.
3. Name the reach: all instances in the network, instances with the listed tags, or instances running as the listed service accounts. Tag membership and service-account assignment are read from the instances themselves; no binding is listed for it here, so report the selector and say membership was not resolved.
4. Report each of the default network's SSH, RDP, and ICMP rules that still exist and still allow all addresses; they are expected on the default network and still count as exposure.

## Check B: Broad rules

Heuristic, not a documented platform check.

Report an enabled allow rule that permits all protocols or all ports from any source other than the network's own ranges, and any ingress allow rule applied to all instances rather than a tag or service account, so the operator can see which rules are not scoped.

## Check C: Unused and disabled rules

Heuristic, except where it defers to Firewall Insights.

- **Disabled rules:** report with name and age if available. They are not enforced.
- **Rules with selectors that match nothing:** a rule whose target tags or service accounts match no instance applies to nothing. Resolving this needs the instance list; if it is not read, report that this check was not performed.
- **Rules with no traffic:** only Firewall Insights can say, through allow rules with no hits, and only for traffic that logging captured. See "Firewall Insights".

## Check D: Shadowed and overlapping rules

Within one network, direction, and target set, report a rule as shadowed when another rule with a lower priority number, or equal priority and action deny, covers it: same or broader protocol and ports, and source/destination ranges and targets that contain it. Same action means redundant; opposite action means the shadowed rule never takes effect. When Firewall Insights is enabled, treat its shadowed-rule insight as the authoritative result and the manual comparison as a cross-check.

Rule targets by tag and by service account can overlap through an instance that has both; membership is not resolvable from the rule alone, so report as "cannot be judged".

## Firewall Insights

Firewall Insights produces: shadowed rules, allow rules with no hits, allow rules classed as obsolete by its adaptive analysis, allow rules with unused attributes, allow rules with overly permissive address or port ranges, and deny rules with no hits during the observation period. It is exposed through the console, the Recommender API, and the Google Cloud CLI.

Preconditions, all documented:
1. The Firewall Insights service and the Recommender service are enabled for the project.
2. Firewall rules logging is on for the rules to be assessed; metrics cover TCP and UDP traffic that matches the logging.
3. The shadowed-rule and overly-permissive-rule insight features are enabled by configuration; they are not on by default, and the overly-permissive feature needs an observation period.
4. Time to results: up to 48 hours after enabling; up to 10 days for the machine-learning predictions on overly permissive rules.
5. Disabling a feature discards previously generated insights.

If any precondition is unmet, report "Firewall Insights not available for this project" with the unmet condition; an empty result is not a clean result. Read the firewall insights for each project, keep the insight's description, target rule, and state, and cross-check each against the rule read in Step 2. Not documented: the subtype names of this insight type; report the value returned.

## Patterns

- A rule that exposes the whole network is more serious than one scoped to a tag, so always report the selector with the source range.
- An allow rule that Firewall Insights marks as having no hits may still be needed for traffic that logging does not capture (it covers TCP and UDP only).
- Hierarchical and network firewall policies also apply to instances; Firewall Insights mentions them but this procedure reads only VPC firewall rules.

## Known limitations

- Read-only. No rule is disabled, edited, or deleted.
- Hierarchical firewall policies, network firewall policies, and Cloud Armor are not read; exposure judged here may be changed by them.
- Rate limits and quotas for the read calls: not documented; back off on a throttling response and report any project that still fails.
- Required read permissions: the Firewall Insights page names a viewer role for the Recommender; other required permissions are not documented. Report a permission error as not read.

## Tools

| Operation | Description | Category |
|---|---|---|
| List firewall rules | All VPC firewall rules in a project | read |
| List Firewall Insights | Firewall insights for a project | read |
| Read Firewall Insights configuration | Whether shadowed and overly-permissive insights are enabled | read |

## Verification checklist

- [ ] Every project read to the last page, or recorded as not read with the error
- [ ] Disabled rules not counted as exposure
- [ ] Each exposure hit checked against lower-numbered (or equal-priority) deny rules
- [ ] Every hit names its target selector, and states whether membership was resolved
- [ ] Firewall Insights state reported (available, or the unmet precondition), never silently skipped
- [ ] No write call was made
