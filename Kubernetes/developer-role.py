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