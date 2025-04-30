from django.urls import path
from task.views import *


app_name = 'task'

urlpatterns = [
    path('', tasks, name='task_list'),
    path('<int:pk>/', task_detail, name='task_detail'),
    path('add/', task_add, name='task_add'),
    path('<int:pk>/edit/', task_edit, name='task_edit'),
    path('<int:pk>/delete/', task_delete, name='task_delete'),
]
