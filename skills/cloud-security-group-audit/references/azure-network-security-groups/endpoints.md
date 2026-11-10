# Azure Network Security Groups — Audit Bindings

Read operations used by the procedure. Source: Azure Virtual Network REST reference and `az network nsg` CLI reference (retrieved 2026-11-10). Unverified: the current `api-version` value; use the version the REST reference documents.

## List network security groups

REST: list all NSGs in a subscription (`GET` on the subscription's `Microsoft.Network/networkSecurityGroups` collection, with `api-version`). CLI: `az network nsg list`, optionally `--resource-group`.
- Paged: follow `nextLink` until absent.
- Output per NSG: `name`, `id`, `location`, `tags`, and `properties` with `securityRules`, `defaultSecurityRules`, `networkInterfaces`, `subnets`, `flowLogs`, `provisioningState`.
- Rule properties: `priority` (100–4096), `direction` (`Inbound`/`Outbound`), `access` (`Allow`/`Deny`), `protocol` (`Tcp`/`Udp`/`Icmp`/`Esp`/`*`), `sourceAddressPrefix` / `sourceAddressPrefixes`, `sourceApplicationSecurityGroups`, `destinationPortRange` / `destinationPortRanges`. Unverified: exact names of the remaining source/destination port, destination prefix, and description properties; read them from the returned objects.

## Get one network security group

CLI: `az network nsg show --resource-group <group> --name <nsg>`. The default rules are returned under `defaultSecurityRules`; a query on that property returns them alone.

## List network security group rules

CLI: `az network nsg rule list --resource-group <group> --nsg-name <nsg>`; one rule: `az network nsg rule show`. Unverified: the `--nsg-name` flag spelling; confirm with `--help` before use.
