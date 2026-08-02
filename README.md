<div align="center">
DevOps Bank System
A containerized, three-tier banking application built to demonstrate real-world DevOps engineering practices.
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-REST%20API-000000?style=flat-square&logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=flat-square&logo=mysql&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF?style=flat-square&logo=github-actions&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Nginx](https://img.shields.io/badge/Nginx-Reverse%20Proxy-009639?style=flat-square&logo=nginx&logoColor=white)
</div>
---
Project Overview
This project is a fully containerized, multi-tier web banking application. It includes a static frontend served by Nginx, a Python/Flask REST API, and a MySQL database — each running in its own Docker container and communicating through isolated custom networks.
The project was built as a hands-on DevOps portfolio piece to practice container orchestration, service networking, reverse proxy configuration, and automated CI/CD pipelines. It is not a production banking product; it is a realistic simulation of one, designed to demonstrate the kind of infrastructure decisions that appear in real engineering environments.
It is aimed at developers and DevOps engineers who want to see how a multi-service application is structured, networked, and deployed using Docker Compose, and how GitHub Actions can automate deployments without rebuilding unaffected services.
---
Key Features
Three-tier architecture: frontend, backend, and database as separate containers
Docker Compose orchestration with dependency ordering
Nginx reverse proxy that proxies `/api/*` requests to the Flask backend
Secure password hashing using bcrypt with salted rounds
MySQL database with automated schema creation and seed data on first boot
Two custom Docker bridge networks with subnet configuration
Database isolated on an internal network unreachable from outside Docker
Named volumes for data persistence across container restarts
Path-scoped GitHub Actions workflows that only rebuild the changed service
Health check endpoint for API liveness verification
---
Architecture
```
                        ┌─────────────────────┐
                        │     User Browser     │
                        └──────────┬──────────┘
                                   │ HTTP :7070
                                   ▼
          ┌──────────────────────────────────────────────────┐
          │              frontend-network                     │
          │              192.168.30.0/24  (Bridge)           │
          │                                                   │
          │  ┌─────────────────────────────────────────────┐  │
          │  │         Frontend Container                   │  │
          │  │         Nginx Alpine  ·  Port 80             │  │
          │  │  Serves static files, proxies /api/ → :5000  │  │
          │  └───────────────────┬─────────────────────────┘  │
          │                      │                             │
          │  ┌───────────────────▼─────────────────────────┐  │
          │  │          Backend Container                   │  │
          │  │          Python 3.11 / Flask  ·  Port 5000   │  │
          │  │  Handles auth, validation, DB queries         │  │
          │  └───────────────────┬─────────────────────────┘  │
          └──────────────────────┼──────────────────────────┘
                                 │
          ┌──────────────────────┼──────────────────────────┐
          │              backend-network                     │
          │              192.168.40.0/24  (Internal)         │
          │                      │                           │
          │  ┌───────────────────▼─────────────────────────┐ │
          │  │          Database Container                  │ │
          │  │          MySQL 8  ·  Port 3306               │ │
          │  │  Schema and seed data loaded on first start   │ │
          │  └─────────────────────────────────────────────┘ │
          └──────────────────────────────────────────────────┘
```
Request flow: A browser request hits Nginx on port 7070. If the path starts with `/api/`, Nginx forwards it to the Flask container on port 5000 via the `frontend-network`. Flask connects to MySQL through the `backend-network` (internal only), processes the query, and returns a JSON response back up the chain to the browser. The database is never directly reachable from the browser or the Nginx container.
---
Technology Stack
Layer	Technologies	Purpose
Frontend	Nginx Alpine, HTML5, CSS3, Vanilla JavaScript	Static file serving and reverse proxy
Backend	Python 3.11, Flask, Flask-CORS, bcrypt	REST API, authentication logic, DB queries
Database	MySQL 8 (Oracle Linux 9)	Relational data storage, schema initialization
Containerization	Docker, Docker Compose v3.9	Container builds, orchestration, networking
CI/CD	GitHub Actions	Automated service rebuild and redeploy on push
---
Project Structure
```
devops-bank-system-main/
├── .env                        # Environment variables for DB credentials
├── docker-compose.yaml         # Service definitions, networks, and volumes
│
├── backend/
│   ├── app.py                  # Flask application: routes and request handlers
│   ├── db.py                   # MySQL connection factory using environment variables
│   ├── dockerfile              # Builds the Python backend image
│   └── requirements.txt        # Python dependencies
│
├── frontend/
│   ├── dockerfile              # Builds the Nginx frontend image
│   ├── nginx.conf              # Nginx config: static serving and API proxy rules
│   └── frontend-files/
│       ├── index.html          # Single-page layout with login, register, balance views
│       ├── app.js              # Fetch API calls and view-switching logic
│       └── style.css           # UI styling and layout
│
├── database/
│   ├── dockerfile              # Builds the custom MySQL image
│   └── init.sql                # Creates schema and inserts seed records on first boot
│
└── .github/
    └── workflows/
        ├── backend.yml         # CI/CD pipeline triggered by changes in backend/
        ├── frontend.yml        # CI/CD pipeline triggered by changes in frontend/
        └── database.yml        # CI/CD pipeline triggered by changes in database/
```
backend/ contains the complete API layer. All database connection details are read from environment var
