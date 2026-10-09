# Slack file delivery

Slack's external-upload flow transfers an existing file and then completes its storage or publication.

## Procedure

1. **Prepare the transfer.** The operation receives an existing filename and its byte length; the supplied channel and optional parent-thread identity define the intended audience. **Repository safeguard: stop and confirm with the operator before proceeding** with transfer of these bytes and intended publication. The preparation response must contain a success flag, upload URL and file identifier.
   - Disallowed types, guest restrictions, disabled uploads, team size restrictions, excessive snippet/image-description size, or storage exhaustion stop transfer; these are not bypassed by another upload format.
   - Invalid parameters are corrected. Authentication, scope, permission, account and token errors stop the operation. The literal error categories are in [endpoints](endpoints.md#error-handling).
2. **Transfer bytes.** The client sends the existing file to the returned upload URL as raw bytes or multipart content. A 200 response confirms that transfer step; any other status is a transfer failure. Asynchronous server processing does not require an invented fixed wait.
3. **Complete and share.** The completion operation receives the returned file identifier and optional title, with the approved channel and parent-thread timestamp. **Stop and confirm with the operator before proceeding** if the audience or content differs from the approved transfer. With no destination the file stays private; omission of completion discards the pending file and metadata.
   - A successful response returns the finalized file information. Completion is callable only once; an uncertain outcome is reported for reconciliation, not blindly replayed.
   - Wrong channel/thread, archive restrictions, permissions and file identifiers stop publication. Rate limiting honors the returned delay. Internal/fatal errors can accompany partial success, so the last known file identifier and phase are retained.
4. **Report the native result.** The result identifies the finalized file and whether an intended destination was supplied. Uploaded bytes alone are not reported as a delivered report; successful sharing is not a read receipt.

## Patterns

- A thread attachment refers to the thread's parent timestamp, not a reply timestamp.
- The upload URL comes from Slack's response; it is not derived from a filename.
- An initial comment takes precedence over structured blocks in the completion binding; the resulting selected presentation is explicit.

## Known limitations

Only Slack's documented external file-upload sequence is covered. Audio generation, automatic transcription, delivery schedules, file deletion and recipient discovery are outside this procedure. A failed publication can still leave an uncertain server-side outcome.

## Tools

| Operation | Description | Category |
|---|---|---|
| Prepare file upload | Reserve an upload URL and file identifier | Write |
| Transfer bytes | Send an existing file to the returned upload service | Write |
| Complete upload | Finalize storage and optional channel/thread sharing | Write |

## Verification checklist

- The intended bytes and audience were approved before transfer.
- Both preparation/completion success flags and transfer HTTP result were checked.
- Completion used the returned file identifier exactly once.
- Private storage, transferred-only, finalized and uncertain outcomes are distinguished.

Sources: Slack [working with files](https://docs.slack.dev/messaging/working-with-files/), [prepare upload](https://docs.slack.dev/reference/methods/files.getUploadURLExternal/), [complete upload](https://docs.slack.dev/reference/methods/files.completeUploadExternal/), retrieved 2026-10-09.
