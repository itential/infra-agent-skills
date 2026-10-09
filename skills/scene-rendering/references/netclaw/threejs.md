# NetClaw Three.js topology scene

Render an explicitly supplied canonical topology into a local HTML scene with the pinned NetClaw Python modules.

## Common Sequences

- Local scene: **Validate model** → **Build scene** → **Write HTML** → **Open artifact**.

### Validate model

The publisher's canonical model represents devices, interfaces, and link endpoints explicitly. Its validation rejects a mismatched interface parent or a link to a missing device/interface. Validation failure ends scene construction. Roles and operational state are supplied observations; absent evidence remains unclassified or unknown, rather than inferred from a hostname. This path uses procedural geometry and does not fetch external models.

### Build scene

The scene builder lays out device positions and interface offsets and returns a payload containing devices, links, source identity, and legend. The HTML builder embeds that payload and the bundled runtime. Publisher defect: the source label is inserted directly into HTML, without escaping. Untrusted labels are outside this procedure; a fixed, trusted display label is required until the publisher corrects interpolation. The metadata filter is only a top-level key denylist and is not a guarantee that nested values contain no secrets; approved non-sensitive input is a prerequisite.

### Write HTML

The writer returns the path after writing the HTML to the publisher's output directory. File errors are failures, not a delivered artifact. Publisher defect: filenames combine a seconds-resolution timestamp with a sanitized snapshot identifier, so repeated writes with the same identifier can overwrite a file. For replacement of an existing artifact: stop and confirm with the operator before proceeding. A new per-render identifier and serial invocation avoid the known same-ID collision; the implementation provides no atomic no-clobber guarantee.

### Open artifact

The browser helper opens the returned local path and returns no display status. A successful file write establishes an HTML artifact; it does not establish a functioning browser/WebGL render. Browser display failure remains a separate result.

## Patterns

The canonical model validates endpoint references but does not independently discover links or verify network state. Scene construction mutates layout positions in the input model. The static artifact reflects its snapshot, not live telemetry.

## Known limitations

No free-form topology inference, live source adapters, external asset selection, health assessment, or automatic distribution. Filename collision, label interpolation, and shallow metadata filtering are publisher defects documented above.

## Tools

Assumes the local modules described in [the bindings](threejs-endpoints.md).

| Operation | Description | Category |
|---|---|---|
| Validate model | Check canonical endpoint and parent references | Local validation |
| Build scene | Produce payload and embedded HTML | Local transformation |
| Write artifact | Save HTML in the publisher output directory | Local file write |
| Open artifact | Request the default browser to open the local file | Local display |

## Verification checklist

- Model validation completed without missing references.
- Payload device/link identities match supplied input.
- The returned path identifies the written HTML.
- Artifact creation and browser rendering are reported separately.

## Sources

- [topology_model.py](https://github.com/automateyournetwork/netclaw/blob/95bb17e27a6a2538fcb0168d0b1d0ab5bbe34692/workspace/skills/threejs-network-viz/topology_model.py). Retrieved 2026-10-09.
- [scene_builder.py](https://github.com/automateyournetwork/netclaw/blob/95bb17e27a6a2538fcb0168d0b1d0ab5bbe34692/workspace/skills/threejs-network-viz/scene_builder.py). Retrieved 2026-10-09.
- [html_template.py](https://github.com/automateyournetwork/netclaw/blob/95bb17e27a6a2538fcb0168d0b1d0ab5bbe34692/workspace/skills/threejs-network-viz/html_template.py). Retrieved 2026-10-09.
- [output.py](https://github.com/automateyournetwork/netclaw/blob/95bb17e27a6a2538fcb0168d0b1d0ab5bbe34692/workspace/skills/threejs-network-viz/output.py). Retrieved 2026-10-09.
