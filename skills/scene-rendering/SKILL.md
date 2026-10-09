---
name: scene-rendering
description: >-
  Render an approved scene or explicitly supplied topology using the selected renderer. Use for Blender single-frame or bounded animation output, NetClaw Three.js HTML scenes, or a static NetClaw Unreal topology render. Covers Blender CLI and NetClaw Three.js / Unreal Editor renderers. Assumes the selected renderer, approved local assets and destination, and any required compatible Editor connection are available.
---

# Scene rendering

Render an approved scene or explicitly supplied topology using the selected renderer.

## When to use this skill

Use for Blender single-frame or bounded animation output, NetClaw Three.js HTML scenes, or a static NetClaw Unreal topology render. Supported platforms: Blender CLI and NetClaw Three.js / Unreal Editor renderers.

## Universal concepts

No common wire protocol is implied by this capability. The supplied scene or topology determines the artifact. Rendering does not discover or validate network state.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

No automatic topology discovery, inferred device roles or health, external model discovery, arbitrary script execution, or automatic distribution is included.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes the selected renderer, approved local assets and destination, and any required compatible Editor connection are available. The selected procedure lists required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
