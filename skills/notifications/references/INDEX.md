# Notifications — Platform Index

One row per supported communications platform. Each platform directory holds its own `procedure.md`
(the full step-by-step, including formatting/rate-limit rules), plus wire-level `endpoints.md` where
the platform is REST/API-driven.

| Platform | Directory | Scope | Notes |
|---|---|---|---|
| Slack | `slack/` | Post a new message or thread reply via `chat.postMessage` (create-only) | Channel/group/DM addressed by ID in the same call; `chat:write` scope required |
| Cisco Webex | `cisco_webex/` | Post a new message or threaded reply via the Messages API's create operation (create-only) | Room or direct-person addressed by ID/email in the same call; one file attachment per message max |
| Microsoft Teams | `microsoft_teams/` | Post a message via a Workflows (Power Automate) webhook (primary, current Microsoft-recommended path) or via the Graph API `chatMessage` create operation (alternate path, needs an Entra app registration) | Destination is fixed at webhook-configuration time for the primary path — not a runtime parameter, unlike Slack/Webex; legacy direct Office 365 Connector webhooks are documented as nearing deprecation |

**Universal-concepts population (first three platforms added):** `SKILL.md`'s "Universal concepts"
section started as an intentionally empty placeholder (per `AGENTS.md` rule 4 — don't pre-populate
before a vendor's real behavior has been checked). Adding Slack, Cisco Webex, and Microsoft Teams
together let it be filled with claims verified across all three at once, rather than one platform's
behavior being generalized prematurely. The most consequential finding: Microsoft Teams' primary
current mechanism (a Workflows/Power Automate webhook) does not take a destination as a runtime
parameter the way Slack's `channel` and Webex's `roomId`/`toPersonId`/`toPersonEmail` do — the
destination is fixed when the webhook is configured. Any future platform addition should re-check
this claim, not assume it.

## Adding a new platform

1. Create `references/<platform>/procedure.md` following the shape of an existing single-vendor
   capability (e.g. `skills/cmdb_asset_management/references/servicenow/procedure.md`) as a
   template: Operational procedure → Patterns → Known limitations → Tools → Verification checklist.
2. Add `endpoints.md` (wire-level calls) alongside it, if the platform is REST/API-driven — a
   CLI-driven platform (unlikely for this capability, but possible for a self-hosted tool) keeps
   commands inline in `procedure.md` instead (see `AGENTS.md` rule 6).
3. State plainly which destination types (channel, thread, direct recipient) and content types
   (plain text, rich formatting, attachments) this platform actually supports — this capability is
   asymmetric across platforms by nature (see `SKILL.md`'s "Universal concepts" note), so don't
   assume parity with another platform already listed here.
4. Add one row to the table above, replacing the placeholder row.
5. Check every existing claim in `SKILL.md`'s "Universal concepts" section against this platform's
   actual behavior before assuming it holds — correct that section explicitly if it doesn't (see
   `AGENTS.md` rule 4).
6. Do NOT add platform-specific procedure content to the top-level `SKILL.md` — see that file's own
   contribution note.
