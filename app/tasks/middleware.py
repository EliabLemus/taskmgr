import time
import logging
from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin
from datetime import datetime

logger = logging.getLogger(__name__)


class MetricsMiddleware(MiddlewareMixin):
    """
    Custom middleware to track:
    - Request count
    - Response latency (p50, p95, p99)
    - Error rate
    - Active users
    """

    def process_request(self, request):
        request.metrics_start_time = time.time()

    def process_response(self, request, response):
        if not hasattr(request, "metrics_start_time"):
            return response

        # Calculate latency
        latency_ms = (time.time() - request.metrics_start_time) * 1000

        # Track in Redis
        now = datetime.utcnow()
        minute_key = now.strftime("%Y-%m-%d-%H-%M")

        try:
            # Increment request counter (initialize if not exists)
            cache_key_requests = f"metrics:requests:{minute_key}"
            current = cache.get(cache_key_requests, 0)
            cache.set(cache_key_requests, current + 1, 3600)

            # Track latencies
            cache_key_latencies = f"metrics:latencies:{minute_key}"
            latencies = cache.get(cache_key_latencies, [])
            latencies.append(latency_ms)
            cache.set(cache_key_latencies, latencies, 3600)

            # Track errors (4xx, 5xx)
            if response.status_code >= 400:
                cache_key_errors = f"metrics:errors:{minute_key}"
                errors = cache.get(cache_key_errors, 0)
                cache.set(cache_key_errors, errors + 1, 3600)

            # Track active users
            if hasattr(request, "user") and request.user.is_authenticated:
                cache_key_users = f"metrics:users:{minute_key}"
                user_set = cache.get(cache_key_users, set())
                user_set.add(request.user.id)
                cache.set(cache_key_users, user_set, 3600)

        except Exception as e:
            # Don't break the response if metrics fail
            logger.error(f"Metrics middleware error: {e}")

        # Log slow requests
        if latency_ms > 500:
            logger.warning(
                f"Slow request: {request.method} {request.path} "
                f"took {latency_ms:.2f}ms"
            )

        return response
