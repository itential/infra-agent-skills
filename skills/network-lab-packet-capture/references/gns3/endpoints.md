# GNS3 link packet capture: bindings

Authenticated GNS3 controller client; paths are relative to the configured controller. This binding covers API v2, not API v3. JSON payloads unless stated otherwise.

| Operation | Binding | Input / result |
|---|---|---|
| Inspect | `GET /v2/projects/{project_id}/links/{link_id}` | `capturing`, `capture_compute_id`, `capture_file_name`, `capture_file_path` |
| Start | `POST /v2/projects/{project_id}/links/{link_id}/start_capture` | Optional `data_link_type`: `DLT_ATM_RFC1483`, `DLT_EN10MB`, `DLT_FRELAY`, `DLT_C_HDLC`, `DLT_PPP_SERIAL`; 201 / 400 |
| Stop | `POST /v2/projects/{project_id}/links/{link_id}/stop_capture` | 201 / 400 |
| Retrieve | `GET /v2/projects/{project_id}/links/{link_id}/pcap` | 200 bytes / 403 / 404 |


## Sources

- [GNS3 capture start](https://api.gns3.net/en/latest/api/v2/controller/link/projectsprojectidlinkslinkidstartcapture.html). Retrieved 2026-10-09.
- [Capture stop](https://api.gns3.net/en/latest/api/v2/controller/link/projectsprojectidlinkslinkidstopcapture.html). Retrieved 2026-10-09.
- [Capture download](https://api.gns3.net/en/latest/api/v2/controller/link/projectsprojectidlinkslinkidpcap.html). Retrieved 2026-10-09.
- [Capture metadata](https://api.gns3.net/en/latest/api/v2/controller/link/projectsprojectidlinkslinkid.html). Retrieved 2026-10-09.
