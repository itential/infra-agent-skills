# Twilio bidirectional stream bindings

The existing voice webhook returns TwiML using the operator-approved destination:

```xml
<Response>
  <Connect>
    <Stream url="wss://media.example.invalid/voice" statusCallback="https://callbacks.example.invalid/stream">
      <Parameter name="context" value="approved-context" />
    </Stream>
  </Connect>
</Response>
```

The placeholder hosts must be replaced only by the authorized application destinations. `wss` is required; query strings are unsupported. Each parameter's name+value combined length must be under500 characters. Signature header: `X-Twilio-Signature`; the official Twilio SDK performs validation using the account Auth Token, actual request URL and the appropriate form/JSON body path. Media servers need TCP443 connectivity from Twilio's public addresses.

| Event | Binding and state |
|---|---|
| Connected | `event:"connected"`, protocol/version |
| Start | `event:"start"`, `start.callSid`,`start.streamSid`,`start.mediaFormat`; encoding `audio/x-mulaw`, sampleRate8000, channels1 |
| Incoming media | `event:"media"`, `streamSid`,`sequenceNumber`,`media.payload` base64, track/chunk/timestamp |
| Outgoing media | `{"event":"media","streamSid":"<stream-sid>","media":{"payload":"<base64-raw-mulaw-8000>"}}` |
| Outgoing mark | `{"event":"mark","streamSid":"<stream-sid>","mark":{"name":"<marker>"}}` |
| Clear buffer | `{"event":"clear","streamSid":"<stream-sid>"}`; pending marks return for cleared audio |
| Stop | `event:"stop"`, stream and call identifiers |
| Status callback | `StreamEvent`=`stream-started`,`stream-stopped`,`stream-error`; failure detail in `StreamError` |

Only inbound audio is received for a bidirectional stream. DTMF reception has `event:"dtmf"` and `dtmf.digit`; sending DTMF in this direction is unsupported. Audio payload excludes container header bytes. Closing the server WebSocket or ending the call stops the stream; REST stream creation is not the bidirectional start mechanism.

Sources: Twilio references in [procedure](procedure.md), retrieved 2026-10-09.
