# Detect virtual environment
VENV := venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
PYTEST := $(VENV)/bin/pytest
ACTIVATE := source $(VENV)/bin/activate

# Check if Docker services are running
SERVICES_RUNNING := $(shell docker compose ps --services --filter "status=running" 2>/dev/null | wc -l | tr -d ' ')

.PHONY: help compose-up compose-down compose-build compose-logs compose-status shell migrate test test-unit test-integration test-phase0 lint docker-build docker-push bench clean venv check-services

help:
	@echo "Available targets:"
	@echo "  venv              - Create/verify virtual environment"
	@echo "  compose-up        - Start all services"
	@echo "  compose-down      - Stop all services"
	@echo "  compose-build     - Build Docker images"
	@echo "  compose-logs      - Tail logs"
	@echo "  compose-status    - Check services status"
	@echo "  check-services    - Verify services are running (internal)"
	@echo "  shell             - Django shell"
	@echo "  migrate           - Run migrations"
	@echo "  test              - Run all tests (auto-starts services)"
	@echo "  test-unit         - Run unit tests only"
	@echo "  test-integration  - Run integration tests (auto-starts services)"
	@echo "  test-phase0       - Run Phase 0 verification tests (auto-starts services)"
	@echo "  lint              - Run linters"
	@echo "  format            - Format code with black and isort"
	@echo "  docker-build      - Build production image"
	@echo "  docker-push       - Push to Docker Hub"
	@echo "  bench             - Run Apache Bench load test"
	@echo "  clean             - Clean up containers and volumes"

# Ensure virtual environment exists
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

# Check if services are running, start them if not
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
	@echo "Docker services status:"
	@docker compose ps

compose-up:
	docker compose up -d
	@echo "Waiting for services to be ready..."
	@sleep 10
	@echo ""
	@echo "Services started. Access points:"
	@echo "  API: http://localhost:8000"
	@echo "  Grafana: http://localhost:3000 (admin/admin)"
	@echo "  Prometheus: http://localhost:9090"
	@echo ""
	@echo "Verify with: make compose-status"

compose-down:
	docker compose down

compose-build:
	docker compose build --no-cache

compose-logs:
	docker compose logs -f api

shell:
	docker compose exec api python manage.py shell

migrate:
	docker compose exec api python manage.py migrate

# Test targets - use venv pytest and ensure services are running
test: venv check-services
	@echo "Running all tests..."
	$(PYTEST) tests/ -v

test-unit: venv
	@echo "Running unit tests (no services needed)..."
	$(PYTEST) tests/ -v -m unit

test-integration: venv check-services
	@echo "Running integration tests..."
	$(PYTEST) tests/ -v -m integration

test-phase0: venv check-services
	@echo "Running Phase 0 verification tests..."
	@echo "Services will be auto-started if not running..."
	@echo ""
	$(PYTEST) tests/test_phase0_verification.py -v --tb=short

# Lint targets - use venv tools
lint: venv
	@echo "Running linters..."
	@$(VENV)/bin/flake8 app/ --max-line-length=120 --exclude=migrations || true
	@$(VENV)/bin/black --check app/ tests/ || true
	@$(VENV)/bin/isort --check-only app/ tests/ || true

format: venv
	@echo "Formatting code..."
	$(VENV)/bin/black app/ tests/
	$(VENV)/bin/isort app/ tests/

docker-build:
	docker build -f infra/docker/Dockerfile -t taskmgr:latest .

docker-push:
	@echo "Configure DOCKERHUB_USERNAME first"
	# docker tag taskmgr:latest $(DOCKERHUB_USERNAME)/taskmgr:latest
	# docker push $(DOCKERHUB_USERNAME)/taskmgr:latest

bench:
	@echo "Apache Bench load test - Phase 3"

clean:
	docker compose down -v
	rm -rf reports/*.log
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true

clean-venv:
	rm -rf $(VENV)
	@echo "Virtual environment removed. Run 'make venv' to recreate."