<h1 align="center">DevOps Bank System</h1>

<p align="center">A containerized, three-tier banking application built to demonstrate real-world DevOps engineering practices.</p>

<p align="center">
  <a href="https://www.docker.com/"><img src="https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker&logoColor=white" alt="Docker"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"></a>
  <a href="https://flask.palletsprojects.com/"><img src="https://img.shields.io/badge/Flask-REST%20API-000000?style=flat-square&logo=flask&logoColor=white" alt="Flask"></a>
  <a href="https://www.mysql.com/"><img src="https://img.shields.io/badge/MySQL-8.0-4479A1?style=flat-square&logo=mysql&logoColor=white" alt="MySQL"></a>
  <a href="https://github.com/features/actions"><img src="https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF?style=flat-square&logo=github-actions&logoColor=white" alt="GitHub Actions"></a>
  <a href="https://nginx.org/"><img src="https://img.shields.io/badge/Nginx-Reverse%20Proxy-009639?style=flat-square&logo=nginx&logoColor=white" alt="Nginx"></a>
</p>

---

# Project Overview

This project is a fully containerized, multi-tier web banking application. It includes a static frontend served by Nginx, a Python/Flask REST API, and a MySQL database — each running in its own Docker container and communicating through isolated custom networks.

The project was built as a hands-on DevOps portfolio piece to practice container orchestration, service networking, reverse proxy configuration, and automated CI/CD pipelines. It is not a production banking product; it is a realistic simulation of one, designed to demonstrate the kind of infrastructure decisions that appear in real engineering environments.

It is aimed at developers and DevOps engineers who want to see how a multi-service application is structured, networked, and deployed using Docker Compose, and how GitHub Actions can automate deployments without rebuilding unaffected services.

---

# Key Features

- Three-tier architecture: frontend, backend, and database as separate containers
- Docker Compose orchestration with dependency ordering
- Nginx reverse proxy that proxies `/api/*` requests to the Flask backend
- Secure password hashing using bcrypt with salted rounds
- MySQL database with automated schema creation and seed data on first boot
- Two custom Docker bridge networks with subnet configuration
- Database isolated on an internal network unreachable from outside Docker
- Named volumes for data persistence across container restarts
- Path-scoped GitHub Actions workflows that only rebuild the changed service
- Health check endpoint for API liveness verification

---

# Architecture

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
          ┌──────────────────────┼──────────────────────────┘
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

**Request flow:** A browser request hits Nginx on port 7070. If the path starts with `/api/`, Nginx forwards it to the Flask container on port 5000 via the `frontend-network`. Flask connects to MySQL through the `backend-network` (internal only), processes the query, and returns a JSON response back up the chain to the browser. The database is never directly reachable from the browser or the Nginx container.

---

# Technology Stack

| Layer | Technologies | Purpose |
|:---|:---|:---|
| Frontend | Nginx Alpine, HTML5, CSS3, Vanilla JavaScript | Static file serving and reverse proxy |
| Backend | Python 3.11, Flask, Flask-CORS, bcrypt | REST API, authentication logic, DB queries |
| Database | MySQL 8 (Oracle Linux 9) | Relational data storage, schema initialization |
| Containerization | Docker, Docker Compose v3.9 | Container builds, orchestration, networking |
| CI/CD | GitHub Actions | Automated service rebuild and redeploy on push |

---

# Project Structure

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

- [backend/app.py](file:///e:/practice-docker/devops-bank-system-main/backend/app.py) contains the complete API layer. All database connection details are read from environment variables, making the same code work locally and inside Docker without modification.
- [frontend/nginx.conf](file:///e:/practice-docker/devops-bank-system-main/frontend/nginx.conf) contains the Nginx server configuration alongside the static HTML, JS, and CSS files. Nginx acts as both a static file server and a reverse proxy, so the browser never needs to know the backend's internal address or port.
- [database/init.sql](file:///e:/practice-docker/devops-bank-system-main/database/init.sql) holds a custom MySQL database schema that runs automatically on first start. This creates the `users` table and inserts placeholder records, removing the need for any manual setup.
- [.github/workflows/backend.yml](file:///e:/practice-docker/devops-bank-system-main/.github/workflows/backend.yml) contains the workflow files — one per service — so a change to the frontend does not trigger a backend rebuild, and vice versa.

---

# API Reference

All API calls from the browser pass through Nginx under the `/api/` prefix.

| Method | Endpoint | Description |
|:---|:---|:---|
| `POST` | `/api/register` | Create a new user account with username, password, and opening balance |
| `POST` | `/api/login` | Authenticate with username and password |
| `GET` | `/api/balance/{username}` | Retrieve the current balance for a given user |
| `GET` | `/api/health` | Confirm the API is running (liveness check) |

### Register — `POST /api/register`

```json
// Request
{
  "username": "alice",
  "password": "yourpassword",
  "balance": 2500.00
}

// Success: 201 Created
{ "message": "User created successfully" }

// Error examples
// 400 — missing fields or negative balance
// 409 — username already exists
// 500 — database error
```

### Login — `POST /api/login`

```json
// Request
{
  "username": "alice",
  "password": "yourpassword"
}

// Success: 200 OK
{ "message": "Login successful" }

// 401 — invalid credentials
```

### Balance — `GET /api/balance/{username}`

```json
// Success: 200 OK
{ "balance": 2500.00 }

// 404 — user not found
```

### Health — `GET /api/health`

```json
// 200 OK
{ "status": "ok" }
```

---

# Getting Started

### Prerequisites

- [Docker Engine](https://docs.docker.com/get-docker/) v20.10 or later
- [Docker Compose](https://docs.docker.com/compose/install/) v2.0 or later

No other dependencies are required. Python, Nginx, and MySQL all run inside containers.

### 1. Clone the repository

```bash
git clone https://github.com/your-username/devops-bank-system.git
cd devops-bank-system
```

### 2. Review environment variables

Open the [.env](file:///e:/practice-docker/devops-bank-system-main/.env) file at the root of the project:

```env
MYSQL_ROOT_PASSWORD=admin
MYSQL_DATABASE=bank_system
```

Change the password value before running in any shared or production environment. See the [Configuration](#configuration) section for details.

### 3. Build and start the containers

```bash
docker compose up --build -d
```

This builds all three images from their Dockerfiles, creates the custom networks and volumes, and starts the services in dependency order: database → backend → frontend.

### 4. Verify the deployment

```bash
docker compose ps
```

All three services should show a status of `Up`. If the database takes a moment to initialize, the backend may restart once before connecting successfully — this is expected behavior.

### 5. Access the application

Open your browser and go to:

```
http://localhost:7070
```

---

# Configuration

The [.env](file:///e:/practice-docker/devops-bank-system-main/.env) file at the project root defines the credentials passed to both the MySQL container and the Flask backend:

| Variable | Default | Description |
|:---|:---|:---|
| `MYSQL_ROOT_PASSWORD` | `admin` | Root password used by MySQL and by Flask to connect |
| `MYSQL_DATABASE` | `bank_system` | Name of the database created on first startup |

The Flask backend also reads the following variables from [docker-compose.yaml](file:///e:/practice-docker/devops-bank-system-main/docker-compose.yaml) directly:

| Variable | Value | Description |
|:---|:---|:---|
| `DB_HOST` | `database` | Docker service name used as the hostname |
| `DB_PORT` | `3306` | Standard MySQL port |
| `DB_USER` | `root` | Database user |
| `DB_PASSWORD` | `${MYSQL_ROOT_PASSWORD}` | Pulled from the `.env` file |
| `DB_NAME` | `${MYSQL_DATABASE}` | Pulled from the `.env` file |

**For production use:** replace hardcoded credentials with Docker secrets or a secrets manager. Never commit real passwords to version control.

---

# Docker Networking

Two custom bridge networks are defined in [docker-compose.yaml](file:///e:/practice-docker/devops-bank-system-main/docker-compose.yaml):

**frontend-network** (`192.168.30.0/24`, Bridge):
Connects the frontend and backend containers. This is the only network through which browser-originated API requests can reach the Flask API.

**backend-network** (`192.168.40.0/24`, Internal Bridge):
Connects the backend and database containers. The `internal: true` flag means Docker does not create a routing rule to the outside world for this network. No container on `frontend-network` can directly reach the database, and nothing outside Docker can either.

This separation ensures the database is never exposed, even accidentally. The Flask API is the only service that can query MySQL, and it only does so after validating the request on its own layer.

---

# Persistent Storage

Three named volumes are defined to prevent data loss when containers are stopped or replaced:

| Volume | Mounted in Container | Purpose |
|:---|:---|:---|
| `frontend-volume` | `/root/frontend-files/` | Frontend static file storage |
| `backend-volume` | `/root/backend-app/` | Backend application file storage |
| `database-volume` | `/root/batabase-files/` | MySQL data directory — persists all registered users and balances |

Without the `database-volume`, every `docker compose down` would wipe all registered users and balances. The volume keeps data intact across restarts and redeploys. The [database/init.sql](file:///e:/practice-docker/devops-bank-system-main/database/init.sql) script only runs when the data directory is empty, so it will not re-seed or drop tables on a container restart.

---

# Security

This project applies several security practices appropriate for its scope:

- **Password hashing**: Passwords are never stored in plaintext. The Flask backend uses `bcrypt` with a randomly generated salt per password before writing to the database. Verification uses `bcrypt.checkpw`, which is timing-safe by design.
- **Environment variables**: Database credentials are never hardcoded in application source files. They are injected at runtime through environment variables, which is the standard 12-factor approach.
- **Network isolation**: The database container is attached only to the internal `backend-network`. It has no route to the internet and is not reachable from the frontend container. The only path to the database is through the Flask API.
- **Reverse proxy**: Nginx acts as the single entry point. The browser communicates with Nginx on port 7070; the Flask port (5000) is exposed on the host for development convenience but would be removed in a hardened deployment.
- **Input validation**: The `/register` endpoint validates that username and password are present, that balance is a non-negative number, and that the username does not already exist before writing anything to the database.

This is a portfolio project, not a hardened production system. Notable gaps include the absence of HTTPS, JWT-based session tokens, and rate limiting.

---

# CI/CD

The repository contains three GitHub Actions workflow files under [.github/workflows/](file:///e:/practice-docker/devops-bank-system-main/.github/workflows/). Each workflow is scoped to a specific directory using the `paths` filter, so a commit that only modifies frontend files will only trigger the frontend workflow — the backend and database containers are left untouched.

**How each workflow operates:**

1. A push to `main` is received by GitHub Actions.
2. The `paths` filter checks whether the changed files fall under `backend/`, `frontend/`, or `database/`.
3. If matched, the workflow runs on a self-hosted runner tagged `rocky`.
4. It executes `docker compose build <service>` to rebuild the image.
5. It then runs `docker compose up -d --no-deps <service>` to replace only that container, leaving others running.

| Workflow | Trigger Path | Build Command | Deploy Command |
|:---|:---|:---|:---|
| `backend.yml` | `backend/**` | `docker compose build backend` | `docker compose up -d --no-deps backend` |
| `frontend.yml` | `frontend/**` | `docker compose build frontend` | `docker compose up -d --no-deps frontend` |
| `database.yml` | `database/**` | `docker compose build database` | `docker compose up -d --no-deps database` |

The `--no-deps` flag is important: it prevents Docker Compose from restarting dependency containers (e.g., restarting the database when only the backend changed).

---

# Useful Docker Commands

```bash
# Check the status of all running containers
docker compose ps

# Follow live logs for all services
docker compose logs -f

# Follow logs for a specific service
docker compose logs -f backend

# List all Docker networks (verify custom networks exist)
docker network ls

# Inspect a specific network and see connected containers
docker network inspect devops-bank-system-main_backend-network

# List all Docker volumes
docker volume ls

# Stop all containers and remove networks (keep volumes)
docker compose down

# Stop all containers, remove networks, and delete volumes (wipes database)
docker compose down -v

# Rebuild a single service image without restarting others
docker compose build backend

# Replace a single running container with a freshly built image
docker compose up -d --no-deps backend

# Open a shell inside a running container
docker exec -it <container-name> bash

# Connect to MySQL inside the database container
docker exec -it <db-container-name> mysql -u root -p
```

---

# Screenshots

> _Screenshots will be added after deployment. Replace the placeholders below with actual images._

| View | Preview |
|:---|:---|
| Home / Login Page | `screenshots/login.png` |
| User Registration | `screenshots/register.png` |
| Account Balance | `screenshots/balance.png` |
| GitHub Actions Workflow | `screenshots/cicd.png` |
| Docker Containers Running | `screenshots/containers.png` |
| Architecture Diagram | `screenshots/architecture.png` |

---

# Future Improvements

The following are planned or potential enhancements:

- **Kubernetes**: Migrate from Docker Compose to Kubernetes manifests for proper orchestration
- **Helm**: Package the Kubernetes deployment as a Helm chart for reusable releases
- **Terraform**: Provision cloud infrastructure (VPC, EC2, RDS) with Infrastructure as Code
- **HTTPS / TLS**: Add SSL termination at the Nginx layer using Let's Encrypt or a load balancer
- **JWT Authentication**: Replace session-based logic with signed JSON Web Tokens
- **Redis**: Add a caching layer for session state or frequently read balances
- **Prometheus + Grafana**: Add metrics collection and dashboards for container and API observability
- **Health checks in Compose**: Add `healthcheck` blocks to `docker-compose.yaml` to replace simple `depends_on` ordering
- **Horizontal scaling**: Demonstrate scaling the backend with `docker compose --scale`
- **Production hardening**: Remove exposed backend port, enforce non-root container users, add rate limiting

---

# Troubleshooting

**Container exits immediately after starting**

Check the logs for the failing container:
```bash
docker compose logs backend
```
Common causes: a missing environment variable, a syntax error in the application code, or a port already in use on the host.

---

**Database connection refused**

The backend may start before MySQL is fully ready. Docker Compose `depends_on` only waits for the container to start, not for MySQL to be accepting connections. If this happens, restart the backend manually:
```bash
docker compose restart backend
```
A proper fix is to add a `healthcheck` to the database service and use `depends_on: condition: service_healthy` in the backend definition.

---

**Port already in use**

```
Error: port 7070 is already allocated
```
Another process is using port 7070 (or 5000 / 3306). Either stop the conflicting process or change the host port in `docker-compose.yaml`:
```yaml
ports:
  - "8080:80"   # change 7070 to any free port
```

---

**Docker Compose build fails**

If the build fails with a pip or package error:
```bash
docker compose build --no-cache backend
```
This forces a clean rebuild without using the Docker layer cache. Useful when a dependency has changed but the cache has not been invalidated.

---

**Changes not reflected after editing files**

Rebuild the affected service image:
```bash
docker compose build frontend
docker compose up -d --no-deps frontend
```

---

# What I Learned

Building this project provided practical experience with the following:

- **Docker fundamentals**: Writing Dockerfiles for different base images (Python slim, Nginx Alpine, MySQL), understanding layer caching, and managing image size
- **Docker Compose**: Defining multi-service applications, controlling startup order with `depends_on`, and separating concerns across services
- **Container networking**: Creating custom bridge networks, understanding internal vs. external network routing, and designing subnet layouts
- **Reverse proxy configuration**: Writing an Nginx config that serves static files on one path and proxies API traffic on another, with proper header forwarding
- **Environment-based configuration**: Designing an application where all environment-specific values are injected at runtime, following twelve-factor app principles
- **Security in containers**: Applying network isolation so that not every container can reach every other container
- **CI/CD with GitHub Actions**: Writing path-filtered workflows that trigger only when the relevant service is changed, and deploying containers with zero downtime for unaffected services
- **Database initialization**: Using MySQL's `/docker-entrypoint-initdb.d/` directory to automatically run SQL scripts on first boot
- **Persistent volumes**: Understanding why stateless containers need external storage for any data that must survive restarts

---

# Author

**Mohamed El-Badawy**

- GitHub: [@your-username](https://github.com/your-username)
- LinkedIn: [linkedin.com/in/your-profile](https://linkedin.com/in/your-profile)
- Email: your.email@example.com

---

# License

This project is licensed under the MIT License.

```
MIT License

Copyright (c) 2026 Mohamed El-Badawy

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

