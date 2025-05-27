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


# add event
@csrf_exempt
def add_event(request):
    if request.method == "POST":
        data = json.loads(request.body)
        Event.objects.create(
            title=data.get('title'),
            start=data.get('start'),
            end=data.get('end') or None,
            description=data.get('description')
        )
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


# delete event
@csrf_exempt
def delete_event(request, event_id):
    if request.method == "DELETE":
        try:
            event = Event.objects.get(id=event_id)
            event.delete()
            return JsonResponse({'success': True})
        except Event.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Event not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})


# edit event
@csrf_exempt
def update_event(request, event_id):
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            event = Event.objects.get(id=event_id)
            event.title = data.get('title')
            event.start = data.get('start')
            event.end = data.get('end') or None
            event.description = data.get('description')
            event.save()
            return JsonResponse({'success': True})
        except Event.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Event not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})
