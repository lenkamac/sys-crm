from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages

from userprofile.forms import SignupForm


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully')
            return redirect('/login/')
    else:
        form = SignupForm()

    return render(request, 'userprofile/register.html', {'form': form})


def my_logout(request):
    logout(request)
    return redirect('index')