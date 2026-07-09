apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: node-admin
# NO namespace! This is cluster-wide
rules:
# Rule 1: Manage nodes
- apiGroups: [""]
  resources: ["nodes"]
  verbs: ["get", "list", "watch"]

# Rule 2: Drain nodes (for maintenance)
- apiGroups: [""]
  resources: ["pods/eviction"]
  verbs: ["create"]