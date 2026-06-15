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