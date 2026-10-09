# Twilio outbound voice call

Twilio's call resource creates one outbound call with supplied speech instructions and exposes its progress.

## Procedure

1. **Prepare the call.** The destination and caller identity come from the request/account. A telephone destination requires a telephone caller identity owned by Twilio or verified for that account. The supplied text becomes speech instructions; voice/language combinations must be supported by Twilio. An invalid pairing can fail speech execution.
2. **Create the call.** **Repository safeguard: stop and confirm with the operator before proceeding**, including recipient, caller identity and spoken content. The creation operation receives inline speech instructions and, if configured, a callback destination for requested call-progress events. Success returns the call identifier and current state; queued means accepted for later dialing, not answered.
   - Invalid request details are corrected from the returned error. Invalid credentials, missing resources and unsupported method errors stop the operation. API concurrency throttling defers requests. Service errors preserve an uncertain result; a timeout does not authorize another call attempt.
3. **Observe progress.** A call-detail read retrieves the saved call resource. It is eventually consistent; authenticated progress callbacks provide live updates when configured. Each callback is validated by the vendor SDK before its data is trusted. Sequence numbers distinguish event order because callbacks can arrive out of order.
4. **Report the terminal result.** Native busy, no-answer, failed and canceled outcomes remain distinct. Completed means a connection transferred audio and ended normally; a person, voicemail or IVR might have answered. There is no claim that the intended person heard or understood the message. If no terminal state is observed, the result remains pending or unknown.

## Patterns

- Account calls-per-second queueing is distinct from API concurrency rejection.
- The completion callback event can carry an unsuccessful terminal call status; its event name alone is insufficient.
- Speech pronunciation of numbers and abbreviations may need verification. No fixed synthesis latency is promised.

## Known limitations

No recording, answering-machine classification, real-time network commands, call termination/update, automatic retries or recurring briefings. Twilio's speech features have their own terms and voice availability; this procedure does not install or select an unverified third-party voice.

## Tools

| Operation | Description | Category |
|---|---|---|
| Create call | Initiate one supplied outbound call | Write |
| Read call | Retrieve the call's saved state | Read |
| Validate callback | Verify incoming provider signature | Local validation |
| Receive call progress | Observe authenticated native state changes | Read |

## Verification checklist

- The recipient and speech were approved at the creation step.
- Creation returned a call identifier, and queued/answered/completed are distinguished.
- Callback signatures and ordering were checked where callbacks are used.
- The final statement does not claim a human acknowledged the call.

Sources: Twilio [Call resource](https://www.twilio.com/docs/voice/api/call-resource), [speech instructions](https://www.twilio.com/docs/voice/twiml/say), [security](https://www.twilio.com/docs/usage/security), [API responses](https://www.twilio.com/docs/usage/twilios-response), retrieved 2026-10-09.
