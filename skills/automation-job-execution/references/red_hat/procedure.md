# Red Hat AAP job-template execution

Launch one existing, unsliced Automation Controller job template and read its native job result using an authenticated AAP 2.6 API client.

## Common Sequences

- Execute an existing template: **Select template** → **Read launch requirements** → **Launch approved job** → **Read job outcome**.
- Inspect an existing run: **Read job outcome**, using its known job identifier.

### Select template

The template collection returns a paginated list; continuation links are followed until the requested template is identified. A detail read supplies its inventory, playbook and settings. Success is an unambiguous template identifier with the intended target scope. A sliced or workflow template is outside this procedure.

### Read launch requirements

The launch-configuration read supplies defaults, required credentials/passwords/variables, and the fields permitted as launch prompts. Success is a complete launch request that satisfies these requirements without assuming that arbitrary template values can be overridden. Missing required input is resolved before launch. Secret prompt values remain in the authenticated client, not in a report.

### Launch approved job

This step can change managed infrastructure: **stop and confirm with the operator before proceeding**, identifying the template, target inventory/limit and approved launch values. The controller launches the existing template with the permitted inputs. The documented resulting job identifier identifies the created run; acceptance is not execution success. A transport failure after submission leaves launch outcome unknown, so it is reconciled against controller job history before another submission is considered.

The publisher's MCP schema snapshot incorrectly models the launch response as another launch-configuration object. Red Hat's execution guide identifies the newly created job identifier as the returned evidence. If the deployed response cannot be resolved to that job, the launch remains unresolved rather than being declared successful.

### Read job outcome

A job read returns its native status. New, pending, waiting and running are nonterminal; successful confirms controller execution completed successfully; failed, error and canceled are preserved as distinct outcomes. Standard output can be read for the same job identifier in the selected supported representation. Successful controller status is not a separate verification of every business effect of the playbook.

The schema snapshot does not enumerate the full error contract for these operations. Authentication, authorization, validation or missing-resource failures retain the server's status and body; missing data is not a successful run. No fixed polling interval or retry count is established here.

## Patterns

Prompt-on-launch controls which supplied values can take effect. The returned job identity and native terminal state establish the lifecycle; a successful launch call alone does not. Red Hat's guide warns that relaunch reapplies user prompts to the template's current defaults; relaunch is consequently outside this procedure.

## Known limitations

No inventory, host/group, project, template or inventory-source CRUD; project/inventory synchronization; Galaxy operations; ad-hoc commands; workflow/sliced job execution; cancellation or relaunch is included. This is a focused extraction from the larger automation toolkit, not a conversion of all 45 source tools.

Sources: Red Hat AAP 2.6 [launch guidance](https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.6/develop-proc_controller_launch_job_template), [execution configuration guide](https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.6/pdf/configuring_automation_execution/Red_Hat_Ansible_Automation_Platform-2.6-Configuring_automation_execution-en-US.pdf), and Ansible's publisher-maintained [controller schema](https://github.com/ansible/aap-mcp-server/blob/186dc1cd880c5ef857b49b1ff7220d86af17ec72/data/controller-schema.json), retrieved 2026-10-09. Bindings and schema caveats are in [endpoints](endpoints.md).

## Tools

| Operation | Purpose | Category |
|---|---|---|
| Select template | List/read existing controller templates | Read |
| Read launch requirements | Retrieve permitted and required launch inputs | Read |
| Launch approved job | Start one existing unsliced template | Execute |
| Read job outcome | Retrieve native status and standard output | Read |

## Verification checklist

- The exact template, inventory and launch scope were reviewed and confirmed.
- Required prompt inputs were satisfied and intended overrides were permitted.
- The resulting job identifier was captured before status reads.
- A native terminal status, not launch acceptance, is reported as the result.
