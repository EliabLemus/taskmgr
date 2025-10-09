from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .models import Task
from .permissions import IsOwner
from .filters import TaskFilter
from drf_spectacular.utils import extend_schema
from .serializers import (
    UserRegistrationSerializer,
    TaskSerializer,
    UserRegistrationResponseSerializer,
    TaskStatsSerializer,
)


class UserRegistrationView(APIView):
    """API endpoint for user registration"""

    permission_classes = [AllowAny]

    @extend_schema(
        request=UserRegistrationSerializer,
        responses={201: UserRegistrationResponseSerializer},
        description="API endpoint for user registration",
    )
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                {
                    "user": {
                        "username": user.username,
                        "email": user.email,
                    },
                    "token": token.key,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing tasks

    list: Get all tasks for authenticated user
    create: Create a new task
    retrieve: Get a specific task
    update: Update a task (PUT)
    partial_update: Partially update a task (PATCH)
    destroy: Delete a task
    stats: Get task statistics
    mark_done: Mark a task as done
    """

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    filterset_class = TaskFilter
    search_fields = ["title", "description"]
    ordering_fields = ["created_at", "updated_at", "due_date", "priority"]
    ordering = ["-created_at"]

    def get_queryset(self):
        """Return tasks owned by the authenticated user"""
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """Set the owner to the current user when creating a task"""
        serializer.save(owner=self.request.user)

    @extend_schema(responses=TaskStatsSerializer)
    @action(detail=False, methods=["get"])
    def stats(self, request):
        """
        Get task statistics for the current user

        Returns:
        - total: Total number of tasks
        - by_status: Count by status (TODO, IN_PROGRESS, DONE)
        - by_priority: Count by priority (LOW, MEDIUM, HIGH)
        """
        queryset = self.get_queryset()

        stats = {
            "total": queryset.count(),
            "by_status": {
                "TODO": queryset.filter(status="TODO").count(),
                "IN_PROGRESS": queryset.filter(status="IN_PROGRESS").count(),
                "DONE": queryset.filter(status="DONE").count(),
            },
            "by_priority": {
                "LOW": queryset.filter(priority="LOW").count(),
                "MEDIUM": queryset.filter(priority="MEDIUM").count(),
                "HIGH": queryset.filter(priority="HIGH").count(),
            },
        }

        return Response(stats)

    @action(detail=True, methods=["post"])
    def mark_done(self, request, pk=None):
        """Mark a task as done"""
        task = self.get_object()
        task.status = "DONE"
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)
