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
  SKILL.md                       # thin, stable router — the shared shape of the capability plus
                                  # an index pointer. Stays roughly constant size regardless of how
                                  # many vendors/platforms are added underneath.
  references/
    INDEX.md                     # table: vendor/platform -> directory -> scope -> notes
    <vendor>/
      procedure.md                # that vendor's full step-by-step — patterns, error handling,
                                   # tools, verification checklist
      endpoints.md                 # literal wire-level calls
```

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
| `alert_monitor_management` | Datadog, New Relic, LogicMonitor, Paessler PRTG |
| `dns_record_management` | Route 53, Azure DNS, Cloudflare, Infoblox NIOS, BlueCat Horizon, BlueCat Address Manager, PowerDNS |
| `dns_zone_management` | Route 53, Cloudflare, PowerDNS |
| `change_management` | ServiceNow, Freshservice, Jira Service Management, BMC Helix ITSM |
| `software_upgrade_lifecycle` | Cisco IOS-XE, Cisco IOS XR, Arista EOS, Juniper Junos EX, Extreme EXOS, NVIDIA Cumulus Linux |
| `ipam_allocation` | NetBox, Infoblox NIOS, SolarWinds IPAM |
| `dhcp_scope_management` | Infoblox NIOS, ISC Kea, Microsoft DHCP Server |
| `cmdb_asset_management` | ServiceNow CMDB |
| `wireless_network_management` | Cisco Meraki, HPE Aruba Networking Central, Cisco Catalyst Center |
| `firewall_management` | Palo Alto PAN-OS/Panorama, Fortinet FortiOS, Cisco ASA |
| `waf_management` | _(scaffolded — no vendor coverage yet)_ |
| `load_balancing` | F5 BIG-IP LTM, Citrix ADC/NetScaler, HAProxy |
| `certificate_management` | ACME (e.g. Let's Encrypt), HashiCorp Vault PKI, AWS Certificate Manager |
| `vpn_tunnel_management` | strongSwan, Palo Alto PAN-OS, Juniper SRX, Cisco ASA *(VTI tunnel creation only)* |
| `routing_troubleshooting` | Cisco IOS-XE, Juniper Junos, FRRouting *(diagnostic: BGP session/route troubleshooting)* |
| `interface_link_troubleshooting` | Cisco IOS-XE, Juniper Junos, Arista EOS *(diagnostic: interface/link troubleshooting)* |
| `vulnerability_lookup` | NVD (National Vulnerability Database), Cisco PSIRT openVuln API *(diagnostic: CVE/CVSS lookup)* |
| `casb_policy_management` | _(scaffolded — no vendor coverage yet)_ |
| `casb_posture_assessment` | _(scaffolded — no vendor coverage yet; diagnostic: CASB risk/compliance posture)_ |
| `crm_contact_management` | Salesforce |
| `dcim_asset_management` | NetTerrain (Graphical Networks) |
| `notifications` | Slack, Cisco Webex (including requested pyATS result reports), Microsoft Teams |
| `secret_retrieval` | HashiCorp Vault, 1Password (Connect API), CyberArk Conjur, CyberArk Privilege Cloud, AWS Secrets Manager, Azure Key Vault |
| `repository_pull_request_management` | GitHub, GitLab, Bitbucket Cloud, Bitbucket Server & Data Center |
| `container_workload_deployment` | Kubernetes (apps/v1 Deployments), Docker Engine, Docker Hub, Cisco pyATS (published Docker image and existing test-job execution) |
| `zero_trust_access_policy_management` | Zscaler Internet Access (ZIA), Zscaler Private Access (ZPA), Netskope |
| `testbed-management` | Cisco pyATS (create/validate YAML and in-memory topology objects) |
| `credential-encoding` | Cisco pyATS (Fernet secret strings and runtime credential markup) |
| `network-state-collection` | Cisco pyATS / Genie (Parse command output, learn feature state, and compare saved network snapshots); NAPALM (Supported read-only driver getters); Linux iproute2 (Local link, address and all-table IPv4/IPv6 route reads) |
| `device-cli-execution` | Cisco pyATS / Unicon (Execute approved CLI commands or apply an approved configuration through a device session); Cisco RADKit (Authorized remote-service command transport); Netmiko (Read-only approved CLI commands); Juniper Junos (Operational CLI session and supplied read commands) |
| `parallel-task-execution` | Cisco pyATS (Run independent callable invocations concurrently and collect their ordered results); Nornir (Host-scoped native read-only task execution) |
| `network-test-execution` | Cisco pyATS (AEtest, Blitz, Robot Framework, Genie harness, integrated Health Check), Cisco XPRESSO (single registered job requests) |
| `device-reprovisioning` | Cisco pyATS Clean (validate/run approved platform-specific Clean definitions) |
| `device-session-recording` | Cisco pyATS / Unicon (record, replay, convert to mock CLI) |
| `device-api-connection` | Cisco pyATS REST connector (DNAC read-session lifecycle only) |
| `container-image-build` | Cisco pyATS Image Builder (build and inspect local test images) |

| `address-service-query` | Infoblox NIOS (Bounded collection reads for A/AAAA/CNAME/PTR/TXT, IPv4 networks, DHCP ranges and fixed addresses) |
| `agent-federation-state-query` | NetClaw mesh daemon (Read federation overview, one peer record, and cached advertised inventory) |
| `agent-security-inspection` | DefenseClaw (Read posture/tool policy/alerts/audit; one-shot skill and MCP scans) |
| `api-documentation-lookup` | Cisco DevNet Content Search (Meraki/Catalyst Center keyword lookup and Meraki operation-ID lookup) |
| `asset-lifecycle-query` | Auvik (Device lifecycle and warranty/service coverage) |
| `automation-content-validation` | Ansible ansible-lint (Project/file/role linting; profiles, rules and tags) |
| `automation-job-execution` | Jenkins MCP Server Plugin (Job/build inspection, trigger/queue/monitor, build display-name/description updates, logs and SCM); Itential MCP (Existing workflow discovery, launch and job list/detail); Red Hat AAP (List/select an existing unsliced job template, inspect launch requirements, launch and read job status/stdout) |
| `browser-evidence-capture` | Chrome DevTools MCP (Page snapshot/screenshot, console/network inspection, optional Lighthouse snapshot audit) |
| `certificate-authority-configuration` | HashiCorp Vault PKI (Internal self-signed root; issuer and role inspection/configuration) |
| `cloud-compute-query` | Google Cloud (Project discovery and source Compute Engine read families) |
| `cloud-cost-query` | AWS Cost Explorer (Cost/usage, forecasts and detected anomalies) |
| `cloud-file-management` | microsoft_graph (listing folders, reading file metadata, sharing permissions, versions and thumbnails, downloading files, and uploading or replacing files up to 250 MB in OneDrive or SharePoint) |
| `cloud-network-inspection` | AWS Network MCP (VPC/ENI/TGW/Cloud WAN/VPN/firewall configuration; logs; route simulation); Azure (VNet, NIC effective policy/routes, NSG, hybrid routing, load-balancer configuration, Application Gateway health and supporting resources); Equinix Fabric (Connections, ports, routers, networks/IP blocks, service catalogues, route/filter relationships and telemetry configuration); Equinix Network Edge (Virtual devices, account/project/metro/device-type catalogues and ACL/template associations) |
| `collaboration-context-query` | Slack (Profiles, presence, DND, conversation discovery, history, thread and message search) |
| `collaboration-file-delivery` | Slack (External upload URL, binary transfer and required completion/share) |
| `configuration-backup-query` | Auvik (List/filter stored backups and retrieve one by ID) |
| `controller-data-query` | Cisco Meraki (Discover and execute a read operation); Cisco Catalyst Center (Discover and execute a read operation); Arista CloudVision (Native inventory, event and existing probe-statistics reads); Cisco ACI APIC (Systems, endpoints, current faults and named-object reads) |
| `dashboard-definition-query` | Grafana MCP (Search/read summaries, native JSON, properties and panel queries) |
| `device-configuration-save` | HPE Aruba AOS-CX (Read running/startup JSON configuration and save running to startup) |
| `device-configuration-transaction` | Juniper Junos MCP (Render/check/commit a supplied template or configuration) |
| `diagram-rendering` | draw.io MCP (Open supplied XML/CSV/Mermaid in an editor; inspect/replace local pages); Markmap CLI (Markdown to HTML mind map); Kroki (Diagram source to a selected supported image format); Python Diagrams (Render an approved explicit Python diagram definition) |
| `digital-experience-query` | Zscaler ZDX (Application scores/trends and ongoing alert reads) |
| `document-artifact-creation` | python-docx (New DOCX with headings, paragraphs, and text tables); openpyxl (New XLSX with supplied cell values); python-pptx (New PPTX with title/content text slides); pypdf (Inspect and fill existing named PDF text fields into a new PDF) |
| `edge-analytics-query` | Cloudflare (DNS counts/response times/trends; daily zone HTTP totals; Worker calculations; Radar HTTP trends) |
| `edge-configuration-query` | Cloudflare (Zone/record, Worker/settings/build, Access/policy, Tunnel/connection and ruleset list/detail) |
| `event-activation-lifecycle` | Red Hat AAP 2.6 EDA (Activation create/read/enable/disable/restart/delete and execution output) |
| `event-record-query` | NetClaw SNMP (Trap list/detail and type/source counts) |
| `event-routing-rule-management` | PagerDuty (inspecting PagerDuty event orchestrations and replacing or adding rules in their service-routing router) |
| `exported-data-query` | DuckDB (Materialize local JSON/CSV exports, inspect schema, query and count) |
| `external-network-measurement` | Globalping (Public ping/traceroute/MTR/DNS/HTTP; probe/limit discovery and result retrieval) |
| `fabric-state-query` | Cisco Nexus 9000 (NVE/VNI, EVPN BGP and MAC/IP reads; 10.6 ESI observations) |
| `firewall-policy-analysis` | AutomateIP FWRule MCP (Supported format discovery, policy parsing and candidate overlap analysis) |
| `firewall-policy-installation` | Fortinet FortiManager (Existing package/device-settings install wizard) |
| `firewall-rule-management` | Zscaler ZIA (Cloud firewall rule read/create/update/delete and configuration activation) |
| `firewall-rule-query` | Cisco Secure Firewall FMC (Profile discovery and policy/target/FMC-wide access or prefilter rule search); Check Point Quantum Management (Package/layer discovery and access/NAT rule reads) |
| `firewall-state-query` | Fortinet FortiGate (System/interface/routing/HA/IPsec observations); Palo Alto Networks Panorama (Managed-device discovery and targeted system reads) |
| `hardware-state-query` | DMTF Redfish (Read system/chassis/manager status, sensors, firmware and logs) |
| `host-state-query` | Linux (Process inventory, directory metadata and curl version/features) |
| `identity-directory-query` | Zscaler ZIdentity (Users, groups and membership reads); AWS IAM (User/group/role metadata, policy reads and existing credential report) |
| `identity-record-management` | Cisco CML (User/group CRUD and explicit memberships) |
| `incident-record-management` | PagerDuty (List/read/create/update incidents; read alerts and related findings; read/add notes; request responders; merge incidents); Datadog (List/read/create/update incidents) |
| `incident-service-management` | PagerDuty (listing, inspecting, creating and updating PagerDuty incident services) |
| `infrastructure-model-management` | OpsMill Infrahub MCP (Schema/query and session-branch object changes through proposed change) |
| `infrastructure-module-discovery` | HashiCorp Terraform MCP (Provider/module search, latest-version lookup and component documentation) |
| `infrastructure-plan-execution` | HashiCorp Terraform CLI (Prepare, inspect, apply or destroy-plan; inspect state/output; import) |
| `infrastructure-workspace-management` | HashiCorp HCP Terraform / Terraform Enterprise (Workspace lifecycle, variable reads, plan-only run lifecycle) |
| `ip-address-enrichment` | gtrace (ASN, geographic and reverse-DNS lookups) |
| `ip-prefix-calculation` | Python ipaddress (IPv4/IPv6 prefix arithmetic and classification) |
| `issue-record-management` | GitHub (List/read/create/update repository issues; list/add comments); GitLab (List/read/create/update project issues; list/add notes); Jira Cloud (JQL search/read, create/edit, workflow transitions, list/add comments) |
| `knowledge-page-management` | Confluence Cloud (List/read/create/update published pages; move published pages to trash); GitLab (List/read/create/update/delete project wiki pages) |
| `lab-platform-query` | Cisco CML (Controller health/statistics, license status and node definitions) |
| `load-balancer-state-query` | F5 BIG-IP (TMSH LTM configuration/status and platform/HA observations) |
| `log-query` | Google Cloud Logging (Entries search and continuation pages); Datadog (Log event search and cursor paging); Elasticsearch (Mapping inspection and scoped Query DSL search/count); Splunk (Scoped search jobs, results and export); Grafana Loki (Label discovery and scoped log queries); AWS CloudWatch Logs (Log-group discovery and bounded Logs Insights QL jobs/results); NetClaw syslog (Retained receiver messages and statistics); Fortinet FortiAnalyzer (Historical Log View filtering and details) |
| `log-source-query` | Splunk Python SDK (Index collection and instance metadata) |
| `media-workflow-execution` | ComfyUI (Approved image workflow queueing and output retrieval) |
| `meeting-asset-query` | Zoom Meetings MCP (Historical meeting search and authorized asset/recording retrieval) |
| `metric-query` | Prometheus (PromQL instant/range evaluation, metric discovery, scrape metadata); Zabbix (Item discovery, typed history, numeric hourly trends); Google Cloud Monitoring (Project time-series retrieval with optional aggregation); Datadog (Scoped time-series points); Auvik (Device/interface/service/component statistics and SNMP poller history/current OID reads); Grafana Prometheus (Metric/label discovery and PromQL evaluation); AWS CloudWatch (Scoped metric statistics and metric-math queries using known metric identities); Docker (One-shot container resource statistics) |
| `monitoring-problem-query` | Zabbix (Current unresolved/recent problems and historical events); Auvik (Scoped alert history and details); AWS CloudWatch (Alarm configuration/state and history reads) |
| `network-access-diagnosis` | Cisco ISE (Read-only session, posture, matched-policy, AAA failure and latency diagnosis) |
| `network-access-policy-query` | Cisco ISE (Policy-set discovery and filtered authentication/authorization rule reads) |
| `network-inventory-query` | Zabbix (Visible hosts, interfaces, groups/templates, and item inventory); Auvik (Network/device/interface/component inventory, details and entity notes/audits) |
| `network-lab-lifecycle` | GNS3 v2 (Create/read/open/close/copy/export/delete; import blocked pending upload contract); Cisco CML (Create/import/export/start/stop/wipe/delete); EVE-NG (Discover/create/read/start/stop/delete); Containerlab (Deploy, inspect, save configurations and destroy supplied labs) |
| `network-lab-node-management` | GNS3 v2 (Template creation, inventory, runtime actions, console metadata, delete); Cisco CML (Create/read/start/stop/wipe/delete and console metadata); EVE-NG (Create/read/start/stop/wipe) |
| `network-lab-packet-capture` | GNS3 v2 (Start/inspect/stop/download); Cisco CML (Start/inspect/stop/download/decode) |
| `network-lab-snapshot-management` | GNS3 v2 (List/create/restore/delete snapshots) |
| `network-lab-startup-config` | Cisco CML (Read/replace/extract stored configuration); EVE-NG (Native startup configuration export) |
| `network-lab-topology-management` | GNS3 v2 (Link create/read/suspend/resume/delete); Cisco CML (Interface creation and link create/read/delete); EVE-NG (Topology inspection and network creation) |
| `network-model-configuration` | OpenConfig gNMI (One delete/replace/update transaction) |
| `network-model-query` | IP Fabric (Health assessment; unicast, gateway and multicast paths/diagrams; discovered read queries); SuzieQ (Table reads, summaries, unique values, assertions and paths); Topolograph IGP (Stored graph inventory, paths, subnets and model analysis); Topolograph BGP (Stored BGP policy/path model queries); Batfish (Existing snapshot initialization issues, forwarding/reachability, filter analysis and differential evidence); Forward Networks (Network/snapshot/device inventory, library NQE and modeled paths) |
| `network-model-snapshot-management` | Batfish (Upload, list and delete configuration snapshots) |
| `network-model-telemetry` | OpenConfig gNMI (Capabilities, snapshots, ONCE/POLL/STREAM subscriptions) |
| `network-path-measurement` | gtrace (Local traceroute/MTR with requested protocol and options) |
| `network-policy-evaluation` | Kubernetes NetworkPolicy (Core NetworkPolicy ingress/egress evaluation) |
| `network-scan-comparison` | Nmap Ndiff (Compare two existing XML scan artifacts) |
| `network-service-discovery` | Nmap (Approved discovery, port/version/OS scans and selected NSE checks) |
| `network-tenant-creation` | Cisco ACI APIC (Create an empty tenant and verify its model object) |
| `network-validation` | Arista ANTA (Run an inventory/catalogue, filter tests, produce native results) |
| `offline-packet-analysis` | Wireshark TShark (File metadata, decode/filter, protocol/conversation/endpoint/expert statistics); Zeek (Generate connection/protocol logs and correlate by connection UID); Suricata 8.0.6 (Offline configured-rule detection and EVE alert/flow review) |
| `oncall-schedule-management` | PagerDuty (querying PagerDuty on-call entries and escalation policies, and creating, updating or overriding legacy V2 schedules) |
| `orchestrator-configuration-sync` | Cisco NSO (Check, confirmed sync-from and recheck) |
| `orchestrator-state-query` | Cisco NSO (Device records, synchronization checks and service inventory) |
| `out-of-band-device-query` | Lantronix Percepxion (Inventory, ports/full telemetry, config/firmware, stored catalogs/logs, audits and existing jobs) |
| `pipeline-job-management` | GitHub Actions (List/read workflow runs and dispatch a configured workflow); GitLab CI/CD (List/read/create/retry/cancel pipelines, list jobs and retrieve trace) |
| `private-application-management` | Zscaler ZPA (Standard application segment read/create/update/delete) |
| `public-routing-registry-query` | RIPEstat (ASN/announced prefixes, WHOIS, abuse contacts, RPKI validation); PeeringDB (Network registration and exchange/facility presence); RIPE Atlas (Probe counts and anchor lists) |
| `public-wiki-page-query` | Wikipedia / MediaWiki (Search, page information, current revision, external links, categories) |
| `retrieval-corpus-query` | NetClaw rag-mcp (List documents/snapshots/replicas, read statistics, search a named collection); MemPalace (Read status, wing/room taxonomy, and bounded stored-text search) |
| `routing-speaker-state-query` | NetClaw protocol MCP (Existing BGP peer/RIB reads; limited local summary/GRE observations) |
| `saved-search-execution` | Splunk (List/read/dispatch saved searches; inspect job and retrieve final results) |
| `scene-rendering` | Blender (Existing scene to image frame or bounded animation); NetClaw Three.js (Explicit topology to local HTML scene); NetClaw Unreal (Static explicit topology into compatible Unreal Editor) |
| `sdwan-state-query` | Prisma SD-WAN Unified SASE API (Inventory, configuration, application definitions, topology, status and event reads); Cisco Catalyst SD-WAN Manager (Inventory, device observations, templates, policy and alarms) |
| `secrets-engine-management` | HashiCorp Vault (Read/enable/tune/disable mounts; list auth methods) |
| `security-audit-query` | Cloudflare (Audit Logs v2, data-security posture findings and IP overview); AWS CloudTrail (Regional paged event-history lookup) |
| `security-traffic-analytics` | Zscaler Z-Insights (Historical web-traffic and threat aggregates) |
| `service-endpoint-diagnosis` | Kubernetes (Service/Ingress references, selectors, ports and endpoint conditions) |
| `service-record-context-query` | Halo (Read tickets, assets, linked records, actions and ticket types) |
| `service-usage-query` | Auvik (Read client or selected-device usage over dates) |
| `social-post-management` | X (V2 mention/recent search/post read, text creation/reply and deletion) |
| `source-of-truth-query` | NetBox (Devices, interfaces, cables, sites, IP addresses, prefixes and VLANs: list/filter/detail); Nautobot (IP address and prefix list/filter/detail by UUID) |
| `standards-document-query` | RFC Editor (Number/keyword lookup, section reading, publication relationships and errata) |
| `switch-state-query` | HPE Aruba Networking AOS-CX (System, interface, VLAN and related-resource reads) |
| `synthetic-network-result-query` | Cisco ThousandEyes (Existing network results, path summaries and agent/round hop details) |
| `telemetry-receiver-management` | syslog (UDP or newline-framed TCP listener); snmptrap (UDP trap listener); ipfix (UDP flow listener) |
| `trace-span-query` | Datadog (V2 indexed span search with cursor pagination) |
| `traffic-flow-query` | Kubeshark (Read L4 flows and aggregate summaries); NetClaw IPFIX (Retained decoded flow and template/statistic queries) |
| `traffic-snapshot-management` | Kubeshark (Create/list/read/delete snapshots and export PCAP) |
| `virtual-machine-lifecycle` | Google Compute Engine (Create/start/stop/reset/resize/delete with operation tracking) |
| `visualization-payload-building` | NetClaw Canvas (Build a supplied-content envelope or error payload) |
| `voice-call-placement` | Twilio (Create an outbound call using inline TwiML and read/observe its status) |
| `voice-media-stream-connection` | Twilio (Bidirectional stream setup, audio exchange and closure) |
| `workload-state-query` | Kubernetes (Pod/controller inventory and pod conditions/events); VMware ESXi (Registered VM inventory and snapshot trees) |
| `world-generation` | World Labs (Text prompt generation and operation/world retrieval) |

See each skill's `references/INDEX.md` for the full vendor/platform breakdown and scope notes.

The [pyATS adaptation map](docs/pyats-adaptation.md) records source-topic destinations,
verified corrections, and explicit scope boundaries.

The [NetClaw adaptation map](docs/netclaw-adaptation.md) accounts for every pinned source skill,
including partial conversions and material that does not satisfy this repository’s procedure contract.
It links the machine-readable source-to-capability manifest and verification instructions.

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
ln -s ../../infra-agent-skills/skills/dns_record_management .claude/skills/dns_record_management
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
