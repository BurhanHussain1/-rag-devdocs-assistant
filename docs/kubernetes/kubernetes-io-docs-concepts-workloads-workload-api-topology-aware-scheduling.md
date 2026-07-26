---
url: https://kubernetes.io/docs/concepts/workloads/workload-api/topology-aware-scheduling/
title: Topology-Aware Workload Scheduling
framework: kubernetes
---

# Topology-Aware Workload Scheduling

FEATURE STATE:
`Kubernetes v1.36 [alpha]`(disabled by default)

*Topology-Aware Scheduling* (TAS) is a feature of the Workload API that optimizes the placement of
pods within the cluster.

TAS ensures that all pods within a PodGroup are co-located into a specific topology domain,
such as a single server rack or zone. This minimizes inter-pod communication latency and prevents
workload fragmentation across the cluster infrastructure.

## Topology-aware scheduling with gang scheduling policy

When applied to PodGroups with `gang` scheduling policy, TAS simulates the potential assignment
(*placement*) of the full group of pods at once. It guarantees that at least the specified
`minCount` pods can fit together into the same topology domain before committing resources.
If no feasible placement is found, the entire PodGroup becomes unschedulable.

This is the recommended approach for workloads like distributed AI and ML training that strictly
require proximity to minimize inter-pod communication latency.

If new pods are added to the PodGroup where some pods are already scheduled (for example, if pods
are recreated), the scheduler will force all new incoming pods to land on the exact same topology
domain where the existing pods currently reside. If that specific domain lacks sufficient capacity
for the new pods, the pods will remain pending - even if it means that less than `minCount` pods
are scheduled at this point.

#### Note:

As of v1.36 Topology-Aware Scheduling does not trigger workload or pod preemption. If no
feasible placement can be found without triggering preemption, the PodGroup becomes unschedulable.

## Topology-aware scheduling with basic scheduling policy

Using TAS with `basic` scheduling policy may exhibit inconsistent behavior. The scheduler may only
observe a subset of pods when entering the PodGroup scheduling cycle - therefore placement
feasibility is only evaluated for the observed pods, rather than the entire PodGroup. To partially
mitigate this limitation, you can use scheduling gates to hold off PodGroup scheduling until all
pods within the PodGroup are in the scheduling queue.

If no feasible placement is found for the entire PodGroup, only a subset of pods may be scheduled,
and they are guaranteed to meet the scheduling constraints.

If new pods are added to the PodGroup where some pods are already scheduled, the scheduler will act
the same as in case of `gang` policy - forcing the new pods into the same domain, unless there is
insufficient capacity (in which case the new pods will remain pending).

## API configuration: scheduling constraints

Every PodGroup (or PodGroupTemplate) may optionally declare the `schedulingConstraints` field,
which is interpreted by the [placement-based PodGroup scheduling algorithm](/docs/concepts/scheduling-eviction/podgroup-scheduling/#placement-scheduling-algorithm).
If constraints are defined in PodGroupTemplate, they will be copied to referencing PodGroups.

As of Kubernetes v1.36, the API supports topology constraints.

#### Note:

As of Kubernetes v1.36, you can specify only a single topology constraint in each PodGroup.

### Topology constraint

To define a topology constraint for a PodGroup you need to set a `key`, which corresponds to
a Kubernetes node label, representing the target topology domain (for example, a rack or a zone).
The scheduler strictly enforces that all pods within the PodGroup are placed onto nodes that share
the exact same value for this specified label.

Here is an example of a PodGroup configured with a topology constraint:

```
apiVersion: scheduling.k8s.io/v1alpha2
kind: PodGroup
metadata:
  name: example-podgroup
spec:
  schedulingPolicy:
    gang:
      minCount: 4
  schedulingConstraints:
    topology:
      - key: topology.example.com/rack
```

## What's next

* Learn about [pod group policies](/docs/concepts/workloads/workload-api/policies/).
* Learn about [plugins related Topology-aware Scheduling](/docs/concepts/scheduling-eviction/topology-aware-scheduling/)
* Read about [gang scheduling](/docs/concepts/scheduling-eviction/gang-scheduling/) algorithm.

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

Last modified March 31, 2026 at 8:55 AM PST: [Apply review comments (9cc579c8a4)](https://github.com/kubernetes/website/commit/9cc579c8a4297033a312d29cabb3b376d259531c)