from django.urls import path
from client.views import *

urlpatterns = [
    path('', clients, name='clients'),
]