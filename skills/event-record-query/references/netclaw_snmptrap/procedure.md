# NetClaw snmptrap stored-record queries

Read the publisher receiver’s existing local collection.

## Common Sequences

- Record lookup: **Check collection** → **Query records** → **Read selected detail**.
- Summary: **Check collection** → **Read native summary**.

### Check collection

Receiver status establishes whether the collection/store has been initialized and whether drops/parse errors affect it. An unstarted-store response is not an empty successful query. No receiver startup is implicit in a read request.

### Query records

The query applies supported filters and returns total matching count, returned count and trap rows in newest-received order. Offset/limit select additional pages. Concurrent arrivals and retention changes can shift offsets, so a multi-page read is not a consistent snapshot. All pages requested by the caller are accounted for with gaps explicit.

The published date-time schema accepts timezone-qualified input, but the implementation compares it with timezone-naive receive timestamps. Such comparisons can fail. Time filters are therefore blocked until a corrected installed implementation is verified; they are not silently dropped or replaced with an assumed timezone. A time-bounded request remains unsupported on this pin.

### Read selected detail

An ID returned by the list selects the complete record. Missing ID, not-found or error-prefixed text remains a failed detail lookup. A record disappearing between list and detail is not reconstructed from another record. SNMPv1/v2c observations retain parse errors and numeric OIDs. Current SNMPv3 rows are placeholders, not authenticated decoded traps. Full-detail serialization can return the community string unmasked although list display masks it; details are sensitive and the community value is excluded from reports.

### Read native summary

The corresponding native count/aggregation operation returns its named groups and totals over the retained collection. The same time-filter limitation applies. Totals describe received/stored data, with deduplication, retention and decode limits; they do not establish all events or traffic on the network.

## Patterns

Transport success and successful record decoding are independent. Embedded text errors must be inspected in addition to the MCP envelope.

## Known limitations

Store data is in memory; restarting a stopped receiver creates a new store. Retention cleanup occurs on insertion, so idle-store reads can contain older data. The publisher records bounded audit data locally; its pending/error status is distinct from receive success. The current SNMPv3 parser returns a placeholder and does not verify USM authentication or decrypt full varbinds, despite broader README wording.

## Tools

Assumes the authenticated client described in [the bindings](endpoints.md).

| Operation | Description | Category |
|---|---|---|
| Query records | Read filtered pages from the initialized store | Read |
| Read detail | Retrieve one returned record identity | Sensitive read |
| Read summary | Retrieve native counts/aggregations | Read |

## Verification checklist

- Collection scope and loss/parse limits are reported.
- Error text is not parsed as data.
- Unsupported time filters remain explicit.
- Page completeness is qualified for concurrent changes.
- Sensitive fields are not disclosed.

## Sources

- [NetClaw publisher receiver implementation](https://github.com/automateyournetwork/netclaw/blob/95bb17e27a6a2538fcb0168d0b1d0ab5bbe34692/mcp-servers/snmptrap-mcp/snmptrap_mcp_server.py). Retrieved 2026-10-09.
- [Publisher receiver guide](https://github.com/automateyournetwork/netclaw/blob/95bb17e27a6a2538fcb0168d0b1d0ab5bbe34692/mcp-servers/snmptrap-mcp/README.md). Retrieved 2026-10-09.
- [Publisher store behavior](https://github.com/automateyournetwork/netclaw/blob/95bb17e27a6a2538fcb0168d0b1d0ab5bbe34692/mcp-servers/snmptrap-mcp/message_store.py). Retrieved 2026-10-09.
- [Publisher record schema](https://github.com/automateyournetwork/netclaw/blob/95bb17e27a6a2538fcb0168d0b1d0ab5bbe34692/mcp-servers/snmptrap-mcp/models.py). Retrieved 2026-10-09.
- [Publisher trap parser](https://github.com/automateyournetwork/netclaw/blob/95bb17e27a6a2538fcb0168d0b1d0ab5bbe34692/mcp-servers/snmptrap-mcp/trap_parser.py). Retrieved 2026-10-09.
