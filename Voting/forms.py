from dataclasses import fields

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class StudentRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'password1', 'password2'
        ]
        labels = {
            'username': 'Admission Number',
            'email': 'Student Email',
            'first_name': "Full Name",
        }


class StudentLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Admission Number'