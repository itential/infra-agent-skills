# Kubernetes workload state inspection

Read workload objects and inspect pod conditions without changing them.

### 1. Establish readable scope

The request identifies a kubeconfig context, namespace and object scope. Commands use `--context <context>` and `--namespace <namespace>`; `--all-namespaces` is used only for a requested cluster-wide list. `kubectl auth can-i list <resource> --namespace <namespace>` checks each needed resource permission, and `kubectl get namespace <namespace>` resolves the namespace when permitted. A denial, missing namespace, unsupported resource, TLS or transport error leaves that scope unresolved. It is not an empty successful inventory.

### 2. Read the requested objects

`kubectl get pods --namespace <namespace> -o json` returns pod identities, labels, phase and container statuses. Requested controller resources are listed explicitly, for example `kubectl get deployments,statefulsets,daemonsets --namespace <namespace> -o json`. A selector is included only when requested and remains visible in the result. A failed resource list is reported separately instead of silently omitted.

### 3. Inspect affected pods

`kubectl describe pod <pod> --namespace <namespace>` provides container states, conditions and recent events. A Pending pod requires the observed scheduling or initialization reason; Pending alone does not identify one cause. Waiting/image-pull failures retain the actual image and event reason. Repeated restarts retain container waiting/termination reasons and restart counts; a displayed backoff is not a distinct Pod phase.

A Running phase means containers have been created and at least one is running, starting or restarting. Readiness is reported independently. Failed and Succeeded phases retain their native meaning; an Unknown phase means state could not be obtained. Missing events do not prove that no failure occurred.

### 4. Report coverage

The output names context, namespace/all-namespace scope, selectors, each resource type inspected, native conditions and observed event messages. The read results confirm inventory collection; workload health is limited to the observed state. No unobserved readiness or root cause is added.

## Patterns

The displayed kubectl status column can contain reasons such as CrashLoopBackOff that are not Pod phases. Containers and Pods have separate state models.

## Known limitations

Pod descriptions may contain environment values and application details; this procedure does not request Secrets or expose credential material in its report. Event retention and the set of visible objects depend on the cluster.

## Tools

| Mechanism | Description | Category |
|---|---|---|
| Authenticated kubectl client | Read workload resources and describe pods | Kubernetes read |

## Verification checklist

- Context and scope are explicit.
- Failed/inaccessible lists remain coverage gaps.
- Pod phase, container state and readiness remain distinct.
- Findings cite observed conditions/events.

## Sources

- [kubectl get](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_get/). Retrieved 2026-10-09.
- [Authorization checks](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_auth/kubectl_auth_can-i/). Retrieved 2026-10-09.
- [Pod lifecycle](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/). Retrieved 2026-10-09.
- [Debug Pods](https://kubernetes.io/docs/tasks/debug/debug-application/debug-pods/). Retrieved 2026-10-09.
