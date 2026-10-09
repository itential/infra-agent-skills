# Kubernetes NetworkPolicy evaluation

Evaluate core NetworkPolicy selection and allowed-connection rules.

### 1. Establish readable scope

The request identifies a kubeconfig context, namespace and object scope. Commands use `--context <context>` and `--namespace <namespace>`; `--all-namespaces` is used only for a requested cluster-wide list. `kubectl auth can-i list <resource> --namespace <namespace>` checks each needed resource permission, and `kubectl get namespace <namespace>` resolves the namespace when permitted. A denial, missing namespace, unsupported resource, TLS or transport error leaves that scope unresolved. It is not an empty successful inventory.

### 2. Establish the connection and relevant labels

The connection identifies source and destination Pods/namespaces or external address, protocol and destination port. `kubectl get pod <pod> --namespace <namespace> -o json` and `kubectl get namespace <namespace> -o json` provide current labels. Missing peers or inaccessible namespace labels prevent a complete selector evaluation. Host-networked Pods and address translation require plugin-specific guidance because the core model does not define a universal outcome.

### 3. Read all relevant policies

`kubectl get networkpolicies --namespace <namespace> -o yaml` collects policies in each relevant Pod namespace. Restricting this list by an unrelated selector can hide applicable policies. `kubectl describe networkpolicy <policy> --namespace <namespace>` shows the API's interpretation when YAML grouping is unclear. A missing CNI-specific resource definition does not establish absence of all policies; only core NetworkPolicy is covered here.

### 4. Evaluate each direction

A Pod is isolated in a direction when a selecting policy includes that direction. With no selecting policy for that direction, core NetworkPolicy imposes no isolation in it. For an isolated direction, allowed connections are the union of applicable allow rules; rule order is not a precedence scheme.

Within a peer entry, namespace and Pod selectors together mean Pods matching both constraints. Separate entries form alternatives. A Pod selector without a namespace selector refers to the policy namespace. An empty Pod selector selects every Pod in that namespace. Address blocks retain their exclusions; translation order can alter observed addresses and is implementation-dependent.

For a connection between Pods, the source's egress and destination's ingress must both permit it. Rule peers and ports constrain the same allowed connection. Protocol and numeric/named port interpretations follow the actual policy. Port ranges require a supported plugin, numeric start/end and an end not below the start.

### 5. Report the modeled result

The result names matching policies and rules for each direction, or the absence of core isolation. It does not claim that all traffic is reachable. The network plugin must implement NetworkPolicy, and the API does not expose the instant a policy becomes enforced. Existing connections, host-networked Pods, non-TCP/UDP/SCTP protocols and translated addresses can require implementation-specific evidence.

## Patterns

Core NetworkPolicy is additive and direction-specific. An ingress-only policy does not isolate egress. A namespace with no core policies can still be subject to other enforcement mechanisms.

## Known limitations

The core resource does not implement explicit deny-rule precedence, TLS policy, Service-name targeting, or an advanced reachability oracle. No policy writes or traffic tests occur here.

## Tools

| Mechanism | Description | Category |
|---|---|---|
| Authenticated kubectl client | Read policies and peer labels | Kubernetes read |

## Verification checklist

- Complete readable scope is established.
- Peer and namespace labels are observed.
- Ingress and egress are evaluated independently and combined.
- Modeled allowance is not reported as verified connectivity.

## Sources

- [kubectl get](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_get/). Retrieved 2026-10-09.
- [Authorization checks](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_auth/kubectl_auth_can-i/). Retrieved 2026-10-09.
- [Network policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/). Retrieved 2026-10-09.
