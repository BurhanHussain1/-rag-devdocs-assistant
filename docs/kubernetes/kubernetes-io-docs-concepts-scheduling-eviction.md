---
url: https://kubernetes.io/docs/concepts/scheduling-eviction/
title: Scheduling, Preemption and Eviction
framework: kubernetes
---

# Scheduling, Preemption and Eviction

In Kubernetes, scheduling refers to making sure that [Pods](/docs/concepts/workloads/pods/ "A Pod represents a set of running containers in your cluster.")
are matched to [Nodes](/docs/concepts/architecture/nodes/ "A node is a worker machine in Kubernetes.") so that the
[kubelet](/docs/reference/command-line-tools-reference/kubelet "An agent that runs on each node in the cluster. It makes sure that containers are running in a pod.") can run them. Preemption
is the process of terminating Pods with lower [Priority](/docs/concepts/scheduling-eviction/pod-priority-preemption/#pod-priority "Pod Priority indicates the importance of a Pod relative to other Pods.")
so that Pods with higher Priority can schedule on Nodes. Eviction is the process
of terminating one or more Pods on Nodes.

## Scheduling

* [Kubernetes Scheduler](/docs/concepts/scheduling-eviction/kube-scheduler/)
* [Assigning Pods to Nodes](/docs/concepts/scheduling-eviction/assign-pod-node/)
* [Pod Overhead](/docs/concepts/scheduling-eviction/pod-overhead/)
* [Pod Topology Spread Constraints](/docs/concepts/scheduling-eviction/topology-spread-constraints/)
* [Taints and Tolerations](/docs/concepts/scheduling-eviction/taint-and-toleration/)
* [Scheduling Framework](/docs/concepts/scheduling-eviction/scheduling-framework/)
* [Dynamic Resource Allocation](/docs/concepts/scheduling-eviction/dynamic-resource-allocation/)
* [Scheduler Performance Tuning](/docs/concepts/scheduling-eviction/scheduler-perf-tuning/)
* [Resource Bin Packing for Extended Resources](/docs/concepts/scheduling-eviction/resource-bin-packing/)
* [Pod Scheduling Readiness](/docs/concepts/scheduling-eviction/pod-scheduling-readiness/)
* [PodGroup Scheduling](/docs/concepts/scheduling-eviction/podgroup-scheduling/)
* [Gang Scheduling](/docs/concepts/scheduling-eviction/gang-scheduling/)
* [Topology-aware Scheduling](/docs/concepts/scheduling-eviction/topology-aware-scheduling/)
* [Workload-Aware preemption](/docs/concepts/scheduling-eviction/workload-aware-preemption/)
* [Descheduler](https://github.com/kubernetes-sigs/descheduler#descheduler-for-kubernetes)
* [Node Declared Features](/docs/concepts/scheduling-eviction/node-declared-features/)

## Pod Disruption

[Pod disruption](/docs/concepts/workloads/pods/disruptions/) is the process by which
Pods on Nodes are terminated either voluntarily or involuntarily.

Voluntary disruptions are started intentionally by application owners or cluster
administrators. Involuntary disruptions are unintentional and can be triggered by
unavoidable issues like Nodes running out of [resources](/docs/reference/glossary/?all=true#term-infrastructure-resource "A defined amount of infrastructure available for consumption (CPU, memory, etc)."),
or by accidental deletions.

* [Pod Priority and Preemption](/docs/concepts/scheduling-eviction/pod-priority-preemption/)
* [Node-pressure Eviction](/docs/concepts/scheduling-eviction/node-pressure-eviction/)
* [API-initiated Eviction](/docs/concepts/scheduling-eviction/api-eviction/)

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

Last modified February 26, 2026 at 11:21 AM PST: [KEP-5710: Update scheduler docs for workload aware preemption (29bd816087)](https://github.com/kubernetes/website/commit/29bd816087990aa2bf7e70ab889421d8014c0fca)