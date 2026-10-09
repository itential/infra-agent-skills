# GNS3 link packet capture

Start, stop and retrieve a capture from a selected GNS3 v2 link.

## Common Sequences

- Collect: **Select link** → **Start** → **Inspect** → **Stop** → **Retrieve**.
- Retrieve existing data: **Select link** → **Inspect** → **Retrieve**.

### Select link

The link catalogue/details identify the selected link and endpoints. Invalid lookup (400) or absent link (404) ends selection without starting another link’s capture.

### Start

Before collecting packets on the selected link: stop and confirm with the operator before proceeding. The publisher starts a capture with the appropriate data-link type and returns 201. Invalid input (400) must be corrected; changing the encapsulation is not an automatic workaround.

### Inspect

Link details expose whether capture is active and the capture compute/file metadata. These values distinguish a started capture from a returned file; no fixed collection duration or minimum packet count is assumed.

### Stop

Before ending the selected link’s capture: stop and confirm with the operator before proceeding. The stop operation returns 201. A 400 means invalid input, not successful termination.

### Retrieve

The publisher streams the capture file from its compute and returns 200. A 403 means access denied; 404 means the file does not exist. Neither error is reported as an empty PCAP. Before saving the capture over an existing local artifact: stop and confirm with the operator before proceeding. Only returned capture bytes are saved, without mixing in API status JSON.

## Patterns

The controller provides the capture stream; a server-side file path is not assumed to be accessible on the caller’s filesystem.

## Known limitations

The start schema labels its capture filename as read-only even in the input table; this procedure omits that optional field rather than relying on the inconsistent label. No arbitrary packet count or retention guarantee is documented.

## Tools

Assumes the authenticated client described in [the bindings](endpoints.md).

| Operation | Description | Category |
|---|---|---|
| Select/inspect | Read link and capture metadata | Read |
| Start/stop | Control capture on the selected link | Change |
| Retrieve | Stream PCAP from compute | Read |

## Verification checklist

- Selected link and data-link type are retained.
- Active capture metadata is distinct from download success.
- A denied or missing file remains an error.

## Sources

- [GNS3 capture start](https://api.gns3.net/en/latest/api/v2/controller/link/projectsprojectidlinkslinkidstartcapture.html). Retrieved 2026-10-09.
- [Capture stop](https://api.gns3.net/en/latest/api/v2/controller/link/projectsprojectidlinkslinkidstopcapture.html). Retrieved 2026-10-09.
- [Capture download](https://api.gns3.net/en/latest/api/v2/controller/link/projectsprojectidlinkslinkidpcap.html). Retrieved 2026-10-09.
- [Capture metadata](https://api.gns3.net/en/latest/api/v2/controller/link/projectsprojectidlinkslinkid.html). Retrieved 2026-10-09.
