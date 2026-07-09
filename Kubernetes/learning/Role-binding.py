apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: developers-binding
  namespace: development
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: developer-role  # Reference the Role
subjects:
# User 1: Alice
- kind: User
  name: alice@example.com
  apiGroup: rbac.authorization.k8s.io

# User 2: Bob
- kind: User
  name: bob@example.com
  apiGroup: rbac.authorization.k8s.io

# Group: All developers
- kind: Group
  name: developers
  apiGroup: rbac.authorization.k8s.io