import django_filters
from django_filters import rest_framework as filters
from .models import Task


class TaskFilter(filters.FilterSet):
    """Custom filter for Task model"""

    status = filters.ChoiceFilter(
        field_name="status",
        choices=Task.STATUS_CHOICES,
        help_text="Filter by task status",
    )

    priority = filters.ChoiceFilter(
        field_name="priority",
        choices=Task.PRIORITY_CHOICES,
        help_text="Filter by task priority",
    )

    created_after = filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="gte",
        help_text="Filter tasks created after this datetime",
    )

    created_before = filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="lte",
        help_text="Filter tasks created before this datetime",
    )

    due_after = filters.DateTimeFilter(
        field_name="due_date",
        lookup_expr="gte",
        help_text="Filter tasks due after this datetime",
    )

    due_before = filters.DateTimeFilter(
        field_name="due_date",
        lookup_expr="lte",
        help_text="Filter tasks due before this datetime",
    )

    class Meta:
        model = Task
        fields = {
            "status": ["exact"],
            "priority": ["exact"],
            "created_at": ["gte", "lte"],
            "due_date": ["gte", "lte"],
        }
