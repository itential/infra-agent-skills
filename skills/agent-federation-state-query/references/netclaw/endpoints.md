# NetClaw federation read bindings

Primary publisher sources: [daemon HTTP contract](https://github.com/automateyournetwork/netclaw/blob/95bb17e27a6a2538fcb0168d0b1d0ab5bbe34692/specs/052-n2n-federation/contracts/n2n-daemon-api.md), [n2n-mcp README](https://github.com/automateyournetwork/netclaw/blob/95bb17e27a6a2538fcb0168d0b1d0ab5bbe34692/mcp-servers/n2n-mcp/README.md), [MCP implementation](https://github.com/automateyournetwork/netclaw/blob/95bb17e27a6a2538fcb0168d0b1d0ab5bbe34692/mcp-servers/n2n-mcp/server.py), commit `95bb17e27a6a2538fcb0168d0b1d0ab5bbe34692`, inspected 2026-10-09.

Documented local base: `http://127.0.0.1:8179`. The daemon's existing authorized local context is required. `BGP_DAEMON_API` configures the companion MCP proxy; this reference does not broaden the daemon's localhost trust boundary.

| Operation | Literal binding | Response |
|---|---|---|
| Read overview | `GET /n2n/status` | `enabled`, `identity`, `peers` with identity/state/inventory freshness |
| Read peer | `GET /n2n/peers/{identity}` | Federation peer, consent state, budget use |
| Read cached inventory | `GET /n2n/peers/{identity}/inventory` | Cached capability inventory, `received_at`, `stale` |

The companion registered tools are `n2n_status()` and `n2n_peer_capabilities(peer, query?)`; direct HTTP reads avoid assuming their optional TOON/GCF serializer returns JSON text. The peer identifier comes from status and is encoded as one path value.

Documented error envelope: `{"error":{"code":"<code>","message":"<detail>"}}`. The contract's cross-operation reserved codes include `not_allowlisted`, `budget_exhausted`, `rate_limited`, `approval_expired`, `severed`, and `peer_offline`; it does not assert that every read can produce all of them. No automatic mutation or fixed retry interval is inferred from those codes.
