# Splunk index and instance discovery

Read accessible index objects and instance information through the publisher SDK.

## Common Sequences

- Discover query scope: **Read instance** → **List indexes**.

### Read instance

The authenticated service's instance-information property returns system metadata as key/value pairs. Failure remains an access/transport error. Only requested non-secret metadata belongs in the report; this operation does not retrieve every configuration file.

### List indexes

The index collection is iterated with a chosen page size. Returned index entities expose their names and metadata; a requested count cap makes the inventory partial. Collection errors are not converted to an empty list. The SDK's list helper can load the collection at once; its iterator is the documented paged alternative. The observed collection confirms accessible indexes, not the caller's ability to read every event.

## Patterns

Collection identity and namespace matter across the SDK. Every uncached list makes a server request; a prior result is not automatically refreshed.

## Known limitations

No generic get-config wrapper is assumed. Broad configuration reads can expose sensitive settings and are outside this scope.

## Tools

Assumes the authenticated client described in [the bindings](endpoints.md).

| Operation | Description | Category |
|---|---|---|
| Read instance | Retrieve server information | Platform read |
| List indexes | Iterate accessible index entities | Log-source read |

## Verification checklist

- Authenticated service and requested scope are explicit.
- Pagination/count caps are reported.
- No inaccessible index is inferred absent.
- No configuration/credential dump is produced.

## Sources

- [Splunk publisher Python SDK client implementation](https://github.com/splunk/splunk-sdk-python/blob/master/splunklib/client.py). Retrieved 2026-10-09.
