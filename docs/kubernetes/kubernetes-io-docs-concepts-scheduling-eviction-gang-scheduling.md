---
url: https://kubernetes.io/docs/concepts/scheduling-eviction/gang-scheduling/
title: Gang Scheduling
framework: kubernetes
---

# Gang Scheduling

FEATURE STATE:
`Kubernetes v1.35 [alpha]`(disabled by default)

Gang scheduling ensures that a group of Pods are scheduled on an "all-or-nothing" basis.
If the cluster cannot accommodate the entire group (or a defined minimum number of Pods),
none of the Pods are bound to a node.

This feature depends on the [PodGroup API](/docs/concepts/workloads/podgroup-api/).
Ensure the [`GenericWorkload`](/docs/reference/command-line-tools-reference/feature-gates/#GenericWorkload)
feature gate and the `scheduling.k8s.io/v1alpha2`
[API group](/docs/concepts/overview/kubernetes-api/#api-groups-and-versioning "A set of related paths in the Kubernetes API.") are enabled in the cluster.

## How it works

When the `GangScheduling` plugin is enabled, the scheduler alters the lifecycle for Pods belonging
to a [PodGroup](/docs/concepts/workloads/podgroup-api/) that has a `gang`
[scheduling policy](/docs/concepts/workloads/workload-api/policies/).
The process follows these steps for each PodGroup:

1. The scheduler holds Pods in the `PreEnqueue` phase until:

   * The referenced PodGroup object exists.
   * The number of `Pods` created for the `PodGroup` is at least equal to `minCount`.

   `Pods` do not enter the active scheduling queue until both conditions are met.
2. Once the quorum is met, the scheduler attempts to find placements for all Pods in the group.
   It utilizes the [PodGroup scheduling](/docs/concepts/scheduling-eviction/podgroup-scheduling/) cycle to make a single,
   atomic scheduling decision. `GangScheduling` plugin implements a `Permit` extension point that is evaluated for each
   schedulable Pod during the cycle. This is used to determine whether the `minCount` constraint is satisfied,
   by comparing the number of successfully placed pods against the `minCount` value.
3. If the scheduler finds valid placements for at least the `minCount` number of Pods,
   it allows those successfully placed Pods to be bound to their assigned nodes.
   If it cannot find enough placements to satisfy the `minCount` requirement, none of the Pods are scheduled.
   Instead, they are moved to the unschedulable queue to wait for cluster resources to free up,
   allowing other workloads to be scheduled in the meantime.

## What's next

* Learn about the [PodGroup API](/docs/concepts/workloads/podgroup-api/) and its [lifecycle](/docs/concepts/workloads/podgroup-api/lifecycle/).
* Read about [PodGroup scheduling policies](/docs/concepts/workloads/workload-api/policies/).
* Read about [PodGroup scheduling](/docs/concepts/scheduling-eviction/podgroup-scheduling/).

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

Last modified April 09, 2026 at 9:20 AM PST: [Address feedback (cb3ce08585)](https://github.com/kubernetes/website/commit/cb3ce08585f4a0df41cd789cd48f66746f95f356)