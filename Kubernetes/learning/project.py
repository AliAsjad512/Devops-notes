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


Phase 2 — Amazon EKS (Production AWS)
GitHub Push (main branch)
    ↓
GitHub Actions
    ├── Job 1: Build image → Push to ECR (tagged with commit SHA)
    └── Job 2: helm upgrade --install → EKS cluster
                    ↓
        AWS Load Balancer (ALB)
                    ↓
        NGINX Ingress Controller
                    ↓
        flask-service (ClusterIP)
                    ↓
        ┌─────────────────────┐
        │  flask-app-dev      │    flask-app-prod      │
        │  2 pods (HPA: 2–6)  │    3 pods (HPA: 3–10)  │