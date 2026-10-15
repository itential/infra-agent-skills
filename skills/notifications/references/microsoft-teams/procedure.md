# Microsoft Teams — Send a Message Procedure

Posts a message into a Microsoft Teams channel or chat. Microsoft's own current guidance is that the
classic Office 365/Microsoft 365 Connector "Incoming Webhook" mechanism is being retired, and the
supported replacement for an external system posting into a channel is a **Workflows (Power
Automate) flow built from the "When a Teams webhook request is received" trigger** — this procedure
treats that as the primary path. A second, separate path exists via the Microsoft Graph API's
`chatMessage` create operation for callers that need to pick the destination channel/chat at request
time rather than at webhook-configuration time (see step 6). Covers posting a new message only — not
editing or deleting a message already sent, and not creating the Teams team/channel itself.

Sources: Microsoft's own Teams developer documentation — "Webhooks and connectors"
(https://learn.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/what-are-webhooks-and-connectors,
retrieved 2026-09-29), "Create an Incoming Webhook"
(https://learn.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook,
retrieved 2026-09-29), and the Microsoft Graph API reference "Send chatMessage in a channel"
(https://learn.microsoft.com/en-us/graph/api/channel-post-messages, retrieved 2026-09-29).

## Operational procedure

### Primary path: Workflows webhook (current Microsoft-recommended mechanism)

1. **Confirm a workflow already exists for the target channel/chat, or create one first.** Unlike
   Slack or Webex, the destination isn't a value passed at send time — it's fixed when the Teams
   Workflows app builds the flow from a template such as "Send webhook alerts to a channel" (or an
   equivalent custom flow using the "When a Teams webhook request is received" trigger), with the
   destination channel/chat chosen during that setup. If no such workflow exists yet for the
   destination the caller needs, that setup is a prerequisite outside the scope of this send
   procedure, not something this procedure's call step can do at request time.
2. **Treat the workflow's webhook URL as a bearer credential, not a plain configuration value.**
   Anyone holding the URL can post into that channel/chat — Microsoft's own connectors model
   describes the URL as the sole gate on who can trigger the flow (beyond whatever "Who can trigger
   this flow" setting was chosen at creation). Resolve it from secure storage at send time rather
   than hardcoding it in a workflow definition or log.
3. **Build the message payload.** The webhook accepts a JSON body; a plain object such as
   `{"text": "..."}` is enough for the simplest configured flows (the flow forwards the request
   body to its own "post message" action). For richer content, build an Adaptive Card (or, per
   Microsoft's own note, a legacy Message Card) and confirm with whoever configured the flow how its
   "post message" action is wired to the incoming body, since that binding is set per-flow, not
   fixed by the webhook trigger itself.
4. **Respect the documented size and rate limits before sending.** Microsoft's own documentation
   states the payload size limit is 28 KB, and that sending more than four requests in a second to
   the same webhook triggers throttling until the window refreshes. If the caller has a burst of
   messages to send, pace them under that per-second ceiling rather than firing all at once.
5. **Submit the call** as an HTTP POST to the workflow's webhook URL with the JSON payload. See
   `endpoints.md` for the literal request shape and the documented throttling/HTTP 429 response
   Microsoft references for this trigger.
6. **Confirm delivery from the HTTP response.** The webhook call's own success is limited
   confirmation — it means the trigger accepted the request, not necessarily that the configured
   flow's "post message" action itself completed without error inside Power Automate. If end-to-end
   confirmation matters, that requires checking the flow's own run history in Power Automate, which
   is outside what the webhook call itself reports.

### Alternate path: Microsoft Graph `chatMessage` create (when the destination must be chosen per-call)

7. **Use this path only when the caller genuinely needs to pick the channel or chat at request
   time**, rather than relying on a fixed, pre-configured webhook. This requires an Entra
   (Azure AD) app registration and a token carrying the `ChannelMessage.Send` delegated permission
   (a work/school account context — Microsoft's own reference states personal Microsoft accounts
   aren't supported for this operation), which is a materially heavier setup than the webhook path
   and typically not worth adopting just to avoid step 1's one-time flow setup.
8. **Build the message body** as a `chatMessage` object — at minimum a `body.content` string, with
   `body.contentType` set to indicate whether the content is plain text or HTML.
9. **Submit the call** to the channel's messages collection. See `endpoints.md` for the literal
   request shape.
10. **Confirm delivery from the HTTP response.** A successful create returns HTTP 201 with the full
    created `chatMessage` object, including its server-assigned `id` — treat that as confirmation
    the message was accepted, in contrast to the webhook path's weaker trigger-level confirmation in
    step 6.

## Patterns

- **The destination is baked into configuration for the webhook path, not passed at send time.**
  This is a structural difference from Slack/Webex, where the destination is a normal request
  parameter — don't assume a "channel ID" argument exists for the primary Teams path the way it does
  for the other two vendors in this skill.
- **Microsoft's own guidance frames the webhook URL itself as the security boundary** for the
  primary path — there's no separate per-request bearer token the way Slack/Webex expect.
- **Two genuinely different mechanisms exist for the same outcome** (webhook vs. Graph API) with
  different setup costs, different confirmation strength, and different security models — pick
  deliberately per step 1 vs. step 7 rather than defaulting to whichever was easiest to find first.

## Known limitations

- Legacy Office 365/Microsoft 365 Connectors (the older direct Incoming Webhook mechanism Teams
  previously supported without the Workflows app) are documented by Microsoft as nearing
  deprecation, with new connector creation being blocked — this procedure does not cover that legacy
  mechanism as a build target, only the current Workflows-based replacement.
- The webhook path's payload size limit is 28 KB (Microsoft's own documented figure) and throttles
  above four requests per second to the same webhook — exceeding either isn't handled gracefully by
  this procedure and must be avoided by the caller (chunking content, pacing sends).
- Webhooks and connectors are documented as unavailable in GCC High, DoD, and 21Vianet-operated Teams
  environments, and only partially available (Incoming Webhook only, admin-enabled) in GCC — confirm
  the target tenant's environment before assuming this procedure's primary path applies.
- The Graph API alternate path does not cover application-only (unattended) sending for ordinary
  messages — Microsoft's own reference states application permissions for this operation are
  supported only for message-migration scenarios (`Teamwork.Migrate.All`), not general notification
  sending; a delegated (signed-in user) context is required for the ordinary send case covered here.
- Neither path in this procedure covers editing or deleting a previously sent message, or creating
  the Teams team/channel/chat itself.

## Tools

| Operation | Description | Category |
|---|---|---|
| Workflows webhook trigger ("When a Teams webhook request is received") | Post a message/card to the channel or chat the flow was configured for | Messaging (primary path) |
| Graph API — Send chatMessage in a channel | Post a new message to a channel chosen at request time | Messaging (alternate path, requires Entra app registration) |

## Verification checklist

- [ ] Confirmed which path applies (webhook vs. Graph API) before building the payload — see
      "Patterns" above
- [ ] For the webhook path: webhook URL resolved from secure storage, not hardcoded or logged in
      plaintext
- [ ] For the webhook path: payload confirmed under the 28 KB limit, and sends paced under four
      requests/second to the same webhook
- [ ] For the webhook path: understood that a successful HTTP response confirms trigger acceptance,
      not necessarily that the flow's own post-message action completed
- [ ] For the Graph API path: token confirmed to carry `ChannelMessage.Send` (delegated, work/school
      account) before attempting the call
- [ ] For the Graph API path: response status 201 and the returned `chatMessage` object's `id`
      checked to confirm creation
