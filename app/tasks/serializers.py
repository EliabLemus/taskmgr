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
