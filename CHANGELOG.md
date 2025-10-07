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
