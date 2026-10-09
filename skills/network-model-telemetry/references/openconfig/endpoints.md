# OpenConfig gNMI telemetry bindings

Sources: [gNMI v0.11.0 specification](https://github.com/openconfig/reference/blob/master/rpc/gnmi/gnmi-specification.md) and [protobuf service](https://github.com/openconfig/gnmi/blob/master/proto/gnmi/gnmi.proto), retrieved 2026-10-09.

The authenticated TLS gRPC channel uses the operator-supplied target address. No universal device port or model path is assumed.

| Operation | Literal binding | Required interpretation |
|---|---|---|
| Discover support | `gnmi.gNMI.Capabilities(CapabilityRequest)` | Response `gNMI_version`, `supported_models`, `supported_encodings`. |
| Read snapshot | `gnmi.gNMI.Get(GetRequest)` | `path[]`, optional `prefix`, `type` (`ALL`, `CONFIG`, `STATE`, `OPERATIONAL`), `encoding`, `use_models[]`; response `notification[]`. |
| Subscribe | `gnmi.gNMI.Subscribe(stream SubscribeRequest)` | Initial `subscribe` contains `subscription[]`, `mode` (`ONCE`, `POLL`, `STREAM`), optional `prefix`, `encoding`, `use_models[]`, `updates_only`. |
| Specify stream behavior | Each `Subscription` | `path`, `mode` (`TARGET_DEFINED`, `ON_CHANGE`, `SAMPLE`), `sample_interval`, `suppress_redundant`, `heartbeat_interval`; intervals are nanoseconds. |
| Poll existing RPC | `SubscribeRequest(poll=Poll())` | Sent only on an established `POLL` subscription. |
| Interpret updates | `SubscribeResponse.update` or `.sync_response` | Notifications include `timestamp`, `prefix`, `update[]`, `delete[]`, optionally `atomic`; timestamps are nanoseconds since the Unix epoch. |

Errors: `NOT_FOUND` for valid snapshot paths with no current/default value; `UNIMPLEMENTED` for unsupported paths or encoding; `INVALID_ARGUMENT` for malformed paths, invalid subscription sequencing, or unsupported requested sampling interval. Authentication/permission errors remain `UNAUTHENTICATED`/`PERMISSION_DENIED` where returned. A valid subscribed path with no present value is not itself an error.

Source correction: specification section 3.5.1.1 labels an invalid-argument case with numeric 4; canonical gRPC `INVALID_ARGUMENT` is 3. Consumers should use generated status symbols, not that inconsistent prose number.
