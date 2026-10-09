# Splunk index and instance discovery: bindings

Publisher `splunklib.client`; `service` is an already authenticated, TLS-verifying Service.

| Operation | SDK binding | Result |
|---|---|---|
| Instance metadata | `service.info` | Dictionary of instance information |
| Index pages | `service.indexes.iter(pagesize=page_size)` | Iterator of Index entities |
| Bounded index list | `service.indexes.list(count=count, offset=offset)` | List of Index entities |

`page_size` is positive; names are read from returned entity objects. SDK errors propagate rather than becoming zero rows. This skill never invokes Index delete, clean, submit or attach methods.

## Sources

- [Splunk publisher Python SDK client implementation](https://github.com/splunk/splunk-sdk-python/blob/master/splunklib/client.py). Retrieved 2026-10-09.
