# UBC USSD Engine

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.12%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.129.0%2B-green.svg)](https://fastapi.tiangolo.com/)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![image](https://img.shields.io/pypi/v/uv.svg)](https://pypi.python.org/pypi/uv)

**Project Code Name:** `ubc-ussd-engine`

A comprehensive USSD (Unstructured Supplementary Service Data) application engine designed for banking and payment services, built with FastAPI and modern Python practices.

---

## 📋 Table of Contents

- [🎯Overview](#overview)
- [✨Features](#features)
- [🏗️Architecture](#architecture)
- [📦Prerequisites](#prerequisites)
- [🚀Installation](#installation)
- [⚙️Configuration](#configuration)
- [🎮Usage](#usage)
  - [Running the Application](#running-the-application)
- [📡API Endpoints](#api-endpoints)
- [📁Project Structure](#project-structure)
- [🗄️Database Schema](#database-schema)
- [🔐Authentication & Authorization](#authentication--authorization)
- [🔄Session Management](#session-management)
- [🛠️Development](#development)
- [🧪Testing](#testing)
- [🚢Deployment](#deployment)
- [🤝Contributing](#contributing)
- [📄License](#license)
- [📞Contact](#contact)

---

## 🎯Overview

The **UBC USSD Engine** is a production-ready FastAPI application designed to power USSD-based banking and payment services. It provides robust session management, role-based access control (RBAC), user authentication, and an admin dashboard for managing the system.

**Organization:** Union Bank Cameroon  
**Version:** 1.0.0  
**Contact:** admin@unionbankcameroon.com

---

## ✨Features

### Core Features
- 🚀 **High-Performance API** - Built with FastAPI for async/await support
- 🔐 **Authentication & Authorization** - Role-based access control (RBAC) with multiple user roles
- 📊 **Admin Dashboard** - Web-based admin interface for user and system management
- 💾 **Session Management** - Secure session handling with token-based authentication
- 🗄️ **Database Management** - SQLite-based storage with support for multiple databases
- 📝 **Audit Logging** - Comprehensive audit trail for all user actions
- 🔄 **Multi-Tenant Support** - Built-in tenant management capabilities
- 🎨 **Templating** - Jinja2 templates for dynamic web pages
- ⚙️ **Configurable** - YAML-based configuration for flexible deployment

### Security Features
- Password hashing (SHA-256)
- Session token management with expiration
- JWT support (configurable)
- CSRF protection
- CORS configuration
- Role-based permissions
- Secure cookie options

### User Roles
- **Admin** - Full system access
- **User** - Standard read/write access
- **Guest** - Read-only access
- **Moderator** - Elevated permissions with audit access
- **Application** - Service account access
- **Auditor** - Read and audit log access

---

## 🏗️Architecture

The application follows a clean architecture pattern with clear separation of concerns:

```
┌─────────────────────────────────────────┐
│          FastAPI Application            │
├─────────────────────────────────────────┤
│  ┌──────────────┐  ┌─────────────────┐  │
│  │   Web UI     │  │   REST API      │  │
│  │  (Jinja2)    │  │   Endpoints     │  │
│  └──────────────┘  └─────────────────┘  │
├─────────────────────────────────────────┤
│  ┌──────────────┐  ┌─────────────────┐  │
│  │ Session      │  │ Authentication  │  │
│  │ Management   │  │ & Authorization │  │
│  └──────────────┘  └─────────────────┘  │
├─────────────────────────────────────────┤
│  ┌──────────────┐  ┌─────────────────┐  │
│  │   Database   │  │  Configuration  │  │
│  │   Layer      │  │     Layer       │  │
│  └──────────────┘  └─────────────────┘  │
└─────────────────────────────────────────┘
```

---

## 📦Prerequisites

- **Python** >= 3.12 (Python 3.8+ compatible with some features)
- **pip** or **uv** package manager
- **SQLite3** (included with Python)
- **Git** (for version control)

### Recommended Development Tools
- **PyCharm** or **VS Code** with Python extensions
- **Postman** or **curl** for API testing
- **SQLite Browser** for database inspection

---

## 🚀Installation

### Method 1: Using UV (Recommended)

```bash
# Clone the repository
git clone https://github.com/your-org/ubc-ussd-engine.git
cd ubc-ussd-engine

# Install dependencies using uv
uv pip install -e .

# Or install from pyproject.toml
uv sync
```

### Method 2: Using pip

```bash
# Clone the repository
git clone https://github.com/your-org/ubc-ussd-engine.git
cd ubc-ussd-engine

# Create a virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On Unix/macOS:
source .venv/bin/activate

# Install dependencies
pip install -e .

# Or install from setup.py
pip install -r requirements.txt
```

### Method 3: Using setuptools

```bash
# Install using setup.py
python setup.py install
```

---

## ⚙️Configuration

The application uses `application-parameters.yaml` for configuration. Key settings include:

### Application Settings
```yaml
app:
  name: ussd-engine
  version: 0.1.0
  env: development
  debug: true
  organization: Union Bank Cameroon
  contact_email: admin@unionbankcameroon.com
```

### Server Configuration
```yaml
server:
  host: 0.0.0.0
  port: 8000
  protocol: http
  workers: 4
```

### Database Configuration
```yaml
database:
  engine: sqlite
  sqlite:
    path: ./data/db.sqlite3
```

### Authentication
```yaml
auth:
  jwt:
    enabled: true
    expire_minutes: 60
    refresh_expire_days: 7
  password_policy:
    min_length: 8
    require_numbers: true
```

**⚠️ Important:** Replace all `null` and placeholder values with secure credentials before deploying to production. Never commit secrets to version control.

---

## 🎮Usage

### Running the Application

#### Windows
```cmd
# Using the batch script
app_runner.bat

# Or directly with uvicorn
uvicorn main:app --reload --port 8080
```

#### Unix/Linux/macOS
```bash
# Using the shell script
chmod +x app_runner.sh
./app_runner.sh

# Or directly with uvicorn
uvicorn main:app --reload --port 8080
```

#### Python
```python
# Run directly
python main.py
```

The application will start on `http://127.0.0.1:8000` (or port 8080 if using runner scripts).

### Accessing the Application

- **Home Page:** http://127.0.0.1:8000/
- **Info Page:** http://127.0.0.1:8000/info
- **Health Check:** http://127.0.0.1:8000/health
- **Admin Login:** http://127.0.0.1:8000/admin/login
- **API Documentation:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

---

## 📡API Endpoints

### Health & Information
- `GET /` - Home page
- `GET /info` - Application information
- `GET /health` - Health check endpoint

### Authentication
- `POST /auth/login` - User login
  ```json
  {
    "username": "user",
    "password": "password"
  }
  ```
- `GET /auth/logout?sessionId={sessionId}` - User logout

### Admin Endpoints
- `GET /admin/login` - Admin login page
- `POST /admin/auth` - Admin authentication
  - Form fields: `username`, `password`, `tenant`
- `POST /admin/logout` - Admin logout

### Response Format
```json
{
  "username": "user",
  "sessionId": "uuid-session-id",
  "reloadToken": "secure-reload-token",
  "status": "Login successful",
  "response-code": 200
}
```

---

## 📁Project Structure

```
ubc-ussd-engine/
├── main.py                          # Application entry point
├── pyproject.toml                   # Python project configuration
├── setup.py                         # Setup script
├── application-parameters.yaml      # Application configuration
├── app_runner.bat                   # Windows runner script
├── app_runner.sh                    # Unix runner script
├── LICENSE                          # MIT License
├── README.md                        # This file
├── uv.lock                         # UV lock file
│
├── src/
│   ├── app/
│   │   ├── admin/                  # Admin functionality
│   │   │   └── admin_authentication.py
│   │   │
│   │   ├── config/                 # Configuration modules
│   │   │   ├── path.py            # Path configurations
│   │   │   ├── data_cleaner.py    # Data cleaning utilities
│   │   │   └── database/
│   │   │       └── db.py          # Database wrapper
│   │   │
│   │   ├── core/                   # Core business logic
│   │   │   └── factory.py         # Factory patterns
│   │   │
│   │   ├── session/                # Session management
│   │   │   ├── authentication.py  # Auth & RBAC system
│   │   │   ├── session_engine.py  # Session engine
│   │   │   └── models.py          # Data models
│   │   │
│   │   └── database/               # SQLite databases
│   │       ├── app.db
│   │       ├── authentication.db
│   │       └── sessions.db
│   │
│   ├── tests/
│   │   └── test_ussd.py           # Test suite
│   │
│   └── web/
│       ├── admin/                  # Admin templates
│       │   ├── admin_dashboard.html
│       │   └── admin_login.html
│       ├── templates/              # User templates
│       │   ├── info.html
│       │   └── login.html
│       └── images/                 # Static images
│           └── ubc-*.png
│
└── __pycache__/                    # Python cache
```

---

## 🗄️Database Schema

The application uses three SQLite databases:

### 1. sessions.db
```sql
CREATE TABLE sessions (
    session_id   TEXT PRIMARY KEY,
    user_id      TEXT NOT NULL,
    created_at   TEXT NOT NULL,
    expires_at   TEXT,
    state        TEXT NOT NULL DEFAULT 'active',
    data         TEXT,
    reload_token TEXT,
    is_active    INTEGER NOT NULL DEFAULT 0
);
```

### 2. authentication.db

**Users Table:**
```sql
CREATE TABLE users (
    user_id       TEXT PRIMARY KEY,
    username      TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    email         TEXT NOT NULL,
    is_active     INTEGER NOT NULL DEFAULT 1,
    created_at    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_modified TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_login    TIMESTAMP NULL
);
```

**Roles Table:**
```sql
CREATE TABLE roles (
    role_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    role_name   TEXT NOT NULL UNIQUE,
    description TEXT,
    created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

**Permissions Table:**
```sql
CREATE TABLE permissions (
    permission_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    permission_name TEXT NOT NULL UNIQUE,
    description     TEXT,
    created_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

**Junction Tables:**
- `user_roles` - Many-to-many relationship between users and roles
- `role_permissions` - Many-to-many relationship between roles and permissions

**Audit Logs:**
```sql
CREATE TABLE audit_logs (
    log_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    action    TEXT NOT NULL,
    user_id   TEXT,
    email     TEXT NOT NULL,
    details   TEXT,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

### 3. app.db
General application data storage.

---

## 🔐Authentication & Authorization

### Role-Based Access Control (RBAC)

The system implements a comprehensive RBAC model:

#### Roles & Permissions Matrix

| Role       | Read | Write | Delete | Manage Users | Manage Roles | Audit Log |
|------------|------|-------|--------|--------------|--------------|-----------|
| Admin      | ✓    | ✓     | ✓      | ✓            | ✓            | ✓         |
| Moderator  | ✓    | ✓     | ✓      | ✗            | ✗            | ✓         |
| User       | ✓    | ✓     | ✗      | ✗            | ✗            | ✗         |
| Guest      | ✓    | ✗     | ✗      | ✗            | ✗            | ✗         |
| Application| ✓    | ✓     | ✗      | ✗            | ✗            | ✗         |
| Auditor    | ✓    | ✗     | ✗      | ✗            | ✗            | ✓         |

### Authentication Flow

1. User submits credentials (username/password)
2. System verifies credentials against hashed password
3. On success, creates session with unique session_id and reload_token
4. Session is stored in database with expiration time
5. Client receives session credentials
6. All subsequent requests include session_id
7. System validates session before processing requests

### Default Admin Credentials

For testing purposes, a backdoor admin user is created:
- **Username:** `admin`
- **Password:** Set by you on first login
- **Email:** `admin@local`
- **Roles:** Admin, Application
- **Permissions:** All

**⚠️ Security Warning:** Remove or disable the backdoor admin user in production!

---

## 🔄Session Management

### Session Lifecycle

1. **Creation** - Sessions created on successful login
2. **Active** - Valid sessions with unexpired tokens
3. **Expired** - Sessions past their expiration time
4. **Revoked** - Manually invalidated sessions

### Session Properties

- **session_id** - Unique UUID identifier
- **user_id** - Associated user identifier
- **reload_token** - Secure token for session refresh
- **created_at** - Session creation timestamp
- **expires_at** - Session expiration timestamp (default: 1 hour)
- **state** - Session state (active/expired/revoked)
- **data** - JSON-serialized session data
- **is_active** - Boolean flag for quick checks

### Session API

```python
from src.app.session import session_engine

# Create session
session = await session_engine.create_session_for_user(
    user_id="user123",
    ttl_seconds=3600,
    data={"role": "admin"}
)

# Get session
session = await session_engine.get_session(session_id)

# Invalidate session
success = await session_engine.invalidate_session(session_id)
```

---

## 🛠️Development

### Setting Up Development Environment

```bash
# Clone repository
git clone https://github.com/your-org/ubc-ussd-engine.git
cd ubc-ussd-engine

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Unix
.venv\Scripts\activate     # Windows

# Install development dependencies
pip install -e ".[test]"

# Run in development mode
uvicorn main:app --reload --log-level debug
```

### Code Style

The project follows Python best practices:
- PEP 8 style guide
- Type hints where applicable
- Async/await for I/O operations
- Dataclasses for structured data

### Adding New Features

1. **Feature Factory Pattern:**
   ```python
   from src.app.core.factory import USSDFeatureFactory
   
   factory = USSDFeatureFactory()
   factory.register_feature("my_feature", MyFeatureClass)
   ```

2. **Database Models:**
   - Add tables to `authentication.py` CREATE_TABLE_SQL
   - Use Database class for queries

3. **API Endpoints:**
   - Add routes to `main.py`
   - Follow RESTful conventions
   - Include proper error handling

### Logging

Logs are written to `app.log` by default. Configure in `application-parameters.yaml`:

```yaml
logging:
  level: INFO
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  console: true
  file: ./logs/app.log
```

---

## 🧪Testing

### Running Tests

```bash
# Run all tests
pytest src/tests/

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest src/tests/test_ussd.py -v
```

### Test Structure

Tests are located in `src/tests/`:
- `test_ussd.py` - USSD functionality tests (to be implemented)

### Writing Tests

```python
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
```

---

## 🚢Deployment

### Production Checklist

- [ ] Update `application-parameters.yaml` with production values
- [ ] Set `app.debug = false`
- [ ] Configure production database
- [ ] Set secure `secret_key`
- [ ] Enable HTTPS/TLS
- [ ] Configure CORS for production domains
- [ ] Set up proper logging and monitoring
- [ ] Enable rate limiting
- [ ] Review and remove test/backdoor accounts
- [ ] Set up database backups
- [ ] Configure firewall rules
- [ ] Set up reverse proxy (nginx/Apache)

### Using Docker (Optional)

```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -e .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
# Build and run
docker build -t ubc-ussd-engine .
docker run -p 8000:8000 ubc-ussd-engine
```

### Using Systemd (Linux)

Create `/etc/systemd/system/ussd-engine.service`:

```ini
[Unit]
Description=UBC USSD Engine
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/ubc-ussd-engine
ExecStart=/opt/ubc-ussd-engine/.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable ussd-engine
sudo systemctl start ussd-engine
```

### Using Nginx Reverse Proxy

```nginx
server {
    listen 80;
    server_name ussd.unionbankcameroon.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## 🤝Contributing

We welcome contributions! Please follow these guidelines:

### Contribution Process

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
   - Write clean, documented code
   - Add tests for new features
   - Update documentation
4. **Commit your changes**
   ```bash
   git commit -m "Add: your feature description"
   ```
5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```
6. **Create a Pull Request**

### Code Review Process

- All PRs require review before merging
- Ensure all tests pass
- Follow existing code style
- Update CHANGELOG.md

### Reporting Issues

Use GitHub Issues to report bugs or request features:
- **Bug Report:** Include steps to reproduce
- **Feature Request:** Describe use case and expected behavior
- **Security Issues:** Email admin@unionbankcameroon.com directly

---

## 📄License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2026 Dev UBC Plc

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## 📞Contact

**Union Bank Cameroon**

- **Email:** admin@unionbankcameroon.com
- **Project Maintainer:** Dev UBC Plc
- **Website:** https://unionbankcameroon.com

---

## 🙏Acknowledgments

- **FastAPI** - Modern, fast web framework
- **Uvicorn** - Lightning-fast ASGI server
- **SQLite** - Lightweight database engine
- **Jinja2** - Powerful templating engine

---

## 📚Additional Resources

### Documentation
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Python Official Docs](https://docs.python.org/3/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [UV Documentation](https://docs.astral.sh/uv/)

### Related Projects
- USSD Gateway Integration
- Payment Processing Services
- Banking Core System Integration

---

## 🔄Version History

### v1.0.0 (Current)
- Initial release
- Core USSD engine functionality
- Authentication and authorization system
- Session management
- Admin dashboard
- Role-based access control

### v0.1.0
- Development version
- Basic API structure
- Database schema design

---

## 🗺️Roadmap

- [ ] Add comprehensive test coverage
- [ ] Implement USSD menu builder
- [ ] Add multi-language support (i18n)
- [ ] Integrate with payment gateways
- [ ] Add API rate limiting
- [ ] Implement Redis caching
- [ ] Add WebSocket support for real-time updates
- [ ] Create CLI management tool
- [ ] Add metrics and monitoring dashboard
- [ ] PostgreSQL/MySQL support
- [ ] Docker Compose setup
- [ ] Kubernetes deployment manifests

---

**Built with ❤️ by Union Bank Cameroon Development Team**
