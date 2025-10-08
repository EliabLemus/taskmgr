"""
Phase 0 Verification Tests
Tests infrastructure setup: Docker services, API endpoints, monitoring stack
"""

import time

import pytest
import redis
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Test Configuration
API_BASE_URL = "http://localhost:8000"
PROMETHEUS_URL = "http://localhost:9090"
GRAFANA_URL = "http://localhost:3000"
REDIS_HOST = "localhost"
REDIS_PORT = 6379

# Retry strategy for flaky network calls
retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
)
adapter = HTTPAdapter(max_retries=retry_strategy)
http = requests.Session()
http.mount("http://", adapter)


@pytest.fixture(scope="module")
def wait_for_services():
    """Wait for all services to be ready before running tests"""
    print("\n⏳ Waiting for services to stabilize...")
    time.sleep(5)
    yield
    print("\n✅ Test suite completed")


class TestDockerInfrastructure:
    """Test Docker containers and basic infrastructure"""

    def test_api_container_running(self):
        """Verify API container is accessible"""
        try:
            response = http.get(f"{API_BASE_URL}/health", timeout=5)
            assert response.status_code == 200, "API container not responding"
        except requests.exceptions.ConnectionError:
            pytest.fail("API container is not running or not accessible")

    def test_redis_container_running(self):
        """Verify Redis container is accessible"""
        try:
            r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, socket_timeout=5)
            assert r.ping(), "Redis not responding to PING"
        except redis.exceptions.ConnectionError:
            pytest.fail("Redis container is not running or not accessible")

    def test_prometheus_container_running(self):
        """Verify Prometheus container is accessible"""
        try:
            response = http.get(PROMETHEUS_URL, timeout=5)
            assert response.status_code == 200, "Prometheus not responding"
        except requests.exceptions.ConnectionError:
            pytest.fail("Prometheus container is not running or not accessible")

    def test_grafana_container_running(self):
        """Verify Grafana container is accessible"""
        try:
            response = http.get(GRAFANA_URL, timeout=5, allow_redirects=True)
            assert response.status_code in [200, 302], "Grafana not responding"
        except requests.exceptions.ConnectionError:
            pytest.fail("Grafana container is not running or not accessible")


class TestAPIEndpoints:
    """Test Django API endpoints"""

    def test_health_endpoint(self, wait_for_services):
        """Test /health endpoint returns correct response"""
        response = http.get(f"{API_BASE_URL}/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "taskmgr-api"

    def test_status_endpoint(self, wait_for_services):
        """Test /status endpoint returns correct response"""
        response = http.get(f"{API_BASE_URL}/status")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    def test_metrics_endpoint(self, wait_for_services):
        """Test /metrics endpoint exposes Prometheus metrics"""
        response = http.get(f"{API_BASE_URL}/metrics")
        assert response.status_code == 200
        content = response.text

        # Check for Django-specific metrics
        assert "django_http" in content, "Django HTTP metrics not found"
        assert "python_info" in content, "Python info metrics not found"

    def test_api_response_time(self, wait_for_services):
        """Test API responds within acceptable time"""
        start = time.time()
        response = http.get(f"{API_BASE_URL}/health")
        elapsed = time.time() - start

        assert response.status_code == 200
        assert elapsed < 1.0, f"API response too slow: {elapsed:.2f}s"


class TestRedisIntegration:
    """Test Redis caching and connectivity"""

    def test_redis_connection(self):
        """Test Redis connection and basic operations"""
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

        # Test PING
        assert r.ping() is True

        # Test SET/GET
        test_key = "test:phase0:verification"
        test_value = "phase0_active"
        r.set(test_key, test_value, ex=60)

        assert r.get(test_key) == test_value

        # Cleanup
        r.delete(test_key)

    def test_redis_info(self):
        """Test Redis server info"""
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
        info = r.info()

        assert "redis_version" in info
        assert info["redis_mode"] == "standalone"


class TestPrometheusMonitoring:
    """Test Prometheus monitoring and scraping"""

    def test_prometheus_ui_accessible(self, wait_for_services):
        """Test Prometheus UI is accessible"""
        response = http.get(PROMETHEUS_URL)
        assert response.status_code == 200

    def test_prometheus_api_health(self, wait_for_services):
        """Test Prometheus API health endpoint"""
        response = http.get(f"{PROMETHEUS_URL}/-/healthy")
        assert response.status_code == 200

    def test_prometheus_targets(self, wait_for_services):
        """Test Prometheus is scraping Django API target"""
        # Give Prometheus time to scrape at least once
        time.sleep(10)

        response = http.get(f"{PROMETHEUS_URL}/api/v1/targets")
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "success"

        # Find django-api target
        targets = data["data"]["activeTargets"]
        django_target = next(
            (t for t in targets if t["labels"]["job"] == "django-api"), None
        )

        assert django_target is not None, "django-api target not found"
        assert (
            django_target["health"] == "up"
        ), f"django-api target is {django_target['health']}"

    def test_prometheus_can_query_metrics(self, wait_for_services):
        """Test Prometheus can query Django metrics"""
        time.sleep(5)

        # Query for django_http metrics
        query = "django_http_requests_total_by_view_transport_method_total"
        response = http.get(f"{PROMETHEUS_URL}/api/v1/query", params={"query": query})

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"


class TestGrafanaMonitoring:
    """Test Grafana dashboard and datasource"""

    def test_grafana_ui_accessible(self, wait_for_services):
        """Test Grafana UI is accessible"""
        response = http.get(GRAFANA_URL, allow_redirects=True)
        assert response.status_code == 200

    def test_grafana_health(self, wait_for_services):
        """Test Grafana health endpoint"""
        response = http.get(f"{GRAFANA_URL}/api/health", auth=("admin", "admin"))
        assert response.status_code == 200
        data = response.json()
        assert data["database"] == "ok"

    def test_grafana_datasource_provisioned(self, wait_for_services):
        """Test Prometheus datasource is provisioned in Grafana"""
        time.sleep(5)  # Give Grafana time to provision

        response = http.get(f"{GRAFANA_URL}/api/datasources", auth=("admin", "admin"))
        assert response.status_code == 200

        datasources = response.json()
        prometheus_ds = next(
            (ds for ds in datasources if ds["name"] == "Prometheus"), None
        )

        assert prometheus_ds is not None, "Prometheus datasource not found"
        assert prometheus_ds["type"] == "prometheus"
        assert prometheus_ds["url"] == "http://prometheus:9090"

    def test_grafana_can_query_prometheus(self, wait_for_services):
        """Test Grafana can query Prometheus datasource"""
        time.sleep(5)

        # Get datasource UID
        response = http.get(
            f"{GRAFANA_URL}/api/datasources/name/Prometheus", auth=("admin", "admin")
        )
        assert response.status_code == 200
        datasource = response.json()

        # Test datasource connectivity
        response = http.get(
            f"{GRAFANA_URL}/api/datasources/uid/{datasource['uid']}/health",
            auth=("admin", "admin"),
        )
        assert response.status_code == 200
        health = response.json()
        assert health["status"] == "OK", f"Datasource health check failed: {health}"


class TestEndToEndMonitoring:
    """End-to-end monitoring tests"""

    def test_metrics_flow_end_to_end(self, wait_for_services):
        """Test metrics flow from Django -> Prometheus -> Grafana"""
        # 1. Generate some API traffic
        for _ in range(5):
            http.get(f"{API_BASE_URL}/health")

        time.sleep(20)  # Wait for Prometheus to scrape

        # 2. Verify Prometheus has the metrics
        query = "django_http_requests_total_by_view_transport_method_total"
        response = http.get(f"{PROMETHEUS_URL}/api/v1/query", params={"query": query})
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert len(data["data"]["result"]) > 0, "No metrics found in Prometheus"

        # 3. Verify Grafana can access Prometheus
        response = http.get(
            f"{GRAFANA_URL}/api/datasources/name/Prometheus", auth=("admin", "admin")
        )
        assert response.status_code == 200

    def test_multiple_concurrent_requests(self, wait_for_services):
        """Test API handles concurrent requests"""
        import concurrent.futures

        def make_request():
            return http.get(f"{API_BASE_URL}/health")

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(20)]
            responses = [f.result() for f in concurrent.futures.as_completed(futures)]

        # All requests should succeed
        assert all(r.status_code == 200 for r in responses)
        assert all(r.json()["status"] == "healthy" for r in responses)


# Integration test marker
pytestmark = pytest.mark.integration


if __name__ == "__main__":
    # Run with: python test_phase0_verification.py
    pytest.main([__file__, "-v", "--tb=short"])
