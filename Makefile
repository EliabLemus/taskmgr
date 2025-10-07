# Detect virtual environment
VENV := venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
PYTEST := $(VENV)/bin/pytest

# Check if Docker services are running
SERVICES_RUNNING := $(shell docker compose ps --services --filter "status=running" 2>/dev/null | wc -l | tr -d ' ')

.PHONY: help compose-up compose-down compose-build compose-logs compose-status shell migrate makemigrations createsuperuser test test-all test-unit test-integration test-phase0 test-phase1 test-cov lint format docker-build clean venv check-services

help:
	@echo "Available targets:"
	@echo ""
	@echo "Docker & Services:"
	@echo "  compose-up        - Start all services"
	@echo "  compose-down      - Stop all services"
	@echo "  compose-build     - Build Docker images"
	@echo "  compose-logs      - Tail API logs"
	@echo "  compose-status    - Check services status"
	@echo ""
	@echo "Django:"
	@echo "  shell             - Django shell"
	@echo "  migrate           - Run migrations"
	@echo "  makemigrations    - Create new migrations"
	@echo "  createsuperuser   - Create Django superuser"
	@echo ""
	@echo "Testing:"
	@echo "  test              - Run all tests (auto-starts services)"
	@echo "  test-all          - Run all tests (same as test)"
	@echo "  test-phase0       - Run Phase 0 infrastructure tests"
	@echo "  test-phase1       - Run Phase 1 API tests"
	@echo "  test-unit         - Run unit tests only"
	@echo "  test-integration  - Run integration tests only"
	@echo "  test-cov          - Run tests with coverage report"
	@echo ""
	@echo "Code Quality:"
	@echo "  lint              - Run linters"
	@echo "  format            - Format code with black and isort"
	@echo ""
	@echo "Other:"
	@echo "  venv              - Create/verify virtual environment"
	@echo "  clean             - Clean up containers and cache"

venv:
	@if [ ! -d "$(VENV)" ]; then \
		echo "Creating virtual environment..."; \
		python3 -m venv $(VENV); \
		$(PIP) install --upgrade pip; \
		$(PIP) install -r requirements.txt; \
		$(PIP) install -r requirements-dev.txt; \
	else \
		echo "✓ Virtual environment already exists"; \
	fi

check-services:
	@echo "Checking Docker services..."
	@if [ "$(SERVICES_RUNNING)" -lt "4" ]; then \
		echo "⚠️  Services not running (found $(SERVICES_RUNNING)/4)"; \
		echo "Starting Docker services..."; \
		docker compose up -d; \
		echo "Waiting 15 seconds for services to initialize..."; \
		sleep 15; \
		echo "✓ Services started"; \
	else \
		echo "✓ All services running ($(SERVICES_RUNNING)/4)"; \
	fi

compose-status:
	@docker compose ps

compose-up:
	docker compose up -d
	@echo "Waiting for services to be ready..."
	@sleep 10
	@echo ""
	@echo "✓ Services started:"
	@echo "  API: http://localhost:8000"
	@echo "  Docs: http://localhost:8000/api/v1/docs/"
	@echo "  Grafana: http://localhost:3000 (admin/admin)"
	@echo "  Prometheus: http://localhost:9090"

compose-down:
	docker compose down

compose-build:
	docker compose build --no-cache

compose-logs:
	docker compose logs -f api

shell:
	docker compose exec api python app/manage.py shell

migrate:
	docker compose exec api python app/manage.py migrate

makemigrations:
	docker compose exec api python app/manage.py makemigrations

createsuperuser:
	docker compose exec api python app/manage.py createsuperuser

# Test targets - NOW WITH AUTO SERVICE START
test: venv check-services
	@echo "Running ALL tests (Phase 0 + Phase 1)..."
	@echo ""
	PYTHONPATH=./app:. $(PYTEST) tests/ -v --tb=short

test-all: test

test-phase0: venv check-services
	@echo "Running Phase 0 infrastructure tests..."
	@echo ""
	$(PYTEST) tests/test_phase0_verification.py -v --tb=short

test-phase1: venv
	@echo "Running Phase 1 API tests..."
	@echo ""
	PYTHONPATH=./app:. $(PYTEST) tests/test_phase1_*.py -v --tb=short

test-unit: venv
	@echo "Running unit tests..."
	PYTHONPATH=./app:. $(PYTEST) tests/ -v -m unit

test-integration: venv check-services
	@echo "Running integration tests..."
	PYTHONPATH=./app:. $(PYTEST) tests/ -v -m integration

test-cov: venv check-services
	@echo "Running tests with coverage..."
	@echo ""
	PYTHONPATH=./app:. $(PYTEST) tests/ -v --cov=app/tasks --cov-report=html --cov-report=term
	@echo ""
	@echo "Coverage report: htmlcov/index.html"

lint: venv
	@echo "Running linters..."
	@$(VENV)/bin/flake8 app/ --max-line-length=120 --exclude=migrations || true
	@$(VENV)/bin/black --check app/ tests/ || true
	@$(VENV)/bin/isort --check-only app/ tests/ || true

format: venv
	@echo "Formatting code..."
	$(VENV)/bin/black app/ tests/
	$(VENV)/bin/isort app/ tests/
	@echo "✓ Code formatted"

docker-build:
	docker build -f infra/docker/Dockerfile -t taskmgr:latest .

clean:
	@echo "Cleaning up..."
	docker compose down -v
	rm -rf reports/*.log reports/*.html
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf htmlcov/ .coverage
	@echo "✓ Cleanup complete"

clean-venv:
	rm -rf $(VENV)
