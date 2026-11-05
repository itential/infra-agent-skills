# 🧰 Infrastructure Agent Skills

Open source library of automation skills for AI agents working on network and infrastructure
operations.

**[What This Is](#what-this-is)** ·
**[How It's Organized](#how-its-organized)** ·
**[Current Skills](#current-skills)** ·
**[Installation](#installation)** ·
**[Contributing](#contributing)** ·
**[License](#license)**

## 📖 What This Is

Each skill teaches an agent how to carry out one operation — provisioning a DNS record, running a
change request to close, upgrading device software — reliably and consistently, regardless of which
vendor platform is behind it. The goal is a single, trustworthy place for an agent (or the team
building one) to find "how do we do X here" and get an answer, instead of every agent re-deriving it
from scratch or from a vendor's raw API docs.

## 🗂️ How It's Organized

Skills are organized by **capability**, not by vendor. A skill is one operation — DNS record
management, software upgrade lifecycle, change management, and so on — with every vendor's
implementation of that operation living underneath it as a reference, rather than as its own
top-level skill. A library with one skill per vendor doesn't scale to a domain with hundreds of
vendor × platform × version permutations; grouping by capability keeps the number of skills small
and stable while the reference material underneath grows.

```
skills/<capability>/
├── SKILL.md                  # thin, stable router: shared shape + index pointer
└── references/
    ├── INDEX.md              # table: vendor/platform -> directory -> scope -> notes
    └── <vendor>/
        ├── procedure.md      # vendor's step-by-step: patterns, errors, verification
        └── endpoints.md      # literal wire-level calls
```

> 💡 **Adding or changing a skill?** See [Contributing](#-contributing) for the naming, scope, and
> `SKILL.md` rules.

## ✅ Current Skills

| Skill | Vendors covered |
|---|---|
| [`alert-monitor-management`](skills/alert-monitor-management/) | Datadog, New Relic, LogicMonitor, Paessler PRTG, Centreon, OP5 Monitor, Thruk |
| [`dns-record-management`](skills/dns-record-management/) | Route 53, Azure DNS, Cloudflare, Infoblox NIOS, BlueCat Horizon, BlueCat Address Manager, PowerDNS, Akamai Edge DNS, GoDaddy, Micetro |
| [`dns-zone-management`](skills/dns-zone-management/) | Route 53, Cloudflare, PowerDNS |
| [`change-management`](skills/change-management/) | ServiceNow, Freshservice, Jira Service Management, BMC Helix ITSM |
| [`software-upgrade-lifecycle`](skills/software-upgrade-lifecycle/) | Cisco IOS-XE, Cisco IOS XR, Arista EOS, Juniper Junos EX, Extreme EXOS, NVIDIA Cumulus Linux, Palo Alto Prisma SD-WAN |
| [`ipam-allocation`](skills/ipam-allocation/) | NetBox, Infoblox NIOS, SolarWinds IPAM, Nautobot, Micetro, phpIPAM |
| [`dhcp-scope-management`](skills/dhcp-scope-management/) | Infoblox NIOS, ISC Kea, Microsoft DHCP Server |
| [`cmdb-asset-management`](skills/cmdb-asset-management/) | ServiceNow CMDB, iTop |
| [`wireless-network-management`](skills/wireless-network-management/) | Cisco Meraki, HPE Aruba Networking Central, Cisco Catalyst Center |
| [`firewall-management`](skills/firewall-management/) | Palo Alto PAN-OS/Panorama, Fortinet FortiOS, Cisco ASA, Juniper SRX, Fortinet FortiManager, WatchGuard Firebox, AWS Network Firewall, Zscaler ZIA, Cloudflare Network Firewall |
| [`waf-management`](skills/waf-management/) | Cloudflare WAF *(zone custom rules, rate limiting rules, managed ruleset deployment)* |
| [`load-balancing`](skills/load-balancing/) | F5 BIG-IP LTM, Citrix ADC/NetScaler, HAProxy, Cloudflare Load Balancing |
| [`certificate-management`](skills/certificate-management/) | ACME (e.g. Let's Encrypt), HashiCorp Vault PKI, AWS Certificate Manager, DigiCert ONE Trust Lifecycle Manager, Sectigo Certificate Manager |
| [`vpn-tunnel-management`](skills/vpn-tunnel-management/) | strongSwan, Palo Alto PAN-OS, Juniper SRX, Cisco ASA *(VTI tunnel creation only)*, Cloudflare WAN *(GRE and IPsec tunnels, tunnel health)* |
| [`routing-troubleshooting`](skills/routing-troubleshooting/) | Cisco IOS-XE, Juniper Junos, FRRouting *(diagnostic: BGP session/route troubleshooting)* |
| [`interface-link-troubleshooting`](skills/interface-link-troubleshooting/) | Cisco IOS-XE, Juniper Junos, Arista EOS *(diagnostic: interface/link troubleshooting)* |
| [`vulnerability-lookup`](skills/vulnerability-lookup/) | NVD (National Vulnerability Database), Cisco PSIRT openVuln API *(diagnostic: CVE/CVSS lookup)* |
| [`casb-policy-management`](skills/casb-policy-management/) | Cloudflare One CASB *(finding-triggered remediation/webhook policies)* |
| [`casb-posture-assessment`](skills/casb-posture-assessment/) | Cloudflare One CASB *(diagnostic: posture and DLP content findings)* |
| [`crm-contact-management`](skills/crm-contact-management/) | Salesforce |
| [`dcim-asset-management`](skills/dcim-asset-management/) | NetTerrain (Graphical Networks), NetBox, Nautobot |
| [`notifications`](skills/notifications/) | Slack, Cisco Webex, Microsoft Teams, Twilio, SendGrid, Mattermost |
| [`secret-retrieval`](skills/secret-retrieval/) | HashiCorp Vault, 1Password (Connect API), CyberArk Conjur, CyberArk Privilege Cloud, AWS Secrets Manager, Azure Key Vault, Delinea Secret Server |
| [`repository-pull-request-management`](skills/repository-pull-request-management/) | GitHub, GitLab, Bitbucket Cloud, Bitbucket Server & Data Center |
| [`container-workload-deployment`](skills/container-workload-deployment/) | Kubernetes (apps/v1 Deployments), Docker Engine, Docker Hub |
| [`zero-trust-access-policy-management`](skills/zero-trust-access-policy-management/) | Zscaler Internet Access (ZIA), Zscaler Private Access (ZPA), Netskope, Cloudflare One Gateway, Cloudflare One Access |
| [`network-state-collection`](skills/network-state-collection/) | Cisco pyATS / Genie (parse commands, learn features, compare snapshots), IP Fabric and Forward Networks (read and compare platform snapshots), Arista CloudVision (read device inventory and events), Zabbix (read current host, interface, and item state), Auvik (read current discovered device and network state), Cisco ACI APIC (read fabric nodes, endpoints, faults, objects), AWS and Azure cloud network configuration *(read-only; AWS Network MCP server, Azure CLI)* |
| [`network-health-verification`](skills/network-health-verification/) | Cisco pyATS (Health Check, integrated job mode) |
| [`incident-management`](skills/incident-management/) | ServiceNow *(incident create, update, assign, hold, resolve, reopen, close)*, PagerDuty *(incident create, acknowledge, reassign, escalate, snooze, merge, resolve, reopen)*, Opsgenie *(incident create, note, resolve, close, reopen, delete)*, Jira Service Management *(incident create, comment, assign, resolve, reopen)*, ManageEngine ServiceDesk Plus *(incident create, edit, assign, note, resolve, close)* |
| [`connector-tunnel-management`](skills/connector-tunnel-management/) | Cloudflare Tunnel *(remotely managed `cloudflared` tunnels: publish, route, diagnose, retire)* |
| [`compute-instance-provisioning`](skills/compute-instance-provisioning/) | Amazon EC2 *(launch, start/stop/reboot, resize, snapshot/image, terminate)*; Google Compute Engine *(create, stop/start, suspend/resume, resize, disk snapshot, delete)*; VMware vSphere *(create, power, resize, delete)*; Morpheus *(create, stop/start, resize, snapshot, delete)* |
| [`sdwan-policy-management`](skills/sdwan-policy-management/) | Cisco Catalyst SD-WAN Manager *(centralized policy, original template-policy model)*, Palo Alto Networks Prisma SD-WAN *(stacked path and QoS policy sets, rules, and stacks; bind to sites)* |
| [`config-backup-management`](skills/config-backup-management/) | Prisma SD-WAN *(site snapshot capture, retrieve, and redeploy as YAML)* |
| [`sdwan-site-onboarding`](skills/sdwan-site-onboarding/) | Prisma SD-WAN *(site template create, branch site deployment from a template, device-shell assignment, verification, removal)*, Versa Director *(branch device creation from a post-staging template, activation, confirmation)* |
| [`network-access-control-management`](skills/network-access-control-management/) | Aruba ClearPass Policy Manager |
| [`automation-job-execution`](skills/automation-job-execution/) | AWX *(job template launch, poll, output, cancel)*, Jenkins *(build trigger; queue/state/stop details unverified)*, GitLab CI *(pipeline create, poll, job logs, cancel)*, Azure DevOps *(pipeline run, poll, logs, cancel)*, Rundeck *(job run, poll, output, abort)*, Puppet Enterprise *(orchestrator task/plan run, poll, report, stop)*, GitHub Actions *(workflow dispatch, run poll, logs, cancel)* |
| [`infrastructure-plan-execution`](skills/infrastructure-plan-execution/) | HashiCorp Terraform CLI *(init, validate, plan, apply a saved plan, destroy plan, state and output reads, import)* |
| [`metric-query`](skills/metric-query/) | Prometheus, Zabbix, Amazon CloudWatch *(read-only metric samples)* |
| [`log-query`](skills/log-query/) | Splunk *(search job, poll, paged results)*, Elasticsearch *(mapping, bounded search, hit-total qualification)*, AWS CloudWatch Logs *(Logs Insights start, poll, page)*, Google Cloud Logging *(entries list, page tokens)*; all read-only |

**149** vendor references across **39** capabilities.

See each skill's `references/INDEX.md` for the full vendor/platform breakdown and scope notes.

## 🔧 Installation

These skills are **framework-agnostic** — plain markdown procedures, not tied to any vendor's agent
runtime. There's nothing to compile or `pip install`; "installing" a skill means putting its
directory somewhere your agent framework looks for skills. Every framework does that lookup a
little differently, so the steps below are the same three-step shape in general form, then worked
through for Claude Code as one concrete example.

### General steps (any framework)

New to git? Skip to [No git? Download a ZIP](#no-git-download-a-zip) below.

1. **Clone or vendor this repo** wherever your project keeps third-party content:
   ```bash
   git clone https://github.com/itential/infra-agent-skills.git
   ```
2. **Pick the capability directory you need** — each one is fully self-contained under
   `skills/<capability>/` (its own `SKILL.md` + `references/`), so you only need to bring in the
   capabilities you actually use, not the whole repo.
3. **Point your framework's skill-loading mechanism at that directory.** If your framework expects
   skills in its own location (a `skills/` folder, a config-declared path, etc.), copy or symlink
   `skills/<capability>/` there — its internal `SKILL.md` + `references/` shape travels as-is,
   nothing needs restructuring.

### No git? Download a ZIP

You don't need git or a command line to get the skills.

1. On the repository page, choose **Code**, then **Download ZIP**.

   > 💡 **Direct link:** [main.zip](https://github.com/itential/infra-agent-skills/archive/refs/heads/main.zip)
   > downloads the same file in one click.

2. Unzip it. The folder is named `infra-agent-skills-main`.
3. Open `infra-agent-skills-main/skills/` and copy the capability folders you want, for example
   `dns-record-management`, into the place your framework looks for skills. Each folder is
   self-contained, so you can leave the rest behind and delete the download.

   > 💡 **Claude Code:** paste the folders into `<project>/.claude/skills/` for one project, or
   > `~/.claude/skills/` for every project.

A ZIP is a snapshot and doesn't update. To refresh a skill, download a new ZIP and replace its folder.

### Install one skill with git, without cloning the whole repo

A sparse checkout downloads only the capability you name, so the rest of the repo never lands on
disk (needs git 2.25 or later):

```bash
git clone --depth 1 --filter=blob:none --sparse https://github.com/itential/infra-agent-skills.git
cd infra-agent-skills
git sparse-checkout set --no-cone skills/dns-record-management
```

Only `skills/dns-record-management/` is now present. Add another with
`git sparse-checkout add --no-cone skills/<capability>`, and update with `git pull`. Then copy or
symlink the directory as in step 3 above. To keep nothing but the skill, copy it out and delete the
clone:

```bash
mkdir -p <project>/.claude/skills
cp -R skills/dns-record-management <project>/.claude/skills/
```

Replace `<project>` with your project root and adjust the destination for your framework. A copy
no longer updates with the repo, so repeat the steps to refresh it.

### Example: Claude Code

Claude Code looks for skills under `.claude/skills/<name>/SKILL.md` — personal (`~/.claude/skills/`)
or project-scoped (`<project>/.claude/skills/`). A symlink keeps this repo as the source of truth,
so pulling updates here doesn't require re-copying anything:

```bash
# From your project root, after cloning infra-agent-skills alongside it
mkdir -p .claude/skills
ln -s ../../infra-agent-skills/skills/dns-record-management .claude/skills/dns-record-management
```

Repeat the `ln -s` line per capability you want available. Claude Code picks up the new skill the
next time it scans `.claude/skills/` (a fresh session, or `/skills` to check what's loaded).

### Other frameworks

Any framework that can read a `SKILL.md` + `references/` directory tree works the same way. Copy
the capability folder to wherever that framework looks for skills.

> 💡 **No skills folder?** Everything here is plain markdown. Paste `skills/<capability>/SKILL.md`
> into your prompt or context-loading mechanism, and add files from its `references/` as the task
> calls for them.

## 🤝 Contributing

New skills and new vendor coverage are welcome.

### ✍️ By hand

Read [CONTRIBUTING.md](CONTRIBUTING.md) for the process: setup, pull request guidelines, and how
changes are reviewed.

### 🤖 With a coding agent

Point your agent at [AGENTS.md](AGENTS.md) before it writes anything. It holds the authoring rules:
naming, scope, file shape, and what may change in a `SKILL.md`.

### 📜 Good to know

This project is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). Report security issues per
[SECURITY.md](SECURITY.md). Contributions require agreement to the [CLA](CLA.md).

## 📄 License

Licensed under the [Apache License, Version 2.0](LICENSE).

Copyright 2026 Itential, Inc.
