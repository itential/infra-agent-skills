# X post and mention operations

X APIv2 retrieves visible mentions and recent posts, creates supplied text/replies, and deletes a selected own post.

## Common Sequences

- Inspect mentions: **Read mentions → Read selected post or recent context**.
- Publish: **Prepare publication → Create post or reply → Read selected post or recent context**.
- Delete: **Read selected post or recent context → Delete selected post**.

### Read mentions

1. The timeline operation receives the supplied user identifier and optional time or post-ID bounds. Start must precede end; a lower post-ID bound must precede the upper bound.
2. Results include posts, metadata and any errors. A returned continuation token retrieves another page with the same filters. Visibility and pagination qualify the outcome; an empty result is not a statement about all historical mentions.
3. At every operation, documented problem responses are preserved: invalid requests require correction; unauthorized fields/resources remain unavailable; missing, disallowed or unavailable resources are reported distinctly; hydration failures retain partial data; internal failures remain incomplete. The problem types and bindings are in [endpoints](endpoints.md). No fixed plan quota or price is assumed.

### Read selected post or recent context

1. Lookup uses the selected post identifier. Explicitly requested fields supply conversation and creation-time evidence when available.
2. Recent search receives a supplied search expression and time/ID bounds. It covers the documented recent window; continuation tokens are followed. This scope does not infer a complete conversation from a partial search page.
3. Any included errors qualify the corresponding fields/resources even when the HTTP response succeeded.

### Prepare publication

1. The exact supplied text, optional reply target, and any already-uploaded media identifiers form the proposed post. Publishing text does not require generating a persona, adding a hashtag or changing the user's wording.
2. Media attachments require prior successful upload and remain subject to posting-account limits. New media-upload operations are outside this procedure; an upload alone is not a published post.

### Create post or reply

1. **Repository safeguard: stop and confirm with the operator before proceeding** with the final text, audience implications, reply target and attachments. Creation uses the authenticated user context and returns a new post identifier on success.
2. For a supplied thread, each next text segment replies to the newly returned prior post identifier. This is a sequence of individual publications, not an atomic transaction. Failure stops remaining segments and reports the identifiers already created.
3. A lookup verifies the returned identifier. An uncertain create response is reconciled before another publication; there is no assumed idempotency key in this binding.

### Delete selected post

1. The selected own post is read to establish its identifier and current content. **Stop and confirm with the operator before proceeding** with irreversible removal.
2. The deletion response must explicitly report successful deletion. A permission or missing-resource error is not treated as a deleted post. An uncertain outcome requires a read before another delete.

## Patterns

- Read APIs may return partial data and errors together.
- Thread creation can leave a published prefix if a later segment fails.
- Post permission and plan availability differ from media-upload success.

## Known limitations

No autonomous replies, relationship tracking, processed-mention database, media uploading, quote posts, scheduled posts or invented fixed280-character rule. Current account/API constraints govern acceptance. Recent search is limited to the last seven days; older context needs a separately supported API.

## Tools

| Operation | Description | Category |
|---|---|---|
| Read mentions/posts/search | Retrieve visible post evidence | Read |
| Create post/reply | Publish the supplied text | Write |
| Delete post | Remove the explicitly selected own post | Destructive |

## Verification checklist

- Read pagination and partial errors are preserved.
- Each published segment has its returned post identifier.
- Confirmation covered the final text and target before publication/deletion.
- Partial threads and uncertain write outcomes remain explicit.

Sources: X APIv2 [create](https://docs.x.com/x-api/posts/create-post), [delete](https://docs.x.com/x-api/posts/delete-post), [mentions](https://docs.x.com/x-api/users/get-mentions), [lookup](https://docs.x.com/x-api/posts/get-post-by-id), [recent search](https://docs.x.com/x-api/posts/search-recent-posts), retrieved 2026-10-09.
