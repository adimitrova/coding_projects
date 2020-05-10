### Kubernetes K8s

K8s Cluster services 
We can enforce a desired state management with specific configuration and the cluster services will run that configuration. 

On the one side we have an API, on the other we have a __Worker__ with a __Kublet process__ that runs which is responsible for communicating with the Kubernetes cluster services

The configuration is in a deployment __.yaml__ file containing a POD configuration. __POD__ is the smallest unit of deployment. In a POD we can have one or more running containers (e.g. Docker etc.). We specify image file(s) for the containers and replica-s (how many instances of a certain POD should be running)

In the deployment file we can have more PODs with their own configurations etc.
The deployment file is taken and fed into the API and it decides how to schedule them. 

PODs are not containers, pods and containers sit inside together 

RC - Replication controllers - manages the replicas. 

-------

Use `kubectl describe pod airflow-yyyyyyyy-xxxxx -n default` to see all of the containers in this pod. `-n` stands for namespace.

In an ordinary command window, not your shell, list the environment variables in the running Container:
> kubectl exec shell-demo env

Get Shell (CLI) into a running pod's container:
> kubectl exec -it airflow-78459b447f-ctsq7 -- bash .   #here we go into the airflow pod

If a Pod has more than one Container, use --container or -c to specify a Container in the kubectl exec command. For example, suppose you have a Pod named my-pod, and the Pod has two containers named main-app and helper-app. The following command would open a shell to the main-app Container.
> kubectl exec -it my-pod --container main-app bash

### [Debugging Pods](https://kubernetes.io/docs/tasks/debug-application-cluster/debug-pod-replication-controller/)
> kubectl describe pods {POD_NAME}

Get logs of the current container
> kubectl logs {POD_NAME} {CONTAINER_NAME}

-------

https://kubernetes.io/docs/reference/kubectl/cheatsheet/

--------

## [Kubernetes CHEATSHEET](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)

Get kubernetes system pods
> kubectl get pods -n kube-system

The 3 most important 3 services for kubernetes are:
- __kube-apiserver-docker-for-desktop__: makes it possible to communicate with the k8s cluster.
- __kube-controller-manager-docker-for-desktop__: responsible for health checks
- __kube-scheduler-docker-for-desktop__: schedules according to a manifest, e.g. replicas, configuration etc.

> kubectl get svc
> kubectl describe svc
> kubectl get pv
> kubectl get pvc

---------

## Links

- [Kubernetes for Docker users manual](https://kubernetes.io/docs/reference/kubectl/docker-cli-to-kubectl/)

- [Kubernetes commands and syntax](https://kubernetes.io/docs/reference/kubectl/overview/#syntax) :heavy_exclamation_mark: 

- [Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)