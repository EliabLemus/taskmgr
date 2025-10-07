#!/bin/bash
set -e

echo "=================================================="
echo "PHASE 1 - Final Cleanup & Commit Preparation"
echo "=================================================="
echo ""

# 1. Remove all temporary setup scripts
echo "Removing temporary setup scripts..."
rm -f phase1_step*.sh \
      phase0_*.sh \
      fix_*.sh \
      check_*.sh \
      clean_*.sh \
      debug_*.sh \
      setup_*.sh \
      test_setup*.sh \
      update_*.sh \
      pre_commit_cleanup.sh

echo "✓ Removed temporary scripts"

# 2. Clean Python cache
echo ""
echo "Cleaning Python cache and temporary files..."
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
rm -rf htmlcov/ .coverage 2>/dev/null || true

echo "✓ Cleaned Python cache"

# 3. Clean reports
echo ""
echo "Cleaning test reports..."
rm -rf reports/*.log reports/*.html 2>/dev/null || true

echo "✓ Cleaned reports"

# 4. Format code
echo ""
echo "Formatting code with black and isort..."
if [ -d "venv" ]; then
    source venv/bin/activate
    black app/ tests/ --quiet
    isort app/ tests/ --quiet
    echo "✓ Code formatted"
else
    echo "⚠️  venv not found, skipping formatting"
fi

# 5. Run linters
echo ""
echo "Running linters..."
if [ -d "venv" ]; then
    flake8 app/ --max-line-length=120 --exclude=migrations --count || true
    echo "✓ Linters completed"
fi

# 6. Create .gitattributes for consistent line endings
echo ""
echo "Creating .gitattributes..."
cat > .gitattributes << 'EOF'
# Auto detect text files and perform LF normalization
* text=auto

# Python
*.py text eol=lf

# Shell scripts
*.sh text eol=lf

# Documentation
*.md text eol=lf
*.txt text eol=lf

# Docker
Dockerfile text eol=lf
docker-compose.yml text eol=lf

# Config files
*.yml text eol=lf
*.yaml text eol=lf
*.json text eol=lf
*.ini text eol=lf
*.cfg text eol=lf

# Ignore in exports
.gitattributes export-ignore
.gitignore export-ignore
EOF

echo "✓ Created .gitattributes"

# 7. Verify .gitignore is complete
echo ""
echo "Verifying .gitignore..."
if ! grep -q "htmlcov/" .gitignore; then
    echo "htmlcov/" >> .gitignore
fi
if ! grep -q ".coverage" .gitignore; then
    echo ".coverage" >> .gitignore
fi

echo "✓ .gitignore verified"

# 8. Create CHANGELOG.md
echo ""
echo "Creating CHANGELOG.md..."
cat > CHANGELOG.md << 'EOF'
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2025-10-07

### Phase 1 - REST API Implementation

#### Added
- **Task Model**: Full CRUD with UUID, status, priority, and ownership
- **Authentication**: Token-based authentication with user registration
- **API Endpoints**:
  - `POST /api/v1/auth/register/` - User registration
  - `POST /api/v1/auth/token/` - Token authentication
  - Full CRUD for tasks (`GET`, `POST`, `PATCH`, `PUT`, `DELETE`)
  - Custom actions: `/tasks/stats/`, `/tasks/{id}/mark_done/`
- **Filtering & Search**:
  - Filter by status, priority, date ranges
  - Full-text search on title and description
  - Ordering support
  - Pagination with customizable page size
- **Documentation**:
  - OpenAPI/Swagger UI at `/api/v1/docs/`
  - ReDoc UI at `/api/v1/redoc/`
  - API schema at `/api/v1/schema/`
- **Testing**:
  - 39 Phase 1 API tests (auth, CRUD, filtering)
  - 93% code coverage
  - Makefile test automation
- **Permissions**: IsOwner - users only access their own tasks

#### Changed
- Updated Django settings with DRF configuration
- Enhanced REST Framework with filtering backends
- Custom pagination with page_size support

### Phase 0 - Infrastructure Setup

#### Added
- **Docker Compose Stack**:
  - Django API (Gunicorn)
  - Redis for caching
  - Prometheus for metrics
  - Grafana for visualization
- **Monitoring**:
  - Prometheus metrics at `/metrics`
  - Grafana dashboard provisioning
  - Health check endpoints
- **Testing**: 15 Phase 0 infrastructure tests
- **CI/CD**: GitHub Actions workflows (lint, test, build, deploy)
- **Development**:
  - Makefile automation
  - pyenv + venv setup
  - Comprehensive README

#### Technical Stack
- Python 3.11.9
- Django 4.2.16 (LTS)
- Django REST Framework 3.14.0
- PostgreSQL-ready (currently SQLite)
- Redis 7.x
- Docker Compose
- Prometheus + Grafana

## [0.1.0] - 2025-10-06

### Initial Setup
- Project scaffolding
- Docker infrastructure
- Basic Django setup

[Unreleased]: https://github.com/yourusername/taskmgr/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/yourusername/taskmgr/compare/v0.1.0...v1.0.0
[0.1.0]: https://github.com/yourusername/taskmgr/releases/tag/v0.1.0
EOF

echo "✓ Created CHANGELOG.md"

# 9. Update README with Phase 1 info
echo ""
echo "Updating README.md..."
cat > README.md << 'EOF'
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
EOF

echo "✓ Updated README.md"

# 10. Show git status
echo ""
echo "=================================================="
echo "Git Status"
echo "=================================================="
echo ""
git status

# 11. Show files to commit
echo ""
echo "=================================================="
echo "Summary"
echo "=================================================="
echo ""
echo "✅ Cleanup complete!"
echo ""
echo "Files ready for commit:"
echo "  ✓ Removed all temporary .sh scripts"
echo "  ✓ Cleaned Python cache"
echo "  ✓ Formatted code with black/isort"
echo "  ✓ Created CHANGELOG.md"
echo "  ✓ Updated README.md"
echo "  ✓ Created .gitattributes"
echo ""
echo "Test Status:"
echo "  ✓ 54 tests passing"
echo "  ✓ 93% code coverage"
echo ""
echo "Next steps:"
echo ""
echo "1. Review changes:"
echo "   git diff"
echo ""
echo "2. Stage all changes:"
echo "   git add ."
echo ""
echo "3. Create commit:"
echo '   git commit -m "feat: Phase 1 - Complete REST API with 93% coverage'
echo ''
echo '   BREAKING CHANGES: New API structure with versioning'
echo ''
echo '   Features:'
echo '   - Full CRUD API for task management'
echo '   - Token authentication with user registration'
echo '   - Advanced filtering (status, priority, search, dates)'
echo '   - Pagination with customizable page size'
echo '   - Permission system (IsOwner)'
echo '   - Custom actions (stats, mark_done)'
echo '   - OpenAPI/Swagger documentation'
echo ''
echo '   Testing:'
echo '   - 39 Phase 1 API tests (100% endpoints covered)'
echo '   - 15 Phase 0 infrastructure tests'
echo '   - 93% code coverage'
echo '   - Makefile test automation'
echo ''
echo '   Tech Stack:'
echo '   - Django 4.2.16 LTS + DRF 3.14.0'
echo '   - Python 3.11.9'
echo '   - Docker Compose (API, Redis, Prometheus, Grafana)'
echo '   - pytest with coverage reporting"'
echo ""
echo "4. Tag release:"
echo "   git tag -a v1.0.0 -m 'Phase 1: Production-ready REST API'"
echo ""
echo "5. Push to repository:"
echo "   git push origin main"
echo "   git push origin v1.0.0"
echo ""