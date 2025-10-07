"""
Django admin configuration for Task model
"""
from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Admin interface for Task model
    """

    list_display = [
        "title",
        "owner",
        "status",
        "priority",
        "due_date",
        "created_at",
        "is_overdue",
    ]
    list_filter = ["status", "priority", "created_at", "owner"]
    search_fields = ["title", "description", "owner__username"]
    readonly_fields = ["id", "created_at", "updated_at", "is_overdue"]
    fieldsets = (
        ("Basic Information", {"fields": ("title", "description", "owner")}),
        ("Status & Priority", {"fields": ("status", "priority")}),
        ("Dates", {"fields": ("due_date", "created_at", "updated_at")}),
        ("System", {"fields": ("id", "is_overdue"), "classes": ("collapse",)}),
    )
    date_hierarchy = "created_at"
    ordering = ["-created_at"]

    def is_overdue(self, obj):
        """Display overdue status"""
        return obj.is_overdue

    is_overdue.boolean = True
    is_overdue.short_description = "Overdue"
