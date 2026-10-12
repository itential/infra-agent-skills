# Cisco Genie — State Collection Bindings

Sources (Cisco rolling documentation; retrieved 2026-10-09):

- [Genie Utilities](https://pubhub.devnetcloud.com/media/genie-docs/docs/userguide/utils/index.html).
- [Ops Use](https://pubhub.devnetcloud.com/media/genie-docs/docs/userguide/Ops/user/ops.html).

Coverage reference: [Genie Feature Browser](https://pubhub.devnetcloud.com/media/genie-feature-browser/docs/).

## Existing device session

The device is a Genie-capable device with an already approved connection.

```python
parsed = device.parse('show version')
learned = device.learn('interface')
state = learned.info
```

Parsing returns the parser's schema structure; learning returns an Ops object.

**Binding assumption:** the `device.learn(...)` shortcut and the `.info` attribute are not shown on
the cited Ops page, which documents `Lookup(...).ops.<feature>(device=...)` followed by `.learn()`.
Confirm the form against the installed Genie release.

## Captured command output

```python
parsed = device.parse('show ip interface brief', output=captured_text)
```

**Binding assumption:** the device wrapper forwards `output` to the selected parser. Only the
parser-level optional output is documented; confirm this wrapper form against the installed Genie
release before relying on it.

`captured_text` is saved output for the selected device OS/parser; no connection is made.

## In-memory comparison

```python
from genie.utils.diff import Diff
comparison = Diff(before_state, after_state, exclude=requested_exclusions)
comparison.findDiff()
```

`before_state` and `after_state` are collected dictionaries or Ops objects. The cited page
documents no default exclusions for the Python `Diff`, so verify before assuming any;
`requested_exclusions` defines the comparison. Ops objects document their own `.diff()` form.
