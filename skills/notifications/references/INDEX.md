# Notifications — Platform Index

One row per supported communications platform. Each platform directory holds its own `procedure.md`
(the full step-by-step, including formatting/rate-limit rules), plus wire-level `endpoints.md` where
the platform is REST/API-driven.

| Platform | Directory | Scope | Notes |
|---|---|---|---|
| Slack | `slack/` | Post a new message or thread reply via `chat.postMessage` (create-only) | Channel/group/DM addressed by ID in the same call; `chat:write` scope required |
| Cisco Webex | `cisco-webex/` | Post a new message or threaded reply via the Messages API's create operation (create-only) | Room or direct-person addressed by ID/email in the same call; one file attachment per message max |
| Microsoft Teams | `microsoft-teams/` | Post a message via a Workflows (Power Automate) webhook (primary, current Microsoft-recommended path) or via the Graph API `chatMessage` create operation (alternate path, needs an Entra app registration) | Destination is fixed at webhook-configuration time for the primary path — not a runtime parameter, unlike Slack/Webex; legacy direct Office 365 Connector webhooks are documented as nearing deprecation |
| Twilio | `twilio/` | Send one SMS/MMS to a phone number via the Programmable Messaging create-message call (create-only) | Recipient-only (E.164 number); no channel or thread. Plain text, optional media; 201 means queued, not delivered; follow status to delivered/undelivered/failed. No `Retry-After` documented for 429 (error 20429) |
| SendGrid | `sendgrid/` | Send an email (plain text and/or HTML, up to 1,000 personalizations per request) via the v3 Mail Send call (create-only) | Recipient-only (email addresses); no channel or thread. 202 means accepted, not delivered; no delivery confirmation in this skill. Mail Send-specific rate limit not stated; 429 resets per a timestamp header |

**Universal-concepts population (first three platforms added):** `SKILL.md`'s "Universal concepts"
section started as an intentionally empty placeholder (per `AGENTS.md` rule 4 — don't pre-populate
before a vendor's real behavior has been checked). Adding Slack, Cisco Webex, and Microsoft Teams
together let it be filled with claims verified across all three at once, rather than one platform's
behavior being generalized prematurely. The most consequential finding: Microsoft Teams' primary
current mechanism (a Workflows/Power Automate webhook) does not take a destination as a runtime
parameter the way Slack's `channel` and Webex's `roomId`/`toPersonId`/`toPersonEmail` do — the
destination is fixed when the webhook is configured. Any future platform addition should re-check
this claim, not assume it.

Correction recorded when Twilio and SendGrid were added: the universal claims that every platform has a
richer formatted body and returns a `Retry-After`-style 429 signal were wrong for them (SMS has no rich
format; neither vendor documents `Retry-After`), and destination addressing now notes that both are
recipient-only. Twilio and SendGrid are separate products and are kept as separate vendors.
