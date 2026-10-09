---
name: firewall-policy-installation
description: >-
  Install an existing controller policy package onto selected managed firewalls. Use for FortiManager policy-package and device-setting validation, preview, immediate or scheduled installation. Covers Fortinet FortiManager 7.6. Assumes an authenticated FortiManager web console and an existing policy package.
---

# Firewall policy installation

Install an existing controller policy package onto selected managed firewalls.

## When to use this skill

Use for FortiManager policy-package and device-setting validation, preview, immediate or scheduled installation.

## Universal concepts

No common wire protocol is implied by this capability. A controller-side package and an installation outcome are different states. Preview and validation precede the confirmed installation, and per-device failures remain visible.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

This procedure uses the documented console wizard; it does not create policies, invent a JSON-RPC binding or claim device traffic validation.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated FortiManager web console and an existing policy package. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
