from django.shortcuts import render
from django.http import JsonResponse
from .models import Event


# Create your views here.
def calendar_view(request):

    return render(request, 'calendarapp/calendar.html')


def events_json(request):
    events = []
    for event in Event.objects.all():
        events.append({
            'id': event.id,
            'title': event.title,
            'start': event.start.isoformat(),
            'end': event.end.isoformat() if event.end else None,
            'description': event.description,
        })
    return JsonResponse(events, safe=False)
