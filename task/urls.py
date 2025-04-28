from django.urls import path
from task.views import *


app_name = 'task'

urlpatterns = [
    path('', tasks, name='task_list'),
    #path('create/', task_create, name='task_create'),
    #path('<int:pk>/', task_detail, name='task_detail'),
    #path('<int:pk>/edit/', task_edit, name='task_edit'),
    #path('<int:pk>/delete/', task_delete, name='task_delete'),
]
