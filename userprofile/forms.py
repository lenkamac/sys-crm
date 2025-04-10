from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from userprofile.models import UserProfile


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

        username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))

        first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
        last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))

        email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
        password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
        password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))


INPUT_CLASSES = 'form-control my-3 w-50'


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'first_name',
            'last_name',
            'email',
            'profile_pic',
            'phone_number',
            'bio',
            'date_of_birth',
            'website',
            'location',
            'user_company',]
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'first name', 'class': INPUT_CLASSES}),
            'last_name': forms.TextInput(attrs={'placeholder': 'last name', 'class': INPUT_CLASSES}),
            'email': forms.EmailInput(attrs={'placeholder': 'email', 'class': INPUT_CLASSES}),
            'profile_pic': forms.ClearableFileInput(attrs={'class': INPUT_CLASSES}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'phone', 'class': INPUT_CLASSES}),
            'bio': forms.Textarea(attrs={'placeholder': 'Tell us about yourself...', 'rows': 4, 'class': INPUT_CLASSES}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': INPUT_CLASSES}),
            'website': forms.URLInput(attrs={'placeholder': 'https://yourwebsite.com', 'class': INPUT_CLASSES}),
            'location': forms.TextInput(attrs={'placeholder': 'Your location', 'class': INPUT_CLASSES}),
            'user_company': forms.TextInput(attrs={'placeholder': 'Your company', 'class': INPUT_CLASSES}),
        }
