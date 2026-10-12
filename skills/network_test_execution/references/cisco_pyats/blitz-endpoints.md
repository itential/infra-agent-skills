# Cisco Genie — Blitz Definition Bindings

Sources (Cisco rolling documentation; retrieved 2026-10-09):

- [Blitz Design](https://pubhub.devnetcloud.com/media/genie-docs/docs/blitz/design/index.html).
- [Blitz Usage](https://pubhub.devnetcloud.com/media/genie-docs/docs/blitz/usage/usage.html).

## blitz.yaml

Original minimal parse example; `dut` is a device in the supplied testbed.

```yaml
collect_version:
  source:
    pkg: genie.libs.sdk
    class: triggers.blitz.blitz.Blitz
  devices: [dut]
  test_sections:
    - capture:
        - parse:
            device: dut
            command: show version
```

There is no additional `testcases:` wrapper in this trigger-datafile example.

## Action-specific bindings

Cisco's [Blitz Design](https://pubhub.devnetcloud.com/media/genie-docs/docs/blitz/design/index.html)
links the action, saved-variable, output-verification, and advanced-action references. A selected
`api`, `rest`, `yang`, `diff`, or restoration action must use that action's documented binding.
No placeholder helper such as `some_check_function` is represented as a shipped API here.
