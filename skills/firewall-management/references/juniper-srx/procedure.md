# Juniper SRX (Junos OS) — Firewall Policy Management Procedure

Manages address books and address sets, custom applications and application sets, and security
policies (zone-pair and global) on an SRX Series firewall or vSRX running Junos OS, through the Junos
CLI, including the commit step that makes a change live. This procedure is CLI-driven: commands stay
inline and there is no `endpoints.md`. Source NAT, destination NAT and static NAT, deactivating a
policy, policy-based or remote-access VPN, the Junos REST interface, Security Director, and
unified/application-aware policy features are out of scope. IPsec tunnel objects and the zone and
policy plumbing around them are covered by the VPN tunnel capability, not here. Assumes CLI access to
the target SRX (console, SSH, or an orchestration layer that runs CLI on your behalf) and that
security zones already exist.

Junos edits a **candidate configuration** in configuration mode. Nothing affects traffic until a
commit activates it, so every write below is followed by the commit steps at the end of the
operational procedure.

## Common Sequences

- **Permit new traffic between two zones:** create or confirm the address entries (and address sets),
  confirm the application or application set, create the policy, check its position against existing
  policies, commit with confirmation, verify.
- **Remove access:** find what references the object or policy, confirm with the operator, delete,
  commit with confirmation, verify.
- **Fix a shadowed policy:** list shadowing relationships, move the more specific policy ahead,
  commit with confirmation, verify.

## Operational procedure

### Enter configuration mode

Statements below are entered in configuration mode. Three entry forms are documented: the default
shared mode, `configure private`, and `configure exclusive`. They differ in what a later commit
activates (see Commit), and the private and exclusive forms keep other users' unfinished edits out of
your commit. Choose deliberately before editing. How to leave configuration mode, and when an exclusive
lock is released, is not covered here; treat it as unknown and confirm on the device.

```
configure
configure private
configure exclusive
```

### Create or update an address entry or address set

Entries live in a named address book. A zone-attached book serves zone-pair policies for the zone it
is attached to; the book named `global` is always present, needs no attachment, serves zones that have
no attached book, and is the only book that global policies and NAT rules can use. A zone with an
attached book looks addresses up there first and falls back to the global book. The book attached to a
zone must hold every address reachable in that zone, and a zone-pair policy needs entries in each of
its two zones' books.

```
set security address-book <book> address <name> <ip-or-prefix>
set security address-book <book> address <name> range-address <low-ip> to <high-ip>
set security address-book <book> address <name> wildcard-address <a.b.c.d/wildcard-mask>
set security address-book <book> address <name> dns-name <fqdn>
set security address-book <book> address-set <set-name> address <name>
set security address-book <book> attach zone <zone>
```

Address entries may be IPv4, IPv6, wildcard, or DNS name. DNS names need DNS services already set up
on the device. A network prefix must carry zero bits beyond its prefix length; a host name or a /32
uses the full length. **Documentation defect:** the vendor's own worked examples include prefixes with
host bits set (for example a host address written with /24). Follow the stated rule and write the
network address, or use a /32 for a single host.

Naming rules: `any`, `any-ipv4` and `any-ipv6` are reserved and cannot be created; address names must
not start with `static_nat_`, `incoming_nat_` or `junos_`; an address and an address set in the same
zone cannot share a name. An address set holds only addresses from the same zone and may mix IPv4 and
IPv6. Nesting an address set inside a set is documented as supported; its exact statement was not
captured in this pass, so confirm it on the device before relying on it. Wildcard addresses, DNS names,
and mixed IPv4/IPv6 sets are not usable in NAT rules (NAT is out of scope here).

### Read address books

```
show security address-book
show security address-book global
```

### Delete an address entry, address set, or address book attachment

**Stop and confirm with the operator before proceeding.** Find every address set and policy that
references the entry first. Junos documents that removing an address still named in an address set
makes the commit fail, so remove it from each set first, and that an address set referenced by a
policy cannot be removed until the policy reference is removed. The source does not state a check for
an address named directly in a policy, so treat that as unchecked and look for it yourself.

```
delete security address-book <book> address <name>
delete security address-book <book> address-set <set-name>
```
(The delete form is the generic Junos `delete` statement; the vendor documentation shows it only for application
statements, so this exact form is an assumption to confirm on the device.)

### Create or update a custom application or application set

Predefined applications (their names start with `junos-`) need no configuration and each carries a full
source port range of 1–65535. A custom application defines a protocol, ports (or ICMP type and code),
and an inactivity timeout; unset, the timeout is 1800 seconds, and `never` disables it. A custom
application that needs an ALG or deep inspection is defined with a term that names the ALG type. Names
must not start with `junos_`. Application sets group applications so policies reference one name; from
Junos release 25.4 an application set that also contains the `any` application is no longer supported,
so review such sets before upgrading.

```
set applications application <name> protocol {tcp | udp} source-port <range> destination-port <range>
set applications application <name> inactivity-timeout {<seconds> | never}
set applications application <name> term <term> alg <alg-type> protocol <proto> destination-port <range>
set applications application-set <set-name> application <application-name>
```

Modifying a custom application means deleting the old port statements and setting the new ones before
the commit; timeouts of several rule entries inside one application are shared.

### Read applications

```
show applications
show applications application <name>
```

### Create or update a security policy

A policy belongs to a from-zone/to-zone pair (a context), has a unique name, and requires three match
criteria (source address, destination address, application) plus one action. Source and destination
addresses are names of address entries or sets in the matching zone's book, or the predefined `any`,
`any-ipv4`, `any-ipv6`; the application is a predefined or custom application, an application set, or
`any`. Actions are permit, deny, or reject; `log` (at session start, session end, or both) and `count`
are optional accounting elements. Within a context, policies are matched top to bottom, the first match
wins, a new policy is appended at the end, and traffic that matches nothing is dropped.

```
set security policies from-zone <from> to-zone <to> policy <name> match source-address <addr-or-set>
set security policies from-zone <from> to-zone <to> policy <name> match destination-address <addr-or-set>
set security policies from-zone <from> to-zone <to> policy <name> match application <app-or-set>
set security policies from-zone <from> to-zone <to> policy <name> then {permit | deny | reject}
set security policies from-zone <from> to-zone <to> policy <name> then log {session-init | session-close}
set security policies from-zone <from> to-zone <to> policy <name> then count
```

Negated matching is available with `match source-address-excluded` or `match destination-address-excluded`
alongside the address statement; excluded entries cannot be wildcard, IPv6, `any`, `any-ipv4`,
`any-ipv6`, or 0.0.0.0, and a policy with exclusions is limited to 10 source or destination addresses.
Wildcard-address policies are capped at 480 per context and should not be used with content-security
services. When IPv6 flow support is on, address counts are limited by the weighted formula the vendor
gives (an IPv6 entry counts four times an IPv4 one, total at most 1024 per side). If a policy that uses
`any` fails to commit with content-security features enabled, the vendor's fix is `any-ipv4` plus
separate IPv6 rules.

**Global policies** live in their own list and are matched only after intra-zone and inter-zone
policies. They use addresses from the global book, and zones are optional match criteria:

```
set security policies global policy <name> match source-address <addr-or-set>
set security policies global policy <name> match destination-address <addr-or-set>
set security policies global policy <name> match application <app-or-set>
set security policies global policy <name> match from-zone <zone>
set security policies global policy <name> match to-zone <zone>
set security policies global policy <name> then {permit | deny | reject}
```

A global policy that names no zones cannot carry a VPN tunnel. A catch-all rule (any/any/any) in any
zone-pair policy means global policies are never reached; with global policies in use, the deny-all
rule belongs in the global list. Multi-zone global policies are safest with identical match criteria
and action across zones, since mixed ones can be satisfied by spoofed traffic. Do not use `global` as a
from-zone or to-zone name in a zone-pair policy (the only exception is a static/incoming NAT case,
which is out of scope).

### Read security policies

```
show security policies
show security policies from-zone <from> to-zone <to> policy-name <name> detail
show security policies global
```

### Delete a security policy

**Stop and confirm with the operator before proceeding.** Removing a policy changes what traffic is
permitted or dropped, and can expose or block traffic that a later policy would otherwise decide.
Confirm the intended effect and the policy's place in the list first.

```
delete security policies from-zone <from> to-zone <to> policy <name>
delete security policies global policy <name>
```
(Same note as above: the delete form is the generic Junos statement, to be confirmed on the device.)

### Reorder policies and detect shadowing

**Stop and confirm with the operator before proceeding** when a reorder changes which policy first
matches live traffic. Reordering uses `insert … before`; an `after` form is not covered by the vendor documentation.
A policy is shadowed when an earlier policy already matches everything it would.

```
insert security policies from-zone <from> to-zone <to> policy <name> before policy <other-name>
show security shadow-policies from-zone <from> to-zone <to>
show security shadow-policies global
```
The vendor's shadow-policy examples also carry a logical-system argument; whether that argument is
optional on a device without logical systems is not stated. The tool reports shadowing and leaves
correction to the operator. **Documentation defect:** the vendor's first reorder example contains
malformed `set` lines (missing policy name); use the full statements shown above instead.

### Commit

**Stop and confirm with the operator before every commit** — a commit activates the candidate
configuration on a live firewall. Check first and prefer the confirmed form, whose auto-rollback is
the vendor's own safeguard.

```
commit check
commit confirmed [<minutes>]
show system commit
commit
```

`commit check` validates syntax without activating. `commit confirmed` activates temporarily; unless a
further `commit` (or `commit check`, as the vendor documentation states) arrives within the window — 10 minutes by
default, or the minutes given — the device rolls back to the prior configuration and broadcasts a
message to logged-in users. `show system commit` lists the scheduled rollback. A commit can fail on
syntax errors, a candidate larger than 700 MB, or another user's exclusive configuration lock.

Candidate scope depends on how configuration mode was entered: the default shared mode commits every
user's pending edits; `configure private` commits only your own edits (and `update` refreshes your copy
after others commit); `configure exclusive` locks the candidate so others cannot commit while you hold
it. A plain `commit` in shared mode therefore activates other people's unfinished changes.

## Patterns

- **Policy changes can disrupt established sessions.** Changing a policy's match or action, adding or
  deleting a policy, or changing order can disturb flow sessions during commit. The documented
  mitigation is the `lookup-intact-on-commit` policy option; it needs free kernel and user heap (at
  least 5% and 1%), a forwarding-plane restart when first enabled, and is set at the root level only.
  `show security policies lookup-intact-on-commit` reports eligibility. File-serialization of policy
  synchronization is on by default and can be turned off with a `no-file-serialization` statement.
  Supported platforms are model-dependent; check feature support for the target model and release.
- **Order is meaning.** Put specific policies above general ones, IPsec tunnel policies near the top,
  and deny-all or reject-all at the bottom.
- **Zone with an attached book versus the global book.** A name that exists in both is resolved from
  the attached book first, so a global-book entry of the same name can be silently hidden.
- **A commit error may mean a platform limit, not a typo.** Per-policy address-object counts are
  platform-specific; exceeding one produces a commit error naming the source (or destination)
  addresses-per-policy limit. Policy, context, and address-object ceilings vary by model; this
  procedure does not carry per-model numbers.
- **Sets expand internally.** A policy referencing sets of addresses and application sets consumes
  resources per member combination, so large sets on both sides plus an application set can exhaust
  policy capacity.

## Known limitations

- All NAT (source, destination, static) is out of scope; NAT rules use only the global address book.
- Deactivating a policy, policy-based VPN, and the Junos REST interface were not covered.
- Per-model scale limits, HA chassis-cluster commit behavior, and `commit synchronize` use on dual
  Routing Engine systems were not verified for this procedure; treat them as unknown.
- Nested address-set syntax, an `insert … after` form, and the delete forms noted above are unverified
  details to confirm on the device.
- Applies to Junos releases whose documentation matches the behavior described; the 25.4 application-
  set change is the one release-specific item captured.

## Tools

| Operation | Description | Category |
|---|---|---|
| Junos CLI session, configuration mode | Create, update, delete, and insert address, application, and policy statements in the candidate configuration, and validate, activate (with optional auto-rollback), and finalize it | Configuration |
| Junos CLI session, operational and configuration-mode `show` | Read address books, applications, policies, shadow-policy report, and commit history | Read |

## Verification checklist

- [ ] Every address and application a policy names exists in the right book for the right zone, checked
      with `show security address-book` and `show applications`
- [ ] The policy's position relative to other policies in its context (and global list) was reviewed,
      and shadowing was checked
- [ ] Deletes were preceded by a reference check and explicit operator confirmation
- [ ] `commit check` passed, the change was activated with `commit confirmed`, and the operator
      confirmed with a final `commit` before the rollback window ended
- [ ] The resulting policy was read back with `show security policies … detail` and matches the intended
      zones, addresses, application, and action
- [ ] Any commit error about per-policy address limits, content-security `any` addresses, or reserved
      names was handled as described above rather than retried unchanged
