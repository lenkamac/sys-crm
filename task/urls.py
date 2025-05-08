from django.urls import path
from task.views import *
from . import views


app_name = 'task'

urlpatterns = [
    path('', tasks, name='task_list'),
    path('<int:pk>/', task_detail, name='task_detail'),
    path('add/', task_add, name='task_add'),
    path('<int:pk>/edit/', task_edit, name='task_edit'),
    path('<int:pk>/delete/', task_delete, name='task_delete'),
    path('<int:pk>/comment/add/', views.add_task_comment, name='add_task_comment'),
    path('<int:task_pk>/comment/<int:pk>/edit/', views.edit_task_comment, name='edit_task_comment'),
    path('<int:task_pk>/comment/<int:pk>/delete/', views.delete_task_comment, name='delete_task_comment'),

]
