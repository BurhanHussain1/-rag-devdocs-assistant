---
url: https://kubernetes.io/docs/concepts/workloads/autoscaling/
title: Autoscaling Workloads
framework: kubernetes
---

# Autoscaling Workloads

With autoscaling, you can automatically update your workloads in one way or another. This allows your cluster to react to changes in resource demand more elastically and efficiently.

In Kubernetes, you can *scale* a workload depending on the current demand of resources.
This allows your cluster to react to changes in resource demand more elastically and efficiently.

When you scale a workload, you can either increase or decrease the number of replicas managed by
the workload, or adjust the resources available to the replicas in-place.

The first approach is referred to as *horizontal scaling*, while the second is referred to as
*vertical scaling*.

There are manual and automatic ways to scale your workloads, depending on your use case.

## Scaling workloads manually

Kubernetes supports *manual scaling* of workloads. Horizontal scaling can be done
using the `kubectl` CLI.
For vertical scaling, you need to *patch* the resource definition of your workload.

See below for examples of both strategies.

* **Horizontal scaling**: [Running multiple instances of your app](/docs/tutorials/kubernetes-basics/scale/scale-intro/)
* **Vertical scaling**: [Resizing CPU and memory resources assigned to containers](/docs/tasks/configure-pod-container/resize-container-resources/)

## Scaling workloads automatically

Kubernetes also supports *automatic scaling* of workloads, which is the focus of this page.

The concept of *Autoscaling* in Kubernetes refers to the ability to automatically update an
object that manages a set of Pods (for example a
[Deployment](/docs/concepts/workloads/controllers/deployment/ "Manages a replicated application on your cluster.")).

### Scaling workloads horizontally

In Kubernetes, you can automatically scale a workload horizontally using a [HorizontalPodAutoscaler](/docs/concepts/workloads/autoscaling/horizontal-pod-autoscale/) (HPA).

It is implemented as a Kubernetes API resource and a [controller](/docs/concepts/architecture/controller/ "A control loop that watches the shared state of the cluster through the apiserver and makes changes attempting to move the current state towards the desired state.")
and periodically adjusts the number of [replicas](/docs/reference/glossary/?all=true#term-replica "Replicas are copies of pods, ensuring availability, scalability, and fault tolerance by maintaining identical instances.")
in a workload to match observed resource utilization such as CPU or memory usage.

There is a [walkthrough tutorial](/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough/) of configuring a HorizontalPodAutoscaler for a Deployment.

### Scaling workloads vertically

FEATURE STATE:
`Kubernetes v1.25 [stable]`

You can automatically scale a workload vertically using a [VerticalPodAutoscaler](/docs/concepts/workloads/autoscaling/vertical-pod-autoscale/) (VPA).
Unlike the HPA, the VPA doesn't come with Kubernetes by default, but is a an add-on that you or a cluster administrator may need to deploy before you can use it.

Once installed, it allows you to create [CustomResourceDefinitions](/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/ "Custom code that defines a resource to add to your Kubernetes API server without building a complete custom server.")
(CRDs) for your workloads which define *how* and *when* to scale the resources of the managed replicas.

#### Note:

You will need to have the [Metrics Server](https://github.com/kubernetes-sigs/metrics-server)
installed to your cluster for the VPA to work.

#### In-place pod vertical scaling

FEATURE STATE:
`Kubernetes v1.35 [stable]`(enabled by default)

As of Kubernetes 1.36, VPA does not support resizing pods in-place,
but this integration is being worked on.
For manually resizing pods in-place, see [Resize Container Resources In-Place](/docs/tasks/configure-pod-container/resize-container-resources/).

### Autoscaling based on cluster size

For workloads that need to be scaled based on the size of the cluster (for example
`cluster-dns` or other system components), you can use the
[*Cluster Proportional Autoscaler*](https://github.com/kubernetes-sigs/cluster-proportional-autoscaler).
Just like the VPA, it is not part of the Kubernetes core, but hosted as its
own project on GitHub.

The Cluster Proportional Autoscaler watches the number of schedulable [nodes](/docs/concepts/architecture/nodes/ "A node is a worker machine in Kubernetes.")
and cores and scales the number of replicas of the target workload accordingly.

If the number of replicas should stay the same, you can scale your workloads vertically according to the cluster size using
the [*Cluster Proportional Vertical Autoscaler*](https://github.com/kubernetes-sigs/cluster-proportional-vertical-autoscaler).
The project is **currently in beta** and can be found on GitHub.

While the Cluster Proportional Autoscaler scales the number of replicas of a workload,
the Cluster Proportional Vertical Autoscaler adjusts the resource requests for a workload
(for example a Deployment or DaemonSet) based on the number of nodes and/or cores in the cluster.

### Event driven Autoscaling

It is also possible to scale workloads based on events, for example using the
[*Kubernetes Event Driven Autoscaler* (**KEDA**)](https://keda.sh/).

KEDA is a CNCF-graduated project enabling you to scale your workloads based on the number
of events to be processed, for example the amount of messages in a queue. There exists
a wide range of adapters for different event sources to choose from.

### Autoscaling based on schedules

Another strategy for scaling your workloads is to **schedule** the scaling operations, for example in order to
reduce resource consumption during off-peak hours.

Similar to event driven autoscaling, such behavior can be achieved using KEDA in conjunction with
its [`Cron` scaler](https://keda.sh/docs/latest/scalers/cron/).
The `Cron` scaler allows you to define schedules (and time zones) for scaling your workloads in or out.

## Scaling cluster infrastructure

If scaling workloads isn't enough to meet your needs, you can also scale your cluster infrastructure itself.

Scaling the cluster infrastructure normally means adding or removing [nodes](/docs/concepts/architecture/nodes/ "A node is a worker machine in Kubernetes.").
Read [Node autoscaling](/docs/concepts/cluster-administration/node-autoscaling/)
for more information.

## What's next

* Learn more about scaling horizontally
  + [Scale a StatefulSet](/docs/tasks/run-application/scale-stateful-set/)
  + [HorizontalPodAutoscaler Walkthrough](/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough/)
* [Resize Container Resources In-Place](/docs/tasks/configure-pod-container/resize-container-resources/)
* [Autoscale the DNS Service in a Cluster](/docs/tasks/administer-cluster/dns-horizontal-autoscaling/)
* Learn about [Node autoscaling](/docs/concepts/cluster-administration/node-autoscaling/)

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

Last modified November 23, 2025 at 1:47 PM PST: [Move HorizontalPodAutoscaler concept page (57e1fdd7f9)](https://github.com/kubernetes/website/commit/57e1fdd7f9217d9379663ed7f9b5614707d64c36)