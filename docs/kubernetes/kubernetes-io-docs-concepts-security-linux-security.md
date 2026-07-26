---
url: https://kubernetes.io/docs/concepts/security/linux-security/
title: Security For Linux Nodes
framework: kubernetes
---

# Security For Linux Nodes

This page describes security considerations and best practices specific to the Linux operating system.

## Protection for Secret data on nodes

On Linux nodes, memory-backed volumes (such as [`secret`](/docs/concepts/configuration/secret/)
volume mounts, or [`emptyDir`](/docs/concepts/storage/volumes/#emptydir) with `medium: Memory`)
are implemented with a `tmpfs` filesystem.

If you have swap configured and use an older Linux kernel (or a current kernel and an unsupported configuration of Kubernetes),
**memory** backed volumes can have data written to persistent storage.

The Linux kernel officially supports the `noswap` option from version 6.3,
therefore it is recommended the used kernel version is 6.3 or later,
or supports the `noswap` option via a backport, if swap is enabled on the node.

Read [swap memory management](/docs/concepts/cluster-administration/swap-memory-management/#memory-backed-volumes)
for more info.

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

Last modified June 22, 2025 at 4:08 PM PST: [Add a linux-security doc entry (24b1f35dfb)](https://github.com/kubernetes/website/commit/24b1f35dfbdb1f63520f5c69d8a825758c0f1b5b)