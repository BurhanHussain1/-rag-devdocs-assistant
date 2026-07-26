---
url: https://kubernetes.io/docs/concepts/workloads/workload-api/policies/
title: PodGroup Scheduling Policies
framework: kubernetes
---

# PodGroup Scheduling Policies

FEATURE STATE:
`Kubernetes v1.35 [alpha]`(disabled by default)

Every [PodGroup](/docs/concepts/workloads/podgroup-api/) must declare a scheduling policy
in its `spec.schedulingPolicy` field. This policy dictates how the scheduler treats the
collection of Pods in the group.

## Policy types

The `schedulingPolicy` field supports two policy types: `basic` and `gang`.
You must specify exactly one.

### Basic policy

The `basic` policy instructs the scheduler to evaluate all Pods on a best-effort basis.
Unlike the `gang` policy, a PodGroup using the `basic` policy is considered feasible
regardless of how many of its Pods are currently schedulable.

The primary reason to use the `basic` policy is to organize Pods into a group for better
observability and management, while still evaluating them together within a single, atomic
[PodGroup scheduling cycle](/docs/concepts/scheduling-eviction/podgroup-scheduling/#podgroup-scheduling-cycle).

This policy is suited for groups that do not require simultaneous startup but logically
belong together, or to open the way for group-level constraints that do not imply
"all-or-nothing" placement.

```
schedulingPolicy:
  basic: {}
```

### Gang policy

The `gang` policy enforces "all-or-nothing" scheduling. This is essential for tightly-coupled
workloads where partial startup results in deadlocks or wasted resources.

This can be used for [Jobs](/docs/concepts/workloads/controllers/job/)
or any other batch process where all workers must run concurrently to make progress.

The `gang` policy requires a `minCount` field, which is the minimum number of Pods that must be
schedulable simultaneously for the group to be feasible:

```
schedulingPolicy:
  gang:
    # The number of Pods that must be schedulable simultaneously
    # for the group to be admitted.
    minCount: 4
```

## Setting policies via PodGroupTemplates

When using the [Workload API](/docs/concepts/workloads/workload-api/), you define scheduling
policies inside `PodGroupTemplates`. The workload controller copies the policy from the
template into each PodGroup it creates, making the PodGroup self-contained. Changes to the
Workload's templates only affect newly created PodGroups, not existing ones.

For standalone PodGroups (created without a Workload), you set `spec.schedulingPolicy`
directly on the PodGroup itself.

## What's next

* See the [PodGroup API](/docs/concepts/workloads/podgroup-api/) for how policies are carried at runtime.
* Learn about the [Workload API](/docs/concepts/workloads/workload-api/) that defines PodGroupTemplates.
* Read about [PodGroup scheduling](/docs/concepts/scheduling-eviction/podgroup-scheduling/).
* Read about the [gang scheduling](/docs/concepts/scheduling-eviction/gang-scheduling/) algorithm.

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