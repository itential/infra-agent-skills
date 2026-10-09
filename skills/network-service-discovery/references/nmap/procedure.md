# Nmap scoped network discovery

Run a specified Nmap scan and retain its native observations.

## Common Sequences

- Host discovery: **Preview scope** → **Discover hosts** → **Preserve results**.
- Port/service scan: **Preview scope** → **Scan ports** → **Identify services/OS** if requested → **Preserve results**.
- Script check: **Preview scope** → **Review scripts** → **Run selected scripts** → **Preserve results**.

### Preview scope

`nmap -sL -n <targets>` lists selected target addresses without sending target probes and disables reverse-name lookups. Explicit exclusions use `--exclude <targets>` or `--excludefile <file>`; a supplied target list uses `-iL <file>`. Resolved target expansion must match the approved scope. Invalid target syntax or resolution failure is not an empty scan result. No NetClaw CIDR allowlist is implied by native Nmap.

### Discover hosts

Discovery sends network traffic: stop and confirm with the operator before proceeding. `nmap -sn -n <targets>` performs discovery without a subsequent port scan. On a local Ethernet network a privileged run normally uses ARP; unprivileged discovery uses a different probe set. Missing replies can be caused by filtering and do not prove that a host does not exist.

### Scan ports

Port scanning can affect services: stop and confirm with the operator before proceeding. The selected operation is `nmap -n -sT -p <ports> <targets>` for TCP connect, `-sS` for raw SYN, or `-sU` for UDP. Raw scan privileges are a prerequisite; a privilege failure is not permission to change the requested scan type silently. The publisher notes that even connect scans can be logged or disrupt poorly implemented services.

The native states `open`, `closed`, `filtered`, `unfiltered`, `open|filtered`, and `closed|filtered` are retained when returned. In particular UDP silence commonly yields `open|filtered`, not a proved open port. Skipping discovery with `-Pn` attempts the selected scans against every target and therefore requires that explicitly approved scope.

### Identify services/OS

Additional probes require their own approved scope: stop and confirm with the operator before proceeding. `-sV` enables service/version identification; optional `--version-intensity <0-9>` selects probe intensity. Default port-name lookup is not equivalent to detected software. The publisher excludes TCP 9100 from version probes because some printers print probe data; that safeguard is preserved and `--allports` is not added.

`-O --osscan-limit` limits requested OS fingerprinting to favorable cases with an open and closed TCP port. Returned matches/accuracy are observations, not a guarantee of the installed OS. No match remains no match; a fingerprint is not submitted externally by this procedure.

### Review scripts

`nmap --script-help '<selected-script-names>'` lists the selected scripts, categories and descriptions without a scan. Each script’s publisher documentation supplies its arguments and effects. NSE scripts are not sandboxed; default and vulnerability categories are not universal safety guarantees. Unverified third-party scripts or a broad `all` selection are outside this procedure.

### Run selected scripts

Before the selected script probes: stop and confirm with the operator before proceeding. `nmap -n -p <ports> --script '<approved-script-names>' <targets>` runs those checks with any documented, approved arguments. Native script errors or timeouts remain incomplete checks. A negative result is limited to the selected scripts and target observations, not a comprehensive vulnerability verdict.

### Preserve results

Appending `-oX <new-result-file>` writes XML for the selected scan. The publisher overwrites an existing output file by default: stop and confirm with the operator before proceeding if the destination already exists. XML append mode can produce an invalid document and is not used. The command scope, native errors, completion status and per-host/port observations accompany the artifact.

## Patterns

`-Pn` changes target treatment, not reachability. Port states depend on vantage point and technique. Version probes and OS fingerprints are distinct from port-name lookup.

## Known limitations

No scan history database, shell-argument filter or automatic audit trail is supplied by Nmap itself. Idle/decoy scans, brute-force/exploit/DoS scripts, automatic repeated scans, and production configuration changes are outside this procedure.

## Tools

| Mechanism | Description | Category |
|---|---|---|
| Local network CLI runner | Run Nmap with explicit argument boundaries and capture output | Active diagnostic |

## Verification checklist

- Target expansion and exclusions match approval.
- Scan method, ports and scripts remain within that scope.
- Native ambiguity and failed checks are preserved.
- XML output does not overwrite an unapproved file.
- No software or security certainty is inferred beyond observations.

## Sources

- [Nmap target specification](https://nmap.org/book/man-target-specification.html). Retrieved 2026-10-09.
- [Nmap host discovery](https://nmap.org/book/man-host-discovery.html). Retrieved 2026-10-09.
- [Nmap scan techniques](https://nmap.org/book/man-port-scanning-techniques.html). Retrieved 2026-10-09.
- [Nmap port-state definitions](https://nmap.org/book/man-port-scanning-basics.html). Retrieved 2026-10-09.
- [Nmap service/version detection](https://nmap.org/book/man-version-detection.html). Retrieved 2026-10-09.
- [Nmap OS detection](https://nmap.org/book/man-os-detection.html). Retrieved 2026-10-09.
- [Nmap scripting engine](https://nmap.org/book/man-nse.html). Retrieved 2026-10-09.
- [Nmap output](https://nmap.org/book/man-output.html). Retrieved 2026-10-09.
