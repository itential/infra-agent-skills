# Terraform Registry artifact discovery

Find a provider or module and retrieve its documentation through HashiCorp's Terraform MCP server.

Source: [Terraform MCP server reference](https://developer.hashicorp.com/terraform/mcp-server/reference), current reference, retrieved 2026-10-09. Bindings are in [endpoints.md](endpoints.md).

## Common Sequences

- Provider component: Discover tools → Search provider documentation → Read component documentation.
- Module: Discover tools → Search modules → Read module documentation.
- Latest release: Discover tools → Read latest version for the identified provider or module.

## Discover tools

The publisher separates public registry, private registry, and Terraform-management toolsets. The authenticated client exposes the enabled tool definitions and their input schemas. Missing tools mean the required toolset or server version is unavailable; they do not mean no artifact exists. The selected tool's live schema supplies the arguments; undocumented argument names are not guessed.

## Search provider documentation

The provider search returns matching documentation identifiers, titles, and categories. Capabilities discovery can first enumerate supported resources, data sources, and functions. A selected result supplies the component identifier for Read component documentation. Search results alone are not the provider's full documentation.

## Read component documentation

The component lookup returns documentation for the chosen result. The outcome includes the namespace/provider/component and version actually retrieved; a mismatch leaves the requested lookup unresolved.

## Search modules

The module search returns candidates with module metadata. Private-registry searches use the configured organization and authentication context. An empty successful search means no match within that search scope. Authentication, connection, and tool errors remain failures rather than empty results.

## Read module documentation

The selected module lookup returns its inputs, outputs, examples, and submodule information. Retrieval is complete when the requested module's documentation is returned. Choosing a deployment architecture from those examples is outside this procedure.

## Read latest version

The corresponding lookup returns the latest published version for the identified public provider or module. This is a latest-version lookup, not a list of every historic release.

## Patterns

The tool names in older wrappers do not define the current publisher's interface. Identity and version are retained with retrieved documentation so a later implementation does not silently mix releases.

## Known limitations

The reference does not provide a stable exhaustive error-code contract for these tools. A tool error is reported with its native diagnostic; there is no invented retry count or rate-limit value. Private-registry authentication and access can hide artifacts from discovery.

## Tools

| Operation | Description | Category |
|---|---|---|
| Discover tools | Reads enabled tool definitions and input schemas | MCP discovery |
| Search artifact | Finds provider documents or module candidates | Read |
| Read documentation | Retrieves the selected artifact's documentation | Read |
| Read latest version | Retrieves the latest public artifact version | Read |

## Verification checklist

- Search and detail refer to the same artifact identity.
- Private versus public registry scope is explicit.
- The result preserves the retrieved version and native tool failure, if any.
