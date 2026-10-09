---
name: device-configuration-save
description: >-
  Read and persist a device configuration. Use for AOS-CX running/startup configuration retrieval and copying the running configuration to startup. Covers HPE Aruba AOS-CX REST API 10.13. Assumes an authenticated HTTPS API client for the target switch.
---

# Device configuration save

Read and persist a device configuration.

## When to use this skill

Use for AOS-CX running/startup configuration retrieval and copying the running configuration to startup.

## Universal concepts

No common wire protocol is implied by this capability. Active and startup configuration are separate resources. Persisting active configuration changes what is available at startup; confirmation covers the complete source configuration.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

No ISSU, firmware transfer, checkpoint restoration, configuration upload or invented checksum schema is included.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated HTTPS API client for the target switch. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
