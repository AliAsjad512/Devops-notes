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
                                           

                                           ech Stack
Tool	Version	Purpose
Python / Flask	3.11	Application
Gunicorn	Latest	Production WSGI server
Docker (multi-stage)	Latest	Container build
Amazon ECR	—	Private image registry
Amazon EKS	Kubernetes 1.34	Container orchestration
eksctl	0.227.0	EKS cluster management
Helm	3	Multi-environment deployment
NGINX Ingress	4.15.1	Traffic routing
Kubernetes HPA	autoscaling/v2	Auto-scaling
GitHub Actions	—	CI/CD pipeline
AWS CLI	v2	AWS resource management