---
name: New capability / skill category
about: Propose an entirely new top-level skill (not just a new vendor under an existing one)
title: "[capability] "
labels: new-capability
---

## Proposed Capability Name

<!-- snake_case, named for the operation (not a tool), e.g. `certificate_management` -->

## Why This Is a Distinct Capability

Explain why this doesn't fit under an existing skill (see README's "How It's Organized" section).
A new capability should be a genuinely different operation, not a different vendor or a variant of
one already covered.

## Infrastructure Operation and Applicability

Which infrastructure operation (network, compute, load balancing, provisioning, troubleshooting, or
an associated process) is this, and what would the skill carry that a capable agent with the vendor's
docs would not already do safely? See AGENTS.md rule 13. Tool manuals, generic command wrappers, and
developer tooling are out of scope.

## Vendors/Platforms/Tools in Scope (at least one to start)

If a tool, API, or MCP server is the vendor, confirm the capability still makes sense without it
(AGENTS.md rule 14).

## Grounding

Is there a wire standard, RFC, or protocol this capability is grounded in (like DNS's RFC
1035/2136/1123), or is it a practice/framework without one (like change management/ITIL)? State
which, since it affects how `SKILL.md`'s "universal concepts" section should be framed.

## Are You Planning to Submit a PR?

- [ ] Yes, I'll open a PR for this
- [ ] No, flagging for someone else to pick up
