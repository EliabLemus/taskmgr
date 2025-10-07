# Task Manager API - Production Ready Django REST Framework

A production-ready Django REST API with monitoring, CI/CD, and comprehensive task management.

## 🚀 Features

### Phase 1 - REST API ✅ COMPLETE
- ✅ **Full CRUD API** for task management
- ✅ **Token Authentication** with user registration
- ✅ **Advanced Filtering** (status, priority, dates, search)
- ✅ **Pagination** with customizable page size
- ✅ **Permissions** - Users only see their own tasks
- ✅ **OpenAPI/Swagger Documentation**
- ✅ **93% Test Coverage** (54 tests passing)

### Phase 0 - Infrastructure ✅ COMPLETE
- ✅ Docker Compose orchestration
- ✅ Prometheus metrics exposure
- ✅ Grafana dashboards
- ✅ Redis caching
- ✅ CI/CD with GitHub Actions

## 📊 Quick Stats

| Metric | Value |
|--------|-------|
| Python Version | 3.11.9 |
| Django Version | 4.2.16 LTS |
| Test Coverage | 93% |
| Total Tests | 54 |
| API Endpoints | 15+ |
| Docker Services | 4 |

## 🏃 Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.11+ with pyenv
- Make

### Setup

```bash
# Clone repository
git clone <your-repo>
cd taskmgr

# Setup Python environment
pyenv install 3.11.9
pyenv local 3.11.9
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Start services
make compose-up

# Run tests
make test
```

## 📚 API Documentation

### Authentication

```bash
# Register new user
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H 'Content-Type: application/json' \
  -d '{"username":"john","email":"john@example.com","password":"secure123"}'

# Get authentication token
curl -X POST http://localhost:8000/api/v1/auth/token/ \
  -H 'Content-Type: application/json' \
  -d '{"username":"john","password":"secure123"}'
```

### Task Management

```bash
# Create task
curl -X POST http://localhost:8000/api/v1/tasks/ \
  -H 'Authorization: Token YOUR_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{"title":"Deploy Phase 1","status":"TODO","priority":"HIGH"}'

# List tasks with filtering
curl "http://localhost:8000/api/v1/tasks/?status=TODO&priority=HIGH" \
  -H 'Authorization: Token YOUR_TOKEN'

# Search tasks
curl "http://localhost:8000/api/v1/tasks/?search=deploy" \
  -H 'Authorization: Token YOUR_TOKEN'

# Get task statistics
curl http://localhost:8000/api/v1/tasks/stats/ \
  -H 'Authorization: Token YOUR_TOKEN'
```

### Interactive Documentation

Visit: http://localhost:8000/api/v1/docs/

## 🧪 Testing

```bash
# Run all tests
make test

# Run Phase 1 API tests only
make test-phase1

# Run with coverage report
make test-cov
open htmlcov/index.html
```

## 📖 API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `POST` | `/api/v1/auth/register/` | Register new user | No |
| `POST` | `/api/v1/auth/token/` | Get auth token | No |
| `GET` | `/api/v1/tasks/` | List user's tasks | Yes |
| `POST` | `/api/v1/tasks/` | Create new task | Yes |
| `GET` | `/api/v1/tasks/{id}/` | Get task detail | Yes |
| `PATCH` | `/api/v1/tasks/{id}/` | Update task (partial) | Yes |
| `PUT` | `/api/v1/tasks/{id}/` | Update task (full) | Yes |
| `DELETE` | `/api/v1/tasks/{id}/` | Delete task | Yes |
| `GET` | `/api/v1/tasks/stats/` | Get task statistics | Yes |
| `POST` | `/api/v1/tasks/{id}/mark_done/` | Mark task as done | Yes |
| `GET` | `/api/v1/schema/` | OpenAPI schema | No |
| `GET` | `/api/v1/docs/` | Swagger UI | No |

### Query Parameters

- `?status=TODO|IN_PROGRESS|DONE` - Filter by status
- `?priority=LOW|MEDIUM|HIGH` - Filter by priority
- `?search=keyword` - Search in title/description
- `?ordering=-created_at` - Order results
- `?page=2&page_size=10` - Pagination

## 🏗️ Architecture

```
┌─────────────┐     ┌──────────┐     ┌────────────┐
│   Grafana   │────▶│Prometheus│────▶│ Django API │
│   :3000     │     │  :9090   │     │   :8000    │
└─────────────┘     └──────────┘     └────────────┘
                                            │
                                            ▼
                                      ┌──────────┐
                                      │  Redis   │
                                      │  :6379   │
                                      └──────────┘
```

## 🛠️ Development

### Makefile Commands

```bash
make help              # Show all commands
make compose-up        # Start all services
make compose-down      # Stop services
make test              # Run all tests
make test-phase1       # Run API tests
make test-cov          # Tests with coverage
make lint              # Run linters
make format            # Format code
make migrate           # Run Django migrations
make shell             # Django shell
```

### Project Structure

```
taskmgr/
├── app/                     # Django application
│   ├── tasks/              # Task management app
│   │   ├── models.py       # Task model
│   │   ├── serializers.py  # DRF serializers
│   │   ├── views.py        # API viewsets
│   │   ├── permissions.py  # Custom permissions
│   │   ├── filters.py      # Query filters
│   │   └── tests/          # (in root tests/)
│   ├── settings.py         # Django settings
│   └── urls.py             # URL configuration
├── tests/                   # Test suite
│   ├── test_phase0_*.py    # Infrastructure tests
│   └── test_phase1_*.py    # API tests
├── infra/                   # Infrastructure
│   ├── docker/             # Dockerfiles
│   └── compose/            # Compose configs
├── .github/workflows/       # CI/CD
├── venv/                    # Virtual environment
├── Makefile                # Automation
└── docker-compose.yml      # Services
```

## 🚦 CI/CD

GitHub Actions workflows:
- **CI**: Lint, test, build on every push
- **CD**: Deploy on tag creation

## 📈 Monitoring

- **API Metrics**: http://localhost:8000/metrics
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/admin)

## 🔐 Security

- Token-based authentication
- Permission-based access control
- Users isolated to their own data
- CSRF protection
- SQL injection prevention (ORM)

## 📝 License

MIT

## 🙏 Acknowledgments

Built with Django, DRF, Docker, Prometheus, and Grafana.
