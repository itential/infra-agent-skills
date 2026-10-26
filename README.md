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

Capability, `name`, and vendor/tool directories are lowercase kebab-case, and a capability is named
for the operation rather than a tool. A vendor can be a platform's API, a CLI/SDK framework, or an MCP
server, as long as the operation is a real infrastructure process and the router stays tool-neutral
— see [AGENTS.md](AGENTS.md) rules 13 and 14.

For a large permutation space (e.g. software upgrades, where one vendor spans several platform
families and install modes), the same shape holds one level deeper:
`references/<vendor>/<platform-family>.md` — grouped by platform family/version line, not by every
individual model, unless behavior genuinely differs at that granularity.

**`SKILL.md` only changes for two reasons: a bug in the shared/router content, or a pointer to a
newly added vendor.** Every vendor-specific fact — a new error code, a corrected field, a changed API
path, a whole new procedure — goes in that vendor's own `references/<vendor>/` files. This keeps
`SKILL.md` small and stable no matter how many vendors accumulate, and keeps a PR that only touches
one vendor's behavior from ever touching the shared file.

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
| [`firewall-management`](skills/firewall-management/) | Palo Alto PAN-OS/Panorama, Fortinet FortiOS, Cisco ASA, Juniper SRX, Fortinet FortiManager, WatchGuard Firebox, AWS Network Firewall |
| [`waf-management`](skills/waf-management/) | _(scaffolded — no vendor coverage yet)_ |
| [`load-balancing`](skills/load-balancing/) | F5 BIG-IP LTM, Citrix ADC/NetScaler, HAProxy, Cloudflare Load Balancing |
| [`certificate-management`](skills/certificate-management/) | ACME (e.g. Let's Encrypt), HashiCorp Vault PKI, AWS Certificate Manager, DigiCert ONE Trust Lifecycle Manager, Sectigo Certificate Manager |
| [`vpn-tunnel-management`](skills/vpn-tunnel-management/) | strongSwan, Palo Alto PAN-OS, Juniper SRX, Cisco ASA *(VTI tunnel creation only)* |
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
| [`network-state-collection`](skills/network-state-collection/) | Cisco pyATS / Genie (parse commands, learn features, compare snapshots), IP Fabric and Forward Networks (read and compare platform snapshots), Arista CloudVision (read device inventory and events), Zabbix (read current host, interface, and item state), Auvik (read current discovered device and network state), Cisco ACI APIC (read fabric nodes, endpoints, faults, objects) |
| [`network-health-verification`](skills/network-health-verification/) | Cisco pyATS (Health Check, integrated job mode) |
| [`incident-management`](skills/incident-management/) | ServiceNow *(incident create, update, assign, hold, resolve, reopen, close)*, PagerDuty *(incident create, acknowledge, reassign, escalate, snooze, merge, resolve, reopen)*, Opsgenie *(incident create, note, resolve, close, reopen, delete)*, Jira Service Management *(incident create, comment, assign, resolve, reopen)*, ManageEngine ServiceDesk Plus *(incident create, edit, assign, note, resolve, close)* |
| [`compute-instance-provisioning`](skills/compute-instance-provisioning/) | Amazon EC2 *(launch, start/stop/reboot, resize, snapshot/image, terminate)*; Google Compute Engine *(create, stop/start, suspend/resume, resize, disk snapshot, delete)*; VMware vSphere *(create, power, resize, delete)*; Morpheus *(create, stop/start, resize, snapshot, delete)* |
| [`sdwan-policy-management`](skills/sdwan-policy-management/) | Cisco Catalyst SD-WAN Manager *(centralized policy, original template-policy model)*, Palo Alto Networks Prisma SD-WAN *(stacked path and QoS policy sets, rules, and stacks; bind to sites)* |
| [`config-backup-management`](skills/config-backup-management/) | Prisma SD-WAN *(site snapshot capture, retrieve, and redeploy as YAML)* |
| [`sdwan-site-onboarding`](skills/sdwan-site-onboarding/) | Prisma SD-WAN *(site template create, branch site deployment from a template, device-shell assignment, verification, removal)*, Versa Director *(branch device creation from a post-staging template, activation, confirmation)* |
| [`network-access-control-management`](skills/network-access-control-management/) | Aruba ClearPass Policy Manager |
| [`automation-job-execution`](skills/automation-job-execution/) | AWX *(job template launch, poll, output, cancel)*, Jenkins *(build trigger; queue/state/stop details unverified)*, GitLab CI *(pipeline create, poll, job logs, cancel)*, Azure DevOps *(pipeline run, poll, logs, cancel)*, Rundeck *(job run, poll, output, abort)*, Puppet Enterprise *(orchestrator task/plan run, poll, report, stop)*, GitHub Actions *(workflow dispatch, run poll, logs, cancel)* |
| [`infrastructure-plan-execution`](skills/infrastructure-plan-execution/) | HashiCorp Terraform CLI *(init, validate, plan, apply a saved plan, destroy plan, state and output reads, import)* |

**129** vendor references across **33** capabilities (3 more are scaffolded with no coverage yet).

See each skill's `references/INDEX.md` for the full vendor/platform breakdown and scope notes.

## 🔧 Installation

These skills are **framework-agnostic** — plain markdown procedures, not tied to any vendor's agent
runtime. There's nothing to compile or `pip install`; "installing" a skill means putting its
directory somewhere your agent framework looks for skills. Every framework does that lookup a
little differently, so the steps below are the same three-step shape in general form, then worked
through for Claude Code as one concrete example.

### General steps (any framework)

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

Any framework that can read a `SKILL.md` + `references/` directory tree works the same way — adjust
step 3's destination path to wherever that framework looks. If your framework has no directory
convention of its own, `skills/<capability>/SKILL.md`'s content is plain markdown and can be pasted
directly into whatever prompt/context-loading mechanism you use.

## 🤝 Contributing

New skills and new vendor coverage are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for how this
repo is organized and the process for submitting changes. This project is governed by our
[Code of Conduct](CODE_OF_CONDUCT.md); report security issues per [SECURITY.md](SECURITY.md).
Contributions require agreement to the [CLA](CLA.md).

## 📄 License

<!-- PLACEHOLDER — license not yet decided; repo is private until this is settled. -->
Not yet finalized — see [LICENSE.md](LICENSE.md).

Copyright (c) 2026 Itential, Inc.
