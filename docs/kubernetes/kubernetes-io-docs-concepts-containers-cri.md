---
url: https://kubernetes.io/docs/concepts/containers/cri/
title: Container Runtime Interface (CRI)
framework: kubernetes
---

# Container Runtime Interface (CRI)

The CRI is a plugin interface which enables the kubelet to use a wide variety of
container runtimes, without having a need to recompile the cluster components.

You need a working
[container runtime](/docs/setup/production-environment/container-runtimes "The container runtime is the software that is responsible for running containers.") on
each Node in your cluster, so that the
[kubelet](/docs/reference/command-line-tools-reference/kubelet "An agent that runs on each node in the cluster. It makes sure that containers are running in a pod.") can launch
[Pods](/docs/concepts/workloads/pods/ "A Pod represents a set of running containers in your cluster.") and their containers.

The Container Runtime Interface (CRI) is the main protocol for the communication between the [kubelet](/docs/reference/command-line-tools-reference/kubelet "An agent that runs on each node in the cluster. It makes sure that containers are running in a pod.") and Container Runtime.

The Kubernetes Container Runtime Interface (CRI) defines the main
[gRPC](https://grpc.io) protocol for the communication between the
[node components](/docs/concepts/architecture/#node-components)
[kubelet](/docs/reference/command-line-tools-reference/kubelet "An agent that runs on each node in the cluster. It makes sure that containers are running in a pod.") and
[container runtime](/docs/setup/production-environment/container-runtimes "The container runtime is the software that is responsible for running containers.").

## The API

FEATURE STATE:
`Kubernetes v1.23 [stable]`

The kubelet acts as a client when connecting to the container runtime via gRPC.
The runtime and image service endpoints have to be available in the container
runtime, which can be configured separately within the kubelet by using the
`--container-runtime-endpoint`
[command line flag](/docs/reference/command-line-tools-reference/kubelet/).

For Kubernetes v1.26 and later, the kubelet requires that the container runtime
supports the `v1` CRI API. If a container runtime does not support the `v1` API,
the kubelet will not register the node.

## Upgrading

When upgrading the Kubernetes version on a node, the kubelet restarts. If the
container runtime does not support the `v1` CRI API, the kubelet will fail to
register and report an error. If a gRPC re-dial is required because the container
runtime has been upgraded, the runtime must support the `v1` CRI API for the
connection to succeed. This might require a restart of the kubelet after the
container runtime is correctly configured.

## List streaming

FEATURE STATE:
`Kubernetes v1.36 [alpha]`(disabled by default)

The standard CRI list RPCs (`ListContainers`, `ListPodSandbox`, `ListImages`) return
all results in a single unary response. On nodes with a large number of containers
(for example, more than roughly 10,000 including both running and stopped), these
responses can exceed gRPC's default 16 MiB message size limit, causing the kubelet
to fail when reconciling state with the container runtime.

With the `CRIListStreaming` feature gate enabled, the kubelet uses server-side
streaming RPCs (such as `StreamContainers`, `StreamPodSandboxes`,
`StreamImages`) that allow the container runtime to divide results across
multiple response messages, bypassing the per-message size limit. This is
particularly useful for:

* High container churn environments (CI/CD systems)
* Large-scale batch processing workloads

If the container runtime does not support streaming RPCs, the kubelet
automatically falls back to the standard unary RPCs for backward
compatibility.

## What's next

* Learn more about the CRI [protocol definition](https://github.com/kubernetes/cri-api/blob/v0.33.1/pkg/apis/runtime/v1/api.proto)

## Feedback

Was this page helpful?

Yes
No

Thanks for the feedback. If you have a specific, answerable question about how to use Kubernetes, ask it on
[Stack Overflow](https://stackoverflow.com/questions/tagged/kubernetes).
Open an issue in the [GitHub Repository](https://www.github.com/kubernetes/website/) if you want to
[report a problem](https://github.com/kubernetes/website/issues/new?title=Issue%20with%20k8s.io)
or
[suggest an improvement](https://github.com/kubernetes/website/issues/new?title=Improvement%20for%20k8s.io).

Last modified February 12, 2026 at 2:22 PM PST: [Add documentation for CRIListStreaming feature gate (c609d9f1c2)](https://github.com/kubernetes/website/commit/c609d9f1c254ba1ee59d62098374b445dffc24c3)