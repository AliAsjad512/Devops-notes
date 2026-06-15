Controller Manager
├── Node Controller          → monitors node health
├── Replication Controller   → maintains desired pod count
├── Endpoints Controller     → links services to pods
├── ServiceAccount Controller→ creates default accounts/tokens
├── Deployment Controller    → manages rollouts
├── Job Controller           → manages one-off jobs
└── Namespace Controller     → manages namespaces


"Remember when your container crashed and auto-healed? That was the Replication Controller detecting: Desired=3, Actual=2, Action=Create 1 pod!"