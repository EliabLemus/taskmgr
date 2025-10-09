from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .metrics_aggregator import MetricsAggregator
from drf_spectacular.utils import extend_schema
from .serializers import MetricsSummarySerializer


@extend_schema(responses=MetricsSummarySerializer, auth=[])
@api_view(["GET"])
@permission_classes([AllowAny])
def metrics_summary(request):
    """
    Get aggregated metrics summary for last 5 minutes

    Also checks thresholds and creates alerts if needed.

    Returns:
    - total_requests
    - total_errors
    - error_rate_percent
    - active_users
    - latency (min, max, avg, p50, p95, p99)
    """
    try:
        # Get metrics
        metrics = MetricsAggregator.get_metrics_summary()

        # Check and create alerts (runs in background)
        alerts = MetricsAggregator.check_and_alert()

        # Add alert info to response
        if alerts:
            metrics["alerts_triggered"] = len(alerts)

        return Response(metrics, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
