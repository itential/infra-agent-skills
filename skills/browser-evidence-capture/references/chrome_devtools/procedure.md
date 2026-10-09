# Chrome browser evidence capture

Official Chrome DevTools MCP operations capture evidence from an authorized page without submitting forms or altering application configuration.

## Common Sequences

- Inspect an existing page: **List pages → Capture page → Read console → Read network activity**.
- Inspect a local artifact or requested URL: **Open inspection page → Wait for expected text → Capture page → Read console → Optional snapshot audit → Close inspection page**.

### List pages

The page inventory identifies the current page IDs and locations. Success is a page list from which the requested target is unambiguous. A connection or browser-launch failure is reported as a tool failure, not a missing page. An existing authenticated tab remains the operator's session; the inspection does not close or navigate it away.

### Open inspection page

The new-page operation opens the requested authorized location and returns page identity. A named isolated browser context separates its cookies/storage from other contexts when independent local-artifact inspection is needed; pages sharing that context share storage. Success is an opened page with the expected location. A timeout or browser-launch failure stops this sequence with its actual error. This scope does not automatically sign in, install software, enter credentials, or submit application forms. A local file's scripts can fetch remote resources, so a local path is not proof of network isolation.

### Wait for expected text

The documented text wait uses one or more expected text strings supplied by the artifact/request and a bounded timeout. It completes when any selected text appears, not when every resource has loaded or a canvas has finished drawing. A timeout is reported as incomplete evidence. No universal rendering threshold is asserted.

### Capture page

A fresh accessibility snapshot returns page text and element identifiers. A screenshot captures the visible viewport, full page, or a selected element from that snapshot. Full-page and element screenshot modes are alternatives. Success is returned snapshot content and an image or saved artifact path. File outputs use a new destination; immediately before overwriting an existing artifact, **stop and confirm with the operator before proceeding**. A failure to capture produces no assertion about page correctness. Login, access-denied, or error content is reported as observed rather than replaced with expected application data.

### Read console

The console listing retrieves messages since the last navigation, optionally including preserved messages from earlier navigations. Pagination/filter scope is recorded. A selected message detail operation returns further information and stack data where available. Success is a message collection or detail; an empty collection means no messages in that captured scope, not a clean application bill of health. A tool failure is not an empty collection.

### Read network activity

The network listing retrieves observed requests since navigation, with optional preserved earlier activity. A selected request detail operation uses an identifier from that listing. Success returns the request/response detail actually captured. The publisher explicitly documents that request details can expose cookies and response cookies; authorized evidence output excludes secrets. Observed routes do not establish a vendor-supported API contract and this procedure does not replay them. Failed requests, missing bodies, and tool failures are retained as such.

### Optional snapshot audit

A Lighthouse snapshot audit analyzes the page's current state without using its reload mode. Success returns the supported audit results/reports. The current tool covers accessibility, SEO, best practices, and agentic browsing; it excludes performance. Performance scores are not inferred from these results. A tool error is reported without a fabricated score.

### Close inspection page

The close operation removes only the dedicated inspection page identified in this sequence. Immediately before closing a page that might contain unsaved live work, **stop and confirm with the operator before proceeding**. A page inventory verifies closure. The publisher prohibits closing the browser's last remaining page; that restriction is retained rather than bypassed.

## Patterns

The current publisher contract differs from older NetClaw examples: page IDs are explicit, the text wait takes an array, and the request identifier is the documented request ID parameter. A screenshot, console result, and audit measure different things; none alone proves semantic correctness of a visualization.

The publisher warns that the MCP exposes browser content to its client. Usage telemetry is enabled by default and has a documented opt-out; performance tooling can separately contact the CrUX service. The selected tool subset does not run performance tracing. Configuration controls and bindings are documented in the companion reference.

## Known limitations

Google Chrome and Chrome for Testing are the publisher-supported browsers. Interactive click/fill, JavaScript evaluation, download/upload, configuration changes, site authentication, and API discovery claims are excluded. The tool reference does not define stable error strings or a complete timeout catalogue; actual tool errors remain authoritative. This procedure is an evidence collection sequence, not a vendor-independent visual correctness decision tree.

## Tools

| Operation | Description | Category |
|---|---|---|
| List pages | Identify browser page targets | Read |
| Open inspection page | Load requested evidence target | Browser navigation |
| Wait for expected text | Observe a specified text condition | Read |
| Capture page | Capture accessibility text and image | Read/local artifact |
| Read console | Retrieve observed console messages | Read |
| Read network activity | Retrieve captured requests and details | Read |
| Optional snapshot audit | Capture current-page audit results | Read/local artifact |
| Close inspection page | Remove dedicated inspection tab | Browser lifecycle |

Literal bindings and citations are in [endpoints.md](endpoints.md).

## Verification checklist

- Every result carries the correct page identity and captured scope.
- Snapshot/image paths exist in the tool result; errors are not converted into successful captures.
- Console and network pagination/filter limits are explicit.
- No performance score, offline guarantee, or semantic correctness claim is inferred.
- Dedicated inspection-page cleanup respects the last-page restriction and existing operator work.
