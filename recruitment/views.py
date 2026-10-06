from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import TaskForm
from .models import Task


def task_list(request):
    tasks = Task.objects.all()

    search = request.GET.get("search", "").strip()
    status = request.GET.get("status")
    priority = request.GET.get("priority")
    task_type = request.GET.get("task_type")

    if search:
        tasks = tasks.filter(
            Q(title__icontains=search)
            | Q(description__icontains=search)
        )

    if status:
        tasks = tasks.filter(status=status)

    if priority:
        tasks = tasks.filter(priority=priority)

    if task_type:
        tasks = tasks.filter(task_type=task_type)

    tasks = tasks.order_by("due_date", "-created_at")

    context = {
        "tasks": tasks,
        "search": search,
        "status_filter": status or "",
        "priority_filter": priority or "",
        "task_type_filter": task_type or "",
        "status_choices": Task.Status.choices,
        "priority_choices": Task.Priority.choices,
        "task_type_choices": Task.TaskType.choices,
    }

    return render(
        request,
        "recruitment/task_list.html",
        context,
    )


def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)

        if form.is_valid():
            task = form.save()

            messages.success(
                request,
                f'La tarea "{task.title}" se ha creado correctamente.',
            )

            return redirect("recruitment:task_list")
    else:
        form = TaskForm()

    return render(
        request,
        "recruitment/task_form.html",
        {
            "form": form,
            "page_title": "Crear tarea",
        },
    )


def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)

    return render(
        request,
        "recruitment/task_detail.html",
        {
            "task": task,
        },
    )


def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)

        if form.is_valid():
            task = form.save()

            messages.success(
                request,
                f'La tarea "{task.title}" se ha actualizado correctamente.',
            )

            return redirect(
                "recruitment:task_detail",
                pk=task.pk,
            )
    else:
        form = TaskForm(instance=task)

    return render(
        request,
        "recruitment/task_form.html",
        {
            "form": form,
            "task": task,
            "page_title": "Editar tarea",
        },
    )


def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == "POST":
        title = task.title
        task.delete()

        messages.success(
            request,
            f'La tarea "{title}" se ha eliminado correctamente.',
        )

        return redirect("recruitment:task_list")

    return render(
        request,
        "recruitment/task_confirm_delete.html",
        {
            "task": task,
        },
    )


def task_complete(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == "POST":
        task.status = Task.Status.COMPLETED
        task.completed_at = timezone.now()
        task.save(update_fields=["status", "completed_at"])

        messages.success(
            request,
            f'La tarea "{task.title}" se ha marcado como completada.',
        )

    return redirect("recruitment:task_list")