---
url: https://kubernetes.io/docs/concepts/security/windows-security/
title: Security For Windows Nodes
framework: kubernetes
---

# Security For Windows Nodes

This page describes security considerations and best practices specific to the Windows operating system.

## Protection for Secret data on nodes

On Windows, data from Secrets are written out in clear text onto the node's local
storage (as compared to using tmpfs / in-memory filesystems on Linux). As a cluster
operator, you should take both of the following additional measures:

1. Use file ACLs to secure the Secrets' file location.
2. Apply volume-level encryption using
   [BitLocker](https://docs.microsoft.com/windows/security/information-protection/bitlocker/bitlocker-how-to-deploy-on-windows-server).

## Container users

[RunAsUsername](/docs/tasks/configure-pod-container/configure-runasusername/)
can be specified for Windows Pods or containers to execute the container
processes as specific user. This is roughly equivalent to
[RunAsUser](/docs/concepts/security/pod-security-policy/#users-and-groups).

Windows containers offer two default user accounts, ContainerUser and ContainerAdministrator.
The differences between these two user accounts are covered in
[When to use ContainerAdmin and ContainerUser user accounts](https://docs.microsoft.com/virtualization/windowscontainers/manage-containers/container-security#when-to-use-containeradmin-and-containeruser-user-accounts)
within Microsoft's *Secure Windows containers* documentation.

Local users can be added to container images during the container build process.

#### Note:

* [Nano Server](https://hub.docker.com/_/microsoft-windows-nanoserver) based images run as
  `ContainerUser` by default
* [Server Core](https://hub.docker.com/_/microsoft-windows-servercore) based images run as
  `ContainerAdministrator` by default

Windows containers can also run as Active Directory identities by utilizing
[Group Managed Service Accounts](/docs/tasks/configure-pod-container/configure-gmsa/)

## Pod-level security isolation

Linux-specific pod security context mechanisms (such as SELinux, AppArmor, Seccomp, or custom
POSIX capabilities) are not supported on Windows nodes.

Privileged containers are [not supported](/docs/concepts/windows/intro/#compatibility-v1-pod-spec-containers-securitycontext)
on Windows.
Instead [HostProcess containers](/docs/tasks/configure-pod-container/create-hostprocess-pod/)
can be used on Windows to perform many of the tasks performed by privileged containers on Linux.

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

Last modified June 18, 2022 at 4:28 PM PST: [Batch fix links (3) (d705d9ed1c)](https://github.com/kubernetes/website/commit/d705d9ed1c285808ab27aeafb602a825e3392f93)