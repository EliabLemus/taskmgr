import os
import redis
import logging
from datetime import datetime, timedelta
from django.core.cache import cache
from .models import Alert
from .slack_alerts import slack_alerter
from django.conf import settings

logger = logging.getLogger(__name__)


class MetricsAggregator:
    """Aggregate metrics and check thresholds"""

    # Thresholds
    ERROR_RATE_THRESHOLD = 0.05  # 5%
    P95_LATENCY_THRESHOLD = 500  # ms
    ALERT_COOLDOWN = 300  # 5 minutes

    @staticmethod
    def get_recent_minutes(count=5):
        """Get list of minute keys for last N minutes"""
        now = datetime.utcnow()
        keys = []
        for i in range(count):
            minute = now - timedelta(minutes=i)
            keys.append(minute.strftime("%Y-%m-%d-%H-%M"))
        return keys

    @classmethod
    def get_metrics_summary(cls):
        """Get aggregated metrics for last 5 minutes"""
        minute_keys = cls.get_recent_minutes(5)

        total_requests = 0
        total_errors = 0
        all_latencies = []
        unique_users = set()

        for minute_key in minute_keys:
            # Requests
            requests = cache.get(f"metrics:requests:{minute_key}", 0)
            total_requests += requests

            # Errors
            errors = cache.get(f"metrics:errors:{minute_key}", 0)
            total_errors += errors

            # Latencies
            latencies = cache.get(f"metrics:latencies:{minute_key}", [])
            all_latencies.extend(latencies)

            # Users
            users = cache.get(f"metrics:users:{minute_key}", set())
            unique_users.update(users)

        # Calculate error rate
        error_rate = (total_errors / total_requests * 100) if total_requests > 0 else 0

        # Calculate latency percentiles
        latency_stats = cls._calculate_latency_stats(all_latencies)

        result = {
            "total_requests": total_requests,
            "total_errors": total_errors,
            "error_rate_percent": round(error_rate, 2),
            "active_users": len(unique_users),
            "latency": latency_stats,
            "time_window": "5 minutes",
        }
        # Obtener métricas de ab (si existen)
        ab_metrics = cls._get_ab_metrics()
        if ab_metrics:
            result["ab_metrics"] = ab_metrics
        return result

    @staticmethod
    def _calculate_latency_stats(latencies):
        """Calculate latency percentiles"""
        if not latencies:
            return {"min": 0, "max": 0, "avg": 0, "p50": 0, "p95": 0, "p99": 0}

        sorted_latencies = sorted(latencies)
        count = len(sorted_latencies)

        def percentile(p):
            index = int(count * p / 100)
            return sorted_latencies[min(index, count - 1)]

        return {
            "min": round(min(latencies), 2),
            "max": round(max(latencies), 2),
            "avg": round(sum(latencies) / count, 2),
            "p50": round(percentile(50), 2),
            "p95": round(percentile(95), 2),
            "p99": round(percentile(99), 2),
        }

    @classmethod
    def check_and_alert(cls):
        """Check metrics against thresholds and send alerts"""
        metrics = cls.get_metrics_summary()

        # Skip if no traffic
        if metrics["total_requests"] == 0:
            return []

        alerts_triggered = []

        # Check error rate
        error_rate = metrics["error_rate_percent"]
        if error_rate > cls.ERROR_RATE_THRESHOLD * 100:
            if cls._should_alert("high_error_rate"):
                alert = cls._create_alert(
                    severity="ERROR",
                    alert_type="high_error_rate",
                    message=f"Error rate is {error_rate:.2f}% (threshold: {cls.ERROR_RATE_THRESHOLD * 100}%)",
                    metric_value=error_rate,
                    threshold_value=cls.ERROR_RATE_THRESHOLD * 100,
                )
                alerts_triggered.append(alert)

        # Check p95 latency
        p95_latency = metrics["latency"]["p95"]
        if p95_latency > cls.P95_LATENCY_THRESHOLD:
            if cls._should_alert("high_latency"):
                alert = cls._create_alert(
                    severity="WARNING",
                    alert_type="high_latency",
                    message=f"P95 latency is {p95_latency:.2f}ms (threshold: {cls.P95_LATENCY_THRESHOLD}ms)",
                    metric_value=p95_latency,
                    threshold_value=cls.P95_LATENCY_THRESHOLD,
                )
                alerts_triggered.append(alert)

        return alerts_triggered

    @classmethod
    def _should_alert(cls, alert_type):
        """Check if we should send alert (cooldown logic)"""
        cooldown_key = f"alert:cooldown:{alert_type}"
        if cache.get(cooldown_key):
            return False
        cache.set(cooldown_key, True, cls.ALERT_COOLDOWN)
        return True

    @classmethod
    def _create_alert(
        cls, severity, alert_type, message, metric_value=None, threshold_value=None
    ):
        """Create alert and send to Slack"""
        # Save to database
        alert = Alert.objects.create(
            severity=severity,
            alert_type=alert_type,
            message=message,
            metric_value=metric_value,
            threshold_value=threshold_value,
            sent_to_slack=False,
        )

        # Send to Slack
        sent = slack_alerter.send_alert(
            severity=severity,
            alert_type=alert_type,
            message=message,
            metric_value=metric_value,
            threshold=threshold_value,
        )

        if sent:
            alert.sent_to_slack = True
            alert.save()

        logger.info(f"Alert created: {alert_type} - {message}")
        return alert

    @staticmethod
    def _get_ab_metrics():
        """
        Recupera métricas de Apache Bench almacenadas en Redis.
        Devuelve un diccionario con claves y valores convertidos a números cuando es posible.
        """
        try:
            redis_url = os.environ.get(
                "REDIS_URL", settings.CACHES["default"]["LOCATION"]
            )
            r = redis.Redis.from_url(redis_url)
            raw = r.hgetall("ab_metrics")
            metrics = {}
            for k, v in raw.items():
                key = k.decode() if isinstance(k, bytes) else k
                try:
                    metrics[key] = float(v)
                except (ValueError, TypeError):
                    metrics[key] = v.decode() if isinstance(v, bytes) else v
            return metrics
        except Exception:
            return {}
