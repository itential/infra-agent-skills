# AOS-CX configuration read and persistence

Retrieve running or startup JSON configuration, or copy the complete running configuration into startup on AOS-CX 10.13.

Sources: HPE Aruba [configuration retrieval](https://developer.arubanetworks.com/aoscx/v10.13/reference/get_fullconfigs-name), [configuration copy](https://developer.arubanetworks.com/aoscx/v10.13/reference/put_fullconfigs-to), [REST behavior](https://developer.arubanetworks.com/aoscx/v10.13/docs/tips-and-tricks-with-aos-cx-rest), retrieved 2026-10-09. Wire bindings are in [endpoints.md](endpoints.md).

## Common Sequences

- Inspect configuration: Read named configuration.
- Persist active configuration: Read named configuration for running and startup → Save running to startup → Read named configuration for startup.

### Read named configuration

The named-configuration read returns the requested running or startup configuration as a JSON object. Success is the returned configuration associated with the selected name. The API schema is generic table/configuration content; it does not define a CLI-text string, checksum or modification timestamp. Configuration data can contain sensitive settings and is handled as a configuration artifact rather than copied wholesale into a report.

### Save running to startup

The native copy operation uses running configuration as its source and startup configuration as its destination. This overwrites the startup configuration: stop and confirm with the operator before proceeding. Success is the documented successful copy response. The source and destination must differ; the publisher states that an identical source/destination fails. No upload body is needed for this local copy. A subsequent named startup read exposes the saved resource; the source does not prescribe a universal checksum or textual equality test.

At either operation, an invalid request requires correcting its name/arguments; unauthenticated or forbidden responses require valid session/access; a missing resource remains not found. Internal/server-unavailable responses remain failed operations. A timeout during saving leaves the outcome unknown; a startup read provides evidence before any newly confirmed retry. No universal retry interval is documented.

## Patterns

- Copying between existing configurations differs from uploading a replacement configuration.
- The source reference path uses the same REST API version as the destination operation.
- The publisher warns that some configuration-management writes are possible even when the REST service is configured read-only; that mode is not a sufficient mutation guard.

## Known limitations

- Saving overwrites startup configuration and can include unrelated active changes.
- Firmware operations, ISSU and checkpoint restore are not included.
- The copy reference misspells running configuration once in its source-name description. The retrieval schema and destination description consistently provide the correct name used by this binding.
- Notifications and NAE do not support these full-configuration resources.

## Tools

| Operation | Description | Category |
|---|---|---|
| Read named configuration | Retrieve running/startup configuration JSON | Read |
| Save running to startup | Copy the active configuration into startup | Change |

## Verification checklist

- The target switch and running/startup names match the requested operation.
- Successful JSON reads remain distinct from invented CLI-text/checksum fields.
- Full startup overwrite was confirmed before the save.
- Save response and subsequent startup read are recorded without exposing sensitive content.
