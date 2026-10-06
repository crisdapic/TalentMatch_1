from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "task_type",
        "priority",
        "status",
        "due_date",
        "created_at",
    )

    list_filter = (
        "task_type",
        "priority",
        "status",
    )

    search_fields = (
        "title",
        "description",
    )

    ordering = (
        "due_date",
    )