# Markmap Markdown rendering

Produce a mind-map HTML artifact from supplied Markdown.

### 1. Resolve input and output

The CLI takes an existing Markdown input and an output filename. The output is an HTML document containing the visualization; the publisher CLI does not document a standalone SVG export in this interface. `markmap --version` identifies the available version.

### 2. Render

The documented noninteractive form is `markmap --no-open --output <output.html> <input.md>`. `--offline` inlines the required assets when a self-contained HTML file is requested; `--no-toolbar` omits viewer controls. Before replacing an existing output: stop and confirm with the operator before proceeding.

### 3. Verify the artifact

The output HTML displays the supplied hierarchy when opened in a compatible browser. CLI errors or an absent/unloadable output remain failures. The usage page gives no exhaustive error strings or exit-code catalogue; the actual diagnostic and exit result remain part of the report.

## Patterns

Without the no-open option the CLI can launch a browser. Watch mode is a separate continuing development process and is not needed for a single artifact.

## Known limitations

HTML output only. NetClaw theme names, fixed character limits, topic selection and SVG download claims are not part of this CLI contract.

## Tools

| Mechanism | Description | Category |
|---|---|---|
| Local CLI runner | Run an installed Markmap CLI | Local rendering |

## Verification checklist

- Input and output paths are explicit.
- The result is identified as HTML.
- The file renders the supplied hierarchy.
- Any overwrite was confirmed.

## Sources

- [Markmap CLI](https://markmap.js.org/docs/packages--markmap-cli). Retrieved 2026-10-09.
