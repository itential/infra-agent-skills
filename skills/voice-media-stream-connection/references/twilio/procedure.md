# Twilio bidirectional media connection

Twilio connects an existing voice call to a prepared media server and exchanges encoded audio through a bidirectional WebSocket stream.

## Procedure

1. **Validate the incoming request.** The prepared voice application validates Twilio's webhook signature with the official SDK and exact request URL/body. A successful signature establishes provider provenance; this procedure makes no claim that caller ID authenticates the human. Failed validation stops processing.
2. **Return the connection instruction.** The supplied media destination uses secure WebSockets. **Repository safeguard: stop and confirm with the operator before proceeding** with routing live call audio to that destination. The voice application returns the vendor's bidirectional stream instruction. Query parameters are unsupported; named custom parameters carry requested metadata.
3. **Observe establishment.** The server validates the WebSocket handshake signature and receives connected, start and then media events. Start identifies the call, stream and audio format. The receiver can consume only the inbound track; one bidirectional stream may be active on a call. A stream-error callback records failure rather than a working connection.
4. **Exchange authorized audio.** The receiver processes the incoming encoded audio. Supplied response audio is sent in the documented format, without file-container headers. **Stop and confirm with the operator before proceeding** if sending audio exceeds the previously approved conversation scope. After sending media, a named mark permits the server to observe playback completion; an explicit buffer-clear also returns pending marks, so a mark following clear is not proof of playback.
5. **Close the stream.** **Stop and confirm with the operator before proceeding** with an operator-requested interruption. Closing the server WebSocket ends the bidirectional stream and allows later call instructions/action handling to continue; ending the call also stops it. A stop event identifies the stream's termination. The stream-noun page's older sentence claiming only call termination can stop a bidirectional stream conflicts with the overview and current WebSocket stop section; this procedure follows those explicit connection-closure rules.

## Patterns

- The connection instruction blocks later call instructions until disconnection.
- A unidirectional stream uses a different instruction and cannot send audio back.
- Audio headers corrupt playback; the transport expects raw encoded samples.

## Known limitations

No voice application deployment, telephone-number configuration, speech recognition, AI backend, whitelist policy, transcript retention, or live device commands. The media server and callback handler must already exist. Outbound DTMF is unsupported on this bidirectional surface.

## Tools

| Operation | Description | Category |
|---|---|---|
| Validate request | Verify provider webhook/handshake signature | Local validation |
| Return connection instruction | Connect live call to approved media server | Write |
| Receive/send media | Exchange raw audio over prepared WebSocket | Read/write |
| Mark/clear/close stream | Observe playback or interrupt buffered media/connection | Write |

## Verification checklist

- Both webhook and handshake validation succeeded.
- The connection destination was approved before routing media.
- Connected/start/media events identify the expected call and format.
- Marks are interpreted with buffer-clear context; stop confirms termination.

Sources: Twilio [Media Streams](https://www.twilio.com/docs/voice/media-streams), [stream instructions](https://www.twilio.com/docs/voice/twiml/stream), [WebSocket messages](https://www.twilio.com/docs/voice/media-streams/websocket-messages), [security](https://www.twilio.com/docs/usage/security), retrieved 2026-10-09.
