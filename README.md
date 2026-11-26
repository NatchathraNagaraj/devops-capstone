# DevOps Capstone: To-Do API with CI/CD, Kubernetes, and Monitoring

![CI](https://github.com/NatchathraNagaraj/devops-capstone/actions/workflows/ci.yml/badge.svg)

A small Flask to-do API used to practice a complete DevOps workflow: automated testing, container builds, security scanning, deployment to Kubernetes, and monitoring.

## Architecture

```
Developer pushes code
   -> GitHub Actions: test -> build image -> Trivy scan -> push to Docker Hub
   -> Kubernetes (minikube): Deployment + Service + probes + ConfigMap/Secret
   -> Prometheus scrapes /metrics -> Grafana dashboard -> Alertmanager alert
```

## Tech stack

| Area | Tool |
|---|---|
| App | Python, Flask |
| Containers | Docker |
| CI/CD | GitHub Actions |
| Security scanning | Trivy |
| Registry | Docker Hub |
| Orchestration | Kubernetes (minikube) |
| Monitoring | Prometheus, Grafana, Alertmanager |

## API endpoints

| Method | Path | Purpose |
|---|---|---|
| GET | `/health` | Health check (used by Kubernetes probes) |
| GET | `/todos` | List all to-dos |
| POST | `/todos` | Add a to-do (`{"title": "..."}`) |
| GET | `/metrics` | Prometheus metrics |

Note: to-dos are stored in memory, so they reset when the container restarts.

## Run locally

```bash
cd app
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
pytest
python app.py
```

Test it:

```bash
curl localhost:5000/health
curl -X POST localhost:5000/todos -H "Content-Type: application/json" -d '{"title":"test"}'
curl localhost:5000/todos
```

## Run with Docker

```bash
docker build -t todo-api:v1 .
docker run -d -p 5000:5000 --name todo todo-api:v1
curl localhost:5000/health
```

Or use the published image:

```bash
docker run -d -p 5000:5000 natchathra14/todo-api:latest
```

## CI/CD pipeline

On every push to `main`, GitHub Actions runs these steps in order:

1. Run tests with pytest
2. Build the Docker image (tagged with the commit SHA)
3. Scan the image with Trivy (fails on CRITICAL vulnerabilities)
4. Log in to Docker Hub using repository secrets
5. Push the SHA tag and `latest`

If any step fails, the pipeline stops and nothing is published.

Required repository secrets: `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`.

## Kubernetes deployment

[Coming in Week 2: Deployment with 3 replicas, readiness/liveness probes on `/health`, ConfigMap, Secret, and Service.]

## Monitoring

[Coming in Week 3: ServiceMonitor, Grafana dashboard, and an Alertmanager alert.]

## Problems I hit and how I fixed them

- **Pipeline did not start:** the default branch was `master`, but the workflow listened on `main`. Renamed the branch to `main`.
- **Trivy action failed to resolve:** the third-party action version could not be found. Ran Trivy directly as a Docker container instead.
- **Docker Hub login failed:** secrets are per repository and were missing in the new repo. Added them under Settings, Secrets and variables, Actions.
- **POST returned 400 on Windows:** PowerShell quoting broke the JSON. Used WSL (or a JSON file) instead.

## What I would do on AWS

- EKS instead of minikube
- ECR instead of Docker Hub
- Terraform to provision the VPC, cluster, and registry
- CloudWatch alongside Prometheus

## Author

Natchathra Nagaraj
