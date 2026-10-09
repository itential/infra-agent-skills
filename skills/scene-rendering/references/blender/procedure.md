# Blender background frame rendering

Render an existing scene with the publisher command-line interface.

### 1. Resolve the scene and renderer

`blender --version` identifies the installed release. The input is an approved existing `.blend` file with its assets; this procedure does not execute supplied Python snippets to construct a scene. `blender -E help` lists available rendering engines. Unavailable assets or engines remain environment/rendering errors.

### 2. Render the requested frame range

For one frame, the documented form is `blender --disable-autoexec -b <scene.blend> -o <output-prefix> -F PNG -f <frame>`. For a bounded animation, the final arguments are `-s <start> -e <end> -a`. Before an output would replace an existing artifact: stop and confirm with the operator before proceeding.

Arguments execute in order: scene loading precedes output overrides and the render trigger comes last. Uppercase format values are case-sensitive. Background mode does not require an open application window. Automatic Python execution remains disabled; scenes that depend on it require separate platform-specific guidance, not silent enablement.

### 3. Verify output

Blender saves each rendered frame using the requested output prefix and frame-number expansion. The result includes produced filenames and renderer diagnostics. A missing output or render error is not a successful frame. The documentation does not establish a universal first-call timeout or safe retry interval; a timed-out process has unknown completion until its state and outputs are resolved.

## Patterns

Output names without a frame placeholder receive a frame-number suffix. Loading a scene can override earlier command-line settings, which is why output arguments follow the scene filename.

## Known limitations

No claim is made that disabling automatic scripts is a complete sandbox. No Windows-only requirement, universal device-count limit, or automatic scene-clearing step is implied.

## Tools

| Mechanism | Description | Category |
|---|---|---|
| Local CLI runner | Run Blender in background mode | Local rendering |

## Verification checklist

- Approved scene and assets resolve.
- Render arguments precede the final frame/animation trigger.
- Requested frames and generated artifacts match.
- Timeout or render failures remain explicit.

## Sources

- [Blender command-line rendering](https://docs.blender.org/manual/en/latest/advanced/command_line/render.html). Retrieved 2026-10-09.
- [Blender command-line arguments](https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html). Retrieved 2026-10-09.
