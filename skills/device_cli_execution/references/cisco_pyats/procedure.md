# Cisco Unicon — Execute or Configure an Approved Device

Uses the selected Unicon plugin to send a caller-supplied, platform-documented CLI payload.

Sources (Cisco rolling documentation; retrieved 2026-10-09):

- [Connections](https://pubhub.devnetcloud.com/media/unicon/docs/user_guide/connection.html).
- [Common Services](https://pubhub.devnetcloud.com/media/unicon/docs/user_guide/services/generic_services.html).

## Common Sequences

- **Read command:** Connect session → Execute command → Disconnect session.
- **Configuration:** Connect session → Configure device → Execute verification command → Disconnect session.

## Connect session

The testbed selects the OS, connection, and credentials. Unicon creates the session and initializes
it with the plugin's commands. **If initialization changes live settings: stop and confirm with
the operator before proceeding.** Success is an established session and its connection log.
The optional initialization overrides are in [endpoints.md](endpoints.md); Linux and ISE do not
provide configuration initialization commands. Connection/authentication failures leave the
sequence incomplete and retain their error evidence.

## Execute command

The execute service sends the supplied payload and returns text for one command, or a command-keyed
dictionary for multiple commands. **For a clear, reset, reload, delete, or other mutating payload:
stop and confirm with the operator before proceeding.** A matching dialog can answer a documented
prompt after approval; automated replies are not approval themselves.

- `SubCommandFailure` records service failure; the output and underlying cause determine the
  platform-specific next step, not an automatic repeat of a possibly completed change.
- `StateMachineError` indicates an unexpected ending state when state changes were not allowed.
  A different ending state requires the selected operation's documented behavior.
- A timeout or an EOF leaves completion uncertain. Cisco documents disconnect/reconnect for EOF,
  but that does not justify replaying a mutating payload.

## Configure device

**Before applying the exact resolved configuration: stop and confirm with the operator before
proceeding.** The configure service enters the plugin's configuration state and sends the supplied
lines, with an optional reply dialog. Success at this layer is service completion with its output;
command-specific errors or a service exception mean the configuration outcome requires inspection.
The selected platform's documented save/commit and success checks remain required inputs. If they
are missing, completion of a persistent configuration is unknown; consult platform-specific guidance.
There is no blanket cross-platform automatic-commit guarantee.

## Execute verification command

The caller's platform procedure supplies the read command and exact expected state. The execute
service returns the evidence for that check. A syntactically accepted configuration is insufficient
proof of the intended state. Missing verification criteria leave the requested change unverified.

## Disconnect session

The connection's disconnect operation closes the session. Success is its completed disconnection;
a disconnect error is reported separately from the payload's observed result.

## Patterns

- The service's normal prompt handlers may already answer some confirmation prompts.
- Error detection depends on plugin and supplied patterns. An empty error-pattern list disables
  that check; it does not turn an error-producing command into a successful change.

## Known limitations

- Commit, persistence, rollback, reload completion, and standby support are platform-specific.
- No destructive payload or catch-all prompt reply is supplied by this skill.
- Unicon's generic execute error-pattern default can be empty. Success must therefore include
  the selected platform's output/state verification, not just absence of an exception.

## Tools

| Mechanism | Description | Category |
|---|---|---|
| Unicon device session | Transport approved CLI payloads and return their output | SSH / console |

## Verification checklist

- [ ] Connection initialization and the actual payload were within the approved scope.
- [ ] The correct platform plugin and prompt behavior were selected.
- [ ] Service errors and command-specific output were checked.
- [ ] Required save/commit and postconditions came from the platform procedure.
- [ ] Session disconnection completed or its failure was reported.
