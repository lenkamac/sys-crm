from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


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