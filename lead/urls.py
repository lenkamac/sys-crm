from django.urls import path
from .views import *
from . import views


app_name = 'lead'

urlpatterns = [
    path("", LeadListView.as_view(), name="list"),
    path('add/', LeadCreateView.as_view(), name='add'),
    path('<int:pk>/', LeadDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', LeadUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', LeadDeleteView.as_view(), name='delete'),
    path('delete_bulk/', views.leads_bulk_delete, name='delete_bulk'),
    path('<int:pk>/add-comment/', AddCommentView.as_view(), name='add_comment'),
    path('<int:pk>/add-file/', AddFileView.as_view(), name='add_file'),
    path('export/', views.leads_export, name='export'),
]