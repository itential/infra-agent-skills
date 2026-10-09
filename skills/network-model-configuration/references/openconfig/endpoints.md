# OpenConfig gNMI configuration bindings

Sources: [gNMI v0.11.0 specification](https://github.com/openconfig/reference/blob/master/rpc/gnmi/gnmi-specification.md) and [protobuf](https://github.com/openconfig/gnmi/blob/master/proto/gnmi/gnmi.proto), retrieved 2026-10-09.

| Operation | Literal binding | Fields |
|---|---|---|
| Discover support | `gnmi.gNMI.Capabilities(CapabilityRequest)` | `supported_models`, `supported_encodings`, `gNMI_version`. |
| Apply transaction | `gnmi.gNMI.Set(SetRequest)` | Optional `prefix`; ordered `delete[]` paths, `replace[]` and `update[]` messages. Each update has `path` and a schema-compatible `val` (`TypedValue`). |
| Inspect result | `SetResponse` | `response[]` containing operation `path` and `op`, with overall RPC status and target timestamp. Generated bindings are authoritative for deprecated status fields. |

`union_replace` is excluded from this procedure and must not be combined with the other operation groups. All paths and addresses are supplied by the approved target schema and configuration.

| Native error | Meaning and response |
|---|---|
| `UNAUTHENTICATED` | Authentication failed; correct credentials. |
| `PERMISSION_DENIED` | Identity cannot modify that path; correct authorization. |
| `INVALID_ARGUMENT` | Unparseable path, invalid key combination/value, or invalid replacement; correct the model payload. |
| `NOT_FOUND` | Requested update/replacement path is invalid for the target schema. |
| `UNIMPLEMENTED` | Target does not support the supplied encoding. |
| `ABORTED` | The transaction did not apply; retain the failing operation's specific error. |

The specification's prose uses historical `Update.value` and status fields in places; current generated protobuf uses `Update.val`. The binding here follows the publisher's current protobuf rather than reproducing stale field names.
