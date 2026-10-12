<!--
Thanks for contributing! Please fill out the sections below — see CONTRIBUTING.md for the full
process (fork-and-pull, branch naming, CLA, labels).
-->

## Summary

Brief description of what this PR does.

## Changes

- List of specific changes made
- Another change

## Skill(s) Affected

<!-- e.g. `dns_record_management` (new vendor: X) / `change_management` (SKILL.md correction) -->

## Why this belongs here

<!-- Which infrastructure operation (network, compute, load balancing, provisioning,
troubleshooting, or an associated process) does this cover, and what does it carry that a capable
agent with the vendor's docs would not already do safely? See AGENTS.md rule 13. -->

## Testing

<!-- How was this verified? For a new/changed vendor procedure, this usually means: -->
- [ ] Every API call, field name, and endpoint path was checked against the vendor's current
      published documentation (link the source)
- [ ] If this corrects or contradicts an existing "universal concepts" assumption in `SKILL.md`,
      that correction is called out explicitly, not just folded into the vendor's own file
- [ ] `references/INDEX.md` for the affected skill is updated to list the new/changed entry

## Related Issues

Closes #123

## Checklist

- [ ] Passes the applicability screen (AGENTS.md rule 13) — not a tool manual, generic
      command/transport wrapper, or developer tooling
- [ ] Capability, `name`, and vendor/tool directories are snake_case (underscores); the capability
      is named for the operation, not a tool (AGENTS.md rules 2 and 14)
- [ ] Nothing in the diff sits outside `skills/` and root governance/README files
- [ ] Branch is up to date with `main`
- [ ] New/changed vendor content lives under `references/<vendor>/`, not in the shared `SKILL.md`
      (unless this PR is specifically fixing a bug in the shared/router content)
- [ ] `SKILL.md` still stays thin — no vendor-specific detail leaked into it
- [ ] Every new task/companion file follows AGENTS.md rule 8 to avoid
      collisions with other vendors' files in the same directory
- [ ] Sign the Contributor License Agreement (CLA) — see [CLA.md](../CLA.md)
