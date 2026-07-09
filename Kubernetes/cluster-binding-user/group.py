apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: sre-team-binding
# NO namespace!
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: node-admin
subjects:
- kind: Group
  name: sre-team
  apiGroup: rbac.authorization.k8s.io