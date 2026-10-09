# Vault mount API bindings

Sources: [mounts](https://developer.hashicorp.com/vault/api-docs/system/mounts), [auth](https://developer.hashicorp.com/vault/api-docs/system/auth), [HTTP API](https://developer.hashicorp.com/vault/api-docs), current, retrieved 2026-10-09.

Base: the authorized Vault address plus `/v1`. Authentication: `X-Vault-Token: <token>` (or bearer token); namespace where required: `X-Vault-Namespace: <namespace>`. TLS verification is expected. Paths below are relative to that prefix.

| Operation | Method and path | Input/result |
|---|---|---|
| Read mounts | `GET /sys/mounts` | `data` map keyed by mount path |
| Read mount | `GET /sys/mounts/{path}` | Engine configuration |
| Read tuning | `GET /sys/mounts/{path}/tune` | Effective TTL values in seconds |
| Enable | `POST /sys/mounts/{path}` | Required `type`; optional `description`, `config`, `options`; KV v2: `type: kv`, `options: {version: "2"}` |
| Tune | `POST /sys/mounts/{path}/tune` | Requested `default_lease_ttl`, `max_lease_ttl`, `description`, or other fields verified against the current schema |
| Disable | `DELETE /sys/mounts/{path}` | Documented 204, with 200 possible if warnings are returned |
| Read auth methods | `GET /sys/auth` | `data` map keyed by auth mount |

Common response handling: 200 has data/warnings; 204 has no body. Errors use `errors`. 400 invalid request; 403 credentials/policy/CORS; 404 absent or inaccessible path (or empty LIST); 405 method unsupported; 412 Enterprise consistency precondition (retry with backoff after reading error); 429 standby-health response or quota pressure depending on endpoint; 472/473 replication/standby health states; 500 internal error; 501 uninitialized; 502 upstream failure; 503 sealed, maintenance, or overload. These statuses do not imply a failed mutation had no effect. Unknown diagnostics remain unverified and require platform guidance.
