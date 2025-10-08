from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from django.db import connection


@api_view(["GET"])
@permission_classes([AllowAny])
def health_check(request):
    """
    Simple health check endpoint
    Returns 200 if service is healthy
    """
    return Response(
        {"status": "healthy", "service": "taskmgr-api"}, status=status.HTTP_200_OK
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def status_check(request):
    """
    Detailed status check with dependencies
    Returns service status + Redis + Database connectivity
    """
    health_status = {"api": "ok", "redis": "unknown", "database": "unknown"}

    # Check Redis
    try:
        cache.set("health_check", "ok", 10)
        if cache.get("health_check") == "ok":
            health_status["redis"] = "ok"
        else:
            health_status["redis"] = "error"
    except Exception as e:
        health_status["redis"] = f"error: {str(e)}"

    # Check Database
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            health_status["database"] = "ok"
    except Exception as e:
        health_status["database"] = f"error: {str(e)}"

    # Determine overall status
    overall_healthy = all(v == "ok" for v in health_status.values())

    return Response(
        {
            "status": "healthy" if overall_healthy else "unhealthy",
            "checks": health_status,
        },
        status=status.HTTP_200_OK
        if overall_healthy
        else status.HTTP_503_SERVICE_UNAVAILABLE,
    )
