from django.urls import path

from client.views import *
from . import views

app_name = 'client'

urlpatterns = [
    path("", ClientListView.as_view(), name="list"),
    path('add/', ClientCreateView.as_view(), name='add'),
    path('<int:pk>/', ClientDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', ClientUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', ClientDeleteView.as_view(), name='delete'),
    path('delete_bulk/', views.clients_bulk_delete, name='delete_bulk'),
    path('<int:pk>/add-comment/', AddCommentView.as_view(), name='add_comment'),
    path('<int:pk>/add-file/', AddFileView.as_view(), name='add_file'),
    path('export/', views.clients_export, name='export'),
]