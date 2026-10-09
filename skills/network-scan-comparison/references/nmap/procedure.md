# Ndiff saved-scan comparison

Compare two Nmap XML artifacts without sending new probes.

### 1. Select the input pair

Ndiff accepts exactly two Nmap XML files. Their scan options and target/port scope accompany the comparison; different options can themselves explain additional findings. Missing or invalid input is a runtime error, not a detected network change.

### 2. Compare

`ndiff --text <before.xml> <after.xml>` returns a human-readable comparison. `--xml` selects structured difference output and `--verbose` includes unchanged hosts/ports. Native result categories include host/port state, detected service versions, OS matches and script output.

### 3. Report native outcome

Exit 0 means Ndiff found no difference in the dimensions it compares. Exit 1 means differences exist; it is not a command failure. Exit 2 is a runtime error such as an unreadable input. Added and removed observations remain distinct from a claimed production change or root cause.

## Patterns

Comparing a short-port scan with a broader scan can create differences even when the network did not change. Ndiff compares two artifacts at a time.

## Known limitations

No network probe, automatic schedule, email delivery or business success threshold is included.

## Tools

| Mechanism | Description | Category |
|---|---|---|
| Local CLI runner | Execute Ndiff on existing XML files | Local comparison |

## Verification checklist

- Input order is before, then after.
- Scan-option differences are disclosed.
- Exit 1 is a difference, while exit 2 is a runtime error.

## Sources

- [Ndiff reference](https://nmap.org/book/ndiff-man.html). Retrieved 2026-10-09.
