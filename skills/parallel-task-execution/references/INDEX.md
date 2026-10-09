# Parallel Task Execution — Platform Index

| Vendor / platform | Directory | Scope | Notes |
|---|---|---|---|
| Cisco pyATS | [cisco_pyats/](cisco_pyats/procedure.md) | Run independent callable invocations concurrently and collect their ordered results | This procedure does not determine whether device changes are independent or supply the operation executed by each worker. |
| Nornir | [nornir/procedure.md](nornir/procedure.md) | Host-scoped native read-only task execution | Host-keyed results; failed hosts may be skipped in later runs |

The platform reference contains its source citations, execution sequence, tools, and verification.
New platforms require their own procedure and a check of the router's shared claims.
