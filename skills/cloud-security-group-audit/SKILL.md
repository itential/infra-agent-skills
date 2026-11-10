---
name: cloud-security-group-audit
description: Audit the network access rules of a public cloud in read-only mode, finding rules open to the whole internet, all-protocol or very wide rules, unattached or unused groups, default groups that carry rules, redundant or shadowed rules, and missing rule descriptions. Use when asked to review, assess, or clean up cloud security groups, network security groups, or VPC firewall rules, or to check what is exposed to the internet. Covers AWS EC2 security groups, Azure network security groups, and Google Cloud VPC firewall rules. Assumes an authenticated, read-capable client for the target cloud account is already available; this skill does not authenticate. It never changes a rule or deletes a group. Checks per platform are in references/INDEX.md.
argument-hint: "[platform] [scope: account|region|subscription|project|vpc|group] [check: exposure|unattached|overlap|hygiene|all]"
---

# Cloud Security Group Audit

Reads the network access rules and group associations of a public cloud and reports where they are
exposed, broader than they need to be, unattached, or redundant, each finding backed by the rule or
association that proves it.

This skill is diagnostic-shaped: the agent reads state, evaluates it against documented behavior of
the platform, and reports findings with evidence. Reading changes nothing, so the procedure has no
confirmation gates. The agent does not revoke rules, delete groups, or detach anything; a change of
that kind is outside this skill and would need its own gate.

## When to use this skill

- Reviewing which rules allow traffic from any address, which groups nothing uses, or which rules
  overlap, across one account, region, subscription, project, or network.
- Checking whether a specific group or rule exposes a service to the internet.
- Not for creating or editing rules, and not for tracing why one packet was dropped.

## Universal concepts

- A rule has a direction, a protocol, a port range, a source or destination, and (where the
  platform has deny rules) an action. The field names differ by platform.
- A rule is open to the internet when its source covers every address. How "every address" is
  written differs by platform and is listed in each platform file.
- Some platforms record which resources use a group, while others apply a rule by selector and
  record no attachment. A check that depends on attachment is defined per platform.
- Where a platform has deny rules it evaluates by priority; where it has only allow rules they
  combine. Judge exposure and overlap with the platform's own rule order.
- Findings describe state at read time. Report the time of the read and any scope that could not be
  read (a region, subscription, or project that failed or was not permitted).

## Procedure

1. Identify the target platform from the request; check `references/INDEX.md`. If no row matches,
   stop: this skill does not cover it.
2. Identify the scope and the checks requested. Default to all checks across everything the
   credentials can read.
3. Open `references/<platform>/procedure.md` and follow it exactly. Bind each named operation to a
   concrete call through that platform's `endpoints.md`; if no binding is available, report that
   instead of improvising a call.
4. Report with the platform's own vocabulary: findings grouped by check, each with the group or
   rule identifier, the evidence, and the platform's documented reason it matters; then counts per
   check, then the scopes read and the scopes not read.

## Known limitations

- Read-only. No rule is changed, no group is deleted.
- Only platforms in `references/INDEX.md` are covered.
- Severity ordering is not defined by the platforms; findings are ordered by check class as the
  platform file lists them, and what is acceptable for a given workload is the operator's call.

## Contributing to this skill

`SKILL.md` changes only to fix a shared concept above or to add a pointer to a newly supported
platform. Platform detail belongs under `references/<platform>/`.

## Tools

Each platform file names the read operations it uses (list groups, list rules, list associations,
and any insights service); the client is the caller's.

## Verification checklist

- [ ] Platform confirmed against `references/INDEX.md`
- [ ] Every scope (region, subscription, project) read fully, or listed as not read with the reason
- [ ] Paged results read to the end
- [ ] Each finding carries the rule or association that proves it
- [ ] Exposure judged with the platform's own rule order, including deny rules where they exist
- [ ] No write call was made
