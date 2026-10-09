# Kubernetes Service endpoint diagnosis

Follow the documented Service object checks and distinguish unresolved backend states.

### 1. Establish readable scope

The request identifies a kubeconfig context, namespace and object scope. Commands use `--context <context>` and `--namespace <namespace>`; `--all-namespaces` is used only for a requested cluster-wide list. `kubectl auth can-i list <resource> --namespace <namespace>` checks each needed resource permission, and `kubectl get namespace <namespace>` resolves the namespace when permitted. A denial, missing namespace, unsupported resource, TLS or transport error leaves that scope unresolved. It is not an empty successful inventory.

### 2. Resolve the Service or Ingress backend

`kubectl get service <service> --namespace <namespace> -o json` establishes the Service, its type, selector, ports and target ports. NotFound is a missing object, not proof of a network outage. For an Ingress request, `kubectl get ingress <ingress> --namespace <namespace> -o json` identifies each configured backend Service/port; each reference is resolved in that namespace. An absent backend Service or unmatched Service port is reported at that link. An Ingress controller must implement the resource for traffic handling; the object alone does not establish that it does.

### 3. Branch on selector and selected Pods

For a Service with a selector, `kubectl get pods --namespace <namespace> --selector <exact-service-selector> -o json` resolves the selected Pods. Zero matching Pods is a selector/available-Pod finding. A selectorless or ExternalName Service does not use this Pod-selection branch; its platform-specific endpoint/DNS behavior remains outside this branch.

For matches, the Service protocol and target port are compared with the intended application port. Named target ports resolve against named Pod ports. Numeric target ports do not require a container-port declaration; the declaration itself cannot prove that an application is listening. Pod readiness and observed condition reasons remain separate evidence.

### 4. Branch on endpoint state

`kubectl get endpointslices --namespace <namespace> --selector kubernetes.io/service-name=<service> -o json` reads all associated slices. Endpoint identities are aggregated and deduplicated across slices, preserving address family, ports, target references and conditions.

No addresses is a missing-backend observation; the preceding selector and Pod evidence determines whether any narrower conclusion is supported. Existing endpoints retain `ready`, `serving` and `terminating` separately. The Service option that publishes non-ready addresses makes ready true even without ordinary readiness; terminating endpoints can still serve during supported draining behavior. Therefore a non-ready count is not a universal zero-capacity verdict.

### 5. State the diagnostic boundary

The result reports every checked relationship and any unresolved one. If references, selection and endpoint states are consistent, the conclusion is that these object checks found no mismatch. Actual traffic, DNS, network-policy enforcement and Service proxy operation remain untested; the publisher's broader service-debug procedure supplies those separate investigations.

## Patterns

An endpoint may appear in multiple slices during updates. One-slice inspection can miss backends. Readiness exceptions and draining behavior invalidate a simple ready/not-ready capacity calculation.

## Known limitations

No workload creation, exec, traffic generation, policy change or proxy reconfiguration is included. API reads across objects are observations over time, not an atomic network snapshot.

## Tools

| Mechanism | Description | Category |
|---|---|---|
| Authenticated kubectl client | Read Service, Ingress, Pod and EndpointSlice objects | Kubernetes read |

## Verification checklist

- Backend names and Service ports resolve or have an explicit missing-object result.
- Exact selectors and matched Pod counts are retained.
- All slices are included and duplicate endpoints handled.
- Readiness exceptions and untested traffic paths are disclosed.

## Sources

- [kubectl get](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_get/). Retrieved 2026-10-09.
- [Authorization checks](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_auth/kubectl_auth_can-i/). Retrieved 2026-10-09.
- [Debug Services](https://kubernetes.io/docs/tasks/debug/debug-application/debug-service/). Retrieved 2026-10-09.
- [EndpointSlices](https://kubernetes.io/docs/concepts/services-networking/endpoint-slices/). Retrieved 2026-10-09.
- [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/). Retrieved 2026-10-09.
