50 Most Frequently Used kubectl commands for DevOps Engineers [Part A]
Kubectl is a command-line tool that allows users to interact with Kubernetes clusters. Kubectl is used to deploy applications, manage & monitor cluster resources.

kubectl help ==> to get help and more information about any command.
kubectl cluster-info ==> shares the K8s cluster information.
kubectl cluster-info dump ==> for troubleshooting K8s cluster issues, we'll get logs.
kubectl get nodes ==> lists all nodes of the cluster.
kubectl describe node <node_name> ==> get all the details about a specific node, change the node name.
kubectl version ==> the version of kubectl client, server and kustomize.
kubectl get all ==> overview of all resources on the cluster like pods, deployments or services etc.
kubectl options ==> Prints the kubectl command options that can be used with kubectl command.
kubectl api-resources ==> Prints all the supported API resources on the server.
kubectl api-versions ==> Prints all the supported API versions on the server.


kubectl get namespaces ==> Lists all namespaces on the cluster.
kubectl create namespace new-namespace ==> It will create a new namespace.
kubectl config set-context --current --namespace=new-namespace ==> Set the default namespace as the new-namespace.
kubectl delete namespace new-namespace ==> Delete the namespace.
kubectl get pods ==> List pods in the default namespace.
kubectl get pods -n namespace_name ==> List pods of a specific namespace.
kubectl get pods --all-namespaces ==> Lists pods of all namespaces.
kubectl get pods -o wide ==> Lists pods with more details.
kubectl describe pod new-pod ==> More details of a pod.
kubectl logs new-pod ==> Shares logs of a pod.


kubectl logs -f new-pod ==> Live or stream logs of a pod.
kubectl exec -it <pod-name> -- /bin/bash ==> Access a pod using SSH.
kubectl run new-pod --image=alpine:latest ==> Run a new pod with an image of your choice.
kubectl delete pod new-pod ==> Delete a pod.
kubectl get deployments ==> See deployments of a namespace.
kubectl get deployments --all-namespaces ==> See all deployments in all namespaces.
kubectl scale deployment deployment-name -n namespace-name --replicas=3 => Scale up a deployment upto 3 pods.
kubectl delete deployment deployment-name ==> Delete a deployment.
kubectl get services ==> List services in the default namespace.
kubectl get services --all-namespaces ==> Services running in all namespaces.


kubectl create service loadbalancer new-loadbalancer-service --tcp=80:8080 ==> It'll create a new loadbalancer service that exposes port 80 & routes traffic to container port 8080.
kubectl describe service new-loadbalancer-service ==> Describes a service and shares more details.
kubectl delete service new-loadbalancer-service ==> Deletes a service.
kubectl get configmaps ==> Lists down configmaps of the default namespace.
kubectl get configmaps --all-namespaces ==> Lists all Configmaps in all namespaces of the cluster.
kubectl describe configmap my-configmap -n namespace ==> See the details of a configmap in a specific namespace.
kubectl delete configmap my-configmap ==> Delete a configmap.
kubectl get secrets ==> The secrets of our K8s cluster.
kubectl get secrets --all-namespaces ==> Secrets in all namespaces of a cluster.
kubectl create secret generic my-secret --from-literal=username=admin --from-literal=password=admin123 ==> It'll create a new secret.