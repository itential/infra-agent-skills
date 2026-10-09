# World Labs text-to-world generation

Submit an approved text prompt and track the resulting Marble world.

## Common Sequences

- Create: **Resolve request** → **Generate** → **Track operation** → **Retrieve world**.
- Existing job: **Track operation** → **Retrieve world**.

### Resolve request

The request supplies the text prompt, supported model and optional display name. The display name is metadata rather than generation guidance. Existing API credentials and credits are prerequisites; no billing or sharing settings are changed here. Content sent to the provider must be within the operator's approved disclosure scope.

### Generate

Generation consumes API credits: stop and confirm with the operator before proceeding. Acceptance returns an operation identifier, not a completed world. Invalid JSON/prompt/model requests require correction; insufficient credits leave generation unaccepted; schema errors identify invalid fields. A rate-limited start is unaccepted and follows the returned retry delay or publisher backoff guidance. An uncertain timeout/server failure is not automatically resubmitted because the first generation may exist.

### Track operation

The operation identifier is retained and polled until its native done flag is true. A non-null terminal error means generation failed; the error code/message remains the outcome. A completed response supplies the generated-world result. A missing or inaccessible operation is distinct from a failed generation. If a world identifier was already returned in metadata, direct world lookup can establish that resource independently; an unknown identifier is not invented.

### Retrieve world

The known world identifier resolves the generated resource and its returned viewer/assets metadata. A missing or unauthorized resource remains a lookup failure. The result retains native asset links and any returned cost information without guessing a price. Generated content is labeled as generated; it is not presented as an exact network topology.

## Patterns

Accepted jobs are polled instead of resubmitted. Operation retention and world-resource lifetime are different; only returned identifiers support recovery.

## Known limitations

Text-only input is the verified subset. No fixed completion time, operation-expiry interval or cost is guaranteed. No automatic new generation follows a failed job.

## Tools

Assumes the authenticated client described in [the bindings](endpoints.md).

| Operation | Description | Category |
|---|---|---|
| Generate | Start approved text-to-world generation | Paid creation |
| Read operation | Observe native asynchronous outcome | Read |
| Read world | Retrieve generated resource/assets | Read |

## Verification checklist

- Prompt/model and credit-consuming gate are explicit.
- Accepted operation ID is retained.
- Done with error is reported as failure.
- Returned world identity and native assets match.
- No exact-topology claim accompanies generated geometry.

## Sources

- [World generation API](https://docs.worldlabs.ai/api/reference/worlds/generate). Retrieved 2026-10-09.
- [Operation API](https://docs.worldlabs.ai/api/reference/operations/get). Retrieved 2026-10-09.
- [World retrieval API](https://docs.worldlabs.ai/api/reference/worlds/get). Retrieved 2026-10-09.
- [Error behavior](https://docs.worldlabs.ai/api/errors). Retrieved 2026-10-09.
- [Generation rate-limit behavior](https://docs.worldlabs.ai/api/rate-limits). Retrieved 2026-10-09.
