# Cisco Genie — State Collection Bindings

Sources (Cisco rolling documentation; retrieved 2026-10-09):

- [Genie Utilities](https://pubhub.devnetcloud.com/media/genie-docs/docs/userguide/utils/index.html).
- [Ops Use](https://pubhub.devnetcloud.com/media/genie-docs/docs/userguide/Ops/user/ops.html).

Coverage reference: [Genie Feature Browser](https://pubhub.devnetcloud.com/media/genie-feature-browser/docs/).

Additional sources: [Genie Cookbook](https://pubhub.devnetcloud.com/media/genie-docs/docs/cookbooks/genie.html)
and [Writing a Parser](https://pubhub.devnetcloud.com/media/pyats-development-guide/docs/writeparser/writeparser.html),
rolling documentation retrieved 2026-10-09.

## Existing device session

The device is a Genie-capable device with an already approved connection.

```python
parsed = device.parse('show version')
learned = device.learn('interface')
state = learned.info
```

These are separate collection operations. The returned parser structure follows its parser
schema; feature learning returns an Ops object. Neither supplies universal health thresholds.

## Captured command output

```python
parsed = device.parse('show ip interface brief', output=captured_text)
```

**Binding assumption:** the device wrapper forwards `output` to the selected parser. The parser
development guide documents the parser-level optional output; this wrapper form also requires
verification with the installed Genie release before use. This form was also checked offline
with Genie 25.2 against synthetic IOS XE interface output during authoring.

`captured_text` is the caller's saved output for the selected device OS/parser. There is no
connection/execute call in this path. Errors remain parsing or coverage failures, not a network
health finding.

## In-memory comparison

```python
from genie.utils.diff import Diff
comparison = Diff(before_state, after_state, exclude=requested_exclusions)
comparison.findDiff()
```

`before_state` and `after_state` are collected dictionaries or Ops objects. The explicit
`requested_exclusions` input defines the intended comparison; CLI default exclusion behavior
must not be assumed for every Python binding.
