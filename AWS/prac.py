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