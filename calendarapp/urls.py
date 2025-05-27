from django.urls import path
from . import views


app_name = 'calendarapp'

urlpatterns = [
    path('', views.calendar_view, name='calendar'),
    path('events/', views.events_json, name='events_json'),
    path('add_event/', views.add_event, name='add_event'),
]

