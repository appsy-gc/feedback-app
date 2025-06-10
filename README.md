# Feedback App: CI/CD Deployment with GitHub Actions and AWS ECS

## Project Overview

This project is a full-stack feedback collection application designed to demonstrate CI/CD automation using GitHub Actions and infrastructure provisioning with Terraform. The application consists of:

* **Frontend**: A React application built with Vite
* **Backend**: A Flask API connected to a local SQLite database
* **Cloud Hosting**: AWS ECS with Fargate, Application Load Balancer, and ECR
* **CI/CD**: GitHub Actions for automated testing, Docker image builds, ECR pushes, and ECS deployments

The live site can be found here: http://feedback-app-alb-128255988.ap-southeast-2.elb.amazonaws.com/

## Purpose

This project was developed for the DEV1004 - DevOps course Assessment 3 to showcase:

* Automation of build, test, and deployment pipelines
* Containerized deployment using Docker
* Infrastructure as Code using Terraform
* Cloud deployment to AWS ECS with ALB and path-based routing

## CI/CD Tools and Systems

### GitHub Actions

GitHub Actions was chosen as the CI/CD platform due to its seamless integration with GitHub repositories, built-in support for Docker, and ability to integrate AWS deployment via community-supported actions.

**Workflow Features:**

* Triggered on push to the `main` branch
* Builds backend and frontend Docker images (for `linux/amd64`)
* Pushes images to Amazon ECR
* Triggers ECS service deployments using `force-new-deployment`

## CI/CD Workflow Explanation

```yaml
on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - Checkout code
      - Configure AWS credentials
      - Login to Amazon ECR
      - Build backend and frontend Docker images
      - Push both images to ECR
      - Force ECS to redeploy backend and frontend services
```

## Infrastructure with Terraform

Terraform provisions all required cloud infrastructure:

* **ECR Repositories**: `feedback-app-backend`, `feedback-app-frontend`
* **ECS Cluster**: Named `feedback-app-cluster`
* **Task Definitions**: For backend and frontend, each running a single container
* **Application Load Balancer**: Routes `/submit` and `/healthz` to the backend, and all other traffic to the frontend
* **Security Groups**: One for ALB, one for ECS tasks
* **CloudWatch Logs**: For backend and frontend logging

### Path-Based Routing

* `http://<alb-dns>/submit` and `/healthz` → Flask backend
* `http://<alb-dns>/` → React frontend

## Application Functionality

### Frontend

* Built with Vite and React 19.1
* Collects name and comment from user
* Sends POST request to backend via ALB at `/submit`

### Backend

* Flask app with `/submit` and `/healthz` endpoints
* Writes feedback to local SQLite database
* Logs actions to CloudWatch

## Testing

Backend includes unit tests using `unittest`, run in CI pipeline:

* `/healthz` responds with status `200`
* `/submit` handles valid and invalid JSON input

## Technologies Used

* **React (Vite)**: Frontend
* **Flask**: Backend API
* **SQLite**: Local database
* **Docker**: Containerization
* **GitHub Actions**: CI/CD automation
* **Terraform**: Infrastructure as Code
* **AWS ECS + ALB + ECR**: Cloud deployment

## Feedback App Diagrams

### Deployment Pipeline
![Deployment Pipeline](feedback-dashboard/public/Deployment-Pipeline.jpg)

### Runtime Flow
![Runtime Flow](feedback-dashboard/public/Runtime-Flow.jpg)

## Setup and Usage

### Local Development

```bash
# Backend
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python app.py

# Frontend
cd feedback-dashboard
npm install
npm run dev
```

### Docker Compose (Local Dev)

```bash
docker-compose up --build
```

### Deploy to AWS

```bash
cd infra
terraform init
terraform apply
```

Push to `main` branch triggers CI/CD:

```bash
git add .
git commit -m "Your message"
git push
```

## Author

Chris Apps
