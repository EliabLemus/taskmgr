# Task Manager API - Production Ready Django REST Framework

A production-ready Django REST API with monitoring, CI/CD, and load testing capabilities.

## Features

- ✅ Django 4.2 LTS + Django REST Framework
- ✅ Token Authentication
- ✅ Prometheus metrics exposure
- ✅ Grafana dashboards
- ✅ Redis caching
- ✅ Docker Compose orchestration
- ✅ CI/CD with GitHub Actions
- ✅ Apache Bench load testing
- ✅ Slack alerting
- ✅ OpenAPI/Swagger documentation
- ✅ Comprehensive test suite with pytest

## Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Python | CPython | 3.11.9 |
| Framework | Django | 4.2.16 (LTS) |
| API | Django REST Framework | 3.14.0 |
| Database | SQLite | 3.x |
| Cache | Redis | 7.x |
| Monitoring | Prometheus + Grafana | Latest |
| WSGI | Gunicorn | 21.2.0 |
| Testing | Pytest | 7.4.3 |

## Prerequisites

- **Docker & Docker Compose** - [Install Docker](https://docs.docker.com/get-docker/)
- **Make** - Build automation
- **Python 3.11+** - For local development
- **pyenv** (recommended) - Python version management

## Local Development Setup

### 1. Install pyenv (if not already installed)

**macOS:**
```bash
brew install pyenv
```

**Linux:**
```bash
curl https://pyenv.run | bash
```

Add to your shell profile (`~/.zshrc` or `~/.bashrc`):
```bash
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
```

Restart your shell or run:
```bash
source ~/.zshrc  # or ~/.bashrc
```

### 2. Clone and Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd taskmgr

# Install Python 3.11.9 (if not already installed)
pyenv install 3.11.9

# Set local Python version (reads from .python-version)
pyenv local 3.11.9

# Verify Python version
python --version  # Should show Python 3.11.9

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 3. Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env if needed (default values work for local development)
```

### 4. Start Services with Docker

```bash
# Build Docker images
make compose-build

# Start all services (API, Redis, Prometheus, Grafana)
make compose-up

# View logs
make compose-logs
```

### 5. Verify Installation

```bash
# Run Phase 0 verification tests
make test-phase0

# Or manually check endpoints
curl http://localhost:8000/health
curl http://localhost:8000/status
```

## Quick Start (Docker Only)

If you just want to run the services without local Python setup:

```bash
# Start everything
make compose-up

# Access services:
# - API: http://localhost:8000
# - Grafana: http://localhost:3000 (admin/admin)
# - Prometheus: http://localhost:9090
```

## Access Points

| Service    | URL                        | Credentials     |
|------------|----------------------------|-----------------|
| API        | http://localhost:8000      | -               |
| Grafana    | http://localhost:3000      | admin/admin     |
| Prometheus | http://localhost:9090      | -               |
| API Docs   | http://localhost:8000/api/v1/docs/ | (Phase 1+) |

## Development Workflow

### Running Tests

```bash
# Activate virtual environment (if not already active)
source venv/bin/activate

# Run all tests
make test

# Run specific test categories
make test-phase0        # Infrastructure tests
make test-unit          # Unit tests
make test-integration   # Integration tests

# Run tests with coverage
pytest --cov=app --cov-report=html

# View coverage report
open htmlcov/index.html
```

### Code Quality

```bash
# Run linters
make lint

# Format code with black
black app/ tests/

# Sort imports
isort app/ tests/

# Type checking
mypy app/
```

### Django Commands

```bash
# Django shell
make shell

# Run migrations
make migrate

# Create superuser (Phase 1+)
docker compose exec api python manage.py createsuperuser

# Collect static files
docker compose exec api python manage.py collectstatic
```

## API Endpoints (Phase 1+)

All endpoints are prefixed with `/api/v1/`

| Method | Endpoint              | Description           | Auth Required |
|--------|-----------------------|-----------------------|---------------|
| GET    | `/health`             | Health check          | No            |
| GET    | `/status`             | Status check          | No            |
| GET    | `/metrics`            | Prometheus metrics    | No            |
| POST   | `/api/v1/auth/token/` | Obtain auth token     | No            |
| GET    | `/api/v1/tasks/`      | List tasks            | Yes           |
| POST   | `/api/v1/tasks/`      | Create task           | Yes           |
| GET    | `/api/v1/schema/`     | OpenAPI schema        | No            |
| GET    | `/api/v1/docs/`       | Swagger UI            | No            |

## Monitoring

### Grafana Dashboard

1. Navigate to http://localhost:3000
2. Login with `admin/admin`
3. View "Task Manager API Metrics" dashboard

### Prometheus

Access raw metrics and queries at http://localhost:9090

### Custom Metrics (Phase 2+)

- Request count by endpoint
- Response time percentiles (p50, p95, p99)
- Error rates
- Active users
- Cache hit/miss rates

## Load Testing (Phase 3)

```bash
# Run Apache Bench load test
make bench

# Run custom traffic simulator
python scripts/traffic_sim.py --rps 10 --duration 60
```

## CI/CD (Phase 4)

GitHub Actions workflows:
- `.github/workflows/ci.yml` - Lint and test on push
- `.github/workflows/cd.yml` - Build and publish on tag

### Required Secrets

Configure in GitHub Settings → Secrets:
- `DOCKERHUB_USERNAME` - Docker Hub username
- `DOCKERHUB_TOKEN` - Docker Hub access token
- `SLACK_WEBHOOK_URL` - Slack webhook for alerts

## Project Structure

```
taskmgr/
├── app/                           # Django application
│   ├── settings.py               # Django settings
│   ├── urls.py                   # URL routing
│   ├── wsgi.py                   # WSGI config
│   └── manage.py                 # Django management
├── tests/                         # Test suite
│   ├── test_phase0_verification.py
│   ├── test_phase1_api.py        # (Phase 1+)
│   └── test_phase2_monitoring.py # (Phase 2+)
├── infra/
│   ├── docker/                   # Dockerfiles
│   ├── compose/                  # Docker Compose configs
│   │   ├── prometheus.yml
│   │   └── grafana/
│   └── ci/                       # CI/CD configs
├── scripts/                       # Utility scripts
│   └── traffic_sim.py            # (Phase 3)
├── docs/                          # Documentation
│   └── api_catalog.json          # API documentation
├── reports/                       # Test/benchmark reports
├── venv/                          # Virtual environment (gitignored)
├── .python-version               # pyenv Python version
├── requirements.txt              # Production dependencies
├── requirements-dev.txt          # Development dependencies
├── Makefile                      # Build automation
├── docker-compose.yml            # Service orchestration
├── pytest.ini                    # Pytest configuration
└── README.md                     # This file
```

## Makefile Commands

```bash
make help              # Show all available commands
make compose-up        # Start all services
make compose-down      # Stop all services
make compose-build     # Build Docker images
make compose-logs      # View logs
make test              # Run all tests
make test-phase0       # Run Phase 0 verification
make lint              # Run linters
make clean             # Clean up containers and cache
```

## Environment Variables

Key environment variables (see `.env.example`):

```bash
# Django
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=true
DJANGO_ALLOWED_HOSTS=*

# Database
SQLITE_PATH=/data/db.sqlite3

# Redis
REDIS_URL=redis://redis:6379/0

# Monitoring
PROMETHEUS_PORT=9090
GRAFANA_PORT=3000

# Alerting
SLACK_WEBHOOK_URL=https://hooks.slack.com/...

# Gunicorn
GUNICORN_WORKERS=3
GUNICORN_TIMEOUT=60
```

## Troubleshooting

### Services won't start

```bash
# Check Docker is running
docker --version
docker info

# View logs
make compose-logs

# Clean and restart
make clean
make compose-build
make compose-up
```

### Tests failing

```bash
# Ensure services are running
docker compose ps

# Wait for services to stabilize
sleep 10

# Run tests again
make test-phase0
```

### Port already in use

```bash
# Check what's using the port
lsof -i :8000  # or :3000, :9090

# Stop the conflicting service or change ports in docker-compose.yml
```

### Virtual environment issues

```bash
# Remove and recreate
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Python version mismatch

```bash
# Check Python version
python --version  # Should be 3.11.9

# If wrong version, ensure pyenv is configured
pyenv local 3.11.9
pyenv which python

# Recreate venv with correct Python
rm -rf venv
python -m venv venv
source venv/bin/activate
```

## Contributing

1. Create a feature branch
2. Make your changes
3. Run tests: `make test`
4. Run linters: `make lint`
5. Commit with meaningful messages
6. Push and create a Pull Request

## Architecture

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

## License

MIT

## Support

For issues and questions:
- Open an issue in the repository
- Check existing documentation
- Review logs with `make compose-logs`
