from django.contrib.auth.decorators import login_required
from django.shortcuts import render


app_name = 'dashboard'


# Create your views here.
@login_required
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')