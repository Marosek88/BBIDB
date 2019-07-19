from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisetrForm(UserCreationForm):
    first_name = forms.TextInput(attrs={'required': True})
    last_name = forms.TextInput(attrs={'required': True})
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
