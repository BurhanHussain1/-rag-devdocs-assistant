---
url: https://kubernetes.io/docs/concepts/storage/storage-limits/
title: Node-specific Volume Limits
framework: kubernetes
---

# Node-specific Volume Limits

This page describes the maximum number of volumes that can be attached
to a Node for various cloud providers.

Cloud providers like Google, Amazon, and Microsoft typically have a limit on
how many volumes can be attached to a Node. It is important for Kubernetes to
respect those limits. Otherwise, Pods scheduled on a Node could get stuck
waiting for volumes to attach.

## Kubernetes default limits

The Kubernetes scheduler has default limits on the number of volumes
that can be attached to a Node:

| Cloud service | Maximum volumes per Node |
| --- | --- |
| [Amazon Elastic Block Store (EBS)](https://aws.amazon.com/ebs/) | 39 |
| [Google Persistent Disk](https://cloud.google.com/persistent-disk/) | 16 |
| [Microsoft Azure Disk Storage](https://azure.microsoft.com/en-us/services/storage/main-disks/) | 16 |

## Dynamic volume limits

FEATURE STATE:
`Kubernetes v1.17 [stable]`

Dynamic volume limits are supported for following volume types.

* Amazon EBS
* Google Persistent Disk
* Azure Disk
* CSI

For volumes managed by in-tree volume plugins, Kubernetes automatically determines the Node
type and enforces the appropriate maximum number of volumes for the node. For example:

* On
  [Google Compute Engine](https://cloud.google.com/compute/),
  up to 127 volumes can be attached to a node, [depending on the node
  type](https://cloud.google.com/compute/docs/disks/#pdnumberlimits).
* For Amazon EBS disks on M5,C5,R5,T3 and Z1D instance types, Kubernetes allows only 25
  volumes to be attached to a Node. For other instance types on
  [Amazon Elastic Compute Cloud (EC2)](https://aws.amazon.com/ec2/),
  Kubernetes allows 39 volumes to be attached to a Node.
* On Azure, up to 64 disks can be attached to a node, depending on the node type. For more details, refer to [Sizes for virtual machines in Azure](https://docs.microsoft.com/en-us/azure/virtual-machines/windows/sizes).
* If a CSI storage driver advertises a maximum number of volumes for a Node (using `NodeGetInfo`), the [kube-scheduler](/docs/reference/command-line-tools-reference/kube-scheduler/ "Control plane component that watches for newly created pods with no assigned node, and selects a node for them to run on.") honors that limit.
  Refer to the [CSI specifications](https://github.com/container-storage-interface/spec/blob/master/spec.md#nodegetinfo) for details.
* For volumes managed by in-tree plugins that have been migrated to a CSI driver, the maximum number of volumes will be the one reported by the CSI driver.

### Mutable CSI Node Allocatable Count

FEATURE STATE:
`Kubernetes v1.36 [stable]`(enabled by default)

CSI drivers can dynamically adjust the maximum number of volumes that can be attached to a Node at runtime. This enhances scheduling accuracy and reduces pod scheduling failures due to changes in resource availability.

To use this feature, you must enable the `MutableCSINodeAllocatableCount` feature gate on the following components:

* `kube-apiserver`
* `kubelet`

#### Periodic Updates

When enabled, CSI drivers can request periodic updates to their volume limits by setting the `nodeAllocatableUpdatePeriodSeconds` field in the `CSIDriver` specification. For example:

```
apiVersion: storage.k8s.io/v1
kind: CSIDriver
metadata:
  name: hostpath.csi.k8s.io
spec:
  nodeAllocatableUpdatePeriodSeconds: 60
```

Kubelet will periodically call the corresponding CSI driver’s `NodeGetInfo` endpoint to refresh the maximum number of attachable volumes, using the interval specified in `nodeAllocatableUpdatePeriodSeconds`. The minimum allowed value for this field is 10 seconds.

If a volume attachment operation fails with a `ResourceExhausted` error (gRPC code 8), Kubernetes triggers an immediate update to the allocatable volume count for that Node. Additionally, kubelet marks affected pods as Failed, allowing their controllers to handle recreation. This prevents pods from getting stuck indefinitely in the `ContainerCreating` state.

### Preventing Pod placement without CSI driver

FEATURE STATE:
`Kubernetes v1.35 [alpha]`(disabled by default)

If `VolumeLimitScaling` [feature gate](/docs/reference/command-line-tools-reference/feature-gates/#VolumeLimitScaling) is enabled and a CSI driver has corresponding `CSIDriver` object installed with `spec.preventPodSchedulingIfMissing` set to true then scheduler will prevent pod placement to nodes that do not yet have CSI driver installed. For example:

```
apiVersion: storage.k8s.io/v1
kind: CSIDriver
metadata:
  name: hostpath.csi.k8s.io
spec:
  preventPodSchedulingIfMissing: true
```

This limitation only applies to pods that require corresponding CSI volume.

### CSI volume attach limits and cluster autoscaler

If `--enable-csi-node-aware-scheduling` option is enabled in cluster-autoscaler, then cluster-autoscaler can
accurately calculate number of nodes required to satisfy pending pods that require CSI volumes.

If you are using cluster-autoscaler in your
Kubernetes cluster, we do not recommend preventing pod placement via `PreventPodSchedulingIfMissing` field,
unless cluster-autoscaler also has `--enable-csi-node-aware-scheduling` command line option enabled. Underlying reason for this limitation while `VolumeLimitScaling`
feature remains in alpha is - preventing pod placement can break scheduling simulation cluster-autoscaler runs if cluster-autoscaler is not already aware of CSI volume limits. We expect this limitation to go away once `--enable-csi-node-aware-scheduling` becomes enabled by default in cluster-autoscaler.

Command line `--enable-csi-node-aware-scheduling` in cluster-autoscaler can be enabled regardless of `VolumeLimitScaling` feature state in Kubernetes. We recommend enabling it if your cluster is
using CSI volumes and you are running into issues related to, too many pods crowding a node when a new node is spun via cluster-autoscaler, because current version of
cluster-autoscaler does not compute correct number of nodes required to satisfy all pending pods.

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

Last modified June 14, 2026 at 9:13 PM PST: [Fix typos in manual documentation pages (7e01eaee12)](https://github.com/kubernetes/website/commit/7e01eaee123c18c295656cea5cd03886fcbd2cc5)