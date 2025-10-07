"""
Task model for the Task Manager API
"""
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Task(models.Model):
    """
    Task model with status tracking and priority management
    """

    class Status(models.TextChoices):
        TODO = "TODO", "To Do"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        DONE = "DONE", "Done"

    class Priority(models.TextChoices):
        LOW = "LOW", "Low"
        MEDIUM = "MEDIUM", "Medium"
        HIGH = "HIGH", "High"

    # Primary key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Core fields
    title = models.CharField(max_length=200, help_text="Task title")
    description = models.TextField(blank=True, help_text="Detailed task description")

    # Status tracking
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.TODO, db_index=True
    )
    priority = models.CharField(
        max_length=10, choices=Priority.choices, default=Priority.MEDIUM, db_index=True
    )

    # Dates
    due_date = models.DateTimeField(null=True, blank=True, help_text="Task due date")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Ownership
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="tasks", help_text="Task owner"
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["owner", "status"]),
            models.Index(fields=["owner", "priority"]),
            models.Index(fields=["-created_at"]),
        ]

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

    @property
    def is_overdue(self):
        """Check if task is overdue"""
        if self.due_date and self.status != self.Status.DONE:
            return timezone.now() > self.due_date
        return False
