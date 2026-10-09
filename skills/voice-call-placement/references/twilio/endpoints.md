# Twilio outbound-call bindings

Base: `https://api.twilio.com/2010-04-01`. Use the authenticated Twilio client/account; REST Basic authentication can use an API key SID and secret. Tokens never appear in example payloads.

| Operation | Binding | Input/output |
|---|---|---|
| Create call | `POST /Accounts/{AccountSid}/Calls.json` | Form-encoded `To`, `From`, `Twiml`;201 resource with `sid`,`status` |
| Read call | `GET /Accounts/{AccountSid}/Calls/{CallSid}.json` |200 call resource, eventually consistent |

Inline `Twiml` is limited to 4000 characters; minimal payload is `<Response><Say>Approved spoken text</Say></Response>`. XML escaping applies to supplied text. Optional `<Say voice="<supported-voice>" language="<supported-locale>">` must match the vendor's current voice table. This procedure does not also supply `Url` or `ApplicationSid` (creation with both Url and Twiml ignores Twiml).

Optional `StatusCallback` and `StatusCallbackEvent` values: `initiated`,`ringing`,`answered`,`completed`; multiple events use repeated form fields. Callbacks include `CallSid`,`CallStatus`, and event `SequenceNumber`; `answered` yields in-progress. Terminal statuses include `completed`,`busy`,`failed`,`no-answer`,`canceled`. `queue_time` is an estimate, not a deadline.

SDK signature validation consumes the exact externally requested URL, received form fields and `X-Twilio-Signature`, using the account Auth Token. The vendor recommends its SDK rather than custom signature code. The security page has contradictory introductory wording about POST bodies; its explicit SDK examples and validation steps include form fields. JSON callbacks use the documented body-hash validation path instead of treating JSON as form parameters.

Errors:400 invalid input;401 credentials;404 missing target;405 incorrect method;429 API concurrency limit;500/503 provider failure. Error JSON exposes `status`,`message`, optional `code` and `more_info`. Unknown creation outcomes remain unresolved before any new attempt.

Sources: method, speech, security and response references in [procedure](procedure.md), retrieved 2026-10-09.
