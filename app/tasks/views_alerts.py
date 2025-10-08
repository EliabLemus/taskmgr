from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Alert
from .serializers import AlertSerializer


class AlertViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing alerts (read-only)

    list: Get all alerts (paginated)
    retrieve: Get specific alert by ID

    Query parameters:
    - severity: Filter by severity (INFO, WARNING, ERROR, CRITICAL)
    - alert_type: Filter by alert type (high_error_rate, high_latency)
    """

    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Allow filtering by severity and alert_type"""
        queryset = Alert.objects.all()

        # Filter by severity
        severity = self.request.query_params.get("severity")
        if severity:
            queryset = queryset.filter(severity=severity.upper())

        # Filter by alert_type
        alert_type = self.request.query_params.get("alert_type")
        if alert_type:
            queryset = queryset.filter(alert_type=alert_type)

        return queryset
