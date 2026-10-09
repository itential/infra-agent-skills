# FortiManager policy-package installation

Validate, preview and install an existing FortiManager policy package and its associated device settings.

Sources: Fortinet [7.6.3 installation wizard](https://docs.fortinet.com/document/fortimanager/7.6.3/administration-guide/153046/installing-policy-packages-and-device-settings), [7.6.0 package prerequisites](https://docs.fortinet.com/document/fortimanager/7.6.0/administration-guide/92081/install-a-policy-package), [7.6.0 installation practices](https://docs.fortinet.com/document/fortimanager/7.6.0/best-practices/950732/installing-policy-packages), retrieved 2026-10-09. Console bindings are in [endpoints.md](endpoints.md).

1. **Select the installation context.** The wizard opens in the ADOM containing the intended existing package. Package installation requires default or per-device object mappings; absent mappings cause installation failure. Success is the intended package and target administrative domain displayed in the wizard.
2. **Set package options.** The package-and-device-settings mode selects the package, optional comment, optional ADOM revision/name/comment, and either immediate or scheduled installation. A schedule includes the displayed date and time. Success is the selected options on the wizard's next page.
3. **Validate targets.** Selected devices or groups undergo policy/object, interface and installation-preparation validation. Devices with validation errors are skipped. Error links expose the highlighted progress report; those targets remain failed rather than counted as installed. If configured, policy consistency checks also produce results. A policy-count threshold warning depends on the configured feature; the publisher says that threshold is disabled by default.
4. **Review the installation preview.** The publisher's best-practice guidance requires reviewing the preview before installation. The selected device controls the displayed changes; multiple devices can be reviewed, and a downloadable preview is optional. The package diff can additionally compare the current controller policy with the device policy. Success is a reviewed preview for the intended targets. Installation can remove unreferenced device objects and include some indirectly related objects; a preview is not merely an additive change list.
5. **Install or schedule the package.** This changes live device configuration, or schedules that change: stop and confirm with the operator before proceeding, including package, ADOM, targets, preview and schedule. The wizard's corresponding completion action begins installation or records the selected schedule. A scheduled request is not an already completed installation.
6. **Review the result and close the wizard.** The wizard displays installation status, devices receiving the settings, warnings and errors. Success is the displayed installation outcome for each requested device, preserving skipped or failed targets. The Finish action closes the wizard after result review; closing it is not a substitute for a successful installation result.

## Patterns

- Validation can skip individual devices; successful installation on one target does not establish fleet-wide success.
- Preview is recommended especially for the first install, when object removals can be unexpected.
- Controller package persistence and actual installation are separate outcomes.

## Known limitations

- This is the official GUI sequence, not an inferred JSON-RPC or NetClaw MCP install operation.
- Installation can remove objects and overwrite device settings.
- The source does not provide a universal retry, completion deadline or automatic rollback guarantee.
- Policy editing, live traffic tests and out-of-band drift comparison are outside this procedure.

## Tools

| Mechanism | Description | Category |
|---|---|---|
| FortiManager web console | Select context/package/targets, validate and review preview | Read |
| FortiManager installation wizard | Confirm and execute or schedule installation; review per-device outcome | Change |

## Verification checklist

- ADOM, package and every selected target match the requested scope.
- Missing mappings and failed validation are resolved or reported as skipped targets.
- Preview and potential object removal were reviewed before confirmation.
- Scheduled status remains distinct from completed installation.
- Per-device outcomes, warnings and errors are retained.
