# Multi-stage build for optimized production image

# Stage 1: Builder
FROM python:3.11-slim AS builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and build wheels
COPY requirements.txt requirements-dev.txt ./
RUN pip install --upgrade pip
RUN pip wheel --no-cache-dir --wheel-dir /build/wheels -r requirements.txt
RUN pip wheel --no-cache-dir --wheel-dir /build/wheels -r requirements-dev.txt

# Stage 2: Runtime
FROM python:3.11-slim

LABEL maintainer="your-email@example.com"
LABEL description="Task Manager API - Production Ready Django REST Framework"

# Create non-root user
RUN useradd -m -u 1000 appuser

# Set working directory to /code
WORKDIR /code

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy wheels from builder and install
COPY --from=builder /build/wheels /wheels
COPY requirements.txt requirements-dev.txt ./
RUN pip install --upgrade pip && \
    pip install --no-cache-dir /wheels/*.whl && \
    rm -rf /wheels

# Copy application code
# Important: Copy app/ to /code/app/
COPY --chown=appuser:appuser app/ /code/app/
COPY --chown=appuser:appuser conftest.py pytest.ini /code/

# Create data directory for SQLite
RUN mkdir -p /data && chown appuser:appuser /data

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/code

# Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose port
EXPOSE 8000

# Run migrations and start server
# Note: manage.py is at /code/app/manage.py
CMD ["sh", "-c", "python /code/app/manage.py migrate --noinput && python /code/app/manage.py collectstatic --noinput && gunicorn --bind 0.0.0.0:8000 --workers ${GUNICORN_WORKERS:-3} --timeout ${GUNICORN_TIMEOUT:-60} --chdir /code/app wsgi:application --access-logfile - --error-logfile -"]
