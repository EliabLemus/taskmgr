"""
Django filters for Task queryset filtering
"""
from django_filters import rest_framework as filters

from .models import Task


class TaskFilter(filters.FilterSet):
    """
    FilterSet for Task model with multiple filter options
    """

    status = filters.ChoiceFilter(
        choices=Task.Status.choices, help_text="Filter by task status"
    )
    priority = filters.ChoiceFilter(
        choices=Task.Priority.choices, help_text="Filter by task priority"
    )
    created_after = filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="gte",
        help_text="Filter tasks created after this date",
    )
    created_before = filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="lte",
        help_text="Filter tasks created before this date",
    )
    due_after = filters.DateTimeFilter(
        field_name="due_date",
        lookup_expr="gte",
        help_text="Filter tasks due after this date",
    )
    due_before = filters.DateTimeFilter(
        field_name="due_date",
        lookup_expr="lte",
        help_text="Filter tasks due before this date",
    )
    is_overdue = filters.BooleanFilter(
        method="filter_overdue", help_text="Filter overdue tasks"
    )

    class Meta:
        model = Task
        fields = ["status", "priority"]

    def filter_overdue(self, queryset, name, value):
        """
        Custom filter for overdue tasks
        """
        from django.utils import timezone

        if value:
            # Return tasks that are overdue (due_date in past and not done)
            return queryset.filter(due_date__lt=timezone.now()).exclude(
                status=Task.Status.DONE
            )
        else:
            # Return tasks that are not overdue
            return (
                queryset.filter(due_date__gte=timezone.now())
                | queryset.filter(due_date__isnull=True)
                | queryset.filter(status=Task.Status.DONE)
            )
