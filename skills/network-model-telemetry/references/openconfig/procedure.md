# OpenConfig gNMI: collect model-defined state

Discover target support and retrieve a bounded snapshot or subscription.

Source: [gNMI specification](https://github.com/openconfig/reference/blob/master/rpc/gnmi/gnmi-specification.md), v0.11.0 (March 2026), sections 3.1–3.3 and 3.5, retrieved 2026-10-09. Bindings appear in [endpoints.md](endpoints.md).

## Common Sequences

- Small snapshot: Discover support → Read snapshot → Report observations.
- One-off large subtree: Discover support → Start subscription in one-off mode → Report observations.
- Ongoing observation: Discover support → Start subscription in polled or streaming mode → End subscription → Report observations.

## Discover support

The session uses TLS and authenticated, authorized RPCs. Capability discovery returns the target's gNMI version, supported models with versions, and supported encodings. The requested paths come from those supported schemas; capability discovery does not enumerate every usable path.

Success: version, models and encoding are known for the selected target. Authentication or authorization failure ends this attempt; the client does not fall back to an unencrypted connection.

## Read snapshot

The snapshot query selects paths, a supported encoding, and the required configuration/state/operational data subset. Each returned notification carries the collection timestamp of its requested path. Small subtrees suit this operation; the specification recommends one-off subscription for large subtrees.

Success: the response contains notifications for the requested paths and the RPC completes successfully. A nonexistent path, unsupported path/encoding, or malformed path is distinguished by the native errors listed in the bindings. The request is corrected against the target's schema rather than interpreting an error as an empty result.

## Start subscription

The initial request defines a nonempty, fixed set of paths and one collection mode. One-off collection ends after synchronization and successful RPC closure. Polled collection retains the RPC and requests a new observation batch when needed; each batch ends with synchronization. Streaming collection supplies changes or samples until cancelled.

Streaming paths choose change-triggered, sampled, or target-selected behavior. A requested sample/heartbeat interval uses the units in the bindings. Unsupported intervals cause a request error. A target-selected subscription does not prescribe a client sample interval. A syntactically valid path that does not yet exist can remain subscribed without producing a value; that silence is not a transport failure.

Success: the initial synchronization marker arrives, followed by the mode's documented completion or ongoing behavior. A second subscription definition on the same RPC, or polling before establishing it, is invalid. Additional paths require a separate subscription. An interrupted stream is reported as incomplete.

## End subscription

The client cancels the specific subscription RPC when the requested observation window ends. Closing the entire session is also defined but would end other subscriptions using it.

Success: the intended RPC is closed and the collected window is identified. Cancellation is normal termination of observation, not a configuration deletion.

## Report observations

The result retains target, paths, model versions, timestamps, native RPC status, and synchronization/completion state. Received messages need not arrive in timestamp order and do not form a single simultaneous snapshot. Deletion notifications remove the indicated subtree from the observed state; a missing value alone is not a deletion. An atomic response describes only the requested subset, so unrequested leaves cannot be presumed removed.

## Patterns

An updates-only subscription omits the initial current values. In one-off or polled mode it therefore returns only synchronization, not a populated snapshot. Changing a path's value to its schema default is an update, not just a delete.

## Known limitations

Target and model compatibility remain platform-specific. The specification's prose contains an inconsistent numeric label for one invalid-argument example; this procedure uses the canonical gRPC symbolic status and the current protobuf contract. No retry cadence, target polling budget, or arbitrary model path is invented here.

## Tools

| Operation | Description | Category |
|---|---|---|
| Discover support | Obtain gNMI version, models and encodings | gNMI RPC |
| Read snapshot | Retrieve a bounded state subtree | gNMI RPC |
| Start or poll subscription | Collect model-defined updates | gNMI streaming RPC |
| End subscription | Cancel the selected observation RPC | Client stream control |

## Verification checklist

- Models, paths and encoding match the selected target.
- RPC errors remain distinct from absent values.
- Synchronization and termination match the chosen mode.
- The reported time window and incomplete streams are explicit.
