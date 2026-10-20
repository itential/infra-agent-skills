---
name: notifications
description: Send a message, notification, summary, or report to a channel, thread, or recipient on a supported communications platform — currently Slack, Cisco Webex, Microsoft Teams, Twilio (SMS/MMS), SendGrid (email), or Mattermost. See references/INDEX.md for exact per-platform scope. Use when an agent needs to post an outbound message (a status update, a summary, a report, an alert) rather than manage a record on some other system. Assumes an authenticated client/credential for the target platform's API is already available (Microsoft Teams' primary path instead assumes a pre-configured per-channel webhook URL — see that platform's own procedure); this skill does not provision or authenticate it. Does not cover reading message history, editing or deleting a previously sent message, or managing channel/membership configuration — this skill is send-only.
argument-hint: "[platform] [destination: channel|thread|recipient] [message/summary/report content]"
---

# Notifications

Sends an outbound message — a chat post, a summary, a report, an alert — to a channel, thread, or
recipient on whichever communications platform the caller is targeting, following that platform's
own documented procedure and formatting rules exactly.

## When to use this skill

- Posting a message, status update, summary, or report to a channel/thread/recipient on a supported
  platform.
- Not for reading prior messages, editing or deleting a message already sent, or managing
  channel/membership configuration — this skill is send-only; those are different capabilities that
  don't exist yet in this repository.

## Universal concepts (shared messaging vocabulary, not a wire standard)

There is no single wire spec grounding this capability the way RFC 1035 grounds DNS — chat platforms
each define their own model. The claims below are only the ones verified true across every platform
currently listed in `references/INDEX.md` (Slack, Cisco Webex, Microsoft Teams, Twilio,
SendGrid, Mattermost); re-verify each one against any new platform's actual behavior before assuming it still
holds (see `AGENTS.md` rule 4).

- **A successful call confirms the platform accepted the message, not that a person has read it.**
  Every platform currently covered distinguishes "the request was accepted" from any notion of a
  recipient actually seeing the content — none exposes a synchronous "message read" signal as
  part of sending.
- **Destination types are not uniform.** Twilio (a phone number) and SendGrid (email addresses) only
  address individual recipients, never a channel or thread.
- **Destination addressing is not uniform.** Slack and Webex both take a destination identifier
  (a channel/room ID, or an email/user ID for a direct message) as a normal parameter on the same
  authenticated API call used to send. Microsoft Teams' current primary mechanism is structurally
  different: the destination channel/chat is fixed when a Workflows (Power Automate) webhook is
  configured, not passed at send time — see `references/microsoft-teams/procedure.md`. Never assume
  a runtime "channel" argument exists just because it does on Slack/Webex.
- **Every platform here supports a plain-text body; most also offer a richer, platform-specific
  format** (Slack Block Kit, Webex Markdown, Teams Adaptive Cards/Message Cards, Mattermost Markdown/message attachments, SendGrid HTML) — but
  the richer formats are not interchangeable across platforms, and SMS through Twilio has none (plain
  text, optionally with media).
- **Platforms limit sending, and several answer excess requests with HTTP 429** — but the ceiling,
  its scope, and the retry signal differ, and not every platform documents a retry-wait value (see
  each platform's procedure). Never reuse one platform's documented limit or retry signal for
  another.

See `references/INDEX.md` for which platforms have a procedure, and each platform file for how it
implements this shape concretely.

## Procedure

1. **Identify the target platform** — from the caller's request or the `platform` argument. Check
   `references/INDEX.md`; if no matching row exists, stop: this skill doesn't cover it yet.
2. **Identify the destination** — a channel, a thread, or a direct recipient — since not every
   platform supports all three, and the exact addressing mechanism (a channel ID, an email address,
   a webhook URL) differs by platform. Check that platform's own `procedure.md` before assuming a
   destination type is supported.
3. **Open `references/<platform>/procedure.md`** and follow it exactly — it contains that platform's
   full operational procedure, formatting rules (e.g. supported markup, attachment/embed limits,
   rate limits), error handling, patterns, known limitations, tools, and verification checklist.
4. **Report the outcome** using that platform procedure's own status vocabulary — confirm the
   message was actually accepted/delivered, not just that the call returned without an error, where
   the platform makes that distinction.

## Known limitations

- Platform coverage is exactly the six platforms in `references/INDEX.md` (Slack, Cisco Webex,
  Microsoft Teams, Twilio, SendGrid, Mattermost) — a platform not listed there needs a new reference file
  before this skill can be used for it.
- Send-only. Does not cover reading message history, editing or deleting a previously sent message,
  or channel/membership management — those are different capabilities, not covered here.
- Not every platform will support every destination type (channel vs. thread vs. direct recipient)
  or every content type (plain text vs. rich formatting vs. attachments) — check
  `references/INDEX.md` and the target platform's own `procedure.md` before promising a specific
  capability to the caller.

## Contributing to this skill

**`SKILL.md` only changes for two reasons: a bug in the universal concepts/router logic above, or
adding a pointer to a newly-supported platform.** Platform-specific procedure changes — a new error
code, a corrected field, a changed API path, a new destination type — belong in that platform's own
`references/<platform>/procedure.md`, never here.

## Tools

Each platform assumes its own authenticated client/credential — see `references/INDEX.md` for
which, and that platform's `procedure.md` for the specific operations.

## Verification checklist

- [ ] Target platform confirmed against `references/INDEX.md` before proceeding
- [ ] Destination type (channel/thread/recipient) confirmed as supported by that platform before
      attempting to send
- [ ] That platform's own `procedure.md` was followed, including its own formatting/rate-limit
      constraints
- [ ] Outcome reported using the platform procedure's own status vocabulary, distinguishing
      "call succeeded" from "message actually delivered" where the platform makes that distinction
