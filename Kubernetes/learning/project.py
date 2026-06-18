Architecture
Phase 1 — Minikube (Local Kubernetes)
GitHub Push
    ↓
GitHub Actions
    ↓
Docker Hub (baqirops/flask-eks-hpa)
    ↓
Minikube Cluster (local VM)
    ├── NGINX Ingress
    ├── flask-service (ClusterIP)
    ├── flask-dashboard pods (HPA: 2–6 pods)
    └── metrics-server (CPU metrics for HPA)