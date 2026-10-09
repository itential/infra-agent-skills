# AAP controller job bindings

AAP 2.6 platform gateway base: `https://<platform-host>/api/controller/v2/`. Red Hat's API overview documents this gateway prefix. The Ansible publisher schema uses controller-relative `/api/v2/` routes; the equivalent suffixes below use the gateway base. An authenticated client carries its existing bearer token; TLS verification remains enabled.

| Operation | Literal binding, relative to gateway base | Evidence |
|---|---|---|
| Template collection | `GET job_templates/` | `count`, `next`, `previous`, `results`; documented `search`, `page`, `page_size` arguments |
| Template detail | `GET job_templates/{id}/` | Selected `JobTemplate` |
| Launch requirements | `GET job_templates/{id}/launch/` | `can_start_without_user_input`, `passwords_needed_to_start`, `variables_needed_to_start`, `credential_needed_to_start`, `inventory_needed_to_start`, `defaults`, `ask_*_on_launch` |
| Launch | `POST job_templates/{id}/launch/` | Red Hat documents the created job's `id`; the publisher schema's response type is inconsistent, so the deployed contract must be checked |
| Job state | `GET jobs/{id}/` | `status`: `new`, `pending`, `waiting`, `running`, `successful`, `failed`, `error`, `canceled` |
| Job output | `GET jobs/{id}/stdout/?format=txt` | Formats also include `ansi`, `ansi_download`, `html`, `json`, `txt_download` |

A launch body may contain only fields supported by the deployed launch schema and template prompts. Verified fields include `inventory` (integer ID), `limit`, `job_tags`, `skip_tags`, `job_type` (`run` or `check`), `credentials` (integer IDs), and `extra_vars`. The source schema leaves `extra_vars` unconstrained while the Red Hat configuration example describes JSON encoded as a string: its exact deployed representation must be confirmed before sending it. No assumed string/object conversion is prescribed here.

The snapshot models normal reads as HTTP 200 but its launch response cannot reliably establish a unique expected HTTP success code. Success requires the documented created job identity. Another snapshot defect places deletion-related prose on the job read; the read method and `JobDetail` schema govern this procedure, not that copied description. The snapshot does not supply complete error schemas; actual HTTP status/body remain authoritative.

Sources: [Red Hat AAP 2.6 API overview](https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.6/pdf/automation_execution_api_overview/Red_Hat_Ansible_Automation_Platform-2.6-Automation_execution_API_overview-en-US.pdf), [execution configuration](https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.6/pdf/configuring_automation_execution/Red_Hat_Ansible_Automation_Platform-2.6-Configuring_automation_execution-en-US.pdf), [publisher controller schema, commit 186dc1c](https://github.com/ansible/aap-mcp-server/blob/186dc1cd880c5ef857b49b1ff7220d86af17ec72/data/controller-schema.json), retrieved 2026-10-09.
