<div align="center">

# 🚀 Task Manager API

### Production-Ready Django REST Framework with Monitoring & Observability

[![Python](https://img.shields.io/badge/Python-3.11.9-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2.16%20LTS-green.svg)](https://www.djangoproject.com/)
[![Tests](https://img.shields.io/badge/Tests-63%2F63%20passing-success.svg)](tests/)
[![Coverage](https://img.shields.io/badge/Coverage-93%25-brightgreen.svg)](htmlcov/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[Features](#-features) • [Quick Start](#-quick-start) • [API Docs](#-api-documentation) • [Architecture](#️-architecture) • [Testing](#-testing)

</div>

---

## 📋 Table of Contents

- [Features](#-features)
- [Quick Stats](#-quick-stats)
- [Quick Start](#-quick-start)
- [API Documentation](#-api-documentation)
- [Architecture](#️-architecture)
- [Testing](#-testing)
- [Development](#️-development)
- [Monitoring](#-monitoring--observability)
- [Security](#-security)
- [What's Next](#-whats-next)

---

## ✨ Features

### 🎯 Phase 2 - Metrics & Alerts ✅ **COMPLETE**

<table>
<tr>
<td width="50%">

#### Metrics & Monitoring
- ✅ Custom metrics middleware
- ✅ Redis-based storage with TTL
- ✅ Per-minute aggregation
- ✅ Real-time latency tracking
- ✅ Error rate monitoring
- ✅ Active user tracking

</td>
<td width="50%">

#### Alerting System
- ✅ Threshold-based alerts
- ✅ Slack webhook integration
- ✅ 5-minute cooldown
- ✅ Alert history API
- ✅ Multiple severity levels
- ✅ Configurable thresholds

</td>
</tr>
</table>

**Metrics Tracked:**
- 📊 Total requests
- ⚡ Response latency (min/max/avg/p50/p95/p99)
- ❌ Error rate (%)
- 👥 Active authenticated users

**Alert Types:**
- 🚨 High error rate (> 5%)
- ⏱️ High latency (p95 > 500ms)

---

### 🔌 Phase 1 - REST API ✅ **COMPLETE**

- ✅ **Full CRUD** - Complete task management
- ✅ **Token Auth** - Secure user authentication
- ✅ **Advanced Filtering** - Status, priority, dates, search
- ✅ **Pagination** - Customizable page sizes
- ✅ **Permissions** - User-scoped data access
- ✅ **OpenAPI/Swagger** - Interactive documentation
- ✅ **39 Tests** - Complete API coverage

---

### 🏗️ Phase 0 - Infrastructure ✅ **COMPLETE**

- ✅ **Docker Compose** - Multi-container orchestration
- ✅ **Prometheus** - Metrics collection
- ✅ **Grafana** - Visualization dashboards
- ✅ **Redis** - Caching & metrics storage
- ✅ **CI/CD** - GitHub Actions pipelines
- ✅ **15 Tests** - Infrastructure verification

---

## 📊 Quick Stats

| Category | Metric | Status |
|----------|--------|--------|
| 🐍 Python | 3.11.9 | ✅ |
| 🎯 Django | 4.2.16 LTS | ✅ |
| ✅ Total Tests | **63/63 passing** | ✅ |
| 📈 Coverage | 93% | ✅ |
| 🌐 API Endpoints | 18+ | ✅ |
| 🐳 Docker Services | 4 | ✅ |
| 🚨 Active Alerts | 2 types | ✅ |

---

## 🚀 Quick Start

### Prerequisites

```bash
# Required
- Docker & Docker Compose
- Python 3.11+ with pyenv
- Make

# Optional
- Slack webhook for alerts
```

### Installation

```bash
# 1️⃣ Clone repository
git clone https://github.com/EliabLemus/taskmgr
cd taskmgr

# 2️⃣ Copy environment file
cp .env.example .env

# 3️⃣ Add your Slack webhook (optional)
# Edit .env:
# SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL

# 4️⃣ Setup Python environment
pyenv install 3.11.9
pyenv local 3.11.9
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 5️⃣ Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 6️⃣ Start all services
make compose-up

# 7️⃣ Verify installation
make test
```

**🎉 Done!** Your API is running at `http://localhost:8000`

---

## 📚 API Documentation

### 🔐 Authentication

```bash
# Register new user
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H 'Content-Type: application/json' \
  -d '{
    "username": "john",
    "email": "john@example.com",
    "password": "secure123"
  }'

# Get authentication token
curl -X POST http://localhost:8000/api/v1/auth/token/ \
  -H 'Content-Type: application/json' \
  -d '{
    "username": "john",
    "password": "secure123"
  }'

# Response
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

---

### 📋 Task Management

```bash
# Create task
curl -X POST http://localhost:8000/api/v1/tasks/ \
  -H 'Authorization: Token YOUR_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "Deploy Phase 2",
    "description": "Complete metrics and alerting",
    "status": "TODO",
    "priority": "HIGH",
    "due_date": "2025-10-15"
  }'

# List all tasks
curl http://localhost:8000/api/v1/tasks/ \
  -H 'Authorization: Token YOUR_TOKEN'

# Filter tasks
curl "http://localhost:8000/api/v1/tasks/?status=TODO&priority=HIGH" \
  -H 'Authorization: Token YOUR_TOKEN'

# Search tasks
curl "http://localhost:8000/api/v1/tasks/?search=deploy" \
  -H 'Authorization: Token YOUR_TOKEN'

# Get task statistics
curl http://localhost:8000/api/v1/tasks/stats/ \
  -H 'Authorization: Token YOUR_TOKEN'

# Mark task as done
curl -X POST http://localhost:8000/api/v1/tasks/{id}/mark_done/ \
  -H 'Authorization: Token YOUR_TOKEN'
```

---

### 📊 Metrics & Monitoring (Phase 2)

```bash
# Get real-time metrics summary (last 5 minutes)
curl http://localhost:8000/api/v1/metrics/summary/

# Response
{
  "total_requests": 1250,
  "total_errors": 45,
  "error_rate_percent": 3.6,
  "active_users": 12,
  "latency": {
    "min": 15.2,
    "max": 850.3,
    "avg": 125.7,
    "p50": 98.5,
    "p95": 450.2,
    "p99": 720.1
  },
  "time_window": "5 minutes"
}
```

---

### 🚨 Alert History

```bash
# List all alerts
curl http://localhost:8000/api/v1/alerts/ \
  -H 'Authorization: Token YOUR_TOKEN'

# Filter by severity
curl "http://localhost:8000/api/v1/alerts/?severity=ERROR" \
  -H 'Authorization: Token YOUR_TOKEN'

# Filter by alert type
curl "http://localhost:8000/api/v1/alerts/?alert_type=high_error_rate" \
  -H 'Authorization: Token YOUR_TOKEN'

# Get specific alert
curl http://localhost:8000/api/v1/alerts/{id}/ \
  -H 'Authorization: Token YOUR_TOKEN'
```

---

### 🌐 Interactive Documentation

| Documentation | URL | Description |
|---------------|-----|-------------|
| 📖 Swagger UI | http://localhost:8000/api/v1/docs/ | Interactive API testing |
| 📘 ReDoc | http://localhost:8000/api/v1/redoc/ | Clean API reference |
| 📄 OpenAPI Schema | http://localhost:8000/api/v1/schema/ | JSON schema |

---

### OpenAPI Schema Formats

The API exposes its OpenAPI specification at /api/v1/schema/ using content negotiation. You can obtain it in JSON or YAML based on the `format` parameter or the `Accept` header.

- For JSON:
  curl -s http://localhost:8000/api/v1/schema/?format=json | jq .
  You can also use the header:
  curl -s -H "Accept: application/vnd.oai.openapi+json" http://localhost:8000/api/v1/schema/ | jq .

- For YAML:
  curl -s http://localhost:8000/api/v1/schema/?format=yaml
  Or with a header:
  curl -s -H "Accept: application/vnd.oai.openapi" http://localhost:8000/api/v1/schema/

This lets you switch between the JSON and YAML formats for the schema as needed.


---

## 🗺️ API Endpoints

### Authentication & User Management

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/api/v1/auth/register/` | Register new user | ❌ |
| `POST` | `/api/v1/auth/token/` | Get authentication token | ❌ |

### Task Management (Phase 1)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/api/v1/tasks/` | List user's tasks | ✅ |
| `POST` | `/api/v1/tasks/` | Create new task | ✅ |
| `GET` | `/api/v1/tasks/{id}/` | Get task detail | ✅ |
| `PATCH` | `/api/v1/tasks/{id}/` | Partial update | ✅ |
| `PUT` | `/api/v1/tasks/{id}/` | Full update | ✅ |
| `DELETE` | `/api/v1/tasks/{id}/` | Delete task | ✅ |
| `GET` | `/api/v1/tasks/stats/` | Get task statistics | ✅ |
| `POST` | `/api/v1/tasks/{id}/mark_done/` | Mark task as done | ✅ |

### Metrics & Alerts (Phase 2) 🆕

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/api/v1/metrics/summary/` | Real-time metrics (5min) | ❌ |
| `GET` | `/api/v1/alerts/` | List alert history | ✅ |
| `GET` | `/api/v1/alerts/{id}/` | Get specific alert | ✅ |

### Infrastructure (Phase 0)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/health` | Health check | ❌ |
| `GET` | `/status` | Detailed status + dependencies | ❌ |
| `GET` | `/metrics` | Prometheus metrics | ❌ |
| `GET` | `/api/v1/schema/` | OpenAPI schema | ❌ |
| `GET` | `/api/v1/docs/` | Swagger UI | ❌ |

---

### Query Parameters

#### Tasks Filtering
```bash
?status=TODO|IN_PROGRESS|DONE  # Filter by status
?priority=LOW|MEDIUM|HIGH       # Filter by priority
?search=keyword                 # Search title/description
?ordering=-created_at           # Order results
?page=2                         # Pagination page
?page_size=10                   # Items per page
?created_after=2025-01-01       # Created after date
?created_before=2025-12-31      # Created before date
?due_date=2025-10-15            # Specific due date
```

#### Alerts Filtering
```bash
?severity=INFO|WARNING|ERROR|CRITICAL  # Filter by severity
?alert_type=high_error_rate|high_latency  # Filter by type
?page=1                                   # Pagination
```

---

## 🏗️ Architecture

```
┌─────────────┐     ┌──────────┐     ┌────────────┐
│   Grafana   │────▶│Prometheus│────▶│ Django API │
│   :3000     │     │  :9090   │     │   :8000    │
└─────────────┘     └──────────┘     └─────┬──────┘
                                            │
                    ┌───────────────────────┼───────────┐
                    ▼                       ▼           ▼
              ┌──────────┐           ┌──────────┐  ┌────────┐
              │  Redis   │           │ Metrics  │  │ Alerts │
              │  :6379   │           │Middleware│  │ System │
              └──────────┘           └──────────┘  └────────┘
                                                        │
                                                        ▼
                                                   ┌────────┐
                                                   │ Slack  │
                                                   └────────┘
```

### Components

| Service | Port | Purpose |
|---------|------|---------|
| 🌐 Django API | 8000 | REST API & Business Logic |
| 💾 Redis | 6379 | Caching & Metrics Storage |
| 📊 Prometheus | 9090 | Metrics Collection |
| 📈 Grafana | 3000 | Visualization |
| 💬 Slack | - | Alert Notifications |

---

## 🧪 Testing

### Run All Tests

```bash
# Run full test suite (63 tests)
make test

# ✅ All tests passing:
# tests/test_phase0_health.py ................  [15 tests]
# tests/test_phase1_api.py ..................  [39 tests]
# tests/test_phase2_metrics.py ..............  [9 tests]
# Total: 63 passed in 12.45s
```

### Phase-Specific Tests

```bash
# Phase 0: Infrastructure tests (15 tests)
make test-phase0

# Phase 1: API tests (39 tests)
make test-phase1

# Phase 2: Metrics & alerts tests (9 tests)
make test-phase2
```

### Coverage Report

```bash
# Generate coverage report
make test-cov

# Open HTML report
open htmlcov/index.html

# Current coverage: 93%
```

---

## 🛠️ Development

### Makefile Commands

```bash
make help              # 📖 Show all available commands

# 🐳 Docker
make compose-up        # Start all services
make compose-down      # Stop all services
make compose-logs      # View logs
make compose-restart   # Restart services

# 🧪 Testing
make test              # Run all tests (63 tests)
make test-phase0       # Infrastructure tests
make test-phase1       # API tests
make test-phase2       # Metrics/alerts tests
make test-cov          # Generate coverage report

# 🔍 Code Quality
make lint              # Run linters (flake8, pylint)
make format            # Format code with black
make check             # Run all checks

# 🗄️ Database
make migrate           # Run Django migrations
make makemigrations    # Create new migrations
make shell             # Open Django shell

# 🔧 Development
make dev               # Start development server
make requirements      # Update requirements.txt
```

---

## 📈 Monitoring & Observability

### Metrics Collection (Phase 2)

#### How It Works

1. **Middleware**: Automatically tracks every HTTP request
2. **Storage**: Redis with per-minute granular keys
3. **Aggregation**: 5-minute rolling window
4. **TTL**: 1-hour automatic cleanup

#### Metrics Tracked

| Metric | Description | Storage |
|--------|-------------|---------|
| 📊 Total Requests | Count per minute | `metrics:requests:{minute}` |
| ❌ Error Count | 4xx/5xx responses | `metrics:errors:{minute}` |
| ⚡ Latency | Response time (ms) | `metrics:latencies:{minute}` |
| 👥 Active Users | Authenticated users | `metrics:users:{minute}` |

#### Latency Percentiles

- **Min**: Fastest response
- **Max**: Slowest response
- **Avg**: Average response time
- **P50**: Median (50th percentile)
- **P95**: 95th percentile (critical threshold)
- **P99**: 99th percentile (outliers)

---

### Alerting System (Phase 2)

#### Alert Types

| Type | Condition | Severity | Action |
|------|-----------|----------|--------|
| 🚨 High Error Rate | Error rate > 5% | ERROR | Slack notification |
| ⏱️ High Latency | P95 > 500ms | WARNING | Slack notification |

---

### Dashboards

| Service | URL | Credentials | Purpose |
|---------|-----|-------------|---------|
| 📊 Prometheus | http://localhost:9090 | - | Metrics database |
| 📈 Grafana | http://localhost:3000 | admin/admin | Visualization |
| 🌐 API Metrics | http://localhost:8000/metrics | - | Prometheus scrape |
| 📊 Summary | http://localhost:8000/api/v1/metrics/summary/ | - | Real-time stats |

---

## 🔐 Security

### Authentication & Authorization

- ✅ Token-based authentication (Django REST Framework)
- ✅ Permission-based access control (`IsOwner`)
- ✅ User data isolation (users only see their own tasks)
- ✅ Secure password hashing (Django's PBKDF2)

### API Security

- ✅ CSRF protection enabled
- ✅ SQL injection prevention (Django ORM)
- ✅ Input validation (DRF serializers)
- ✅ Rate limiting ready (Redis-backed)
- ✅ CORS configuration

### Infrastructure Security

- ✅ Environment-based secrets (`.env`)
- ✅ No secrets in repository
- ✅ Docker container isolation
- ✅ Minimal Docker image (Alpine-based)
- ✅ GitHub Actions secrets

---

## ⚙️ Configuration

### Environment Variables

```bash
# Django Core
DJANGO_SECRET_KEY=your-secret-key-here-change-in-production
DJANGO_DEBUG=false
DJANGO_ALLOWED_HOSTS=*,localhost,127.0.0.1

# Database
SQLITE_PATH=/data/db.sqlite3

# Redis
REDIS_URL=redis://redis:6379/0

# Slack Alerts (optional)
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL

# Gunicorn
GUNICORN_WORKERS=3
GUNICORN_TIMEOUT=60

# Metrics & Alerts (Phase 2)
ERROR_RATE_THRESHOLD=5.0        # Error rate alert threshold (%)
LATENCY_P95_THRESHOLD=500.0     # P95 latency threshold (ms)
ALERT_COOLDOWN_SECONDS=300      # 5 minutes
```

---

## 🎯 What's Next?

### Phase 3 - Traffic Simulation & Load Testing (Planned)

- [ ] 🔸 Traffic simulator script with configurable parameters
- [ ] 🔸 Apache Bench integration for benchmarking
- [ ] 🔸 Enhanced Grafana dashboards with load test history
- [ ] 🔸 Rate limiting demonstrations

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. 🍴 Fork the repository
2. 🌿 Create a feature branch (`git checkout -b feature/amazing-feature`)
3. ✍️ Commit your changes (`git commit -m 'Add amazing feature'`)
4. 📤 Push to the branch (`git push origin feature/amazing-feature`)
5. 🔁 Open a Pull Request

---

## 🙏 Acknowledgments

Built with ❤️ using:

- [Django](https://www.djangoproject.com/) - Web framework
- [Django REST Framework](https://www.django-rest-framework.org/) - API toolkit
- [Docker](https://www.docker.com/) - Containerization
- [Prometheus](https://prometheus.io/) - Metrics & monitoring
- [Grafana](https://grafana.com/) - Visualization
- [Redis](https://redis.io/) - Caching & storage
- [pytest](https://pytest.org/) - Testing framework

---

<div align="center">

### 📊 Current Status

**Phase 2 Complete** ✅ | **63/63 Tests Passing** ✅ | **Production Ready** 🚀

[⬆ Back to Top](#-task-manager-api)

</div>