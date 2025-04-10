from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib import messages


from userprofile.models import UserProfile
from userprofile.forms import SignupForm, UserProfileForm

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


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create a new UserProfile instance when a User is created
        UserProfile.objects.create(user=instance)



# Edit userprofile
@login_required
def edit_profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if form.is_valid():
            form.save()

            return redirect('userprofile:account')

    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'userprofile/edit_profile.html', {
        'form': form
    })


@login_required
def myaccount(request):
    try:
        user_profile = get_object_or_404(UserProfile, user=request.user)
    except UserProfile.DoesNotExist:
        messages.error(request, "User profile does not exist. Please contact support or try later.")
        return redirect('dashboard')  # Redirect to a safe page or dashboard

    return render(request, 'userprofile/account.html', {'user_profile': user_profile})


def my_logout(request):
    logout(request)
    return redirect('index')