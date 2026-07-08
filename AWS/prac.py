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