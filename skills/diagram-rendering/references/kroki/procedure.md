# Kroki diagram rendering

Render supplied text using an available Kroki backend and supported output format.

## Common Sequences

- Render an image: **Select renderer** → **Render** → **Verify output**.

### Select renderer

The requested diagram language and output format must be supported by the selected Kroki deployment. The caller supplies a trusted rendering destination because diagram content is transmitted to that service. Backend-specific syntax and options remain those of the chosen renderer.

### Render

The rendering operation submits the source, diagram type and output format. The JSON form can carry diagram options; the plain-text form chooses type/format in its binding. Options from the JSON body take precedence over headers, which take precedence over query parameters. A rejected source or unavailable backend remains a rendering failure, preserving the service response rather than retrying with an unrelated diagram language.

### Verify output

The response contains the rendered image in the requested supported format. A service error body is not saved or reported as a successful diagram. Before overwriting an existing local artifact: stop and confirm with the operator before proceeding. The generated image reflects the input model; it does not verify real connectivity.

## Patterns

The compressed URL form is an alternative transport for encoded source, not a privacy boundary. PlantUML can include source in image metadata; its documented no-metadata option omits that embedded source when requested.

## Known limitations

No complete cross-backend error catalogue or guaranteed format matrix is assumed. Backend syntax validation, public-service capacity, authentication and quotas depend on the deployment. Content classification and automatic sharing are outside scope.

## Tools

Assumes the authenticated client described in [the bindings](endpoints.md).

| Operation | Description | Category |
|---|---|---|
| Render | Submit source to the selected rendering backend | Rendering API |
| Save artifact | Persist returned image bytes | Local file write |

## Verification checklist

- Renderer, deployment and format were explicitly selected.
- Service errors remain errors.
- The returned artifact is the requested image format.
- No network-health conclusion is inferred.

## Sources

- [Kroki usage](https://docs.kroki.io/kroki/setup/usage/). Retrieved 2026-10-09.
- [Diagram options](https://docs.kroki.io/kroki/setup/diagram-options/). Retrieved 2026-10-09.
