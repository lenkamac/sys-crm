from django.shortcuts import render
from .models import Event
from datetime import datetime


# Create your views here.
def calendar_view(request):

    return render(request, 'calendarapp/calendar.html')
