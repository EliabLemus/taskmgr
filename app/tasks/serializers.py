from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task, Alert


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""

    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
        )
        return user


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for Task model"""

    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "priority",
            "due_date",
            "owner",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "owner", "created_at", "updated_at"]


class AlertSerializer(serializers.ModelSerializer):
    """Serializer for Alert model"""

    class Meta:
        model = Alert
        fields = [
            "id",
            "severity",
            "alert_type",
            "message",
            "metric_value",
            "threshold_value",
            "sent_to_slack",
            "created_at",
        ]
        read_only_fields = fields


# Serializadores de apoyo para las respuestas de registro, estadísticas y métricas


class UserRegistrationResponseSerializer(serializers.Serializer):
    """Respuesta de registro: devuelve usuario y token"""

    user = serializers.DictField()
    token = serializers.CharField()


class TaskStatsSerializer(serializers.Serializer):
    """Respuesta para /api/v1/tasks/stats/"""

    total = serializers.IntegerField()
    by_status = serializers.DictField()
    by_priority = serializers.DictField()


class LatencyStatsSerializer(serializers.Serializer):
    """Desglose de latencias"""

    min = serializers.FloatField()
    max = serializers.FloatField()
    avg = serializers.FloatField()
    p50 = serializers.FloatField()
    p95 = serializers.FloatField()
    p99 = serializers.FloatField()


class MetricsSummarySerializer(serializers.Serializer):
    """Resumen agregado de métricas de los últimos 5 minutos"""

    total_requests = serializers.IntegerField()
    total_errors = serializers.IntegerField()
    error_rate_percent = serializers.FloatField()
    active_users = serializers.IntegerField()
    latency = LatencyStatsSerializer()
    time_window = serializers.CharField()
    # Métricas de Apache Bench (opcional)
    ab_metrics = serializers.DictField(required=False)
    # Número de alertas generadas durante la petición (opcional)
    alerts_triggered = serializers.IntegerField(required=False)
