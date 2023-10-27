# forms.py
from django import forms
from .models import *
from django.contrib.auth.models import User
class BookStatusForm(forms.Form):
    currently_reading = forms.BooleanField(required=False)
    want_to_read = forms.BooleanField(required=False)


class UpdateUserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'full_name']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
        }