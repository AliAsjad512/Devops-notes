Controller Manager
├── Node Controller          → monitors node health
├── Replication Controller   → maintains desired pod count
├── Endpoints Controller     → links services to pods
├── ServiceAccount Controller→ creates default accounts/tokens
├── Deployment Controller    → manages rollouts
├── Job Controller           → manages one-off jobs
└── Namespace Controller     → manages namespaces


"Remember when your container crashed and auto-healed? That was the Replication Controller detecting: Desired=3, Actual=2, Action=Create 1 pod!"


Node 🖥️

A physical or virtual machine in the cluster
It's the infrastructure that runs workloads
Can have multiple pods running on it
Has resources like CPU, RAM, Storage
Examples: EC2 instance, a VM, a bare metal server

Pod 📦

The smallest deployable unit in Kubernetes
Runs inside a Node
Contains one or more containers (e.g., your nginx container)
Has its own IP address
If a pod dies, Kubernetes restarts it


Control Plane NodeWorker NodeRuns pods?❌✅Runs API Server?✅❌Also calledMaster NodeJust "Node"In MinikubeSame machineSame machine


Let's delete these files and start fresh. It will free up disk space and help avoid any performance issues while we work 


kubectl to create, manage, inspect, and delete Kubernetes resources such as Pods, Deployments, Services, ConfigMaps, and Secrets. 

The main purpose of creating a test Pod is to create a file inside it and store some data. Then, we delete the Pod to check whether the data is preserved or lost. This helps us understand whether the Pod's storage is persistent or ephemeral. 



question.
Your question in natural English
"We're using this command to create a file inside a Pod, right? But the file is being created in the /tmp directory. How do I know that this file is actually being created inside the Pod and not somewhere else? What tells me that /tmp/myfile.txt belongs to the Pod? How can I verify that the file is inside the Pod?"
