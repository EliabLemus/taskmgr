"""
API Views for Task Manager
"""
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .filters import TaskFilter
from .models import Task
from .pagination import CustomPageNumberPagination
from .permissions import IsOwner
from .serializers import (
    TaskCreateSerializer,
    TaskListSerializer,
    TaskSerializer,
    TaskUpdateSerializer,
    UserSerializer,
)


class UserRegistrationView(generics.CreateAPIView):
    """
    API endpoint for user registration
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        """Create user and return user data with token"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Create token for the new user
        token, created = Token.objects.get_or_create(user=user)

        return Response(
            {"user": UserSerializer(user).data, "token": token.key},
            status=status.HTTP_201_CREATED,
        )


class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Task CRUD operations

    list: Get all tasks for the authenticated user
    create: Create a new task
    retrieve: Get a specific task by ID
    update: Full update of a task
    partial_update: Partial update of a task
    destroy: Delete a task
    """

    permission_classes = [IsAuthenticated, IsOwner]
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = TaskFilter
    search_fields = ["title", "description"]
    ordering_fields = ["created_at", "updated_at", "due_date", "priority", "status"]
    ordering = ["-created_at"]

    def get_queryset(self):
        """
        Return tasks owned by the current user only
        """
        return Task.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        """
        Return appropriate serializer based on action
        """
        if self.action == "list":
            return TaskListSerializer
        elif self.action == "create":
            return TaskCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return TaskUpdateSerializer
        return TaskSerializer

    def perform_create(self, serializer):
        """
        Set the owner to the current user when creating a task
        """
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=["get"])
    def stats(self, request):
        """
        Custom endpoint to get task statistics for the current user
        GET /api/v1/tasks/stats/
        """
        queryset = self.get_queryset()

        stats = {
            "total": queryset.count(),
            "by_status": {
                "todo": queryset.filter(status=Task.Status.TODO).count(),
                "in_progress": queryset.filter(status=Task.Status.IN_PROGRESS).count(),
                "done": queryset.filter(status=Task.Status.DONE).count(),
            },
            "by_priority": {
                "low": queryset.filter(priority=Task.Priority.LOW).count(),
                "medium": queryset.filter(priority=Task.Priority.MEDIUM).count(),
                "high": queryset.filter(priority=Task.Priority.HIGH).count(),
            },
            "overdue": sum(1 for task in queryset if task.is_overdue),
        }

        return Response(stats)

    @action(detail=True, methods=["post"])
    def mark_done(self, request, pk=None):
        """
        Custom endpoint to mark a task as done
        POST /api/v1/tasks/{id}/mark_done/
        """
        task = self.get_object()
        task.status = Task.Status.DONE
        task.save()

        serializer = self.get_serializer(task)
        return Response(serializer.data)
