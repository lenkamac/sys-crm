from django.urls import path
from task.views import *

urlpatterns = [
    path('', tasks, name='tasks_list')
]