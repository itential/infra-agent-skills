# SD-WAN Policy Management — Vendor Index

One row per supported vendor. Each vendor directory holds its own `procedure.md` (the full step-by-step),
plus wire-level `endpoints.md`.

| Vendor / Platform | Directory | Scope | Notes |
|---|---|---|---|
| Cisco Catalyst SD-WAN Manager | `cisco_catalyst_sdwan/` | Look up/create/edit/activate/deactivate/delete a centralized policy (original template-policy model) | Save-then-activate: a saved policy has no effect until activated. Task-status polling, edit-while-active, and delete-while-active are not documented in the sources and are marked in the procedure. Configuration-group/policy-group model, localized policy, and text-type (`cli`) policies are not covered. Cisco also sells security and wireless products; those belong to other skills |
| Palo Alto Networks Prisma SD-WAN | `prisma_sdwan/` | Look up, create, edit, and delete path (network) and QoS (priority) policy sets and their rules; build simple or advanced stacks (one to four ordered sets); bind a stack to sites, confirm via set status, unbind, and delete (stacked policy model) | Set, stack, and bind with no activate step: a stack takes effect when bound to a site (one stack per type per site). Routes are pinned to the newest spec version of each. How a site update applies or clears a stack reference, stack or bind-level status, and the spec's claim that a profile call must follow token minting are unverified and marked in the procedure. Security, NAT, and performance stacks, and the legacy original policy model, are not covered. Prisma also sells security and Prisma Access products; those belong to other skills |

## Notes on the shared concepts

Adding Prisma SD-WAN as the second platform corrected `SKILL.md`'s universal concepts (`AGENTS.md`
rule 4). Cisco saves a policy and then activates it; Prisma has no activate step, and attaching a
stack to a site is what makes it live. The concepts on saved versus effective state, and on
asynchronous completion, were reworded so they no longer assume an activation step. In the
`activate_policy` and `deactivate_policy` arguments, "activate" and "deactivate" mean bind and unbind
a stack to sites on Prisma SD-WAN.

## Adding a new vendor

1. Create `references/<vendor>/procedure.md` following the shape of an existing single-vendor
   capability (e.g. `skills/cmdb_asset_management/references/servicenow/procedure.md`) as a
   template: Common Sequences → Status vocabulary → Operations → Patterns → Known limitations → Tools →
   Verification checklist (`AGENTS.md` rule 12).
2. Add `endpoints.md` (wire-level calls) alongside it, if the platform is REST/API-driven — CLI-driven
   platforms keep commands inline in `procedure.md` instead (see `AGENTS.md` rule 6).
3. If this vendor also appears in `wireless_network_management`'s, `firewall_management`'s, or
   `vpn_tunnel_management`'s `INDEX.md` (a common case for vendors with converged products), note
   that in this row's Notes column. Never merge reference files across skills even for the same
   vendor — the object models differ.
4. Add one row to the table above.
5. Check every existing claim in `SKILL.md`'s "Universal concepts" section against this vendor's
   actual behavior before assuming it holds — correct that section explicitly if it doesn't (see
   `AGENTS.md` rule 4). Each added vendor re-tests those claims; a second vendor is the first real test of them.
6. Do NOT add vendor-specific procedure content to the top-level `SKILL.md` — see that file's own
   contribution note.
