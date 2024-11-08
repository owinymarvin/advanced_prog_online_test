from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.forms import AuthenticationForm


class CustomLoginForm(AuthenticationForm):
    # Limit length to prevent buffer overflow
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class CustomSignupForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
