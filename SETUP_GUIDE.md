# Quick Setup Guide

## First Time Setup

### 1. Install Prerequisites

```bash
# macOS
brew install pyenv make docker

# Ubuntu/Debian
sudo apt-get install make
curl https://pyenv.run | bash
# Install Docker: https://docs.docker.com/engine/install/ubuntu/
```

### 2. Setup Python Environment

```bash
cd taskmgr

# Install Python 3.11.9
pyenv install 3.11.9
pyenv local 3.11.9

# Verify
python --version  # Should show Python 3.11.9

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 3. Start Services

```bash
# Copy environment file
cp .env.example .env

# Build and start Docker services
make compose-build
make compose-up
```

### 4. Verify Setup

```bash
# Run tests
make test-phase0

# Check services
curl http://localhost:8000/health
open http://localhost:3000  # Grafana (admin/admin)
open http://localhost:9090  # Prometheus
```

## Daily Development Workflow

```bash
# Activate virtual environment
source venv/bin/activate

# Start services (if not running)
make compose-up

# Make changes to code...

# Run tests
make test

# View logs
make compose-logs

# Stop services when done
make compose-down
```

## Common Commands

```bash
# Tests
make test              # All tests
make test-phase0       # Phase 0 only
pytest -v              # Verbose output
pytest -k test_name    # Run specific test

# Code Quality
make lint              # Run all linters
black app/ tests/      # Format code
isort app/ tests/      # Sort imports

# Docker
make compose-up        # Start services
make compose-down      # Stop services
make compose-logs      # View logs
make clean             # Clean everything

# Django
make shell             # Django shell
make migrate           # Run migrations
```

## Troubleshooting

**Virtual environment not working?**
```bash
deactivate  # If already in a venv
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Docker services not starting?**
```bash
make clean
make compose-build
make compose-up
docker compose ps  # Check status
```

**Tests failing?**
```bash
# Wait for services
sleep 10
make test-phase0

# Check logs
make compose-logs
```

**Wrong Python version?**
```bash
pyenv versions  # List installed versions
pyenv local 3.11.9  # Set correct version
python --version  # Verify
```
