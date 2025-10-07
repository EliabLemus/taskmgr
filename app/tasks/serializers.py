"""
DRF Serializers for Task Manager API
"""
from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Task


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User registration and display
    """

    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "first_name", "last_name"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        """Create user with encrypted password"""
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )
        return user


class TaskSerializer(serializers.ModelSerializer):
    """
    Main Task serializer for list and detail views
    """

    owner = UserSerializer(read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    priority_display = serializers.CharField(
        source="get_priority_display", read_only=True
    )

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "status_display",
            "priority",
            "priority_display",
            "due_date",
            "created_at",
            "updated_at",
            "owner",
            "is_overdue",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "owner"]


class TaskCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating tasks
    """

    class Meta:
        model = Task
        fields = ["title", "description", "status", "priority", "due_date"]

    def validate_title(self, value):
        """Ensure title is not empty or just whitespace"""
        if not value or not value.strip():
            raise serializers.ValidationError("Title cannot be empty")
        return value.strip()

    def validate(self, data):
        """Cross-field validation"""
        # Ensure status is valid
        if "status" in data and data["status"] not in dict(Task.Status.choices):
            raise serializers.ValidationError(
                {
                    "status": f"Invalid status. Choose from: {', '.join(dict(Task.Status.choices).keys())}"
                }
            )

        # Ensure priority is valid
        if "priority" in data and data["priority"] not in dict(Task.Priority.choices):
            raise serializers.ValidationError(
                {
                    "priority": f"Invalid priority. Choose from: {', '.join(dict(Task.Priority.choices).keys())}"
                }
            )

        return data


class TaskUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating tasks (allows partial updates)
    """

    class Meta:
        model = Task
        fields = ["title", "description", "status", "priority", "due_date"]

    def validate_title(self, value):
        """Ensure title is not empty or just whitespace if provided"""
        if value is not None and (not value or not value.strip()):
            raise serializers.ValidationError("Title cannot be empty")
        return value.strip() if value else value


class TaskListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for task lists (excludes owner details)
    """

    owner_username = serializers.CharField(source="owner.username", read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "status",
            "priority",
            "due_date",
            "created_at",
            "owner_username",
            "is_overdue",
        ]
        read_only_fields = ["id", "created_at", "owner_username"]
