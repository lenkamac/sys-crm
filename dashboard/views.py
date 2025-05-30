from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from lead.models import Lead
from client.models import Client


app_name = 'dashboard'


# Create your views here.
@login_required
def dashboard(request):
    lead_count = Lead.objects.filter(created_by=request.user).count()
    client_count = Client.objects.filter(created_by=request.user).count()
    latest_leads = Lead.objects.filter(created_by=request.user).order_by('-created_at')[:5]
    latest_clients = Client.objects.filter(created_by=request.user).order_by('-created_at')[:5]

    context = {
        'lead_count': lead_count,
        'client_count': client_count,
        'latest_leads': latest_leads,
        'latest_clients': latest_clients,
    }
    return render(request, 'dashboard/dashboard.html', context)