import json

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

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


@csrf_exempt
def add_event(request):
    if request.method == "POST":
        data = json.loads(request.body)
        Event.objects.create(
            title=data.get('title'),
            start=data.get('start'),
            end=data.get('end'),
            description=data.get('description')
        )
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})
