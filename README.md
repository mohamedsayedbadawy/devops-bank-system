🏦 DevOps Containerized Bank System
A modern, multi-tier, containerized microservices-style banking web application built to demonstrate end-to-end DevOps practices. The system features isolated service networks, persistent volume storage, automated database initialization, secure password hashing, reverse proxy routing, and GitHub Actions CI/CD workflows.
---
📐 Architecture Overview
```
               +----------------------------------------+
               |              User Browser              |
               +----------------------------------------+
                                   |
                             (Port 7070)
                                   v
+--------------------------------------------------------------------+
|                         FRONTEND CONTAINER                         |
|  • Nginx Alpine Server                                             |
|  • Serves HTML5 / CSS3 / Vanilla JS                                |
|  • Proxies /api/ requests -> http://backend:5000/                  |
+--------------------------------------------------------------------+
       | (frontend-network: 192.168.30.0/24)
       v
+--------------------------------------------------------------------+
|                         BACKEND CONTAINER                          |
|  • Python 3.11 Slim / Flask API                                    |
|  • Bcrypt Password Hashing \& Input Validation                      |
|  • Exposes endpoints: /register, /login, /balance/<user>, /health  |
+--------------------------------------------------------------------+
       | (backend-network: 192.168.40.0/24 - Internal Only)
       v
+--------------------------------------------------------------------+
|                        DATABASE CONTAINER                          |
|  • MySQL (Oracle Linux 9 Base)                                     |
|  • Pre-seeded via /docker-entrypoint-initdb.d/init.sql             |
|  • Isolated on internal backend network                            |
+--------------------------------------------------------------------+
```
---
🛠️ Technology Stack
Tier	Technology	Description
Frontend	Nginx Alpine, HTML5, Vanilla JS, CSS3	Web server & reverse proxy. Proxies `/api/\*` to the Flask backend.
Backend	Python 3.11, Flask, Bcrypt, `mysql-connector-python`	RESTful API handling authentication, security, and financial queries.
Database	MySQL 8 (Oracle Linux 9)	Relational database pre-initialized with tables & seed records.
Containerization	Docker, Docker Compose	Multi-container orchestration, persistent storage, and custom bridge networking.
CI/CD	GitHub Actions	Automated image build and service deployment triggered by code changes.
---
📁 Repository Structure
```
devops-bank-system-main/
├── .env                       # Environment variables (DB password, DB name)
├── docker-compose.yaml        # Docker Compose service orchestration blueprint
├── README.md                  # Comprehensive project documentation
├── backend/                   # Flask API Backend service
│   ├── app.py                 # Main Flask application \& REST API routes
│   ├── db.py                  # MySQL database connection helper module
│   ├── dockerfile             # Docker build definition for Flask container
│   └── requirements.txt       # Python dependencies (Flask, bcrypt, mysql-connector)
├── frontend/                  # Web Frontend service
│   ├── dockerfile             # Docker build definition for Nginx container
│   ├── nginx.conf             # Nginx reverse proxy \& static file server configuration
│   └── frontend-files/        # Web client assets
│       ├── app.js             # API integration \& UI state logic
│       ├── index.html         # User interface layout
│       └── style.css          # Styling \& visual layout
├── database/                  # Database service
│   ├── dockerfile             # Custom MySQL container build definition
│   └── init.sql               # Database schema creation \& seeding script
└── .github/
    └── workflows/             # GitHub Actions CI/CD pipelines
        ├── backend.yml        # CI/CD pipeline for backend updates
        ├── database.yml       # CI/CD pipeline for database updates
        └── frontend.yml       # CI/CD pipeline for frontend updates
```
---
✨ Features & Functionality
User Registration (`POST /api/register`):
Secure account creation with username, password, and starting balance validation.
Passwords hashed using `bcrypt` salted hashing before storage.
User Authentication (`POST /api/login`):
Verifies credentials against bcrypt hashes in MySQL.
Balance Query (`GET /api/balance/<username>`):
Retrieves live account balances securely.
Health Check (`GET /api/health`):
Simple health probe for monitoring API uptime.
Nginx Reverse Proxy & Route Abstraction:
Masks internal container ports by forwarding `/api/\*` requests seamlessly to the backend.
Network Isolation:
Database resides on an internal network (`backend-network`) inaccessible from external networks or the frontend container directly.
---
🚀 Getting Started
Prerequisites
Ensure you have the following installed on your host machine:
Docker Engine (v20.10+)
Docker Compose (v2.0+)
1. Environment Configuration
The repository includes a default `.env` file for quick local deployment:
```env
MYSQL\_ROOT\_PASSWORD=admin
MYSQL\_DATABASE=bank\_system
```
(Modify these values for production environments).
2. Launching the Application
Run the following command from the root directory to build and start all containers in detached mode:
```bash
docker compose up --build -d
```
3. Accessing the Application
Open your browser and navigate to:
👉 http://localhost:7070
Initial Seed Accounts (for testing):
User: `mohamed`
User: `sara`
---
🔒 Networking & Storage Configuration
Docker Networks
`frontend-network` (Bridge, `192.168.30.0/24`): Connects Frontend container and Backend container.
`backend-network` (Internal Bridge, `192.168.40.0/24`): Isolated network connecting Backend and Database containers.
Docker Volumes
`frontend-volume`: Mounted at `/root/frontend-files/`
`backend-volume`: Mounted at `/root/backend-app/`
`database-volume`: Mounted at `/root/batabase-files/` for MySQL persistence
---
🔄 CI/CD Automation (GitHub Actions)
The repository includes automated GitHub Actions workflows under `.github/workflows/` that trigger on pushes to `main`:
`backend.yml`: Rebuilds and re-deploys the `backend` container when changes occur in `backend/`.
`frontend.yml`: Rebuilds and re-deploys the `frontend` container when changes occur in `frontend/`.
`database.yml`: Rebuilds and re-deploys the `database` container when changes occur in `database/`.
---
🧹 Teardown
To stop and remove containers, networks, and volumes:
```bash
# Stop containers and networks
docker compose down

# Stop containers and remove persistent volumes
docker compose down -v
```
