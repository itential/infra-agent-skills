# Slack collaboration context

Slack's Web API returns caller-visible profile attributes, availability signals and conversation evidence.

## Common Sequences

- Person context: **Read person context**.
- Conversation evidence: **Locate conversation → Read history or thread**.
- Topic search: **Search messages → Read history or thread** for a selected match.

### Read person context

1. The user-information operation returns the supplied member identifier and available basic attributes; the profile operation returns supplied custom fields and status. Missing profile values remain unknown. Display names are mutable; identity uses user and workspace identifiers.
2. Presence retrieval for another user returns active or away. The richer connection/activity fields apply to the authenticated user, not arbitrary colleagues. DND retrieval returns the requested member's available DND state; snooze details are restricted to the current user.
3. Success requires the response's success flag and expected result, not merely a successful HTTP status. At every operation in this procedure, the error categories in [endpoints](endpoints.md#error-handling) apply: auth/access failures stop the lookup, invalid parameters require correction, throttling honors the returned delay, and unavailable or unknown results remain incomplete.

### Locate conversation

1. The conversation list uses the requested workspace and conversation types. It returns only the caller's visible subset; a workspace-level token ignores the organization-level workspace selector.
2. The returned continuation cursor is followed until empty. Filtering happens after Slack selects a virtual page, so a short or empty page with a continuation cursor is not completion.
3. Success is the selected conversation identifier and its visible metadata. Missing membership does not authorize joining a channel through this read-only procedure.

### Read history or thread

1. History retrieval selects the resolved conversation and supplied time bounds. A thread read additionally identifies an existing parent or thread message. A message with no replies returns as a single message.
2. Cursor pagination continues using the returned cursor. Timestamp bounds are exclusive unless inclusion is requested. History is returned newest first; thread history is returned earliest first. This procedure uses cursors rather than combining conflicting manual time-pagination assumptions.
3. The result retains timestamps, message types and any retention-limited flag. Thread participant references can contain bot identifiers, so not every participant is a human user suitable for profile lookup.
4. Success means complete visible evidence for the selected scope or an explicitly incomplete result. It does not establish that omitted historical messages never existed.

### Search messages

1. The legacy search operation uses a user token and a supplied query, optionally scoped to a channel or speaker. Results are affected by that user's Slack search filters.
2. Matching messages and page information are retrieved through the documented pagination. Nearby matches may collapse into one search result; searching is not an exhaustive export.
3. A selected result supplies conversation and timestamp identity for **Read history or thread**. No relevant match is reported as no visible match, without inventing a historical incident.

## Patterns

- DND and active/away are platform observations, not an escalation or shift-coverage decision.
- Missing emails can reflect scopes or workspace display settings.
- History and thread limits vary by app distribution; rate-limit responses take precedence over a presumed universal tier.

## Known limitations

No sending, channel membership changes, presence setting, incident assignment, or inferred working hours. The vendor labels message search legacy and recommends its newer real-time search API; the latter is not part of this binding.

## Tools

| Operation | Description | Category |
|---|---|---|
| Read person/profile/presence/DND | Retrieve requested member context | Read |
| List conversations | Resolve visible conversation identifiers | Read |
| Read history/thread | Retrieve timestamped evidence | Read |
| Search messages | Find visible topic matches | Read |

## Verification checklist

- Success flags and expected result fields are checked.
- Cursors/pages are exhausted or incompleteness is reported.
- Caller visibility, retention and app-specific limits remain explicit.
- No availability observation is treated as an on-call assignment.

Sources: Slack Web API method references linked individually in [endpoints](endpoints.md), rolling documentation, retrieved 2026-10-09.
