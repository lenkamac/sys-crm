from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Task


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
