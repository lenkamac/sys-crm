from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .forms import TaskForm, TaskCommentForm
from .models import Task, TaskComment


@login_required
def tasks(request):
    # Get all users for the filter dropdown
    users = User.objects.all()

    # Get tasks with filters
    tasks_list = Task.objects.all()

    # Apply filters
    status = request.GET.get('status')
    if status:
        tasks_list = tasks_list.filter(status=status)

    priority = request.GET.get('priority')
    if priority:
        tasks_list = tasks_list.filter(priority=priority)

    assigned_to = request.GET.get('assigned_to')
    if assigned_to:
        tasks_list = tasks_list.filter(assigned_to_id=assigned_to)

    # Pagination
    paginator = Paginator(tasks_list, 10)  # Show 10 tasks per page
    page = request.GET.get('page')
    tasks = paginator.get_page(page)

    context = {
        'tasks': tasks,
        'users': users,
    }

    return render(request, 'task/task_list.html', context)


@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task_comments = TaskComment.objects.filter(task_id=pk)
    form = TaskCommentForm()
    return render(request, 'task/task_detail.html', {'task': task, 'task_comments': task_comments,
                                                     'form': form})


# Add this new view function
@login_required
def task_add(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            messages.success(request, 'Task was created successfully.')
            return redirect('task:task_list')
    else:
        initial_data = {}
        # Pre-fill lead or client if provided in URL parameters
        if 'lead_id' in request.GET:
            initial_data['lead'] = request.GET.get('lead_id')
        elif 'client_id' in request.GET:
            initial_data['client'] = request.GET.get('client_id')
        form = TaskForm(initial=initial_data)

    return render(request, 'task/task_form.html', {
        'form': form,
        'title': 'Add Task'
    })


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)

    # Check if user has permission to delete the task
    if not (request.user == task.created_by or request.user == task.assigned_to):
        raise PermissionDenied("You don't have permission to delete this task.")

    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task was deleted successfully.')
        return redirect('task:task_list')

    return render(request, 'task/task_confirm_delete.html', {
        'task': task
    })


@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)

    # Check if user has permission to edit the task
    if not (request.user == task.created_by or request.user == task.assigned_to):
        raise PermissionDenied("You don't have permission to edit this task.")

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task was updated successfully.')
            return redirect('task:task_detail', pk=task.pk)
    else:
        form = TaskForm(instance=task)

    return render(request, 'task/task_form.html', {
        'form': form,
        'title': 'Edit Task',
        'task': task
    })


# task comment
@login_required
def add_task_comment(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == 'POST':
        form = TaskCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.created_by = request.user
            comment.save()
            return redirect('task:task_detail', pk=task.pk)

    return redirect('task:task_detail', pk=task.pk)


@csrf_exempt
def edit_tasks_comment(request, comment_id):
    if request.method == "POST":
        comment = get_object_or_404(TaskComment, id=comment_id)

        # Check if the user is authorized to update the comment
        if request.user != comment.created_by:
            return JsonResponse({"error": "Unauthorized"}, status=403)

        new_content = request.POST.get("content", "")
        if new_content.strip() == "":
            return JsonResponse({"error": "Content cannot be empty"}, status=400)

        # Update the comment
        comment.content = new_content
        comment.save()
        return JsonResponse({"success": True, "updated_comment": comment.content})
    return JsonResponse({"error": "Invalid request"}, status=400)


@login_required
def delete_task_comment(request, comment_id):
    if request.method == "POST":
        comment = get_object_or_404(TaskComment, id=comment_id)

        # Check if the user is authorized to delete the comment
        if request.user != comment.created_by:
            return JsonResponse({"error": "Unauthorized"}, status=403)

        # Delete the comment
        comment.delete()
        return JsonResponse({"success": True})

    return JsonResponse({"error": "Invalid request"}, status=400)


