🔐 The Access Control Saga
Document 11 of 15 • Kubernetes Security & RBAC

📖 The Scenario: Chaos in TechVault
Date: Wednesday, 3:00 PM. Agastya's team has grown from 3 to 15 people. New developers, DevOps engineers, interns - all with access to the production cluster.

The Incident: This morning, a junior developer accidentally ran `kubectl delete deployment production-api` while trying to test something. The entire production system went down for 4 hours. Clients were furious. Agastya's boss demanded: "WHO has access to WHAT and WHY?"

Current Status: Everyone has admin access to everything (kubeadmin). Zero access control. Pure chaos.

The Need: Implement proper access control - developers can deploy only in dev, DevOps can manage production, interns can view metrics only.

👨‍💻 Agastya (Cluster Admin)
Crisis: Production down 4 hours
Problem: No access control
Need: Secure access policies
🎓 Vashisht (Security Architect)
Teaching: RBAC fundamentals
Focus: Roles, RoleBindings, ClusterRoles
Mission: Implement least privilege
👨‍🔬 Aarav (Identity Expert)
Role: ServiceAccounts & Auth
Focus: Who is accessing what
Goal: Audit trail for compliance
🏗️ Nandan (DevOps Lead)
Teaching: Real-world RBAC design
Focus: Multi-team access patterns
Mission: Zero trust deployment




🛡️ RBAC: Role-Based Access Control
"Agastya, the good news - Kubernetes has built-in RBAC (Role-Based Access Control). The bad news - it's not enabled by default on many clusters! Let me teach you how to implement proper access control." - Vashisht
The RBAC Model
Subject: WHO wants to access? (User, ServiceAccount, Group)
Verb: WHAT action? (get, create, delete, update, etc.)
Resource: WHICH object? (pods, deployments, services, secrets)
Scope: WHERE? (namespace-scoped or cluster-wide)
📋 RBAC Flow
User runs: `kubectl delete pod my-pod -n production`
Kubernetes API server: "Who are you?"
User identifies via certificate/token (authentication)
API server checks: Does this user have permission to DELETE pods in production namespace?
Look up user's RoleBindings → Find assigned Roles → Check for delete action on pods
If YES → action allowed; If NO → access denied


RBAC Objects
Object	Scope	Purpose	Example
Role	Namespace	Define permissions in ONE namespace	developers-role (in dev namespace)
RoleBinding	Namespace	Bind Role to users/groups in ONE namespace	developer-alice to developers-role
ClusterRole	Cluster-wide	Define permissions across all namespaces	cluster-admin, node-reader
ClusterRoleBinding	Cluster-wide	Bind ClusterRole to users/groups	sre-team to cluster-admin
Key Insight: Role = namespace-scoped permissions. ClusterRole = cluster-wide permissions. Use RoleBinding/ClusterRoleBinding to assign them.
📝 Creating Roles (Namespace-Scoped)
"Let's create roles for different teams. First, a role for developers in the dev namespace where they can deploy, but NOT delete." - Aarav
Developer Role (Create & Update, No Delete)
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: developer-role
  namespace: development  # Namespace-scoped!
rules:
# Rule 1: Deployments - create, get, list, update, patch (NO delete)
- apiGroups: ["apps"]
  resources: ["deployments"]
  verbs: ["create", "get", "list", "update", "patch"]

# Rule 2: Pods - get, list, logs (read-only)
- apiGroups: [""]
  resources: ["pods", "pods/logs"]
  verbs: ["get", "list", "watch"]

# Rule 3: Services - get, list, create (NO delete)
- apiGroups: [""]
  resources: ["services"]
  verbs: ["get", "list", "create"]
# Apply the Role
kubectl apply -f developer-role.yaml

# List roles in development namespace
kubectl get roles -n development

# View the role details
kubectl describe role developer-role -n development
Read-Only Role (For Monitoring/Observability)
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: observer-role
  namespace: production
rules:
# Rule 1: Pods - read only
- apiGroups: [""]
  resources: ["pods", "pods/logs", "pods/status"]
  verbs: ["get", "list", "watch"]

# Rule 2: Events - read only
- apiGroups: [""]
  resources: ["events"]
  verbs: ["get", "list"]

# Rule 3: Deployments/Services - read only
- apiGroups: ["apps"]
  resources: ["deployments", "statefulsets"]
  verbs: ["get", "list"]